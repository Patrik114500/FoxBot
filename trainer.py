import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import simplemma

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

lemmatizer = WordNetLemmatizer()
intents = json.loads(open("int.json", encoding='utf-8').read())

words = []
classes = []
answers = []
documents = []
ignore_letters = ['?', '!', '.', ',']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern.lower())
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])
    if 'answers' in intent:
        for answer in intent['answers']:
            for pattern in answer['patterns']:
                word_list = nltk.word_tokenize(pattern.lower())
                words.extend(word_list)
                documents.append((word_list, answer['tag']))
                if answer['tag'] not in classes:
                    classes.append(answer['tag'])

lemmatized_words = [simplemma.lemmatize(word, lang='hu') for word in words if word not in ignore_letters]
lemmatized_words = sorted(set(lemmatized_words))
classes = sorted(set(classes))
answers = sorted(set(classes))

pickle.dump(lemmatized_words, open('words.okl', 'wb'))
pickle.dump(classes, open('classes.okl', 'wb'))
pickle.dump(answers, open('answers.okl', 'wb'))

training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [simplemma.lemmatize(word.lower(), lang='hu') for word in word_patterns]
    for word in lemmatized_words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = list(training[:, 0])
train_y = list(training[:, 1])

model = Sequential()
model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(train_y[0]), activation='softmax'))

sgd = SGD(learning_rate=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])

model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbotmodel.h5')

print(lemmatized_words)
print("Done")
