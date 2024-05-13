"""LZW compression algorithm"""

class LZW:
    '''LZW compression algorithm'''

    @staticmethod
    def get_extension(file: str) -> str:
        '''Returns the extension of the file'''
        with open(file, "rb") as f:
            text = f.readline()
        return text.split(b"|", maxsplit=1)[0].decode()

    @staticmethod
    def encode(file_bytes: bytes) -> tuple[bytes, int]:
        '''Compresses the bytes'''

        if not file_bytes:
            return b"", 1

        dictionary = {bytes([i]): i for i in range(256)}

        bytes_amount = 3

        encoded_text = bytearray()
        temp = b""
        counter = 256

        while True:
            try:
                for char in file_bytes:
                    temp += bytes([char])
                    if temp not in dictionary:
                        encoded_text.extend(
                            dictionary[temp[:-1]].to_bytes(bytes_amount, "big")
                        )
                        dictionary[temp] = counter
                        counter += 1
                        temp = bytes([char])
                encoded_text.extend(dictionary[temp].to_bytes(bytes_amount, "big"))
                break
            except OverflowError:
                bytes_amount += 1
                dictionary = {bytes([i]): i for i in range(256)}
                encoded_text = bytearray()
                temp = b""
                counter = 256

        return bytes(encoded_text), bytes_amount

    @staticmethod
    def decode(code: bytes, bytes_per_code: int) -> bytes:
        '''Decompresses the bytes'''

        if not code:
            return b""

        dictionary = {i: bytes([i]) for i in range(256)}
        decoded_text = bytearray()
        code_length = len(code)

        code_index = 0
        next_code = 256

        temp = b""

        while code_index < code_length:
            current_code = int.from_bytes(
                code[code_index : code_index + bytes_per_code], "big"
            )
            code_index += bytes_per_code

            if current_code not in dictionary:
                dictionary[current_code] = temp + bytes([temp[0]])

            decoded_text += dictionary[current_code]

            if temp:
                dictionary[next_code] = temp + bytes([dictionary[current_code][0]])
                next_code += 1

            temp = dictionary[current_code]

        return bytes(decoded_text)

    @staticmethod
    def encode_file(path: str, file_name: str):
        '''Compresses the file'''

        with open(path, "rb") as file:
            file_bytes = file.read()

        if '.' in path:
            file_extension = path.split(".")[-1]
        else:
            file_extension = ""

        encoded_text, bytes_amount = LZW.encode(file_bytes)

        with open(file_name, "wb") as file:
            file.write(
                file_extension.encode()
                + b"|"
                + bytes_amount.to_bytes(1, "big")
                + b"|"
                + encoded_text
            )

    @staticmethod
    def decode_file(path: str, file_name: str):
        '''Decompresses the file'''

        with open(path, "rb") as file:
            text = file.read()

        file_extension, bytes_amount, encoded_text = text.split(b"|", 2)
        file_extension = file_extension.decode()
        bytes_amount = int.from_bytes(bytes_amount, "big")

        decoded_text = LZW.decode(encoded_text, bytes_amount)

        with open(file_name, "wb") as file:
            file.write(decoded_text)
