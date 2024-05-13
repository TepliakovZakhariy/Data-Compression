from time import time

class LZ77:
    def __init__(self, buffer_size: int) -> None:
        self.buffer_size = buffer_size

    def encode(self, text: str) -> str:
        encoding = "latin-1"
        i = 0
        encoded_bytes = bytearray()
        text_len = len(text)
        while i < text_len:
            buffer_start = max(0, i - self.buffer_size)
            buffer_end = i
            code_len = 0
            last_code_len = 0
            first_i = 0
            for buffer_i in range(buffer_start, buffer_end):
                code_len = 0
                encoded_el = ""
                if text[buffer_i] == text[i]:
                    code_len += 1
                    encoded_el = text[buffer_i]
                    buffer_i2 = buffer_i + 1
                    while buffer_i2 < buffer_end + code_len:
                        if i + code_len >= text_len:
                            break
                        if text[buffer_i2] == text[i + code_len]:
                            code_len += 1
                            encoded_el += text[buffer_i2]
                        else:
                            break
                        buffer_i2 += 1
                if code_len >= last_code_len:
                    first_i = i - buffer_i if code_len else 0
                    last_code_len = code_len
            last_el = text[i + last_code_len] if i + last_code_len < text_len else ""
            encoded_bytes.extend(f"{first_i},{last_code_len},{last_el}".encode(encoding))
            i += last_code_len + 1
        return bytes(encoded_bytes)

    def encode_file(self, file_path: str, encoded_path: str) -> str:
        encoding = "latin-1"
        with open(file_path, "rb") as file:
            file_bytes = file.read()
            file_text = file_bytes.decode(encoding)

        extension = file_path.split(".")[-1]
        encoded_bytes = (extension + "|").encode(encoding) + self.encode(file_text)

        with open(encoded_path, "wb") as file:
            file.write(encoded_bytes)

    @staticmethod
    def _text2list(text: str) -> list[tuple]:
        code = []
        part = 0
        num = ""
        code_part = tuple()
        for char in text:
            if part == 2:
                code.append((code_part[0], code_part[1], char))
                code_part = tuple()
                part = 0
            elif char == ",":
                code_part = code_part + (int(num),)
                num = ""
                part += 1
            else:
                num += char
        if part == 2:
            code.append((code_part[0], code_part[1], ""))
        return code

    @staticmethod
    def get_extension(encoded_path: str) -> str:
        encoding = "latin-1"
        with open(encoded_path, "rb") as file:
            read_bytes = file.read()
        encoded_text = read_bytes.decode(encoding)
        extension = ""
        for sym in encoded_text:
            if sym == "|":
                break
            extension += sym
        return extension

    def decode_file(self, encoded_path: str, new_path: str):
        encoding="latin-1"
        with open(encoded_path, "rb") as file:
            read_bytes = file.read()

        encoded_text = read_bytes.decode(encoding)
        for i, sym in enumerate(encoded_text):
            if sym == "|":
                break
        encoded_text = encoded_text[i + 1:]

        decoded_text = self.decode(encoded_text)
        with open(new_path, "wb") as file:
            file.write(decoded_text.encode(encoding))


    def decode(self, text: str) -> str:
        i = 0
        code = self._text2list(text)
        decoded_text = ""
        for buffer_i, code_len, last_el in code:
            if code_len - buffer_i > 0:
                encoded_part = decoded_text[i - buffer_i: i] * (code_len // buffer_i + 1)
                decoded_text += encoded_part[:code_len] + last_el
            else:
                decoded_text += decoded_text[i - buffer_i: i - buffer_i + code_len] + last_el
            i += code_len + 1
        return decoded_text

if __name__ == "__main__":
    lz = LZ77(100)
    file_path = r"tree.jpg"
    encoded_path = r"encoded_tree.lz77"
    decoded_path = "decoded_tree.jpg"
    start = time()
    lz.encode_file(file_path, encoded_path)
    print("encoding time:", time() - start)
    start = time()
    lz.decode_file(encoded_path, decoded_path)
    print("decoding time:", time() - start)
    with open(file_path, "rb") as file:
        with open(decoded_path, "rb") as file2:
            assert file.read() == file2.read()