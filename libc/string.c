/*
 * Phoenix-RTOS
 *
 * libc-tests
 *
 * Testing string.h functions
 *
 * Copyright 2021 Phoenix Systems
 * Author: Mateusz Niewiadomski
 *
 * This file is part of Phoenix-RTOS.
 *
 * %LICENSE%
 */

#include <string.h>

#include <unity_fixture.h>

#define SRC_SIZE  5
#define DEST_SIZE 5

#define SRC1_SIZE 4
#define SRC2_SIZE 6
#define BUF_SIZE  12


/* fixtures for strlcpy */
char source[SRC_SIZE];
char dest[DEST_SIZE];

/* fixtures for strlcat */
char source1[SRC1_SIZE];
char source2[SRC2_SIZE];
char buffer[BUF_SIZE];

/* common fixtures */
int retval;


TEST_GROUP(string_strlcpy);


TEST_SETUP(string_strlcpy)
{
	memcpy(source, "abcd", SRC_SIZE);
	memcpy(dest, "xxxx", DEST_SIZE);
}


TEST_TEAR_DOWN(string_strlcpy)
{
}


TEST(string_strlcpy, strlcpy_fullcopy)
{
	/* Test full copy */
	retval = strlcpy(dest, source, sizeof(source));
	TEST_ASSERT_EQUAL_INT(sizeof(source) - 1, retval);
	TEST_ASSERT_EQUAL_STRING(source, dest);
}


TEST(string_strlcpy, strlcpy_shorter)
{
	/* Test shorter than source copy */
	retval = strlcpy(dest, source, sizeof(source) - 2);
	TEST_ASSERT_EQUAL_STRING("ab", dest);
	TEST_ASSERT_EQUAL_INT(sizeof(source) - 1, retval);
}


TEST(string_strlcpy, strlcpy_longer)
{
	/* Test longer than source copy */
	source[3] = '\0'; /* source is now "abc" null terminated; */
	retval = strlcpy(dest, source, sizeof(source));
	TEST_ASSERT_EQUAL_STRING("abc", dest);
	TEST_ASSERT_EQUAL_INT(sizeof(source) - 2, retval);
	source[3] = 'd';
}


TEST(string_strlcpy, strlcpy_onelength)
{
	/* Test 1 length copy */
	retval = strlcpy(dest, source, 1);
	TEST_ASSERT_EQUAL_STRING("", dest);
	TEST_ASSERT_EQUAL_INT(sizeof(source) - 1, retval);
}


TEST(string_strlcpy, strlcpy_zerolength)
{
	/* Test 0 length copy */
	retval = strlcpy(dest, source, 0);
	TEST_ASSERT_EQUAL_STRING("xxxx", dest);
	TEST_ASSERT_EQUAL_INT(sizeof(source) - 1, retval);
}


TEST_GROUP_RUNNER(string_strlcpy)
{
	RUN_TEST_CASE(string_strlcpy, strlcpy_fullcopy);
	RUN_TEST_CASE(string_strlcpy, strlcpy_shorter);
	RUN_TEST_CASE(string_strlcpy, strlcpy_longer);
	RUN_TEST_CASE(string_strlcpy, strlcpy_onelength);
	RUN_TEST_CASE(string_strlcpy, strlcpy_zerolength);
}


TEST_GROUP(string_strlcat);


TEST_SETUP(string_strlcat)
{
	memcpy(source1, "abc", SRC1_SIZE);
	memcpy(source2, "defgh", SRC2_SIZE);
	memcpy(buffer, "klmnopqrstu", BUF_SIZE);
}


TEST_TEAR_DOWN(string_strlcat)
{
}


TEST(string_strlcat, strlcat_fullconcat_empty)
{
	memset(buffer, '\0', sizeof(buffer));

	/* Normal, full concat to empty string */
	retval = strlcat(buffer, source1, sizeof(buffer));
	TEST_ASSERT_EQUAL_INT(3, retval);
	TEST_ASSERT_EQUAL_STRING(source1, buffer);
}


TEST(string_strlcat, strlcat_fullconcat_part)
{
	buffer[3] = '\0';

	/* Normal full concat to partially filled string */
	retval = strlcat(buffer, source2, sizeof(buffer));
	TEST_ASSERT_EQUAL_INT(sizeof(source2) + 2, retval);
	TEST_ASSERT_EQUAL_STRING("klmdefgh", buffer);
}


TEST(string_strlcat, strlcat_partconcat_overflow)
{
	buffer[8] = '\0';

	/* Partial concat to partially filled string that should overflow the buffer */
	retval = strlcat(buffer, source2, sizeof(buffer));
	TEST_ASSERT_EQUAL_INT(sizeof(buffer) + 1, retval);
	TEST_ASSERT_EQUAL_STRING("klmnopqrdef", buffer);
}


TEST(string_strlcat, strlcat_onelength)
{
	/* 1 length concat */
	buffer[6] = '\0';
	retval = strlcat(buffer, source2, 1);
	TEST_ASSERT_EQUAL_INT(sizeof(source2), retval);
	TEST_ASSERT_EQUAL_STRING("klmnop", buffer);
}


TEST(string_strlcat, strlcat_zerolength)
{
	/* 0 length concat */
	buffer[6] = '\0';
	retval = strlcat(buffer, source2, 0);
	TEST_ASSERT_EQUAL_INT(sizeof(source2) - 1, retval);
	TEST_ASSERT_EQUAL_STRING("klmnop", buffer);
}


TEST_GROUP_RUNNER(string_strlcat)
{
	RUN_TEST_CASE(string_strlcat, strlcat_fullconcat_empty);
	RUN_TEST_CASE(string_strlcat, strlcat_fullconcat_part);
	RUN_TEST_CASE(string_strlcat, strlcat_partconcat_overflow);
	RUN_TEST_CASE(string_strlcat, strlcat_onelength);
	RUN_TEST_CASE(string_strlcat, strlcat_zerolength);
}
