"""
This module is responsible for handling server (actually there is no such thing as server in multicast protocol but for
simplicity I will call it as server).
"""

import socket
from src.packet import SessionEstablishmentPacket, ExtensionElement

server_ip = '127.0.0.1'
server_port = 12345
server_address = (server_ip, server_port)
buffer_size = 1024

# Create a UDP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

print(f"UDP server up and listening at {server_address}")

try:
    while True:
        bytes_address_pair = server_socket.recvfrom(buffer_size)
        message_bytes = bytes_address_pair[0]
        address = bytes_address_pair[1]

        # Decode the incoming bytes into a SessionEstablishmentPacket
        packet = SessionEstablishmentPacket.decode(message_bytes)

        print(f"Received packet from {address}")
        print(
            f"Packet data: Version: {packet.version}, Session ID: {packet.session_id}, Group Size: {packet.group_size}")


except KeyboardInterrupt:
    print("Server is shutting down.")
finally:
    server_socket.close()
