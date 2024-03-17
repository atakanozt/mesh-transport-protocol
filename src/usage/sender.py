"""
This module is responsible for handling server-side logic for a multicast protocol.
"""

import socket
from src.packet import SessionEstablishmentPacket, ExtensionElement, BaseMessage

server_ip = '127.0.0.1'
server_port = 12345
server_address = (server_ip, server_port)
buffer_size = 1024

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

print(f"UDP server up and listening at {server_address}")

NODES_INFO = []


def send_session_establishment_response(client_address):
    """
    Sends a SessionEstablishmentPacket back to the client.
    """
    response_packet = SessionEstablishmentPacket(version=1, session_id=99, group_size=len(NODES_INFO),
                                                 nodes_info=NODES_INFO)
    packet_bytes = response_packet.encode()
    server_socket.sendto(packet_bytes, client_address)
    print(f"Sent SessionEstablishmentPacket to {client_address}")


def handle_message_request(message_bytes, client_address):
    processed_message = BaseMessage.decode(message_bytes)
    if processed_message.message_type == 'JOIN_REQUEST':
        NODES_INFO.append(client_address)
        send_session_establishment_response(client_address)
    # NOT IMPLEMENTED YET


try:
    while True:
        message_bytes, client_address = server_socket.recvfrom(buffer_size)
        print(f"Received packet from {client_address}")
        handle_message_request(message_bytes, client_address)


except KeyboardInterrupt:
    print("Server is shutting down.")
finally:
    server_socket.close()
