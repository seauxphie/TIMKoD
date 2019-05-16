import string
import math

def count_subarray(subarr, arr): 
    count=0
    j=0
    for i in range(len(arr)):
        if arr[i]==subarr[j]:
            j+=1
            if j==len(subarr):
                count+=1
                j=0
        elif arr[i]==subarr[0]:
            j=1
        else:
            j=0
    return count

def frequency(text):
    dic={}
    probability=[]
    alphabet=[]
    signs='0123456789 '+string.ascii_lowercase
    l=len(text)
    for i in signs: 
        dic[i]= text.count(i)/l
        probability.append(dic[i])
        alphabet.append(i)
    return probability, alphabet

def probability_word(text):
    dic={}
    probability=[]
    words=[]
    text=text.split(' ')
    length=len(text)
    for word in text:
        if word != '' and dic.get(word) == None :
            dic[word]= text.count(word)/length
            probability.append(dic[word])
            words.append(word)
    return probability, words


#entropia
print((-1)*math.log((1/37), 2))

def get_ngram_probabilities_words(text, n): 
    words=text.split(' ')
    dic={}
    dic2={}
    counts=[]
    ngrams=[]
    count_all=0
    for i in range(0, len(words)-n+1):
        ngram_arr=words[i:i+n]
        #print(ngram_arr)
        ngram=tuple(ngram_arr)
        if dic.get(ngram) == None:
            c = count_subarray(ngram_arr, words)
            dic[ngram]=c
            count_all+=c
            #print(dic[ngram])
    for key, value in dic.items():
        dic2[key]=value/count_all
    return dic2


def get_ngram_probabilities_chars(text, n): #znajduje wszystkie bigramy
    dic={}
    dic2={}
    count_all=0
    for i in range(n, len(text)):
        ngram=text[i-n:i]
        if dic.get(ngram) == None:
            dic[ngram]=text.count(ngram)
            count_all+=dic[ngram]
    for key, value in dic.items():
        dic2[key]=value/count_all
    return dic2


def get_probabilities_chars(ngrams, begins_with):  
    letters=[]                              
    probabilities=[]
    count_all=0
    for key, value in ngrams.items():
        if key[:-1] == begins_with and value > 0:
            letters.append(key[-1])
            probabilities.append(value)
            count_all+=value
    for i in range(len(probabilities)):
        probabilities[i]=probabilities[i]/count_all
    return letters, probabilities






def get_probabilities_words(ngrams, begins_with):  
    words=[]                              
    probabilities=[]
    count_all=0
    begins_with=tuple(begins_with)
    for key, value in ngrams.items():
        if key[:-1] == begins_with and value > 0:
            words.append(key[-1])
            probabilities.append(value)
            count_all+=value
    for i in range(len(probabilities)):
        probabilities[i]=probabilities[i]/count_all
    return words, probabilities



def entropy_chars(text):
    probability, alphabet = frequency(text)
    H=0
    for p in probability:
        if p>0:
            H-=p*(math.log(p, 2))
    return H

def entropy_words(text):
    probability, words = probability_word(text)
    H=0
    for p in probability:
        H-=(p*math.log(p, 2))
    return H

def cond_entropy_chars(text, n):
    ngrams_n1 = get_ngram_probabilities_chars(text, n+1)
    ngrams_n = get_ngram_probabilities_chars(text, n)

    H=0

    for ngram, prob in ngrams_n.items():
        letters, probabilities = get_probabilities_chars(ngrams_n1, ngram)
        for letter, probability in zip(letters, probabilities):
            new_ngram = ngram+letter
            p1 = ngrams_n1.get(new_ngram)
            H-=p1*math.log(probability, 2)
    return H

def cond_entropy_words(text, n):
    ngrams_n1 = get_ngram_probabilities_words(text, n+1)
    ngrams_n = get_ngram_probabilities_words(text, n)

    H=0

    for ngram, prob in ngrams_n.items():
        words, probabilities = get_probabilities(ngrams_n1, ngram)
        for word, probability in zip(words, probabilities):
            new_ngram = tuple(list(ngram).append(word))
            p1 = ngrams_n1.get(new_ngram)
            H-=p1*math.log(probability, 2)
    return H





input=open("data/norm_wiki_en.txt", 'r')
output=open("result.txt", 'w')
text1=input.read()[:10000]


result = entropy_chars(text1)
print(result)
output.write("norm_wiki_en.txt\nEntropia znaków:")
output.write(str(result))

result = entropy_words(text1)
print(result)
output.write("norm_wiki_en.txt\nEntropia słów:")
output.write(str(result))

result = cond_entropy_chars(text1, 1)
print(result)
output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 1 rzędu:")
output.write(str(result))
"""
result = cond_entropy_chars(text1, 2)
print(result)
output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 2 rzędu:")
output.write(str(result))

result = cond_entropy_chars(text1, 3)
print(result)
output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 3 rzędu:")
output.write(str(result))

result = cond_entropy_chars(text1,4)
print(result)
output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 4 rzędu:")
output.write(str(result))


result = cond_entropy_chars(text1,5)
print(result)
output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 5 rzędu:")
output.write(str(result))
"""
result = cond_entropy_words(text1,1)
print(result)
output.write("norm_wiki_en.txt\nEntropia arunkowa znaków 5 rzędu:")
output.write(str(result))


output.close()



