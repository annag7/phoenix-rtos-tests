# Phoenix-RTOS
#
# phoenix-rtos-tests
#
# common tools for psh related tests
#
# Copyright 2022 Phoenix Systems
# Author: Damian Loewnau
#
# This file is part of Phoenix-RTOS.
#
# %LICENSE%
#

import psh.tools.psh as psh

# according to control sequence introducer pattern
CONTROL_CODE = r'(\x1b\[[\x30-\x3F]*[\x20-\x2F]*[\x40-\x7E])'
OPTIONAL_CONTROL_CODE = CONTROL_CODE + r'?'


def create_testdir(p, dirname):
    # TODO: has to be changed after adding rm implementation and removing test directories
    msg = '\n'.join(['Wrong output when creating a test directory!',
                     'Probably the directory has already been created.',
                     'Try to re-build the project and run specified test second time.'])

    psh.assert_cmd(p, f'mkdir {dirname}', '', msg)
