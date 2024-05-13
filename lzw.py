'''LZW compression algorithm'''

from os import path as os_path

class LZW:

    def encode(self, file_bytes: bytes) -> tuple[bytes, int]:
        if not file_bytes:
            return b'', []

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
                        encoded_text.extend(dictionary[temp[:-1]].to_bytes(bytes_amount, 'big'))
                        dictionary[temp] = counter
                        counter += 1
                        temp = bytes([char])
                encoded_text.extend(dictionary[temp].to_bytes(bytes_amount, 'big'))
                break
            except OverflowError:
                bytes_amount += 1
                dictionary = {bytes([i]): i for i in range(256)}
                encoded_text = bytearray()
                temp = b""
                counter = 256


        return bytes(encoded_text), bytes_amount


    def decode(self, code: str, coding_dict: list) -> str:
        coding_dict = dict(enumerate(coding_dict))
        coding_dict_start = coding_dict.copy()

        decoded_text = ""
        temp = ""
        code = list(map(int, code.split()))

        for num in code:
            if num in coding_dict:
                decoded_text += coding_dict[num]
                temp += coding_dict[num]
                if num in coding_dict_start:
                    if temp not in coding_dict.values():
                        coding_dict[len(coding_dict)] = temp
                        temp = temp[-1]
                else:
                    temp_2 = ""
                    for char in temp:
                        temp_2 += char
                        if temp_2 not in coding_dict.values():
                            coding_dict[len(coding_dict)] = temp_2
                            temp_2 = temp_2[:-1]
                            break
                    temp = temp[len(temp_2) :]
            else:
                temp = temp + temp[0]
                coding_dict[len(coding_dict)] = temp
                decoded_text += coding_dict[num]
        return decoded_text

    def encode_file(self, path: str):
        with open(path, "rb") as file:
            file_bytes = file.read()

        file = os_path.basename(path)
        file_extension = file.split('.')[1]

        encoded_text, bytes_amount = self.encode(file_bytes)

        with open(f"encoded_{file}.lzw", 'wb') as file:
            file.write(file_extension.encode()+b'|'+bytes_amount.to_bytes(1, 'big'+b'|'+encoded_text))
