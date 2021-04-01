from django.shortcuts import render
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer  # to encode text to int
from tensorflow.keras.preprocessing.sequence import pad_sequences   # to do padding or truncating
from tensorflow.keras.models import load_model   # load saved model
from django.http import HttpResponse
import re
from .models import Movie

# Create your views here.
def form(request):
    return render(request,'form.html')

#Helper function for classifying
def classify_review(review_stmt):#returns 1 for positive,0 for negative
    english_stops = set(stopwords.words('english'))
    max_length=130#From train data
    #Loading stored model
    loaded_model = load_model('/home/dsdroid/Desktop/6th Sem/SWLAB/Assignment 4/Sentiment-Analysis/review_classifier/review/sentiment.h5')
    # Pre-process input
    regex = re.compile(r'[^a-zA-Z\s]')
    review_stmt = regex.sub('', review_stmt)
    #print('Cleaned: ', review_stmt)

    words = review_stmt.split(' ')
    filtered = [w for w in words if w not in english_stops]
    filtered = ' '.join(filtered)
    filtered = [filtered.lower()]

    #print('Filtered: ', filtered)
    token = Tokenizer(lower=False)
    tokenize_words = token.texts_to_sequences(filtered)
    tokenize_words = pad_sequences(tokenize_words, maxlen=max_length, padding='post', truncating='post')

    result = loaded_model.predict(tokenize_words)
    #print(result)
    if result >= 0.5:
        #print('positive')
        return True#1
    else:
        #print('negative')
        return False#0

def review_process(request):
    if request.method=='POST':
        review_stmt=request.POST.get('review')
        english_stops = set(stopwords.words('english'))
        max_length=130#From train data
        #Loading stored model
        loaded_model = load_model('/home/dsdroid/Desktop/6th Sem/SWLAB/Assignment 4/Sentiment-Analysis/review_classifier/review/sentiment.h5')
        # Pre-process input
        regex = re.compile(r'[^a-zA-Z\s]')
        review_stmt = regex.sub('', review_stmt)
        print('Cleaned: ', review_stmt)

        words = review_stmt.split(' ')
        filtered = [w for w in words if w not in english_stops]
        filtered = ' '.join(filtered)
        filtered = [filtered.lower()]

        print('Filtered: ', filtered)
        token = Tokenizer(lower=False)
        tokenize_words = token.texts_to_sequences(filtered)
        tokenize_words = pad_sequences(tokenize_words, maxlen=max_length, padding='post', truncating='post')

        result = loaded_model.predict(tokenize_words)
        print(result)
        if result >= 0.5:
            print('positive')
            return HttpResponse('Positive review')
        else:
            print('negative')
            return HttpResponse('Negative review')
    else:
        return render(request,'form.html')

def updateReviews(request):
    if request.method=='POST':
        #Get the movie id
        print('Req received')
        m_id = request.POST.get('id')
        print(m_id)
        review_stmt = request.POST.get('review')
        isPositive = classify_review(review_stmt)
        Movie_object = Movie.objects.get(id=m_id)
        if isPositive:
            Movie_object.num_positive+=1
        else:
            Movie_object.num_negative+=1
        Movie_object.save()
        return HttpResponse('Recorded')

    else:
        movie=Movie.objects.get(id=2)
        print(movie.id)
        print(movie.poster)
        return render(request,'movie.html',{'movie':movie})
        #return HttpResponse('Here will be kartik\'s page')

def movieData(request):
    movie=Movie.objects.get(id=2)
    print(movie.id)
    print(movie.poster)
    return render(request,'movie.html',{'movie':movie})