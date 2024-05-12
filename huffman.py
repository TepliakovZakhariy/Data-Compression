
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
        encoded_text = ''.join(huffman_code[text[i: i + self.block_size]] for i in range(0, len(text), self.block_size))
        return encoded_text, huffman_code

    def decode(self, code: str, coding_dict: dict[str, str], byte = False) -> str:
        decoded_text = ""
        temp = ""
        if byte:
            zeros = 8 - len(bin(code[0])) + 2 if code else 0
            myhex = code.hex()
            myint = int(myhex, 16)
            binary_string = "0"*zeros + "{:08b}".format(myint)
            k = 0
            end_k = 0
            for char in binary_string:
                end_k += 1
                temp = binary_string[k: end_k]
                if temp in coding_dict:
                    decoded_text += coding_dict[temp]
                    k = end_k
                
            return decoded_text
        reverse=dict((v,k) for k,v in coding_dict.items())
        for char in code:
            temp += char
            if temp in reverse:
                decoded_text += reverse[temp]
                temp = ""
        return decoded_text

    def encode_file(self, path: str, encoding: str):
        with open(path, 'rb') as file:
            text = file.read()
            text_str = text.decode(encoding)

        encoded_text, coding_dict = self.encode(text_str)

        with open('encoded_'+path.split(".", 1)[0], 'wb') as file:
            encoded_dict = ",".join(rf"{el}:{code}" for el, code in coding_dict.items())
            bits_to_bytes = bytes(int(encoded_text[i:i+8],2) for i in range(0, len(encoded_text),8))
            file.write((path.replace(";", "")+";"+encoded_dict+";").encode(encoding)+bits_to_bytes)
        print("encoded")

    def decode_file(self, path: str, encoding: str):
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
            if not creating_dict:
                if sym == ";":
                    creating_dict = True
                    continue
                last_path += sym
            elif sym == "," and code_time:
                code_time = False
                coding_dict[code] = chars
                code = ""
                chars = ""
            elif code_time:
                if sym == ";":
                    coding_dict[code] = chars
                    no_dict_i = i
                    break
                code += sym
            elif sym == ":" and coding_text_dict[i + 1] in "01":
                code_time = True
            else:
                chars += sym
        print("created_dict")
        code_i = len(coding_text_dict[:no_dict_i].encode(encoding)) + 1
        code = text[code_i:]

        decoded_text = self.decode(code, coding_dict, True)

        with open("decoded_" + last_path, "wb") as img:
            img.write(decoded_text.encode(encoding))
        print("decoded")


if __name__ == "__main__":
    huffman = Huffman(1)
    name = "What_ Meme (1).mp4"
    huffman.encode_file(name, "latin-1")
    huffman.decode_file("encoded_"+name.split(".", 1)[0], "latin-1")
