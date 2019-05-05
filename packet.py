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

        data_bytes = bytearray(self.data, 'utf-8')
        header = header + data_bytes

        self.checksum = self.create_checksum(header)

        header = struct.pack("!bbHHh", self.p_type, self.code,
                             self.checksum, self.ident, self.seq)

        return header + data_bytes

    def create_checksum(self, source_string):
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


# def receive_ping(my_socket, packet_id, time_sent, timeout):
#         # Receive the ping from the socket.
#     time_left = timeout
#     while True:
#         started_select = time.time()
#         ready = select.select([my_socket], [], [], time_left)
#         how_long_in_select = time.time() - started_select
#         if ready[0] == []:  # Timeout
#             return
#         time_received = time.time()
#         rec_packet, addr = my_socket.recvfrom(1024)
#         icmp_header = rec_packet[20:28]
#         type, code, checksum, p_id, sequence = struct.unpack(
#             'bbHHh', icmp_header)
#         if p_id == packet_id:
#             return time_received - time_sent
#         time_left -= time_received - time_sent
#         if time_left <= 0:
#             return


# # def send_one(addr, timeout):
#     try:
#         my_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
#     except Exception as e:
#         print(e)

#     try:
#         host = gethostbyname(addr)
#     except Exception as e:
#         print(e)

#     packet_id = int((id(timeout) * random.random()) / 65535)
#     packet = Packet(8, packet_id, 1, "Hello World")
#     packet_to_send = packet.parse_packet()

#     while (packet):
#         sent = my_socket.sendto(packet_to_send, (addr, 1))
#         packet_to_send = packet_to_send[sent:]

#     delay = receive_ping(my_socket, packet_id, time.time(), timeout)
#     my_socket.close()
#     return delay


#print(send_one("www.google.com", 1))
