"""
This module is responsible for clients or nodes as you may call.
"""
import socket
from src.packet import SessionEstablishmentPacket

# Client setup
server_ip = '127.0.0.1'
server_port = 12345
server_address = (server_ip, server_port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create a packet to send
nodes_info = [("192.168.1.1", 8080), ("192.168.1.2", 8081)]
packet = SessionEstablishmentPacket(version=1, session_id=42, group_size=len(nodes_info), nodes_info=nodes_info)

# Encode the packet to bytes
packet_bytes = packet.encode()

# Send the packet
client_socket.sendto(packet_bytes, server_address)
print(f"Sent packet to server at {server_address}")

# Optionally, receive a response from the server and process it

client_socket.close()
