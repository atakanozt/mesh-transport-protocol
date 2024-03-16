import socket
import struct
import time
from typing import List, Tuple


class SessionEstablishmentPacket:
    # Constant for the length of the session ID in bytes when packed
    SESSION_ID_PACKED_LENGTH = 32

    def __init__(self, version: int, session_id: int, group_size: int, nodes_info: List[Tuple[str, int]],
                 timestamp: float = None):
        """
        Initialize a session establishment packet.

        :param version: The version of the session establishment protocol.
        :param session_id: Unique identifier for the session as an integer.
        :param group_size: The number of nodes (size of the group).
        :param nodes_info: A list of tuples containing node IP addresses and port numbers.
        :param timestamp: The timestamp, defaults to the current time if not provided.
        """
        self.version = version
        self.session_id = session_id
        self.group_size = group_size
        self.timestamp = timestamp or time.time()
        self.nodes_info = nodes_info if nodes_info is not None else []

    def encode(self) -> bytes:
        """
        Encode the packet data into bytes suitable for transmission.

        :return: The binary representation of the packet.
        """
        # Header: version (1 byte), session_id (32 bytes), group size (2 bytes)
        packet = struct.pack('!B', self.version)
        packet += struct.pack('!{}s'.format(self.SESSION_ID_PACKED_LENGTH),
                              self.session_id.to_bytes(self.SESSION_ID_PACKED_LENGTH, 'big'))
        packet += struct.pack('!H', self.group_size)

        # Add node information (IP and port for each node)
        for ip, port in self.nodes_info:
            packet += struct.pack('!4sH', socket.inet_aton(ip), port)

        # Add timestamp
        packet += struct.pack('!d', self.timestamp)

        # Header length and re-add the header to include the length byte itself
        hlen = len(packet) + 1
        packet = struct.pack('!B', hlen) + packet

        return packet

    @classmethod
    def decode(cls, packet: bytes) -> 'SessionEstablishmentPacket':
        """
        Decode a binary packet into a SessionEstablishmentPacket instance.

        :param packet: The binary data to decode.
        :return: A SessionEstablishmentPacket instance.
        """
        # Extract the header length
        hlen = struct.unpack('!B', packet[0:1])[0]

        # Unpack and instantiate the packet
        version, = struct.unpack('!B', packet[1:2])
        session_id = int.from_bytes(packet[2:2 + cls.SESSION_ID_PACKED_LENGTH], 'big')
        group_size, = struct.unpack('!H', packet[34:36])

        nodes_info = []
        current_pos = 36
        for _ in range(group_size):
            ip_packed, port = struct.unpack('!4sH', packet[current_pos:current_pos + 6])
            ip = socket.inet_ntoa(ip_packed)
            nodes_info.append((ip, port))
            current_pos += 6

        timestamp, = struct.unpack('!d', packet[current_pos:current_pos + 8])

        return cls(version, session_id, group_size, nodes_info, timestamp)


if __name__ == '__main__':
    # Example usage
    nodes = [("192.168.1.1", 8080), ("192.168.1.2", 8080)]
    packet = SessionEstablishmentPacket(version=1, session_id=123456789, group_size=len(nodes), nodes_info=nodes)
    encoded_packet = packet.encode()
    # To decode, simply pass the binary data to the decode class method
    decoded_packet = SessionEstablishmentPacket.decode(encoded_packet)

