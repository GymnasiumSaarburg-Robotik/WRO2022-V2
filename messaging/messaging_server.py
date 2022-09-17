#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!
from time import sleep

from pybricks.messaging import BluetoothMailboxServer, NumericMailbox
from pybricks.hubs import EV3Brick

class messaging_server:

    # 0 -> Zone links: Frei
    # 1 -> Zone links: Belegt
    # 2 -> Zone rechts: Frei
    # 3 -> Zone rechts: Belegt

    def __init__(self):
        self.ev3 = EV3Brick()
        try:
            self.server = BluetoothMailboxServer()
            self.databox_server = NumericMailbox('data_server', self.server)
            self.databox_client = NumericMailbox('data_client', self.server)
            # Depends on starting pos
            self.zone0unoccupied = False
            self.zone1unoccupied = False
            self.ev3.speaker.beep(400, 15)
            self.server.wait_for_connection()
            self.ev3.speaker.beep(400, 15)
        except:
            self.zone0unoccupied = True
            self.zone1unoccupied = True
            self.ev3.speaker.beep(300, 500)

    def is_zone0_unoccupied(self):
        return self.zone0unoccupied

    def is_zone1_unoccupied(self):
        return self.zone1unoccupied

    def refresh(self, value=None):
        if self.databox_server.read() is None:
            return
        if value is None:
            value = self.databox_server.read()
        if value == 0:
            self.zone0unoccupied = True
        if value == 1:
            self.zone0unoccupied = False
        if value == 2:
            self.zone1unoccupied = True
        if value == 3:
            self.zone1unoccupied = False

    def send(self, value):
        self.ev3.speaker.beep(400, 50)
        self.databox_client.send(value)

    def wait_for_zone0(self, value=True):
        while True:
            self.refresh()
            if value is self.zone0unoccupied:
                self.zone0unoccupied = False
                break

    def wait_for_zone1(self, value=True):
        while True:
            self.refresh()
            if value is self.zone1unoccupied:
                self.zone1unoccupied = False
                self.databox_server.send(3)
                break

