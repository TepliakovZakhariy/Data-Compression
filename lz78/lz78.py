"""
LZ78 
"""

from lz78.algorythm import LZ78

class Codder:
    """
    codder class
    """

    @staticmethod
    def encoding(path: str, path_to_save: str):
        """
        encodes
        """
        with open(path, "rb") as file:
            image = file.read()

        encoded_data = LZ78.encode(image)

        file_type_previous = path.split(".", maxsplit=1)[-1]
        byte_type = bytes(file_type_previous, encoding="latin1")
        length = len(file_type_previous).to_bytes(1, byteorder="big")

        with open(path_to_save, "wb") as file:
            file.write(length)
            file.write(byte_type)
            for value in encoded_data:
                val0 = value[0] if value[0] else 0
                val0 = val0.to_bytes(3, byteorder="big")
                file.write(val0)
                file.write(value[1])


    @staticmethod
    def decoding(path: str, path_to_save: str):
        """
        decodes
        """

        decoded = LZ78.decode(path)

        with open(path_to_save, "wb") as file:
            file.write(decoded)

        return decoded

    @staticmethod
    def get_extension(path):
        """
        gets extension from path
        """
        with open(path, "rb") as file:

            length = int(int.from_bytes(file.read(1), byteorder="big"))

            return str(file.read(length))[2:-1]
