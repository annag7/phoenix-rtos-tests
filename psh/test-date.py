# Phoenix-RTOS
#
# phoenix-rtos-tests
#
# psh date command test
#
# Copyright 2021 Phoenix Systems
# Author: Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

import psh.tools.psh as psh

MSG_HELP = (
    "Usage: date [-h] [-s EPOCH] [-d @EPOCH] [+FORMAT]",
    "  -h:  shows this help message",
    "  -s:  set system time described by EPOCH (POSIX time format)",
    "  -d:  display time described by EPOCH (POSIX time format)",
    "  FORMAT: string with POSIX date formatting characters",
    "NOTE: FORMAT string not supported by options: '-s', '-d'")

DFLT_DATE_REG = r'Thu, 01 Jan 70 \d{2}:\d{2}:\d{2}\r+\n'  # default date when image is flashed
SPEC_DATE_REG = r'Sun, 13 Sep 20 12:\d{2}:\d{2}\r+\n'  # arbitrary deta of epoch 1600000000 GMT


# Utility functions
def invalid_format(format):
    return f"date: invalid format '{str(format)}'"


def invalid_date(format):
    return f"date: invalid date '{format}'"


def unrec_arg(arg):
    return f"Unrecognized argument: {arg}"


def test_date(p, cmd, expected_cmd, expected_date, should_succeed):
    # 3) 'date text' does not change date
    if should_succeed:
        psh.assert_cmd(p, cmd=cmd, expected=expected_cmd, msg=f"'{cmd}' does not succeeded", is_regex=True)
        psh.assert_cmd(p, cmd='date', expected=expected_date, msg=f"date not amended by '{cmd}'", is_regex=True)
    else:
        psh.assert_cmd(p, cmd=cmd, expected=expected_cmd, msg=f"'{cmd}' does not fail")
        psh.assert_cmd(p, 'date', expected_date, msg=f"date amended by '{cmd}', but should not", is_regex=True)


# Test parts
def test_corrects(p):
    '''Testing correct `date` commands'''

    # Test help
    psh.assert_cmd(p, 'date -h', MSG_HELP)

    # Test printing and formatting
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, "'date' does not print date", is_regex=True)
    psh.assert_cmd(p, 'date +%Y', "1970", 'date does not process formatting properly')
    psh.assert_cmd(
        p,
        'date +%H:%M:%Sformat',
        r'00:0\d{1}:\d{2}format\r+\n',
        'date does not process formatting properly',
        is_regex=True)

    # Test setting to value
    psh.assert_cmd(p, 'date -s @1600000000', SPEC_DATE_REG, is_regex=True)
    psh.assert_cmd(p, 'date', SPEC_DATE_REG, is_regex=True)

    # Test setting to 0
    psh.assert_cmd(p, 'date -s @0', DFLT_DATE_REG, is_regex=True)
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # Test date parsing
    psh.assert_cmd(p, 'date -d @1600000000', SPEC_DATE_REG, is_regex=True)
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)


def test_incorrect_dateprint(p):
    '''Test incorrect or rare commandlines for printing date'''

    # Incorrect FORMAT passed when printing date
    psh.assert_cmd(p, 'date operand1', invalid_format("operand1"))
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # Incorrect FORMAT passed when printing date
    psh.assert_cmd(p, 'date +operand1', "operand1")
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # too many arguments passed to print, should print first redundant
    psh.assert_cmd(p, 'date operand1 operand2 operand3', unrec_arg("operand2"))
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # nonexistent format '%k' passed to print
    psh.assert_cmd(p, 'date +%Y%k%Y', "1970%k1970")
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)


def test_incorrect_datewrite(p):
    '''Test incorrect commandlines for setting date (no edge cases)'''

    # No argument passed
    psh.assert_cmd(p, 'date -s', "date: option requires an argument -- s")
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # invalid time value
    psh.assert_cmd(p, 'date -s 123456789operand1', invalid_date("123456789operand1"))

    # too many arguments
    psh.assert_cmd(p, 'date -s 1600000000 +format operand1', unrec_arg("operand1"))
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)


def test_incorrect_dateparse(p):
    # No argument passed
    psh.assert_cmd(p, 'date -d', "date: option requires an argument -- d")
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # too many arguments
    psh.assert_cmd(p, 'date -d @1600000000 +format operand1', unrec_arg("operand1"))
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # invalid time value
    psh.assert_cmd(p, 'date -d @1600000000operand1', invalid_date("@1600000000operand1"))
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)

    # no '@' sign
    psh.assert_cmd(p, 'date -d 1600000000', invalid_date("1600000000"))
    psh.assert_cmd(p, 'date', DFLT_DATE_REG, is_regex=True)


def test_edges_datewrite(p):
    '''Test edge cases for epoch value passed to `date -s epoch'''

    # set time to:
    # epoch = 0x7FFFFFFFF0000000
    # epoch < max(signed long long)
    psh.assert_cmd(p, 'date -s @9223372036586340352', r'Thu, 16 Apr 15 \d{2}:\d{2}:\d{2}\r+\n', is_regex=True)
    psh.assert_cmd(p, 'date', r'Thu, 16 Apr 15 \d{2}:\d{2}:\d{2}\r+\n', is_regex=True)
    psh.assert_cmd(p, 'date +%Y', '586515')
    psh.assert_cmd(p, 'date -s @0', DFLT_DATE_REG, is_regex=True)


def harness(p):
    psh.init(p)

    psh.assert_prompt(p)

    test_corrects(p)
    test_incorrect_dateprint(p)
    test_incorrect_datewrite(p)
    test_incorrect_dateparse(p)
    test_edges_datewrite(p)
