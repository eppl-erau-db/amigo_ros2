#include <algorithm>
#include <chrono>
#include <cctype>
#include <cstdlib>
#include <iostream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

#include <unitree/robot/b2/motion_switcher/motion_switcher_client.hpp>
#include <unitree/robot/channel/channel_factory.hpp>
#include <unitree/robot/go2/robot_state/robot_state_client.hpp>
#include <unitree/robot/go2/sport/sport_client.hpp>

#include "network_interface_utils.hpp"

namespace
{

struct Options
{
    std::string network_interface;
    std::string motion_mode = "normal";
    std::string gait = "static_walk";
    double wait_s = 2.0;
    int retries = 10;
    double retry_interval_s = 2.0;
    double post_switch_delay_s = 1.0;
};

std::string normalize_token(std::string value)
{
    std::transform(
        value.begin(),
        value.end(),
        value.begin(),
        [](unsigned char ch) {
            if (ch == '-' || ch == ' ') {
                return static_cast<unsigned char>('_');
            }
            return static_cast<unsigned char>(std::tolower(ch));
        });
    return value;
}

void sleep_seconds(double seconds)
{
    if (seconds <= 0.0) {
        return;
    }
    std::this_thread::sleep_for(std::chrono::duration<double>(seconds));
}

void dump_service_list()
{
    unitree::robot::go2::RobotStateClient robot_state_client;
    robot_state_client.SetTimeout(10.0F);
    robot_state_client.Init();

    std::vector<unitree::robot::go2::ServiceState> services;
    const int32_t list_result = robot_state_client.ServiceList(services);
    if (list_result != 0) {
        std::cerr << "RobotStateClient::ServiceList failed with code " << list_result << ".\n";
        return;
    }

    std::cout << "Unitree service list (" << services.size() << "):\n";
    for (const auto &service : services) {
        std::cout << "  name=" << service.name
                  << " status=" << service.status
                  << " protect=" << service.protect << '\n';
    }
}

std::string motion_mode_description(const std::string &mode_name)
{
    const std::string normalized = normalize_token(mode_name);
    if (normalized.empty()) {
        return "released";
    }
    if (normalized == "normal" || normalized == "sport_mode") {
        return "sport_mode (normal)";
    }
    if (normalized == "ai" || normalized == "ai_sport") {
        return "ai_sport";
    }
    if (normalized == "advanced" || normalized == "advanced_sport") {
        return "advanced_sport";
    }
    return mode_name;
}

std::vector<std::string> motion_mode_candidates(const std::string &motion_mode)
{
    const std::string normalized = normalize_token(motion_mode);
    if (
        normalized.empty() ||
        normalized == "none" ||
        normalized == "off" ||
        normalized == "skip")
    {
        return {};
    }
    if (
        normalized == "normal" ||
        normalized == "sport" ||
        normalized == "sport_mode")
    {
        return {"normal", "sport_mode"};
    }
    if (normalized == "ai" || normalized == "ai_sport") {
        return {"ai", "ai_sport"};
    }
    if (normalized == "release" || normalized == "released") {
        return {"release"};
    }
    return {motion_mode};
}

bool motion_mode_is_release(const std::string &motion_mode)
{
    const std::string normalized = normalize_token(motion_mode);
    return normalized == "release" || normalized == "released";
}

bool motion_mode_matches(const std::string &current_mode, const std::string &requested_mode)
{
    const std::string current = normalize_token(current_mode);
    const std::string requested = normalize_token(requested_mode);

    if (
        requested.empty() ||
        requested == "none" ||
        requested == "off" ||
        requested == "skip")
    {
        return true;
    }
    if (requested == "release" || requested == "released") {
        return current.empty();
    }
    if (requested == "normal" || requested == "sport" || requested == "sport_mode") {
        return current == "normal" || current == "sport_mode";
    }
    if (requested == "ai" || requested == "ai_sport") {
        return current == "ai" || current == "ai_sport";
    }
    return current == requested;
}

std::string canonical_gait(const std::string &gait)
{
    const std::string normalized = normalize_token(gait);
    if (
        normalized.empty() ||
        normalized == "none" ||
        normalized == "off" ||
        normalized == "skip")
    {
        return "none";
    }
    if (normalized == "static" || normalized == "static_walk") {
        return "static_walk";
    }
    if (
        normalized == "economic" ||
        normalized == "economic_gait" ||
        normalized == "endurance")
    {
        return "economic_gait";
    }
    if (normalized == "classic" || normalized == "classic_walk") {
        return "classic_walk";
    }
    if (normalized == "free" || normalized == "free_walk") {
        return "free_walk";
    }
    if (normalized == "upright" || normalized == "walk_upright") {
        return "walk_upright";
    }
    if (normalized == "trot" || normalized == "trot_run") {
        return "trot_run";
    }
    return normalized;
}

int32_t send_gait_command(unitree::robot::go2::SportClient &sport_client, const std::string &gait)
{
    const std::string selected_gait = canonical_gait(gait);
    if (selected_gait == "static_walk") {
        return sport_client.StaticWalk();
    }
    if (selected_gait == "economic_gait") {
        return sport_client.EconomicGait();
    }
    if (selected_gait == "classic_walk") {
        return sport_client.ClassicWalk(true);
    }
    if (selected_gait == "free_walk") {
        return sport_client.FreeWalk();
    }
    if (selected_gait == "walk_upright") {
        return sport_client.WalkUpright(true);
    }
    if (selected_gait == "trot_run") {
        return sport_client.TrotRun();
    }

    throw std::runtime_error(
        "Unsupported gait \"" + gait +
        "\". Expected one of: none, static_walk, economic, classic_walk, free_walk, walk_upright, trot_run.");
}

void print_usage(const char *argv0)
{
    std::cout
        << "Usage: " << argv0 << " [options]\n"
        << "  --network-interface <iface>\n"
        << "  --motion-mode <normal|sport_mode|ai|ai_sport|release|none>\n"
        << "  --gait <static_walk|economic|classic_walk|free_walk|walk_upright|trot_run|none>\n"
        << "  --wait <seconds>\n"
        << "  --retries <count>\n"
        << "  --retry-interval <seconds>\n"
        << "  --help\n";
}

std::string require_value(int argc, char **argv, int &index)
{
    if (index + 1 >= argc) {
        throw std::runtime_error("Missing value for argument \"" + std::string(argv[index]) + "\".");
    }
    ++index;
    return argv[index];
}

Options parse_arguments(int argc, char **argv)
{
    Options options;

    for (int index = 1; index < argc; ++index) {
        const std::string arg = argv[index];
        if (arg == "--help" || arg == "-h") {
            print_usage(argv[0]);
            std::exit(0);
        }
        if (arg == "--network-interface") {
            options.network_interface = require_value(argc, argv, index);
            continue;
        }
        if (arg == "--motion-mode") {
            options.motion_mode = require_value(argc, argv, index);
            continue;
        }
        if (arg == "--gait") {
            options.gait = require_value(argc, argv, index);
            continue;
        }
        if (arg == "--wait") {
            options.wait_s = std::stod(require_value(argc, argv, index));
            continue;
        }
        if (arg == "--retries") {
            options.retries = std::max(1, std::stoi(require_value(argc, argv, index)));
            continue;
        }
        if (arg == "--retry-interval") {
            options.retry_interval_s = std::stod(require_value(argc, argv, index));
            continue;
        }

        throw std::runtime_error("Unknown argument \"" + arg + "\".");
    }

    return options;
}

bool apply_motion_mode(
    unitree::robot::b2::MotionSwitcherClient &motion_switcher_client,
    const Options &options)
{
    const auto candidates = motion_mode_candidates(options.motion_mode);
    if (candidates.empty()) {
        return true;
    }

    std::string form;
    std::string current_mode;
    int32_t check_result = motion_switcher_client.CheckMode(form, current_mode);
    if (check_result != 0) {
        std::cerr << "MotionSwitcherClient::CheckMode failed with code " << check_result << ".\n";
    } else {
        std::cout << "Current motion mode: " << motion_mode_description(current_mode) << ".\n";
    }

    if (motion_mode_matches(current_mode, options.motion_mode)) {
        std::cout << "Requested motion mode already active: "
                  << motion_mode_description(current_mode) << ".\n";
        return true;
    }

    if (!current_mode.empty() && !motion_mode_is_release(options.motion_mode)) {
        std::cout
            << "Active motion mode \""
            << motion_mode_description(current_mode)
            << "\" is already running.\n"
            << "Skipping explicit mode handoff during launch because ReleaseMode() can drop the "
               "robot into damping.\n"
            << "Proceeding with high-level gait commands instead.\n";
        return true;
    }

    int32_t result = -1;
    if (motion_mode_is_release(options.motion_mode)) {
        std::cout << "Releasing the currently active motion mode.\n";
        result = motion_switcher_client.ReleaseMode();
        if (result != 0) {
            std::cerr << "ReleaseMode failed with code " << result << ".\n";
            return false;
        }
    } else {
        for (const auto &candidate : candidates) {
            std::cout << "Selecting motion mode candidate \"" << candidate << "\".\n";
            result = motion_switcher_client.SelectMode(candidate);
            if (result == 0) {
                break;
            }
            std::cerr << "SelectMode(\"" << candidate << "\") failed with code " << result << ".\n";
        }
        if (result != 0) {
            dump_service_list();
            return false;
        }
    }

    sleep_seconds(options.post_switch_delay_s);

    form.clear();
    current_mode.clear();
    check_result = motion_switcher_client.CheckMode(form, current_mode);
    if (check_result != 0) {
        std::cerr << "MotionSwitcherClient::CheckMode verification failed with code "
                  << check_result << ".\n";
        dump_service_list();
        return false;
    }
    if (!motion_mode_matches(current_mode, options.motion_mode)) {
        std::cerr << "Requested motion mode did not stick. Current mode is "
                  << motion_mode_description(current_mode) << ".\n";
        dump_service_list();
        return false;
    }

    std::cout << "Selected motion mode: " << motion_mode_description(current_mode) << ".\n";
    return true;
}

bool apply_gait(unitree::robot::go2::SportClient &sport_client, const std::string &gait)
{
    const std::string selected_gait = canonical_gait(gait);
    if (selected_gait == "none") {
        return true;
    }

    int32_t result = send_gait_command(sport_client, selected_gait);
    if (result == 0) {
        std::cout << "Applied gait: " << selected_gait << ".\n";
        return true;
    }

    std::cerr << "Initial gait command \"" << selected_gait
              << "\" failed with code " << result << ". Trying StandUp() once before retrying.\n";
    const int32_t stand_up_result = sport_client.StandUp();
    if (stand_up_result != 0) {
        std::cerr << "StandUp() failed with code " << stand_up_result << ".\n";
        return false;
    }

    sleep_seconds(0.75);
    result = send_gait_command(sport_client, selected_gait);
    if (result != 0) {
        std::cerr << "Retrying gait command \"" << selected_gait
                  << "\" failed with code " << result << ".\n";
        return false;
    }

    std::cout << "Applied gait after StandUp(): " << selected_gait << ".\n";
    return true;
}

bool configure_motion(const Options &options)
{
    unitree::robot::b2::MotionSwitcherClient motion_switcher_client;
    motion_switcher_client.SetTimeout(10.0F);
    motion_switcher_client.Init();

    if (!apply_motion_mode(motion_switcher_client, options)) {
        return false;
    }

    if (canonical_gait(options.gait) == "none") {
        return true;
    }

    unitree::robot::go2::SportClient sport_client;
    sport_client.SetTimeout(10.0F);
    sport_client.Init();
    return apply_gait(sport_client, options.gait);
}

}  // namespace

int main(int argc, char **argv)
{
    try {
        const Options options = parse_arguments(argc, argv);

        std::cout << "go2_motion_mode_switcher starting with motion_mode=\""
                  << options.motion_mode << "\", gait=\"" << options.gait << "\".\n";

        sleep_seconds(options.wait_s);

        const auto network_interface = go2_driver::network_interface::resolve(
            options.network_interface);
        if (network_interface.changed) {
            std::cerr
                << "Requested Unitree network interface \""
                << network_interface.requested
                << "\" is not available";
            if (!network_interface.available_interfaces.empty()) {
                std::cerr << " (available: " << network_interface.available_interfaces << ")";
            }
            std::cerr << ". " << network_interface.reason << ": "
                      << (network_interface.selected.empty() ? "<auto>" : network_interface.selected)
                      << ".\n";
        }

        if (network_interface.selected.empty()) {
            unitree::robot::ChannelFactory::Instance()->Init(0);
            std::cout << "Initialized Unitree ChannelFactory with auto-selected network interface.\n";
        } else {
            unitree::robot::ChannelFactory::Instance()->Init(0, network_interface.selected);
            std::cout << "Initialized Unitree ChannelFactory with network interface \""
                      << network_interface.selected << "\".\n";
        }

        bool success = false;
        for (int attempt = 1; attempt <= std::max(1, options.retries); ++attempt) {
            std::cout << "Motion configuration attempt " << attempt
                      << " / " << std::max(1, options.retries) << ".\n";
            if (configure_motion(options)) {
                success = true;
                break;
            }
            if (attempt < std::max(1, options.retries)) {
                sleep_seconds(options.retry_interval_s);
            }
        }

        unitree::robot::ChannelFactory::Instance()->Release();
        return success ? 0 : 1;
    } catch (const std::exception &error) {
        std::cerr << "go2_motion_mode_switcher failed: " << error.what() << '\n';
        return 1;
    }
}
