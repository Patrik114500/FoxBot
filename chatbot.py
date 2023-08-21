import random
import json
import pickle
import numpy as np
import simplemma
import mysql.connector as sql
import string
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow import keras
from keras.models import load_model

mydb = sql.connect(
   host="localhost",
   port=3306,
   user="root",
   password="",
   database="foxbot"
)

lemmatizer = WordNetLemmatizer()

try:
    with open("int.json", encoding='UTF8') as file:
        intents = json.load(file)
except FileNotFoundError:
    print("Hiba: Az intent fájl nem található.")
except json.JSONDecodeError:
    print("Hiba: Az intent JSON fájl érvénytelen formátumú.")

try:
    with open('words.okl', 'rb') as file:
        words = pickle.load(file)
except FileNotFoundError:
    print("Hiba: A words fájl nem található.")

try:
    with open('classes.okl', 'rb') as file:
        classes = pickle.load(file)
except FileNotFoundError:
    print("Hiba: A classes fájl nem található.")

try:
    model = load_model('chatbotmodel.h5')
except FileNotFoundError:
    print("Hiba: A chatbotmodel.h5 fájl nem található.")

CDIq=["szomorú","értéktelen","hatékonyság","boldog","rossz_viselkedés","paranoia","öngyűlölet","önhibáztatás","öngyilkosság","sírás","harag","társaság","döntés","külső","házifeladat","alvás","fáradtság","étvágy","ijedt","magány","iskola","barátok","rossz_tanuló","hasonlítás","szeretve_lenni","szófogadás","veszekedés"]
previoustags = []
quiz = ""

def clean_up_sentence(sentence):
    sentence_word = nltk.word_tokenize(sentence.lower())
    sentence_word = [simplemma.lemmatize(word, lang='hu') for word in sentence_word if word not in ['.', '!', '?', ':']]
    return sentence_word

def bag_of_words(sentence):
    sentence_word = clean_up_sentence(sentence.lower())
    bag = [0] * len(words)
    for w in sentence_word:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_TREDHOLD = 0.15
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_TREDHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

def get_response(intents_list, intents_json, username):
    global quiz
    global previoustags
    result = "Nem értem, mit szeretne."
    nextq = ""
    index = 0
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM cdi WHERE id = (SELECT CDIid FROM user WHERE username = '"+username+"')")
    answears = mycursor.fetchall()
    firstintent = ""
    
    for intent in intents_list:
        if intent['intent'] not in ['answer3', 'answer2', 'answer1'] and firstintent == "":
            firstintent = intent['intent']

    if intents_list[0]['intent'] == "CDI":
        quiz = "CDIq"

    for i in range(1, len(answears[0])):
        if answears[0][i] is not None and CDIq[i-1] not in previoustags:
            previoustags.append(CDIq[i-1])
            previoustags.append(1)

    if quiz == "CDIq":
        for i in CDIq:
            if i not in previoustags and 0 not in previoustags:
                quiz = "CDIq"
                tag = i
                break
            elif 0 in previoustags:
                tag = firstintent
                break
            else:
                tag = firstintent
    else: 
        tag = firstintent

    list_of_intents = intents_json['intents']

    for i in list_of_intents:
        if i['tag'] == tag:
            if i['tag'] in CDIq and tag not in previoustags:
                result = i['question'][0]
                previoustags.append(i['tag'])
                previoustags.append(0)
            else:
                result = random.choice(i['responses'])

        while nextq == "" and index <= len(CDIq):
            if CDIq[index] in previoustags:
                index += 1
            else:
                nextq = CDIq[index]
            if index == len(CDIq) and nextq == "":
                nextq = "kvíz_vége"

        for j in range(len(previoustags)):
            if previoustags[j] == 0 and previoustags[j-1] == i['tag']:
                for k in i['answers']:
                    if k['tag'] == intents_list[0]['intent']:
                        previoustags[j] = 1
                        mycursor = mydb.cursor()
                        sql = "UPDATE cdi SET answear"+k['code'].split('.')[1]+"='"+k['code'].split('.')[2]+"' WHERE id = (SELECT CDIid FROM user WHERE username = '"+username+"')"
                        mycursor.execute(sql)
                        mydb.commit()
                        result = k['responses'][0]
                        break

        if i['tag'] == nextq and quiz != "":
            if nextq != "kvíz_vége":
                result = i['question'][0]
                previoustags.append(nextq)
                previoustags.append(0)
            else:
                result = i['question'][0]

    if nextq == "kvíz_vége":
        quiz = ""
    if 0 not in previoustags:
        previoustags = []
    print(intents_list, firstintent)

    return result
