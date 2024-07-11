add_test( QueryAfterClear.SingleBlock /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests/regression_test_query_after_clear [==[--gtest_filter=QueryAfterClear.SingleBlock]==] --gtest_also_run_disabled_tests)
set_tests_properties( QueryAfterClear.SingleBlock PROPERTIES WORKING_DIRECTORY /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==] ENVIRONMENT [==[ASAN_OPTIONS=protect_shadow_gap=0]==])
set( regression_test_query_after_clear_TESTS QueryAfterClear.SingleBlock)
