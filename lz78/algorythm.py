"""
LZ78 class
"""
import io

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
        decodes encoded be  file
        """
        dictionary = {0: bytearray()}
        output = bytearray()

        with open(path, "rb") as file:
            length = int.from_bytes(file.read(1), byteorder="big")
            file.read(length)

            byte_buffer = io.BytesIO(file.read())
            while True:
                try:
                    byte = byte_buffer.read(4)
                    if not byte:
                        break

                    number = int.from_bytes(byte[:3], "big")
                    character = byte[3:4]
                    decoded = dictionary[number] + character
                    output += decoded
                    dictionary[len(dictionary)] = decoded

                except IndexError:
                    output += byte

        return bytes(output)
