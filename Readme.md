### Huffman

**Huffman** algorithm is a general-purpose lossless data compression algorithm created by David A. Huffman in 1952. While studying at MIT he had a choice. Write final exam or term paper on the problem of finding the most efficient binary code. Only when the time for writing exam got closer he came up with this solution.

Inspite of being made by the student this algorithm is Shannon–Fano coding which was the best at that time. The main idea of Huffman algorith is to make a binary tree sorted by frequency and start building codes from the bottom of the tree which provides the shortest code for the most frequent characters and longer code for the least frequent characters. This is obiously effective because most of the time we are using less space for storing data.

While implementing this algorithm we decided to try block coding. It isn't regular block coding because we do not go through all possible blocks in an input.

#### Implementation

- **encode()**

  The **encode** method takes a string as input.
  We are using sliding window with size of block size. For example, if the block size is 1 we just iterate over every charecter. if the block size is 2 and the input is abcde, we iterate over ab, cd and e. while iterating over blocks we count their frequency by creating dictionary beforehand and adding one to their key in that dictionary when we encounter them in input.
  
  In second step we take frequency dictionary and convert it to sorted list by frequency, which afterwards is converted to double linked list, because inserting in a list is too slow.

  Here we calculate codes for every block. For that we take two least frequent add their frequency and add 1 to the beginning of code of the first one and 0 to the beginning of the second one. we merge them into one but the codes remain separate. Then we find the place where block with such frequency could be placed to keep our linked list sorted. For optimisation we rememeber the place where we last time inserted the merged block which helps us to reduce time for insertion.

  We finally have codes, so we just iterate over blocks of input and
  replace them with created codes. while iterating we convert encoded text to bytes

- **decode()**

  The **decode** function takes encoded bytes and dictionary for encoding and decoding.
  Firstly, we convert bytes to string of bits. After that we just take that string of bits and convert it using the dictionary.

- **encode_files()**

  The **encode_files** function takes a file path and a name to name the encoded file.

  Firstly, the function reads the bytes of the input file and encodes them using the encode() function.

  After that, the function places number of keys, block size, the smallest block size and file extension at the beginning of the encoded file. They are separated by "/" and end with "|". After that we write to the file coding dictionary sorted by length of block in descending order and converted to string, ";" for separation and encoded bytes.

- **decode_files()**

  The **decode_files** function takes the path to the encoded file and the name to be given to the decoded file

  The function reads the file from path and takes first chunk of information that ends with "|". this chunk includes such values: amount of keys, block size, the smallest block size and extension.

  After that function reads the dictionary which is possible because we have all needed information from first chunk of information. We use amount of blocks to know where to look for the smalles block. and smalles block size to know how many symbols is in that block.

  then we decode the file by giving the rest of the file and coding dict to **decode()** function and write decoded_text to new path.


- **get_extension()**

  This function accepts an encoded file and returns its original extension, which is required for the program itself.
  