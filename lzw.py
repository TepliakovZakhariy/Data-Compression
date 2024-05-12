from misc_funcs import read_file, dict_to_str, huffman_to_bytes, lst_to_bytes, bytes_to_lst
from huffman import Huffman

class LZW:
    def encode(self, text: str) -> tuple[list, list]:
        if not text:
            return "", []

        dictionary = {}
        i = 0
        text1 = len(set(text))
        counter = 0

        for char in text:
            if counter == text1:
                break
            if char not in dictionary:
                dictionary[char] = i
                i += 1
                counter += 1

        result_dictionary = list(dictionary.keys())

        # encoded_text = ''
        # encoded_text = []
        encoded_text = b''
        temp = ""
        counter = len(dictionary)
        abcc=0

        for char in text:
            temp += char
            if temp not in dictionary:
                # encoded_text += (str(dictionary[temp[:-1]])) + " "
                # encoded_text.append(dictionary[temp[:-1]])
                encoded_text += dictionary[temp[:-1]].to_bytes(3, 'big')
                print(abcc)
                abcc+=1
                dictionary[temp] = counter
                counter += 1
                temp = char

        # encoded_text += str(dictionary[temp])
        # encoded_text.append(dictionary[temp])
        encoded_text += dictionary[temp].to_bytes(3, 'big')

        return encoded_text, result_dictionary

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

    def encode_file(self, path: str, encoding: str):
        huffman = Huffman()

        file_str = read_file(path, encoding)

        encoded_text_huffman, coding_dict_huffman = huffman.encode(file_str)
        print(len(encoded_text_huffman))
        # coding_dict_huffman = dict_to_str(coding_dict_huffman)
        # # print(encoded_text_huffman)
        # # print(coding_dict_huffman)
        # print(2)
        # file_extension = path.split(".", 1)[1]
        # file_name = path.split(".", 1)[0]

        # encoded_text_lzw, coding_dict_lzw = self.encode(encoded_text_huffman)
        # coding_dict_lzw = bytes(int(coding_dict_lzw[0]))
        # # print(encoded_text_lzw)
        # # print(coding_dict_lzw)

        # # print(encoded_text_lzw)
        # # print(coding_dict_lzw)
        # print(1)
        # # encoded_text_bytes, byte = lst_to_bytes(encoded_text_lzw)
        # # print(encoded_text_bytes)

        # with open(f"encoded_{file_name}.lzw", "wb") as file:
        #     file.write(file_extension.encode(encoding) + b";" + coding_dict_lzw + b";" + encoded_text_lzw)


if __name__ == "__main__":
    lzw = LZW()
    lzw.encode_file("bug.png", "latin-1")
    # print(lzw.encode("abracadabraabraca"))
