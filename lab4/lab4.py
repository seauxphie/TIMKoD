import string
from bitarray import bitarray
#from bitstring import BitArray

#letters_to_bits={}
#bits_to_letters={}


#create code
def create(frequency):
    i=0
    letters_to_bits={}
    bits_to_letters={}
    for _, c in frequency:
        s=bin(i)[2:]
        while len(s)<6:
            s='0'+s
        letters_to_bits[c]=bitarray(s)
        temp = bitarray(s).tobytes()
        bits_to_letters[temp]=c
        i+=1
    return letters_to_bits, bits_to_letters

def encode(text, code):
    encode_text=bitarray()
    for c in text:
        encode_text+=code[c]
    return encode_text

def decode(text, code):
    decoded_text=""
    for i in range(0,len(text),6):
        temp = text[i:i+6].tobytes()
        decoded_text += code[temp]
    return decoded_text

def save(text, code):
    compressed_file = open("encoded", 'wb')
    encoded_text=encode(text, code)
    encoded_text.tofile(compressed_file)
    return encoded_text

def load(text, code):
    decoded_text = decode(text, code)
    return decoded_text

def frequency(text):
    chars='0123456789 '+string.ascii_lowercase
    length=len(text)
    result = [(text.count(c)/length, c) for c in chars]
    result.sort(reverse=True)
    return result





file=open("norm_wiki_sample.txt",'r')
text=file.read()
letters_to_bits, bits_to_letters = create(frequency(text))
encoded = save(text, letters_to_bits)
decoded = load(encoded, bits_to_letters)
#print(decoded)
if decoded == text:
    print("The original and decoded documents are the same")
else:
    print("The documents are different")
