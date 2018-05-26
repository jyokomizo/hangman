#!/usr/bin/python
# Jonathan Yokomizo

import requests
import json
import time

# response = requests.get("website", params=parameters??)
# dumps: takes Python obj + convert to string
# loads: take JSON str + convert to python obj

class entry:
    def __init__(self, word):
        self.word = word
        self.n_letters = len(word)
        self.frq = 1
        # self.letters = {}
        # for char in self.word:
        #     if not char in self.letters:
        #         self.letters[char] = 1
        #     else:
        #         self.letters[char] += 1

    # Entries are equal if they contain the same word
    def __hash__(self):
        return hash((self.word))
    def __eq__(self, other):
        return self.word == other.word


# This is the global structure to store all of the words from past games and will be filled as such:
# Each element will be a list of entry's (defined above) that are all of the same word length
# Each list will be sorted by word frequency
dictionary = {}

# Later implementation: letter counter for better guessing

# DELETE ME LATER PLEASE DON'T FORGET YOU IDIOT
# inorder_letters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'p', 'g', 'w', 'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z']

# Used to sort list of words of same length
def sort_by_frq(element):
    return element.frq

"""
Adds the passed string as an entry object to the dictionary

Parameters:
string - the word needed to be added

Returns:
No return value
"""
def entry_to_store(string):
    global dictionary
    new_word = entry(string)
    dictionary[new_word.n_letters] = dictionary.get(new_word.n_letters, list())
    if dictionary[new_word.n_letters]:
        if new_word in dictionary[new_word.n_letters]:
            loc = dictionary[new_word.n_letters].index(new_word)
            dictionary[new_word.n_letters][loc].frq += 1
            dictionary[new_word.n_letters] = sorted(dictionary[new_word.n_letters],
                key=sort_by_frq, reverse=True)
        else:
            dictionary[new_word.n_letters].append(new_word)
    else:
        dictionary[new_word.n_letters].append(new_word)

"""
Picks which word out of the phrase to be guessed to attempt to fill in
Returns index within phrase to be guessed
"""
def pick_word(phrase):
    # 2D list to hold index, letter count, and length
    completed = []
    # Check if no letters guessed in phrase
    empty = True
    for i in range(len(phrase)):
        word = phrase[i]
        num_letters = 0
        for c in word:
            if c.isalpha():
                num_letters += 1
                empty = False
        # Adds dummy value to list if completed word
        if num_letters == len(word):
            completed.append(-1)
        else:
            completed.append(num_letters)
    print("completed:", completed)
    tmp_spot = -1
    if not empty:
        tmp_letter = 0
        for i in completed:
            if i > tmp_letter:
                tmp_spot = completed.index(i)
    return tmp_spot

"""

"""
def select_letter(word, nums):
    # Set to arbitrary number greater than number of letters in alphabet
    place = 255
    for i in range(len(word)):
        if i in nums:
            continue
        temp = inorder_letters.index(word[i])
        print("temp:", temp)
        if temp < place:
            place = temp
    return inorder_letters[place]

"""
Guesses letter in phrase
"""
def post_letter(phrase, index):
    guess = ""
    phrase_length = len(phrase)
    selection = dictionary[phrase_length]
    indices = []
    for i in range(index, len(selection)):
        print("curr:", selection[i].word)
        for j in range(phrase_length):
            if phrase[i][j] != "_":
                indices.append(j)
                print("curr let:", selection[i].word[j], "phrase", phrase[i][j])
                if selection[i].word[j] == phrase[i][j]:
                    guess = select_letter(selection[i].word, indices)
                    return guess, i
    return guess, -1


def loop_func():
    varb = 0
    global dictionary
    while (varb < 20):
        # Set up initial game
        response = requests.get('http://upe.42069.fun/gLq72')
        response.raise_for_status()
        data = response.json()
        for header in data:
            print ("header:", header)
            print ("data:", data[header])
        
        # List of most commonly used English letters
        # Taken from: http://letterfrequency.org/
        inorder_letters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'p', 'g', 'w', 'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z']

        letters_guessed = set()
        # # Import words from text file, insert into data structure
        # file_data = (line.strip('\n') for line in open('words.txt', 'r'))
        # # https://stackoverflow.com/questions/3277503/in-python-how-do-i-read-a-file-line-by-line-into-a-list
        # # "bin" not actually in text file, used to initialize 2D set
        # curr_word = entry("bin")
        # dictionary = { len(curr_word.word) : {curr_word} }
        # for word in file_data:
        #     curr = entry(word)
        #     dictionary[len(word)] = dictionary.get(len(word), set())
        #     dictionary[len(word)].add(curr)
        # print("data:", dictionary)

        print ("store:", dictionary)
        for a in dictionary:
            print("length bin:", a)
            for b in dictionary[a]:
                print("word val:", b.word, "frq:", b.frq)

        dict_index = 0

        while data['status'] == 'ALIVE':
            num_words = 0
            current_phrase = []
            s = ""
            correct_guess = set()
            for i in data['state']:
                if i.isalpha():
                    s += i
                    correct_guess.add(i)
                if i == '_':
                    s += i
                if i.isspace():
                    if s != "":
                        num_words += 1
                        # current_word = entry(s)
                        current_phrase.append(s)
                        s = ""
            if s != "":
                num_words += 1
                # current_word = entry(s)
                current_phrase.append(s)

            print("phrase:", current_phrase)
            for a in current_phrase:
                print("word:", a)
            print("correct guesses:", correct_guess)

            # for lyric in current_phrase:
            #     time.sleep(2)
            #     dictionary[lyric.n_letters] = dictionary.get(lyric.n_letters, list())
            #     if dictionary[lyric.n_letters]:
            #         for a in dictionary[lyric.n_letters]:
            #             print("data word:", a.word)

            spot = pick_word(current_phrase)
            char_to_guess = ""
            if spot != -1:
                # guess based on spot
                try:
                    char_to_guess, dict_index = post_letter(current_phrase[spot], dict_index)
                except KeyError:
                    char_to_guess = ""
            # No char chosen
            if char_to_guess == "":
                # guess from inorder_letters
                char_to_guess = inorder_letters.pop(0)
                print("random guess:", char_to_guess)
            else:
                inorder_letters.pop(inorder_letters.index(char_to_guess))

            letters_guessed.add(char_to_guess)

            print("letters guessed:", letters_guessed)

            time.sleep(2)

            # for i in range(25):
            #     time.sleep(2)
            #     char_to_guess = inorder_letters.pop(0)
            #     correct_guess.add(char_to_guess)
            #     print("guessed letters:", correct_guess)
            post = requests.post('http://upe.42069.fun/gLq72', data = {"guess" : char_to_guess})
            post.raise_for_status()
            data = post.json()
            for header in data:
                print ("header:", header)
                print ("data:", data[header])
            if data['status'] != 'ALIVE':
                break;

        s = ""
        for i in data['lyrics']:
            if i.isalpha():
                s += i
            if i.isspace():
                if s != "":
                    entry_to_store(s)
                    s = ""
        # Add last word to dictionary
        if s != "":
            entry_to_store(s)

        print ("store:", dictionary)
        for a in dictionary:
            print("length bin:", a)
            for b in dictionary[a]:
                print("word val:", b.word, "frq:", b.frq)

        print("correct guesses:", correct_guess)

        varb += 1

    # # import sys
    # # data = []

    # data = ["_", "______", "__", "___s", "____s"]
    # entry_to_store("soups")
    # entry_to_store("then")
    # entry_to_store("turn")

    # spot = pick_word(data)
    # print("chosen:", spot)
    # dict_index = 0

    # if spot != -1:
    #     # guess based on spot
    #     char_to_guess, dict_index = post_letter(data[spot], dict_index)
    # # No char chosen
    # if char_to_guess == "":
    #     # guess from inorder_letters
    #     char_to_guess = inorder_letters.pop(0)
    # else:
    #     inorder_letters.pop(inorder_letters.index(char_to_guess))

    # print("guess?", char_to_guess)
    # print("remaining:", inorder_letters)

    # data = "i wonder if this works cause if this doesn't, i will be so sad; cats and dogs, but, i and such sad work please if not i cry; but and' imma i'm scold but who, am. you are, and, sad cats, but crying happy dogs are so am pleasing but not please food for the food up above around the corner in working cause works but also"
    # s = ""
    # for i in data:
    #     if i.isalpha():
    #             s += i
    #     if i.isspace():
    #         if s != "":
    #             entry_to_store(s)
    #             s = ""
    # # Add last word to dictionary
    # if s != "":
    #     entry_to_store(s)

    # print ("store:", dictionary)
    # for a in dictionary:
    #     print("length bin:", a)
    #     for b in dictionary[a]:
    #         print("word val:", b.word, "frq:", b.frq)

def main():
    loop_func()
    

if __name__ == "__main__":
    main()
