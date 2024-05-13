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
        with open(path, 'rb') as file:
            image = file.read()

        encoded_data = LZ78.encode(image)

        file_type = path[::-1].split('.', maxsplit=1)[0][::-1]
        file_path = path[::-1].split('.', maxsplit=1)[1][::-1]+'.' + LZ78.name.lower()
        file_type_previous = path.split('.', maxsplit=1)[-1]
        byte_type = bytes(file_type_previous, encoding = "latin1")
        length = len(file_type_previous).to_bytes(1, byteorder = "big")

        with open(path_to_save, 'wb') as file:
            file.write(length)
            file.write(byte_type)
            for value in encoded_data:
                val0 = value[0] if value[0] else 0
                val0 = val0.to_bytes(3, byteorder='big')
                file.write(val0)
                file.write(value[1])

        return file_path, file_type, LZ78()

    @staticmethod
    def decoding(path: str, path_to_save: str):
        """
        decodes
        """
        with open(path, 'rb') as file:
            encoded_data = []

            length = int(int.from_bytes(file.read(1), byteorder='big'))

            f_type = str(file.read(length))[2:-1]

            while len(byte := file.read(4)) == 4:

                number = int.from_bytes(byte[:3], byteorder='big')
                character = bytes([byte[3]])
                encoded_data.append((number, character))

        if len(byte) != 4:
            encoded_data.append((0, byte))

        decoded = LZ78.decode(encoded_data)

        file_path = path[::-1].split('.', maxsplit=1)[1][::-1]+'_decoded.'+f_type
        with open(path_to_save + '\\' + file_path, 'wb') as file:
            file.write(decoded)

        return decoded

# if __name__ == "__main__":

#     file_m = Codder()

#     encoded = file_m.encoding("lz78\high.jpg")
#     decoded = file_m.decoding("lz78\high.lz78")
