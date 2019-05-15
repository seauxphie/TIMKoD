import random

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


def get_ngram_counts(text, n): 
    words=text.split(' ')
    
    dic={}
    counts=[]
    ngrams=[]
    for i in range(0, len(words)-n+1):
        ngram_arr=words[i:i+n]
        #print(ngram_arr)
        ngram=tuple(ngram_arr)
        if dic.get(ngram) == None:
            dic[ngram]=count_subarray(ngram_arr, words)
            #print(dic[ngram])
    for key, value in dic.items():
        counts.append(value)
        ngrams.append(key)
    return dic

def get_ngram_counts_with_first(text, n, first_word): 
    words=text.split(' ')
    dic={}
    counts=[]
    ngrams=[]
    for i in range(0, len(words)-n+1):
        ngram_arr=words[i:i+n]
        ngram=tuple(ngram_arr)
        if dic.get(ngram) == None and ngram_arr[0]==first_word:
            dic[ngram]=count_subarray(ngram_arr, words)
    for key, value in dic.items():
        counts.append(value)
        ngrams.append(key)
    return dic

def get_probabilities(ngrams, begins_with):  
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

def generate_using_ngrams(basic_text, n, length):
    ngrams = get_ngram_counts(basic_text, n)
    text=list(random.choice(list(ngrams))[0:n-1])
    for i in range(n-1, length):   

        words, probs = get_probabilities(ngrams, text[i-n+1:i])
        if len(words) == 0:
            break
        word = random.choices(words, probs)[0]
        text.append(word)

    result=(' ').join(text)
    return result


def generate_with_1st_word(basic_text, length, begins_with):
    text=[begins_with]
    ngrams = get_ngram_counts(basic_text, 2)
    words, probs = get_probabilities(ngrams, [begins_with])
    text.append(random.choices(words, probs)[0])
    ngrams = get_ngram_counts(basic_text, 3)
    print(text)
    for i in range(2, length): 
        words, probs = get_probabilities(ngrams, text[i-2:i])
        if len(words) == 0:
            break
        word = random.choices(words, probs)[0]
        text.append(word)

    result=(' ').join(text)
    return result

file=open("wiki.txt",'r')
text=file.read()

print("Tekst wygenerowany na podstawie 1 poprzedniego wyrazu:")
print(generate_using_ngrams(text, 2, 100))
print("\nTekst wygenerowany na podstawie 2 poprzednich wyrazów:")
print(generate_using_ngrams(text, 3, 100))
print("\nTekst wygenerowany na podstawie 2 poprzednich wyrazów z pierwszym 'probability':")
print(generate_with_1st_word(text, 100, 'probability'))