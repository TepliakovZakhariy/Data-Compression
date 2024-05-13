from time import time
from random import randint


class DoubleNode:
    def __init__(self, data, prev = None, nxt = None) -> None:
        self.data =data
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
    @staticmethod
    def count_frequency(text: str) -> dict[str, int]:
        frequency = {}

        for char in text:
            frequency.setdefault(char, 0)
            frequency[char] += 1

        return frequency

    def encode(self, text: str) -> tuple[str, dict[str, str]]:
        if not text:
            return '', {}

        frequency = {}
        for i in range(0, len(text), self.block_size):
            cur_chars = text[i: i + self.block_size]
            frequency[cur_chars] = frequency.get(cur_chars, 0) + 1

        tree = [Node(weight, [[char,'']]) for char, weight in frequency.items()]
        tree = sorted(tree, key = lambda node: node.weight)
        tree_len = len(tree)
        if tree_len == 1:
            return '0'*frequency[text[0]], {text[0]: '0'}
        head = DoubleNode(tree[0])
        node = head
        for el in tree[1:]:
            node.next = DoubleNode(el, node)
            node = node.next
        last_node = None
        while head and head.next:
            first_min=head.data
            second_min=head.next.data
            head = head.next.next
            if head:
                head.prev = None
            for char in first_min:
                char[1] = '1' + char[1]
            for char in second_min:
                char[1] = '0' + char[1]
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
                    if prev_node and prev_node.data.weight <= new_weight <= node.data.weight:
                        prev_node.next = DoubleNode(first_min + second_min, prev_node, node)
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
            temp += huffman_code[text[i: i + self.block_size]]
            while len(temp) >= 8:
                encoded_bytes.append(int(temp[0:8], 2))
                temp = temp[8:]
        if temp:
            encoded_bytes.append(int(f"{temp:0<8}", 2))
        return encoded_bytes, huffman_code

    def decode(self, code: str, coding_dict: dict[str, str], reverse = True, extra = ("", {}, "")) -> str:

        true_encoded_bytes, true_coding_dict, true_decoded_text = extra
        decoded_text = ""
        temp = ""
        code_lst = list(code)
        codezero = code[0]
        zeros = 8 - len(bin(code[0])) + 2 if code else 0
        myhex = code.hex()
        myint = int(myhex, 16)
        binary_string = "0"*zeros + "{:08b}".format(myint)
        end_k = 0
        true_coding_dict = {v: c for c, v in true_coding_dict.items()}
        res = true_coding_dict == coding_dict
        if reverse:
            coding_dict = {v: c for c, v in coding_dict.items()}
        else:
            print(res)
            if not res:
                print(set(true_coding_dict.keys()).difference(coding_dict.keys()))
                print(set(true_coding_dict.values()).difference(coding_dict.values()))
            print(code == true_encoded_bytes)
        min_len = len(min(coding_dict.keys(), key=len))
        max_len = len(max(coding_dict.keys(), key=len))
        string_len = len(binary_string)
        sum_time = 0
        counter = 0
        for char in binary_string:
            if end_k % 100000 == 0:
                print(end_k / string_len)
            end_k += 1
            temp += char
            counter += 1
            start = time()
            if counter >= min_len and temp in coding_dict:
                decoded_text += coding_dict[temp]
                temp = ""
                counter = 0
            elif counter > max_len:
                print(temp)
                print(end_k / string_len)
                break
            sum_time += time() - start
        if not reverse:
            print(f"time:", sum_time)
            print(decoded_text == true_decoded_text)
        return decoded_text, decoded_text == true_decoded_text

    def encode_file(self, path: str, encoding: str):
        with open(path, 'rb') as file:
            text = file.read()
            text_str = text.decode(encoding)

        encoded_bytes, coding_dict = self.encode(text_str)

        with open('encoded_'+path.split(".", 1)[0], 'wb') as file:
            sorted_coding_dict = sorted(coding_dict.items(), key=lambda els: len(els[0]), reverse=True)
            encoded_dict = ",".join(rf"{el}:{code}" for el, code in sorted_coding_dict)
            front_string = ".".join([str(len(coding_dict.keys())), str(self.block_size), str(len(sorted_coding_dict[-1][0]))]) + "."
            file.write((front_string+path.replace(";", "")+";"+encoded_dict+";").encode(encoding)+encoded_bytes)
        print("encoded")
        return encoded_bytes, coding_dict, self.decode(encoded_bytes, coding_dict)[0]

    def decode_file(self, path: str, encoding: str, extra, best_block, best_decoded):
        with open(path, "rb") as file:
            text = file.read()
        coding_text_dict = text.decode(encoding)
        last_path = ""
        coding_dict = {}
        chars = ""
        code = ""
        no_dict_i = 0
        creating_dict = False
        code_time = False

        for i, sym in enumerate(coding_text_dict):
            mas = coding_text_dict[i-20:i+20]
            if not creating_dict:
                if sym == ";":
                    codes_left, block_size, smallest_block, last_path = last_path.split(".", 3)
                    codes_left= int(codes_left)
                    block_size = int(block_size)
                    smallest_block = int(smallest_block)
                    
                    creating_dict = True
                    continue
                last_path += sym
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
                    if len(chars) == block_size or codes_left == 1 and len(chars) == smallest_block:
                        code_time = True
                        continue
                chars += sym
        code_i = len(coding_text_dict[:no_dict_i].encode(encoding)) + 1
        code = text[code_i:]

        decoded_text, correct = self.decode(code, coding_dict, False, extra)

        print("created_dict")
        if not best_block or (new_len:=len(decoded_text)) < len(best_decoded):
            best_block = self.block_size
            best_decoded = decoded_text
        with open("decoded_" + last_path, "wb") as img:
            img.write(decoded_text.encode(encoding))
        print("decoded")
        return correct, best_block, best_decoded



if __name__ == "__main__":
    lst = []
    best_block = None
    best_decoded = None
    for _ in range(1, 30):
        huffman = Huffman(_)
        name = "tree.jpg"
        encoded_bytes, coding_dict, decoded_text = huffman.encode_file(name, "latin-1")
        res, best_block, best_decoded = huffman.decode_file("encoded_"+name.split(".", 1)[0], "latin-1", (encoded_bytes, coding_dict, decoded_text), best_block, best_decoded)
        if not res:
            lst += [_]
    print(best_block)
    print(lst)
