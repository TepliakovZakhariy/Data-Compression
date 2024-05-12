class LZW:
    def encode(self, text: str) -> tuple[str, list]:
        if not text:
            return '', []

        dictionary={}
        i=0

        for char in text:
            if len(dictionary)==len(set(text)):
                break
            if char not in dictionary:
                dictionary[char]=i
                i+=1
        
        result_dictionary = list(dictionary.keys())
 
        encoded_text = ''
        temp = ""

        for char in text:
            temp += char
            if temp not in dictionary:
                encoded_text+=(str(dictionary[temp[:-1]]))+' '
                dictionary[temp] = len(dictionary)
                temp = char

        encoded_text+=str(dictionary[temp])

        return encoded_text, result_dictionary

    def decode(self, code: str, coding_dict: list) -> str:
        coding_dict = {i : char for i, char in enumerate(coding_dict)}
        coding_dict_start = coding_dict.copy()

        decoded_text = ""
        temp=''
        code = list(map(int,code.split()))

        for num in code:
            if num in coding_dict:
                decoded_text += coding_dict[num]
                temp+=coding_dict[num]
                if num in coding_dict_start:
                    if temp not in coding_dict.values():
                        coding_dict[len(coding_dict)] = temp
                        temp = temp[-1]
                else:
                    temp_2=''
                    for char in temp:
                        temp_2+=char
                        if temp_2 not in coding_dict.values():
                            coding_dict[len(coding_dict)] = temp_2
                            temp_2 = temp_2[:-1]
                            break
                    temp = temp[len(temp_2):]
            else:
                temp=temp+temp[0]
                coding_dict[len(coding_dict)] = temp
                decoded_text += coding_dict[num]
        return decoded_text
    
    