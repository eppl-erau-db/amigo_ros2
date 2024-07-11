add_test( MultiMapperTest.MaskOnAndOff /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests/test_multi_mapper [==[--gtest_filter=MultiMapperTest.MaskOnAndOff]==] --gtest_also_run_disabled_tests)
set_tests_properties( MultiMapperTest.MaskOnAndOff PROPERTIES WORKING_DIRECTORY /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==] ENVIRONMENT [==[ASAN_OPTIONS=protect_shadow_gap=0]==])
set( test_multi_mapper_TESTS MultiMapperTest.MaskOnAndOff)
