def read_file(path: str, encoding: str) -> str:
    with open(path, "rb") as file:
        text = file.read().decode(encoding)
    return text

def dict_to_str(dictionary: dict) -> str:
    return ",".join(rf"{el}:{code}" for el, code in dictionary.items())

def huffman_to_bytes(encoded_text: str) -> bytes:
    return bytes(int(encoded_text[i:i+8],2) for i in range(0, len(encoded_text),8))

def lst_to_bytes(lst: list) -> bytes:
    all_bytes = b''
    byte = 3

    # while True:
    #     for number in lst:
    #         try:
    #             all_bytes += number.to_bytes(byte, 'big')
    #         except OverflowError:
    #             all_bytes = b''
    #             byte+=1
    #             break
    #     else:
    #         break

    for number in lst:
        all_bytes += number.to_bytes(byte, 'big')

    return all_bytes, byte

def bytes_to_lst(byte: bytes, byte_size: int) -> list:
    lst = []
    for i in range(0, len(byte), byte_size):
        lst.append(int.from_bytes(byte[i:i+byte_size], 'big'))

    return lst

# def str_to_bin(string: str) -> str:
#     return ''.join(format(ord(char), '08b') for char in string)