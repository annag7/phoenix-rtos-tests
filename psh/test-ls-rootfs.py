# Phoenix-RTOS
#
# phoenix-rtos-tests
#
# additional psh ls command test for targets with root file system
#
# Copyright 2022 Phoenix Systems
# Author: Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

import psh.tools.psh as psh
from psh.test_ls import SEPARATOR_PATTERN
from psh.tools.common import OPTIONAL_CONTROL_CODE, create_testdir


ROOT_TEST_DIR = 'test_ls_rootfs_dir'


def assert_ls_pshcmds(p, psh_cmds):
    # history and exit symlinks shouldn't be present in bin
    psh_cmds = set(psh_cmds) - {'history', 'exit'}

    psh_cmd_pattern = OPTIONAL_CONTROL_CODE
    psh_cmd_pattern += r'(?P<cmd>' + '|'.join(psh_cmds) + r')'
    psh_cmd_pattern += SEPARATOR_PATTERN

    cmd = 'ls bin'
    listed_psh_cmds = set()
    p.sendline(cmd)
    p.expect(cmd)

    while p.expect([psh.PROMPT, psh_cmd_pattern]):
        listed_psh_cmds.add(p.match['cmd'])

    missing_cmds = psh_cmds - listed_psh_cmds
    msg = ("Not all psh commands from help are listed in /bin!"
           + f"\nMissing commands: {missing_cmds}")

    assert not missing_cmds, msg


def assert_ls_t(p):
    msg_date = "Wrong output when setting date!"
    msg_touch = "Wrong output when creating file!"
    msg_mkdir = "Wrong output when creating directory!"
    date_pattern = r'\w{3},\s+\d{2}\s+\w{3}\s+\d{2}\s+\d{2}:\d{2}:\d{2}' + psh.EOL

    psh.assert_cmd(p, 'date -s @160000000', date_pattern, msg_date, is_regex=True)
    psh.assert_cmd(p, f'touch {ROOT_TEST_DIR}/file_created_earliest', '', msg_touch)

    psh.assert_cmd(p, 'date -s @162000000', date_pattern, msg_date, is_regex=True)
    psh.assert_cmd(p, f'mkdir {ROOT_TEST_DIR}/dir_created_second', '', msg_mkdir)

    psh.assert_cmd(p, 'date -s @164000000', date_pattern, msg_date, is_regex=True)
    psh.assert_cmd(p, f'touch {ROOT_TEST_DIR}/file_created_last', '', msg_touch)

    expected_pattern = r'.*?file_created_last.*?dir_created_second.*?file_created_earliest.*?'
    expected_pattern = expected_pattern + psh.EOL

    msg = "files are not printed in the correct order when calling `ls -t`"
    psh.assert_cmd(p, f'ls -t {ROOT_TEST_DIR}', expected_pattern, msg, is_regex=True)


def assert_ls_S(p):
    expected_pattern = r'.*?psh' + SEPARATOR_PATTERN + r'.*?empty_file' + SEPARATOR_PATTERN + r'.*?'
    expected_pattern = expected_pattern + psh.EOL

    psh.assert_cmd(p, 'touch /bin/empty_file', '', 'Wrong output when creating empty file!')

    # TODO: use only newly created files, when it will be possible to write content to a file
    psh.assert_cmd(
        pexpect_proc=p,
        cmd='ls -1S /bin',
        expected=expected_pattern,
        msg='Wrong output, when calling `ls -1S`',
        is_regex=True)


def assert_multi(p):
    files = []
    for i in range(20):
        files.append(f'file{i}')
    testdir_multi = f'{ROOT_TEST_DIR}/multi'
    psh.assert_cmd(p, f'mkdir {testdir_multi}', '', 'Wrong output when creating test directory for multiple files')
    for file in files:
        psh.assert_cmd(p, f'touch {testdir_multi}/{file}', '', f'Wrong output when creating {testdir_multi}/{file}')
    # assert at least 2 rows of listed files, list's content isn't checked here
    expected = r'([^\r\n]+(\r+\n)){2,}'
    msg = "Multiple files wasn't listed correctly in two lines"
    psh.assert_cmd(p, f'ls {testdir_multi}', expected, msg, is_regex=True)


def assert_extralong(p):
    testdir_long = f'{ROOT_TEST_DIR}/long'
    # fname longer than standard window size: 80
    long_fname = 'loremipsum' * 9
    # there shouldn't be any new line separator in listed fname, window size should split it up if necessarily
    expected = OPTIONAL_CONTROL_CODE + long_fname + OPTIONAL_CONTROL_CODE + psh.EOL
    psh.assert_cmd(p, f'mkdir {testdir_long}', '', 'Wrong output when creating test directory for long file')
    psh.assert_cmd(p, f'touch {testdir_long}/{long_fname}', '', f'Wrong output when creating file: {long_fname}')

    msg = "Extra long file name hasn't been printed properly!"
    psh.assert_cmd(p, f'ls {testdir_long}', expected, msg, is_regex=True)


def harness(p):
    psh.init(p)
    create_testdir(p, ROOT_TEST_DIR)

    # these cases may not work on non-rootfs targets, because of too many internal directories
    assert_multi(p)
    assert_extralong(p)

    psh_cmds = psh.get_commands(p)
    assert_ls_t(p)
    assert_ls_S(p)
    assert_ls_pshcmds(p, psh_cmds)
