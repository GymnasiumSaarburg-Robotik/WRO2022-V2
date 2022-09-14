#!/usr/bin/env pybricks-micropython

# Before running this program, make sure the client and server EV3 bricks are
# paired using Bluetooth, but do NOT connect them. The program will take care
# of establishing the connection.

# The server must be started before the client!
from pybricks.hubs import EV3Brick
from pybricks.messaging import BluetoothMailboxServer, TextMailbox, BluetoothMailboxClient, NumericMailbox
from pybricks.hubs import EV3Brick


class messaging_client:

    # 0 -> Zone links: Frei
    # 1 -> Zone links: Belegt
    # 2 -> Zone rechts: Frei
    # 3 -> Zone rechts: Belegt

    def __init__(self):
        self.ev3 = EV3Brick()
        try:
            self.client = BluetoothMailboxClient()
            self.databox_server = NumericMailbox('data_server', self.client)
            self.databox_client = NumericMailbox('data_client', self.client)

            self.client.connect("ev3dev")

            # Depends on starting pos
            self.zone0unoccupied = False
            self.zone1unoccupied = True
            self.ev3.speaker.beep(500, 50)
        except:
            self.ev3.speaker.beep(300, 500)

    def is_zone0_unoccupied(self):
        return self.zone0unoccupied

    def is_zone1_unoccupied(self):
        return self.zone1unoccupied

    def refresh(self, value=None):
        if value is None:
            value = self.databox_client.read()
        if value is None:
            return
        if value == -1:
            self.ev3.speaker.beep(300, 50)
        if value == 0:
            self.zone0unoccupied = True
        if value == 1:
            self.zone0unoccupied = False
        if value == 2:
            self.zone1unoccupied = True
        if value == 3:
            self.zone1unoccupied = False

    def send(self, value):
        self.databox_server.send(value)