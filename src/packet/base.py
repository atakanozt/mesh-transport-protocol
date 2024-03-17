class BaseMessage:
    # Mapping of message type identifiers to classes
    message_types = {
        1: 'JoinRequestMessage',
        2: 'AckMessage',
    }

    def __init__(self, message_type, data):
        self.message_type = message_type
        self.data = data

    @staticmethod
    def decode(message_bytes):
        # first byte indicates the message type
        message_type_id = message_bytes[0]

        # The rest of the message is the data
        data = message_bytes[1:]

        # Determine the message class based on the type identifier
        if message_type_id in BaseMessage.message_types:
            message_class = globals()[BaseMessage.message_types[message_type_id]]
            return message_class(data)
        else:
            raise ValueError("Unknown message type")


class JoinRequestMessage(BaseMessage):
    def __init__(self, data):
        super().__init__("JOIN_REQUEST", data)


class AckMessage(BaseMessage):
    def __init__(self, data):
        super().__init__("ACK", data)
