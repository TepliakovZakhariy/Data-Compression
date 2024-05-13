"""
LZ78 class
"""

import time
class LZ78:
    """
    lz78 class
    """

    name = "lz78"

    @staticmethod
    def encode(data):
        """
        encodes binary data
        """

        dictionary = {}
        output = []

        prefix = b""

        for byte in data:
            prefix += bytes([byte])

            if prefix not in dictionary:
                dictionary[prefix] = len(dictionary) + 1
                output.append((dictionary.get(prefix[:-1], 0), prefix[-1:]))
                prefix = b""

        if prefix:
            output.append((0, prefix))

        return output

    @staticmethod
    def decode(path):
        """
        decodes binary sequence
        """

        dictionary = {0: b""}
        output = b""

        with open(path, "rb") as file:

            length = int(int.from_bytes(file.read(1), byteorder="big"))
            counter = 1
            file.read(length)

            try:
                while byte := file.read(4):
                    number = int.from_bytes(byte[:3], "big")
                    character = bytes([byte[3]])
                    decoded = dictionary[number] + character
                    output += decoded
                    dictionary[counter] = decoded
                    counter += 1

            except IndexError:
                output += byte

            return output
