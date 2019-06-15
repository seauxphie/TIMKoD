import cv2
from bitarray import bitarray

def compress_text(text):
    max_dict_size=None
    dict_size = 128
    dictionary = {chr(i): i for i in range(128)}
    result = []
    previous=""
    for char in text:
        fragment = previous+char
        if fragment in dictionary:
            previous = fragment
        else:
            result.append(dictionary[previous])
            dictionary[fragment]=dict_size
            dict_size+=1
            previous = char
    if previous:
        result.append(dictionary[previous])

    return result

def decompress(input):
    max_dict_size=None
    dict_size = 128
    dictionary = {i: chr(i) for i in range(128)}
    result=[]
    temp = chr(text.pop(0))
    result.append(temp)
    for fragment in input:
        decoded = None
        if fragment in dictionary:
            decoded = dictionary[fragment]
        else:
            print(temp)
            decoded = temp+temp[0]
        result.append(decoded)

        dictionary[dict_size] = temp+decoded[0]
        dict_size+=1
        temp = decoded
    return result

def decompress_text(text):
    result = decompress(text)
    return "".join(result)

image = cv2.imread("lena.bmp")
text = open("norm_wiki_sample.txt").read()[:100]
print(text)
code = compress_text(text)
print(code)
print(decompress_text(code))
