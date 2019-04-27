# Imports
from socket import *
import threading
import sys
import struct
from packet import Packet


def create_socket():
    try:
        new_socket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
        new_socket.bind(("", 4000))
        return new_socket

    except Exception as e:
        print(f"Failed to create socket: {e}")


def send_file(add, conn_socket):
    file_path = input("File path: ")

    with open(file_path, 'r') as upload_file:
        file_contents = upload_file.read()
        if (sys.getsizeof(file_contents) > 950):
            split_array = split(file_contents)
            print(split_array)


def split(message):
    split_message = [message[i:i+950] for i in range(0, len(message), 950)]
    print(split_message)
    return split_message


def send_msg(addr, conn_socket):
    while True:
        msg = input("Type your message: ")
        if (msg == "<file>"):
            send_file(addr, conn_socket)
        else:
            create_packet = Packet(8, 1, 1, msg)
            complete_packet = create_packet.parse_packet()

            while (complete_packet):
                sent = conn_socket.sendto(complete_packet, (addr, 1))
                complete_packet = complete_packet[sent:]


def get_msg(addr, conn_socket):
    while True:
        recv_packet, recv_addr = conn_socket.recvfrom(1024)
        header = recv_packet[20:28]
        ptype, code, checksum, pid, seq = struct.unpack('bbHHh', header)

        if (gethostbyname(addr) == recv_addr[0] and ptype != 0):
            print(f"Reply: {recv_packet[28:].decode()}")


def main():
    conn_addr = input("Connection Address: ")
    conn_socket = create_socket()

    send_worker_thread = threading.Thread(
        target=send_msg, args=(conn_addr, conn_socket))
    recv_worker_thread = threading.Thread(
        target=get_msg, args=(conn_addr, conn_socket))

    send_worker_thread.start()
    recv_worker_thread.start()


if __name__ == "__main__":
    main()
