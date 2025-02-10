# -*- coding: utf-8 -*-
"""PRAssignmentml2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1aCa3y0cFdQF6ayU9tc1pFN1iUoo4jY13

Step 1: Import necessary libraries for our tasks
"""

import numpy as np
import pandas as pd
import time
# Instead of 'from keras.preprocessing.text import Tokenizer', use:
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SimpleRNN, LSTM, GRU, Dropout, Dense

"""# Step 2: given dataset will be loaded"""

# Load dataset
Seattle_Hotels_address_description = pd.read_csv('/content/Seattle_Hotels_address_description.csv', encoding='latin-1')

"""# Step 3: Tokenize the  given dataset"""

# Tokenization
corpus = Seattle_Hotels_address_description ['desc'].tolist()
t = Tokenizer(num_words=None, filters='!"#$%&()*+,-./:;<=>?@[\\]^_`{|}~\t\n', lower=True, split=' ', char_level=False, oov_token=None, document_count=0)
t.fit_on_texts(corpus)

"""# Step 4: Displaying the necessary logs from the Tokenizer object:"""

# Displaying the logs
print("Word Counts:", t.word_counts)
print("Word Docs:", t.word_docs)
print("Document Count:", t.document_count)
print("Word Index:", t.word_index)
print("Found %s unique tokens." % len(t.word_index))

"""# Step 5: Apply tokenization to the corpus:"""

# Function to get sequence of tokens
def get_sequence_of_tokens(corpus):
    t.fit_on_texts(corpus)
    total_words = len(t.word_index) + 1
    input_sequences = []
    for line in corpus:
        token_list = t.texts_to_sequences([line])[0]
        for i in range(1, len(token_list)):
            n_gram_sequence = token_list[:i+1]
            input_sequences.append(n_gram_sequence)
    return input_sequences, total_words

input_sequences, total_words = get_sequence_of_tokens(corpus)
print(input_sequences[:10])
print(total_words)

"""# Step 6: Apply padding to make consistent input sizes:"""

# Function to generate padded sequences
def generate_padded_sequences(input_sequences):
    max_sequence_len = max([len(x) for x in input_sequences])
    input_sequences = np.array(pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre'))
    predictors, label = input_sequences[:, :-1], input_sequences[:, -1]
    label = to_categorical(label, num_classes=total_words)
    return predictors, label, max_sequence_len

predictors, label, max_sequence_len = generate_padded_sequences(input_sequences)

"""# Step 7. Design three RNN models with Simple-RNN, LSTM, and GRU layers"""

# Model 1: Simple RNN
Recurrent_model = Sequential([
    Embedding(input_dim=total_words, output_dim=10, input_length=max_sequence_len - 1),
    SimpleRNN(100),
    Dropout(0.1),
    Dense(total_words, activation='softmax')
])

Recurrent_model.compile(loss='categorical_crossentropy', optimizer='adam')

start_time_for_RNN = time.time()
Recurrent_model.fit(predictors, label, epochs=20, verbose=1)
end_time_for_RNN = time.time()
print("Here is the Training time for Simple RNN :", end_time_for_RNN - start_time_for_RNN)

print("Here is the Training time for Simple RNN :", end_time_for_RNN - start_time_for_RNN)

import time

# Function to generate text based on the trained model
def generate_text(seed_text, next_words, model, max_seq_len):
    start_time = time.time()
    for _ in range(next_words):
        token_list = t.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_seq_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = ''
        for word, index in t.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text = seed_text + " " + output_word
    end_time = time.time()
    return seed_text.title(), end_time - start_time

# #Example input prompts
prompts = [
    "hilton seattle downtown",
    "best western seattle airport hotel",
    "located in the heart of downtown seattle"
]

# Generate descriptions for all prompts using all three models
for i, prompt in enumerate(prompts, 1):
    print(f"Prompt {i}: {prompt}")

    # Simple RNN
    desc_rnn, time_rnn = generate_text(prompt.lower(), 10, Recurrent_model, max_sequence_len)
    print("Simple RNN:", desc_rnn)
    print("Time taken for Simple RNN:", time_rnn)
    print()

# Model 2: LSTM
LSTM_model = Sequential([
    Embedding(input_dim=total_words, output_dim=10, input_length=max_sequence_len - 1),
    LSTM(100),
    Dropout(0.1),
    Dense(total_words, activation='softmax')
])

LSTM_model.compile(loss='categorical_crossentropy', optimizer='adam')

start_time_for_LSTM = time.time()
LSTM_model.fit(predictors, label, epochs=20, verbose=1)
end_time_for_LSTM = time.time()

print("Training time for LSTM:", end_time_for_LSTM - start_time_for_LSTM)

# Generate descriptions for all prompts using all three models
for i, prompt in enumerate(prompts, 1):
    print(f"Prompt {i}: {prompt}")


    # LSTM
    desc_lstm, time_lstm = generate_text(prompt.lower(), 10, LSTM_model, max_sequence_len)
    print("LSTM:", desc_lstm)
    print("Time taken for LSTM:", time_lstm)
    print()

# Model 3: GRU
Gated_Recurrent_model = Sequential([
    Embedding(input_dim=total_words, output_dim=10, input_length=max_sequence_len - 1),
    GRU(100),
    Dropout(0.1),
    Dense(total_words, activation='softmax')
])

Gated_Recurrent_model.compile(loss='categorical_crossentropy', optimizer='adam')

start_time_for_GRU = time.time()
Gated_Recurrent_model.fit(predictors, label, epochs=10, verbose=1)
end_time_for_GRU = time.time()

print("Training time for GRU:", end_time_for_GRU - start_time_for_GRU)

import time

# Function to generate text based on the trained model
def generate_text(seed_text, next_words, model, max_seq_len):
    start_time = time.time()
    for _ in range(next_words):
        token_list = t.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_seq_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = ''
        for word, index in t.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text = seed_text + " " + output_word
    end_time = time.time()
    return seed_text.title(), end_time - start_time

#

#Example input prompts
prompts = [
    "hilton seattle downtown",
    "best western seattle airport hotel",
    "located in the heart of downtown seattle"
]

# Generate descriptions for all prompts using all three models
for i, prompt in enumerate(prompts, 1):
    print(f"Prompt {i}: {prompt}")

    # GRU
    desc_gru, time_gru = generate_text(prompt.lower(), 10, Gated_Recurrent_model, max_sequence_len)
    print("GRU:", desc_gru)
    print("Time taken for GRU:", time_gru)

    print()