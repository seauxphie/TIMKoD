import string
from bitarray import bitarray
import math
#from bitstring import BitArray

letters_to_bits={}
bits_to_letters={}

class Tree(object):
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None 

def encode(text, code):
    encode_text=bitarray()
    for c in text:
        encode_text+=code[c]
    return encode_text

def decode(text):
    decoded_text=""
    start=0
    i=1
    while i<len(text)+1:
        temp=text[start:i]
        tempb = temp.tobytes()

        if tempb in bits_to_letters.keys() and letters_to_bits[bits_to_letters.get(tempb)]==temp:
            stop=len(letters_to_bits[bits_to_letters[tempb]])
            i=start+stop
            start=i
            decoded_text += bits_to_letters[tempb]
        i+=1
        
    return decoded_text

def save(text, code):
    compressed_file = open("encoded", 'wb')
    encoded_text=encode(text, code)
    encoded_text.tofile(compressed_file)
    
    key=open("key.txt",'w')
    key.write("key \n")
    for k, v in letters_to_bits.items():
        key.write("%s %s \n" % (k, v))
        
    key.close()
    compressed_file.close()
    return encoded_text

def load():
    text=bitarray()
    compressed_file=open("encoded",'rb')
    text.fromfile(compressed_file)
    key=open("key.txt",'r')
    keys=key.readlines()
    for k in range (1,len(keys)):
        letters_to_bits[keys[k][0]]=bitarray(keys[k][12:len(keys[k])-4])
        temp = bitarray(keys[k][12:len(keys[k])-4]).tobytes()
        bits_to_letters[temp]=keys[k][0]
    
    decoded_text = decode(text)
    key.close()
    compressed_file.close()
    return decoded_text

def frequency(text):
    chars='0123456789 '+string.ascii_lowercase
    length=len(text)
    result = [(text.count(c)/length, c) for c in chars]
    result.sort(reverse=True)
    j=0
    while(j<len(result) and result[j][0]>0):
        j+=1
    result=result[:j]
    return result
    
def sort_trees(trees_list):
    for i in range(len(trees_list)-1):
        maxi=trees_list[i].data[0]
        indeks=i
        for j in range(i+1,len(trees_list)):
            if trees_list[j].data[0]>maxi:
                maxi=trees_list[j].data[0]
                indeks=j
        pom=trees_list[indeks]
        trees_list[indeks]=trees_list[i]
        trees_list[i]=pom
    return trees_list

def Huffman(freq):
    trees_list=[]
    for f in freq:
        root=Tree()
        root.data=f
        trees_list.append(root)

    while(len(trees_list)>1):
        #for t in trees_list:
            #print(t.data)
        new_tree=Tree()
        pom=[]
        s=trees_list[len(trees_list)-1].data[0]+trees_list[len(trees_list)-2].data[0]
        pom.append(s)
        tupla=tuple(pom)
        new_tree.data=tupla
        new_tree.right=trees_list[len(trees_list)-1]
        new_tree.left=trees_list[len(trees_list)-2]
        #print(new_tree.left.data,new_tree.right.data, new_tree.data[0])
        trees_list=trees_list[:len(trees_list)-2]
        trees_list.append(new_tree)
        sort_trees(trees_list) 
        #print('\n')
    return trees_list
      
def erase_node(tree3,node,s):
    if len(s)>2:
        if s[1]=='0':
            node=erase_node(node,node.left,s[1:])
        else:
            node=erase_node(node,node.right,s[1:])
    else:
        if len(s)>1:
            if s[1]=='0':
                node.left=None
            else:
                node.right=None
        else:
            node=None
    if s[0]=='0':
        tree3.left=node
    else:
        tree3.right=node
    return tree3
    
    
def dfs(tree):
    node=tree
    s=''
    while type(node.left) == Tree or type(node.right) == Tree:
        while type(node.left) == Tree:
            node=node.left
            s+='0'
        while type(node.right) == Tree:
            node=node.right
            s+='1'

    if len(node.data)==2:
        print(node.data, s)
        letters_to_bits[node.data[1]]=bitarray(s)
        temp = bitarray(s).tobytes()
        bits_to_letters[temp]=node.data[1]
        
    if s[0]=='0':
        node=tree.left
    else:
        node=tree.right
    tree2=tree
    tree=erase_node(tree2,node,s)
        
    return tree
    

def create_Huffman(freq):
    tree=Huffman(freq)[0]
    while type(tree.left)==Tree or type(tree.right)==Tree:
        tree=dfs(tree)
    #for k,v in letters_to_bits.items():
            #print (k,v)

def efficiency(freq):
    H=0
    L=0
    print('')
    for f in freq:
        H-=f[0]*math.log(f[0],2)
        L+=len(letters_to_bits[f[1]])*f[0]
    print("H=",H," L=",L)

    eff=H/L
    print("efektywnosć:",eff)
    


file=open("norm_wiki_sample.txt",'r')
text=file.read()
freq=frequency(text)
create_Huffman(freq)
efficiency(freq)
encoded=save(text,letters_to_bits)
#print('')
#print(encoded)
decoded=load()
#print(decoded)

file.close()