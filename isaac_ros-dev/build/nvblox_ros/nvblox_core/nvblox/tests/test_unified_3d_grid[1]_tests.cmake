add_test( Unified3DGridTest.SetGridToValue /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests/test_unified_3d_grid [==[--gtest_filter=Unified3DGridTest.SetGridToValue]==] --gtest_also_run_disabled_tests)
set_tests_properties( Unified3DGridTest.SetGridToValue PROPERTIES WORKING_DIRECTORY /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==] ENVIRONMENT [==[ASAN_OPTIONS=protect_shadow_gap=0]==])
set( test_unified_3d_grid_TESTS Unified3DGridTest.SetGridToValue)
