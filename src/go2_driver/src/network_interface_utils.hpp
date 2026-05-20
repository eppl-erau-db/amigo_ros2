#pragma once

#include <algorithm>
#include <cctype>
#include <cstdlib>
#include <ifaddrs.h>
#include <net/if.h>
#include <sys/socket.h>
#include <regex>
#include <sstream>
#include <string>
#include <vector>

namespace go2_driver
{
namespace network_interface
{

struct InterfaceInfo
{
    std::string name;
    unsigned int flags = 0;
    bool has_ipv4 = false;
    bool has_ipv6 = false;
};

struct Resolution
{
    std::string requested;
    std::string selected;
    std::string reason;
    std::string available_interfaces;
    bool changed = false;
};

inline std::string trim(const std::string &value)
{
    const auto begin = value.find_first_not_of(" \t\r\n");
    if (begin == std::string::npos) {
        return "";
    }
    const auto end = value.find_last_not_of(" \t\r\n");
    return value.substr(begin, end - begin + 1);
}

inline std::string lowercase(std::string value)
{
    std::transform(
        value.begin(),
        value.end(),
        value.begin(),
        [](unsigned char ch) { return static_cast<char>(std::tolower(ch)); });
    return value;
}

inline bool starts_with(const std::string &value, const std::string &prefix)
{
    return value.rfind(prefix, 0) == 0;
}

inline bool is_auto_token(const std::string &value)
{
    const std::string normalized = lowercase(trim(value));
    return (
        normalized.empty() ||
        normalized == "auto" ||
        normalized == "default" ||
        normalized == "none" ||
        normalized == "off");
}

inline std::vector<InterfaceInfo> list_interfaces()
{
    std::vector<InterfaceInfo> interfaces;
    ifaddrs *ifaddr = nullptr;
    if (getifaddrs(&ifaddr) != 0 || ifaddr == nullptr) {
        return interfaces;
    }

    for (ifaddrs *entry = ifaddr; entry != nullptr; entry = entry->ifa_next) {
        if (entry->ifa_name == nullptr) {
            continue;
        }

        const std::string name(entry->ifa_name);
        auto existing = std::find_if(
            interfaces.begin(),
            interfaces.end(),
            [&name](const InterfaceInfo &info) { return info.name == name; });

        if (existing == interfaces.end()) {
            InterfaceInfo info;
            info.name = name;
            info.flags = entry->ifa_flags;
            interfaces.push_back(info);
            existing = interfaces.end() - 1;
        } else {
            existing->flags |= entry->ifa_flags;
        }

        if (entry->ifa_addr != nullptr) {
            if (entry->ifa_addr->sa_family == AF_INET) {
                existing->has_ipv4 = true;
            } else if (entry->ifa_addr->sa_family == AF_INET6) {
                existing->has_ipv6 = true;
            }
        }
    }

    freeifaddrs(ifaddr);
    return interfaces;
}

inline std::string join_interface_names(const std::vector<InterfaceInfo> &interfaces)
{
    std::ostringstream stream;
    for (std::size_t index = 0; index < interfaces.size(); ++index) {
        if (index > 0) {
            stream << ", ";
        }
        stream << interfaces[index].name;
    }
    return stream.str();
}

inline const InterfaceInfo *find_interface(
    const std::vector<InterfaceInfo> &interfaces,
    const std::string &name)
{
    const auto match = std::find_if(
        interfaces.begin(),
        interfaces.end(),
        [&name](const InterfaceInfo &info) { return info.name == name; });
    return match == interfaces.end() ? nullptr : &(*match);
}

inline int interface_score(const InterfaceInfo &info)
{
    const bool is_up = (info.flags & IFF_UP) != 0;
    const bool is_running = (info.flags & IFF_RUNNING) != 0;
    const bool is_loopback = (info.flags & IFF_LOOPBACK) != 0;
    const bool is_point_to_point = (info.flags & IFF_POINTOPOINT) != 0;
    const bool is_multicast = (info.flags & IFF_MULTICAST) != 0;
    const bool is_broadcast = (info.flags & IFF_BROADCAST) != 0;

    if (is_loopback || starts_with(info.name, "can")) {
        return -10000;
    }

    int score = 0;
    score += is_up ? 100 : -100;
    score += is_running ? 60 : 0;
    score += is_point_to_point ? -100 : 20;
    score += is_multicast ? 30 : -40;
    score += is_broadcast ? 20 : 0;
    score += info.has_ipv4 ? 25 : 0;
    score += info.has_ipv6 ? 10 : 0;

    const std::string name = lowercase(info.name);
    if (starts_with(name, "en") || starts_with(name, "eth")) {
        score += 35;
    } else if (starts_with(name, "mgbe")) {
        score += 25;
    } else if (starts_with(name, "wl") || starts_with(name, "wlan")) {
        score += 5;
    }

    if (
        starts_with(name, "docker") ||
        starts_with(name, "br-") ||
        starts_with(name, "virbr") ||
        starts_with(name, "veth") ||
        starts_with(name, "tailscale") ||
        starts_with(name, "tun") ||
        starts_with(name, "tap") ||
        starts_with(name, "l4tbr") ||
        starts_with(name, "usb"))
    {
        score -= 80;
    }

    return score;
}

inline std::string best_interface(const std::vector<InterfaceInfo> &interfaces)
{
    const InterfaceInfo *best = nullptr;
    int best_score = -10000;
    for (const auto &info : interfaces) {
        const int score = interface_score(info);
        if (score > best_score) {
            best = &info;
            best_score = score;
        }
    }

    return (best != nullptr && best_score > 0) ? best->name : "";
}

inline std::string getenv_trimmed(const char *name)
{
    const char *value = std::getenv(name);
    return value == nullptr ? "" : trim(value);
}

inline std::string cyclonedds_uri_interface()
{
    const std::string uri = getenv_trimmed("CYCLONEDDS_URI");
    if (uri.empty()) {
        return "";
    }

    std::smatch match;
    const std::regex pattern("<\\s*NetworkInterface[^>]*\\bname\\s*=\\s*[\"']([^\"']+)[\"']");
    if (std::regex_search(uri, match, pattern) && match.size() > 1) {
        return trim(match[1].str());
    }
    return "";
}

inline std::string configured_interface(const std::vector<InterfaceInfo> &interfaces)
{
    const std::vector<std::string> candidates = {
        getenv_trimmed("GO2_UNITREE_NETWORK_INTERFACE"),
        getenv_trimmed("UNITREE_NETWORK_INTERFACE"),
        cyclonedds_uri_interface(),
    };

    for (const auto &candidate : candidates) {
        if (!candidate.empty() && find_interface(interfaces, candidate) != nullptr) {
            return candidate;
        }
    }
    return "";
}

inline Resolution resolve(const std::string &requested_value)
{
    Resolution result;
    result.requested = trim(requested_value);

    if (is_auto_token(result.requested)) {
        result.selected = "";
        result.reason = "Unitree SDK auto-selection requested";
        return result;
    }

    const auto interfaces = list_interfaces();
    result.available_interfaces = join_interface_names(interfaces);

    if (find_interface(interfaces, result.requested) != nullptr) {
        result.selected = result.requested;
        result.reason = "requested interface is available";
        return result;
    }

    const std::string configured = configured_interface(interfaces);
    if (!configured.empty()) {
        result.selected = configured;
        result.changed = true;
        result.reason = "requested interface was unavailable; using configured interface";
        return result;
    }

    const std::string fallback = best_interface(interfaces);
    if (!fallback.empty()) {
        result.selected = fallback;
        result.changed = true;
        result.reason = "requested interface was unavailable; using best active interface";
        return result;
    }

    result.selected = "";
    result.changed = true;
    result.reason = "requested interface was unavailable; falling back to Unitree SDK auto-selection";
    return result;
}

}  // namespace network_interface
}  // namespace go2_driver
