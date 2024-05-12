"""
LZ78 
"""

import lz78 as lz78

class Codder:
    """
    codder class
    """

    @staticmethod
    def encoding(path:str, compress_algorithm:object):
        """
        encodes
        """
        with open(path, 'rb') as file:
            image = file.read()

        print(len(image))

        encoded_data = compress_algorithm.encode(image)

        file_type = path[::-1].split('.', maxsplit=1)[0][::-1]
        file_path = path[::-1].split('.', maxsplit=1)[1][::-1]+'.'+compress_algorithm.name.lower()

        with open(file_path, 'wb') as file:
            for value in encoded_data:
                val0 = value[0] if value[0] else 0
                val0 = val0.to_bytes(3, byteorder='big')
                file.write(val0)
                file.write(value[1])

        return file_path, file_type, compress_algorithm

    @staticmethod
    def decoding(path:str, f_type:str, compress_algorithm:object, start_dict:dict = None):
        """
        decodes
        """
        with open(path, 'rb') as file:
            encoded_data = []

            while len(byte := file.read(4)) == 4:

                number = int.from_bytes(byte[:3], byteorder='big')
                character = bytes([byte[3]])
                encoded_data.append((number, character))

        if len(byte) != 4:
            encoded_data.append((0, byte))

        if start_dict:
            decoded = compress_algorithm.decode(encoded_data, start_dict)
        else:
            decoded = compress_algorithm.decode(encoded_data)

        file_path = path[::-1].split('.', maxsplit=1)[1][::-1]+'_decoded.'+f_type
        with open(file_path, 'wb') as file:
            file.write(decoded)

        return decoded

if __name__ == "__main__":

    codder = lz78.LZ78()
    file_m = Codder()

    encoded = file_m.encoding("high.jpg", codder)
    decoded = file_m.decoding("high.lz78", "jpg", codder)
