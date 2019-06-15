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
    
    key=open("key.txt",'w')
    key.write("key \n")
    for k, v in letters_to_bits.items():
        key.write("%s %s \n" % (k, v))
        
    compressed_file.close()
    key.close()
    return encoded_text

def load(code):
    text=bitarray()
    compressed_file=open("encoded",'rb')
    text.fromfile(compressed_file)
    key=open("key.txt",'r')
    keys=key.readlines()
    for k in range (1,len(keys)):
        letters_to_bits[keys[k][0]]=bitarray(keys[k][12:18])
        temp = bitarray(keys[k][12:18]).tobytes()
        bits_to_letters[temp]=keys[k][0]
    
    decoded_text = decode(text, code)
    
    compressed_file.close()
    key.close()
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
decoded = load(bits_to_letters)
#print(decoded)

file.close()
