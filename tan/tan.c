#include <math.h>

#include <unity_fixture.h>

#define UNITY_DOUBLE_PRECISION 10e-12f

TEST_GROUP(test_tan);

TEST_SETUP(test_tan)
{
}
 
TEST_TEAR_DOWN(test_tan)
{
}

TEST(test_tan, tan_boundary_values_left_0)
{
	(tan(-M_PI_2) != tan(-M_PI_2)) ? PASS("test passed for input outside the domain") : FAIL("test failed for input outside the domain");
}

TEST(test_tan, tan_boundary_values_left_1)
{
	TEST_ASSERT_EQUAL_DOUBLE(999999.999999666667, tan(-M_PI_2 + 10e-6));
}

TEST(test_tan, tan_boundary_values_right_0)
{
	(tan(M_PI_2) != tan(M_PI_2)) ? PASS("test passed for input outside the domain") : FAIL("test failed for input outside the domain");
}

TEST(test_tan, tan_boundary_values_right_1)
{
	TEST_ASSERT_EQUAL_DOUBLE(999999.999999666667, tan(M_PI_2 - 10e-6));
}


TEST(test_tan, tan_middle_values)
{
	TEST_ASSERT_EQUAL_DOUBLE(-1.0, tan(-M_PI_4));
	TEST_ASSERT_EQUAL_DOUBLE(0.0, tan(0));
	TEST_ASSERT_EQUAL_DOUBLE(1.732050807569, tan(M_PI / 3));
}


TEST_GROUP_RUNNER(test_tan)
{
	RUN_TEST_CASE(test_tan, tan_boundary_values_left_0);
	RUN_TEST_CASE(test_tan, tan_boundary_values_left_1);
	RUN_TEST_CASE(test_tan, tan_boundary_values_right_0);
	RUN_TEST_CASE(test_tan, tan_boundary_values_right_1);
	RUN_TEST_CASE(test_tan, tan_middle_values);
}

void runner(void)
{
	RUN_TEST_GROUP(test_tan);
}

int main(int argc, char *argv[])
{
	UnityMain(argc, (const char **)argv, runner);
	return 0;
}