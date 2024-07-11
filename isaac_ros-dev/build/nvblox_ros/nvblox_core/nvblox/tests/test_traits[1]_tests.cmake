add_test( TraitsTest.LayerTraits /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests/test_traits [==[--gtest_filter=TraitsTest.LayerTraits]==] --gtest_also_run_disabled_tests)
set_tests_properties( TraitsTest.LayerTraits PROPERTIES WORKING_DIRECTORY /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==] ENVIRONMENT [==[ASAN_OPTIONS=protect_shadow_gap=0]==])
set( test_traits_TESTS TraitsTest.LayerTraits)
