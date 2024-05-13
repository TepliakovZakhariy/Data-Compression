# Data-Compression

A program for compressing files using such algorithms as **LZW**, **Huffman code**, **LZ77** and **LZ78**, **Deflate**.

## Installation

Requirements: Python 3.11

```
git clone https://github.com/TepliakovZakhariy/Data-Compression
cd Data-Compression
pip install -r requirements.txt
python src/main.py
```

## Description of algorithms

### LZW

**Lempel-Ziv-Welch (LZW)** algorithm is a general-purpose lossless data compression algorithm created by Abraham Lempel, Jacob Ziv and Terry Welch. It was published by Welch as an improved implementation of the LZ78 algorithm published by Lempel and Ziv.

A notable feature of the LZW algorithm is its simplicity of implementation. The main advantage of the algorithm is that its initial dictionary for encoding and decoding is always the same, so we don't need to put it in the compressed file itself, which significantly reduces the file weight.

#### Implementation

- **encode()**

  The **encode** method takes a byte string as input, and then checks whether it is empty - otherwise, it returns an empty string and a single byte. If the string is not empty, then an initial algorithm is created that contains all single-byte characters and their sequence number from 0 to 255. This is the main advantage of the algorithm - we don't need to pass the dictionary to the decoding function because the same dictionary is created there at the beginning.

  After that, an empty byte list encoded_text and an empty byte string temp are created. Then, according to the LZW algorithm, the algorithm searches through each character of the text and adds it to temp. If temp is not in the dictionary, then the code corresponding to temp without the last character is added to the encoded text, the key equal to temp in its binary representation is added to the dictionary, and temp is changed only to the last character of the byte string temp. How does it work? It would be illogical to encode each number as a sequence of digits in the form of a string, so instead we will encode numbers as numbers. At the beginning, the algorithm tries to encode each number with 3 bits, which allows us to encode numbers from 0 to 2^(8\*3)-1 = 2^24-1. If the input file is too large and the numbers we want to encode are larger than this upper limit, the algorithm will use more bytes than 3: 4, 5, 6... After the algorithm has gone through all the characters of the text, temp is added to encoded_text, and the algorithm returns the encoded text and the number of bytes each number is encoded with.

- **decode()**

  The **decode** function takes encoded byte text and the number of bytes that encode each number. At the beginning, the function checks whether the input text is an empty string, otherwise the function returns an empty string as well. After that, it creates an identical dictionary to the one in the encoding function, which contains all the one-byte characters numbered from 0 to 255. The method starts by iterating through the encoded byte sequence. It reads the encoded bytes in the chunks specified by the bytes_per_code parameter, interpreting them as integer values. These integers represent the codes generated during the encoding process.

  For each code, the algorithm checks whether it is in the dictionary. If not, the algorithm adds the value of the previous entry with its first byte to the dictionary. When processing each code, the corresponding sequence from the dictionary is added to decoded_text. The function returns a sequence of bytes that can be written to the output file, resulting in a decoded file.

- **encode_files()**

  The **encode_files** function takes a file path and a name to name the encoded file.

  First, the function reads the bytes of the input file and encodes them using the encode() function. After that, the function places the extension of the original file, the number of bytes that encode each number, and the encoded text of the file into the encoded file. These values are separated by the "|" character.

- **decode_files()**

  The **decode_files** function takes the path to the encoded file and the name to be given to the decoded file

  At the beginning, the function reads the bytes of the input file and divides them into three elements with the "|" character - the file extension, the number of bytes that encode each number, and the encoded text of the file.

  After that, the text is decoded with the decode() function, and the resulting bytes are written to the output file.

- **get_extension()**

  This function accepts an encoded file and returns its original extension, which is required for the program itself.
