import random
    

def get_ngram_probabilities(text, n): #znajduje wszystkie bigramy
    dic={}
    probabilities=[]
    ngrams=[]
    #dic2={}
    count_all=0
    for i in range(0, len(text)-n+1):
        ngram=text[i:i+n]
        if dic.get(ngram) == None:
            dic[ngram]=text.count(bigram)
            count_all+=dic[ngram]
    for key, value in dic.items():
        probabilities.append(value/count_all)
        ngrams.append(key)
    return ngrams, probabilities

def get_ngram_counts(text, n): #znajduje wszystkie ngramy i zapisuje ile ich jest w tekście
    dic={}
    counts=[]
    ngrams=[]
    for i in range(0, len(text)-n+1):
        ngram=text[i:i+n]
        if dic.get(ngram) == None:
            dic[ngram]=text.count(ngram)
    for key, value in dic.items():
        counts.append(value)
        ngrams.append(key)
    return dic

def get_probabilities(ngrams, chars_before): #zllicza ngramy zaczynające się na chars_before 
    letters=[]                              #i liiczy prawdopodobieństwo wystąpienia kolejnej litery po tyvh znakach
    probabilities=[]
    count_all=0
    #print(chars_before)

    for key, value in ngrams.items():
        #print(key)
        #print(key[:-1])
        #print(key[-1])
        if key[:-1] == chars_before:
            letters.append(key[-1])
            probabilities.append(value)
            count_all+=value
    for i in range(len(probabilities)):
        probabilities[i]=probabilities[i]/count_all
    #print(sum(probabilities))
    return letters, probabilities
    
#podpunkt 1  
def generate_using_bigrams(text, length,start_letter):
    ngrams = get_ngram_counts(text, 2)
    #text=chr(random.randint(97, 122))
    text=start_letter
    for i in range(1, length):
        letters, probs = get_probabilities(ngrams, text[i-1])
        text+=random.choices(letters, probs)[0]
    return text

#podpunkt 2
def generate_using_4grams(basic_text, length):
    ngrams = get_ngram_counts(basic_text, 4)
    text=random.choice(list(ngrams)[0:3])
    
    for i in range(3, length):   
        #print(text[i-3:i])
        letters, probs = get_probabilities(ngrams, text[i-3:i])
        
        if len(letters) == 0:
            text+=generate_using_bigrams(basic_text,2,text[i-1])[1]
        else:
            text+=random.choices(letters, probs)[0]
            
    return text

#podpunkt 3
def generate_using_6grams(basic_text, length):
    ngrams = get_ngram_counts(basic_text, 6)
    text='probability'
    for i in range(11, length):   
        letters, probs = get_probabilities(ngrams, text[i-5:i])
        if len(letters) == 0:
            text+=chr(random.randint(97, 122))
        else:
            text+=random.choices(letters, probs)[0] 
            
    return text

def get_avg_word_length(text):
	spaces=text.count(' ')
	return len(text)/(spaces+1)

file=open("norm_hamlet.txt",'r')
text=file.read()
print('Na podstawie 1 poprzedniego znaku:')
print(generate_using_bigrams(text, 300, chr(random.randint(97, 122))))
print('\n\nNa podstawie 3 poprzednich znaków:')
print(generate_using_4grams(text, 300))
print('\n\nNa podstawie 5 poprzednich znaków:')
txt = generate_using_6grams(text, 300)
avg = get_avg_word_length(txt)
print(txt)
print("\nŚrednia dł. słowa: "+str(avg))