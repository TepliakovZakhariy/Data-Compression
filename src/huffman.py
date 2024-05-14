class DoubleNode:
    def __init__(self, data, prev=None, nxt=None) -> None:
        self.data = data
        self.prev = prev
        self.next = nxt

    def __repr__(self) -> str:
        output = f"{self.data}"
        node = self.next
        while node:
            if node is self:
                break
            output += f" -> {node.data}"
            if node is node.next:
                break
            node = node.next
        return output

    def __str__(self):
        return repr(self)


class Node:
    def __init__(self, weight: int, chars: list[list[str]]):
        self.weight = weight
        self.chars = chars

    def __lt__(self, other):
        return self.weight < other.weight

    def __add__(self, other):
        return Node(self.weight + other.weight, self.chars + other.chars)

    def __iter__(self):
        return iter(self.chars)

    def __repr__(self):
        return f"node: {self.weight}, {self.chars}"


class Huffman:
    def __init__(self, block_size: int = 1) -> None:
        self.block_size = block_size

    def count_frequency(self, text: str) -> dict[str, int]:
        frequency = {}
        for i in range(0, len(text), self.block_size):
            cur_chars = text[i : i + self.block_size]
            frequency[cur_chars] = frequency.get(cur_chars, 0) + 1
        return frequency

    def encode(self, text: str) -> tuple[str, dict[str, str]]:
        if not text:
            return "", {}
        frequency = self.count_frequency(text)

        tree = [Node(weight, [[char, ""]]) for char, weight in frequency.items()]
        tree = sorted(tree, key=lambda node: node.weight)
        tree_len = len(tree)
        if tree_len == 1:
            return "0" * frequency[text[0]], {text[0]: "0"}
        head = DoubleNode(tree[0])
        node = head
        for el in tree[1:]:
            node.next = DoubleNode(el, node)
            node = node.next
        last_node = None
        while head and head.next:
            first_min = head.data
            second_min = head.next.data
            head = head.next.next
            if head:
                head.prev = None
            for char in first_min:
                char[1] = "1" + char[1]
            for char in second_min:
                char[1] = "0" + char[1]
            new_weight = first_min.weight + second_min.weight
            if not head:
                tree = [first_min + second_min]
                break
            elif new_weight <= head.data.weight:
                head.prev = DoubleNode(first_min + second_min, None, head)
                head = head.prev
            else:
                node = head if last_node is None else last_node
                prev_node = None if last_node is None else last_node.prev
                while node:
                    if (
                        prev_node
                        and prev_node.data.weight <= new_weight <= node.data.weight
                    ):
                        prev_node.next = DoubleNode(
                            first_min + second_min, prev_node, node
                        )
                        last_node = prev_node.next
                        node.prev = last_node
                        break
                    if node.next is None:
                        node.next = DoubleNode(first_min + second_min, node)
                        last_node = node.next
                        break
                    prev_node = node
                    node = node.next
            tree_len -= 1
        huffman_code = {rf"{item[0]}": item[1] for item in tree[0]}
        temp = ""
        encoded_bytes = bytearray()
        for i in range(0, len(text), self.block_size):
            temp += huffman_code[text[i : i + self.block_size]]
            while len(temp) >= 8:
                encoded_bytes.append(int(temp[0:8], 2))
                temp = temp[8:]
        if temp:
            encoded_bytes.append(int(f"{temp:0<8}", 2))
        return bytes(encoded_bytes), huffman_code

    def decode(self, code: str, coding_dict: dict[str, str], reverse=True) -> str:
        decoded_text = ""
        temp = ""
        if code:
            zeros = 8 - len(bin(code[0])) + 2 if code else 0
            myhex = code.hex()
            myint = int(myhex, 16)
            binary_string = "0" * zeros + "{:08b}".format(myint)
        else:
            binary_string = ""
        if reverse:
            coding_dict = {v: c for c, v in coding_dict.items()}
        min_len = len(min(coding_dict.keys(), key=len))
        counter = 0
        for char in binary_string:
            temp += char
            counter += 1
            if counter >= min_len and temp in coding_dict:
                decoded_text += coding_dict[temp]
                temp = ""
                counter = 0
        return decoded_text

    @staticmethod
    def get_extension(encoded_path: str) -> None:
        encoding = "latin-1"
        with open(encoded_path, "rb") as file:
            encoded_text = file.read().decode(encoding)
        extension = ""
        for sym in encoded_text:
            if sym == "|":
                break
            if sym == "/":
                extension = ""
                continue
            extension += sym
        return extension

    def encode_file(self, file_path: str, encoded_path: str) -> None:
        encoding = "latin-1"

        with open(file_path, "rb") as file:
            text = file.read()
            text_str = text.decode(encoding)

        encoded_bytes, coding_dict = self.encode(text_str)

        with open(encoded_path, "wb") as file:
            sorted_coding_dict = sorted(
                coding_dict.items(), key=lambda els: len(els[0]), reverse=True
            )
            encoded_dict = ",".join(rf"{el}:{code}" for el, code in sorted_coding_dict)
            front_string = "/".join(
                [
                    str(len(coding_dict.keys())),
                    str(self.block_size),
                    str(len(sorted_coding_dict[-1][0])),
                    file_path.split(".")[-1],
                ]
            )
            file.write(
                (front_string + "|" + encoded_dict + ";").encode(encoding)
                + encoded_bytes
            )
        return encoded_bytes, coding_dict

    def decode_file(self, encoded_path: str, new_path: str) -> None:
        encoding = "latin-1"
        with open(encoded_path, "rb") as file:
            text = file.read()
        coding_text_dict = text.decode(encoding)
        info_extension = ""
        coding_dict = {}
        chars = ""
        code = ""
        no_dict_i = 0
        creating_dict = False
        code_time = False
        for i, sym in enumerate(coding_text_dict):
            if not creating_dict:
                if sym == "|":
                    codes_left, block_size, smallest_block, _ = info_extension.split(
                        "/", 3
                    )
                    codes_left = int(codes_left)
                    block_size = int(block_size)
                    smallest_block = int(smallest_block)
                    creating_dict = True
                    continue
                info_extension += sym
                continue
            if sym == "," and code_time:
                code_time = False
                coding_dict[code] = chars
                codes_left -= 1
                code = ""
                chars = ""
            elif code_time:
                if sym == ";":
                    coding_dict[code] = chars
                    no_dict_i = i
                    break
                code += sym
            else:
                if sym == ":":
                    if (
                        len(chars) == block_size
                        or codes_left == 1
                        and len(chars) == smallest_block
                    ):
                        code_time = True
                        continue
                chars += sym
        code_i = len(coding_text_dict[:no_dict_i].encode(encoding)) + 1
        code = text[code_i:]

        decoded_text = self.decode(code, coding_dict, False)
        with open(new_path, "wb") as img:
            img.write(decoded_text.encode(encoding))
