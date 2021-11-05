#
# Phoenix-RTOS test runner
#
# Stm32l4 runner
#
# Copyright 2021 Phoenix SYstems
# Authors: Mateusz Niewiadomski
#
import subprocess
import serial
import time
import pexpect
import pexpect.fdpexpect
import re

from .common import DeviceRunner
from .common import _BOOT_DIR


class Stm32l4Runner(DeviceRunner):

    class oneByOne_fdspawn(pexpect.fdpexpect.fdspawn):

        def send(self, s):
            for c in s:
                super().send(c)
                time.sleep(0.03)

        def sendline(self, s):
            self.send(s)
            super().send('\n')

    OPENOCD_CMD = ['openocd -f interface/stlink.cfg -f target/stm32l4x.cfg -c "reset_config srst_only srst_nogate connect_assert_srst" -c "program ', ' 0x08000000 verify reset exit"']
    IMAGE = 'phoenix-armv7m4-stm32l4x6.bin'

    def __init__(self, port1, port2 = None):
        super().__init__(port1)
        self.port2 = port2
        self.image_flashed = False
        self.openocd_cmd = self.OPENOCD_CMD[0] + str(_BOOT_DIR / self.IMAGE) + self.OPENOCD_CMD[1]

    def flash(self):
        # Flashing with openocd as a separate process
        openocd_process = subprocess.Popen(str(self.openocd_cmd), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = openocd_process.communicate()
        openocd_process.wait()
        # Chcecking openocd flashing result
        verify1 = str(stderr).find('** Verified OK **')
        verify2 = str(stderr).find('shutdown command invoked')
        assert verify1 >= 0 and verify2 >= 0 , "STM32l4Runner: OpenOCD failed to flash target"


    def run(self, test):
        if test.skipped():
            return

        if not test.is_type('harness'):
            test.skip()
            return

        try:
            self.serial = serial.Serial(self.port, baudrate=115200)
        except serial.SerialException:
            test.handle_exception()
            return

        proc = self.oneByOne_fdspawn(self.serial, encoding='ascii', timeout=test.timeout)
        proc.send("\n")

        try:
            test.handle(proc)
        finally:
            self.serial.close()
            