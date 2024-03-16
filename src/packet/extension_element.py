import struct


class ExtensionElement:
    """
    This class represents an extension element with a pointer to the next element and information.

    Attributes:
        next_element (int): An integer specifying the type of the next element, or 0 if this is the last element.
        information (bytes): Raw bytes containing the information for this element.
    """

    def __init__(self, next_element: int, information: bytes):
        """
        Constructs an ExtensionElement with the specified next_element type and information content.

        Parameters:
            next_element (int): The type of the next extension element or 0 if this is the last one.
            information (bytes): The information content of this extension element as raw bytes.
        """
        self.next_element = next_element
        self.information = information

    def encode(self):
        """
        Encodes the ExtensionElement into bytes, with a 4-byte next_element field and variable-length information.

        Returns:
            bytes: The byte representation of the extension element.
        """
        # Pack the next_element as a 4-byte unsigned integer and append the information bytes
        element_format = '!I'
        packed_element = struct.pack(element_format, self.next_element) + self.information
        return packed_element

    @staticmethod
    def decode(encoded_element):
        """
        Decodes a byte-encoded ExtensionElement back into an instance of the class.

        Parameters:
            encoded_element (bytes): The byte-encoded extension element.

        Returns:
            ExtensionElement: The decoded extension element as an instance of the class.
        """
        # Unpack the next_element from the first 4 bytes and then extract the information
        element_format = '!I'
        next_element_size = struct.calcsize(element_format)
        next_element, = struct.unpack(element_format, encoded_element[:next_element_size])
        information = encoded_element[next_element_size:]

        return ExtensionElement(next_element, information)
