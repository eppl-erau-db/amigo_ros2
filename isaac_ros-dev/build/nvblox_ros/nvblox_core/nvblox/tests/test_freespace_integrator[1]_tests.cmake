add_test( FreespaceIntegratorTest.FreespacePlane /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests/test_freespace_integrator [==[--gtest_filter=FreespaceIntegratorTest.FreespacePlane]==] --gtest_also_run_disabled_tests)
set_tests_properties( FreespaceIntegratorTest.FreespacePlane PROPERTIES WORKING_DIRECTORY /workspaces/isaac_ros-dev/build/nvblox_ros/nvblox_core/nvblox/tests SKIP_REGULAR_EXPRESSION [==[\[  SKIPPED \]]==] ENVIRONMENT [==[ASAN_OPTIONS=protect_shadow_gap=0]==])
set( test_freespace_integrator_TESTS FreespaceIntegratorTest.FreespacePlane)
