import struct
import binascii
from socket import *
import time
import random
import select
import sys

"""
packet.py
Author: Alex Basagoitia & Matt Houston
Date: 05/05/2019
Description: Defines fabricated ICMP packets.
"""


class Packet:
    def __init__(self, p_type, ident, seq, data):
        self.p_type = p_type
        self.code = 0
        self.checksum = 0
        self.ident = 1  # ident
        self.seq = seq
        self.data = data

    def parse_packet(self):
        header = struct.pack("!bbHHh", self.p_type, self.code,
                             self.checksum, self.ident, self.seq)
        # https://www.programiz.com/python-programming/methods/built-in/bytearray
        data_bytes = bytearray(self.data, 'utf-8')
        header = header + data_bytes

        self.checksum = self.create_checksum(header)

        header = struct.pack("!bbHHh", self.p_type, self.code,
                             self.checksum, self.ident, self.seq)

        return header + data_bytes

    def create_checksum(self, source_string):
        # http://ferozedaud.blogspot.com/2016/10/implementing-ping-client-in-python-part_4.html
        # https://github.com/JanKari/python_ping
        countTo = (int(len(source_string)/2))*2
        sum = 0
        count = 0

        loByte = 0
        hiByte = 0
        while count < countTo:
            if (sys.byteorder == "little"):
                loByte = source_string[count]
                hiByte = source_string[count + 1]
            else:
                loByte = source_string[count + 1]
                hiByte = source_string[count]
            try:
                sum = sum + (hiByte * 256 + loByte)
            except:
                sum = sum + (ord(hiByte) * 256 + ord(loByte))
            count += 2

        # Handle last byte if applicable (odd-number of bytes)
        # Endianness should be irrelevant in this case
        if countTo < len(source_string):  # Check for odd length
            loByte = source_string[len(source_string)-1]
            try:      # For Python3
                sum += loByte
            except:   # For Python2
                sum += ord(loByte)

        # Truncate sum to 32 bits (a variance from ping.c, which
        sum &= 0xffffffff
        # uses signed ints, but overflow is unlikely in ping)

        sum = (sum >> 16) + (sum & 0xffff)    # Add high 16 bits to low 16 bits
        sum += (sum >> 16)                    # Add carry from above (if any)
        answer = ~sum & 0xffff  # Invert and truncate to 16 bits
        answer = htons(answer)
        return answer
