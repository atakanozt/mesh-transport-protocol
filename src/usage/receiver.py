"""
Client-side script to send a Join Request Message.
"""
import socket
from src.packet import SessionEstablishmentPacket

server_ip = '127.0.0.1'
server_port = 12345
server_address = (server_ip, server_port)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def send_join_request():
    message_type_id = 1
    data = b"Client wants to join"
    join_request_message = bytes([message_type_id]) + data

    client_socket.sendto(join_request_message, server_address)
    print("Sent JOIN REQUEST to the server.")

    response_bytes, _ = client_socket.recvfrom(1024)
    print("Received response from the server:", SessionEstablishmentPacket.decode(response_bytes))


send_join_request()

client_socket.close()
