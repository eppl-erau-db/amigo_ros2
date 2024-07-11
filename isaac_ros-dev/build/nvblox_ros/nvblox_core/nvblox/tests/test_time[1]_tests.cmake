add_test( TimeTest.TestAll /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests/test_time [==[--gtest_filter=TimeTest.TestAll]==] --gtest_also_run_disabled_tests)
set_tests_properties( TimeTest.TestAll PROPERTIES WORKING_DIRECTORY /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==] ENVIRONMENT [==[ASAN_OPTIONS=protect_shadow_gap=0]==])
set( test_time_TESTS TimeTest.TestAll)
