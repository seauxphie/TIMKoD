import random

def count_subarray(subarr, arr): #znajduje ile razy subarr znajduje się w arr (zachowana kolejność wyrazow)
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


def get_ngram_counts(text, n): #znajduje wszystkie ngramy i zapisuje ile ich jest w tekście
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

def get_probabilities(ngrams, begins_with): #zllicza ngramy zaczynające się na chars_before 
    words=[]                              #i liiczy prawdopodobieństwo wystąpienia kolejnej litery po tyvh znakach
    probabilities=[]
    count_all=0
    begins_with=tuple(begins_with)
    for key, value in ngrams.items():

        if key[:-1] == begins_with:
            words.append(key[-1])
            probabilities.append(value)
            count_all+=value
    for i in range(len(probabilities)):
        probabilities[i]=probabilities[i]/count_all
    #print(sum(probabilities))
    return words, probabilities

def generate_using_ngrams(basic_text, n, length):
    ngrams = get_ngram_counts(basic_text, n)
    text=list(random.choice(list(ngrams))[0:n-1])
    for i in range(n-1, length):   

        words, probs = get_probabilities(ngrams, text[i-n+1:i])
        word = random.choices(words, probs)[0]

        text.append(word)

        """if len(letters) == 0:
            text+=generate_using_bigrams(basic_text,2,text[i-1])[1]
        else:
            text+=random.choices(letters, probs)[0]
        """
    result=(' ').join(text)
    return result
file=open("norm_romeo_and_juliet.txt",'r')
text=file.read()[:6000]

print("Tekst wygenerowany na podstawie 1 poprzedniego wyrazu:")
print(generate_using_ngrams(text, 2, 100))
print("\nTekst wygenerowany na podstawie 2 poprzednich wyrazów:")
print(generate_using_ngrams(text, 3, 100))