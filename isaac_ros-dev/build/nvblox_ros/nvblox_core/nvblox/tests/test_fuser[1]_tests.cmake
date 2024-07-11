add_test( FuserTest.CommandLineFlags /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests/test_fuser [==[--gtest_filter=FuserTest.CommandLineFlags]==] --gtest_also_run_disabled_tests)
set_tests_properties( FuserTest.CommandLineFlags PROPERTIES WORKING_DIRECTORY /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==] ENVIRONMENT [==[ASAN_OPTIONS=protect_shadow_gap=0]==])
set( test_fuser_TESTS FuserTest.CommandLineFlags)
