#!/usr/bin/python
# Jonathan Yokomizo

import requests
import json
import time

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

inorder_letters = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'p', 'g', 'w', 'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z']
const_letters_list = ['e', 't', 'a', 'o', 'i', 'n', 's', 'r', 'h', 'l', 'd', 'c', 'u', 'm', 'f', 'p', 'g', 'w', 'y', 'b', 'v', 'k', 'x', 'j', 'q', 'z']
letters_guessed = set()
avoid = []

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
    # 2D list to hold index
    completed = []
    # Check if no letters guessed in phrase
    empty = True
    for i in range(len(phrase)):
        word = phrase[i]
        length = len(word)
        num_letters = 0
        if i in avoid:
            # Add dummy value to list if avoid word to keep indexing consistent
            completed.append([-2, length])
            continue
        for c in word:
            if c.isalpha():
                num_letters += 1
                empty = False
        # Adds dummy value to list if completed word
        if num_letters == length:
            completed.append([-1, length])
        else:
            completed.append([num_letters, length])
    print("completed:", completed)
    tmp_spot = -1
    tmp_length = 255
    if not empty:
        tmp_letter = 0
        for i in completed:
            # print("i", i, "tmp vals (let len):", tmp_letter, tmp_length)
            if i[0] != 0 or i[0] != -1 or i[0] != -2:
                # Choose word with most letters completed or shorter word if equal
                if i[0] > tmp_letter or (i[0] == tmp_letter and i[1] < tmp_length):
                    tmp_spot = completed.index(i)
                    tmp_letter = i[0]
                    tmp_length = i[1]
    # else:
    #     for i in completed:
    #         # Choose shortest word (with entries in dictionary of same length)
    #         if i[1] < tmp_length:
    #          # and dictionary.get(i[1]):
    #             tmp_spot = completed.index(i)
    #             tmp_length = i[1]
    return tmp_spot

"""

"""
def select_letter(word, nums):
    # global inorder_letters
    print("indices", nums)
    # Set to arbitrary number greater than number of letters in alphabet
    place = 255
    for i in range(len(word)):
        # If looking at already guessed letter in word
        if i in nums:
            continue
        # 
        if word[i] in letters_guessed:
            continue
        # temp = const_letters_list.index(word[i])
        temp = inorder_letters.index(word[i])
        print("temp:", temp)
        # if temp in nums:
        #     continue
        if temp < place:
            place = temp
            print("place:", place)
    print("place", place)
    if place == 255:
        return "+"
    return inorder_letters[place]

"""
Guesses letter in phrase
"""
def post_letter(phrase, index):
    guess = "+"
    phrase_length = len(phrase)
    selection = dictionary[phrase_length]
    indices = set()
    if index == -1:
        index = 0
    print("start in dict:", index)
    for i in range(index, len(selection)):
        print("curr:", selection[i].word)
        match = []
        for j in range(phrase_length):
            if phrase[j] != "_":
                indices.add(j)
                print("j:", j, "curr let:", selection[i].word[j], "phrase", phrase[j])
                if selection[i].word[j] == phrase[j]:
                    match.append(1)
                else:
                    match.append(0)
        print("match", match)
        # Checks if all letters in phrase == selectionp[i].word
        # https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
        if match and match[0] != 0 and match.count(match[0]) == len(match):
            guess = select_letter(selection[i].word, indices)
            if guess == "+":
                continue
            return guess, i
    return guess, -1

def loop_func():
    varb = 0
    global dictionary
    global inorder_letters
    global letters_guessed
    global avoid
    while (varb < 100):
        # Set up initial game
        response = requests.get('http://upe.42069.fun/gLq72')
        response.raise_for_status()
        data = response.json()
        for header in data:
            print ("header:", header)
            print ("data:", data[header])

        # Import words from text file, insert into data structure
        file_data = (line.strip('\n') for line in open('sample.txt', 'r'))
        # https://stackoverflow.com/questions/3277503/in-python-how-do-i-read-a-file-line-by-line-into-a-list
        for word in file_data:
            curr = entry(word)
            dictionary[len(word)] = dictionary.get(len(word), list())
            dictionary[len(word)].append(curr)
        # print("store:", dictionary)

        # print ("store:", dictionary)
        for a in dictionary:
            print("length bin:", a)
            for b in dictionary[a]:
                print("word val:", b.word, "frq:", b.frq)

        inorder_letters = list(const_letters_list)
        dict_index = 0
        correct_guess = set()
        list_selection = False
        # List of spots in current_phrase to skip over
        avoid = []
        letters_guessed = set()
        spot = -1
        past_spot = -1
        # past_word = ""

        while data['status'] == 'ALIVE':
        # while not ends:
            # got_guess = False
            num_words = 0
            current_phrase = []
            temp_correct = set()
            s = ""
            for i in data['state']:
            # for i in udrs[varb]:
                if i.isalpha():
                    s += i
                    temp_correct.add(i)
                if i == '_':
                    s += i
                if i.isspace():
                    if s != "":
                        num_words += 1    
                        current_phrase.append(s)
                        s = ""
            if s != "":
                num_words += 1
                current_phrase.append(s)

            print("spot after current_phrase", spot)
            # # Reset dict_index if word from last game fully guessed
            # if spot != -1:
            #     if current_phrase[spot].isalpha():
            #         dict_index = 0
            #         print("reset dict_index")

            print("next dict_index:", dict_index)

            print("phrase:", current_phrase)
            for a in current_phrase:
                print("word:", a)
            print("correct guesses:", correct_guess)

            spot = pick_word(current_phrase)
            print("spot to guess:", spot, "past_spot", past_spot)
            if spot != past_spot:
                # past_word = current_phrase[past_spot]
                # print("assign past word")
                past_spot = spot
                dict_index = 0
                print("updated past_spot and reset dict_index")
            # spot == past_spot
            else:
                # if guess from last game failed
                # print("list_selection %s", list_selection, "past_word", past_word, "curr word", current_phrase[past_spot])
                print("list_selection %s", list_selection, "temp", len(temp_correct), "corr", len(correct_guess))
                if list_selection and len(temp_correct) == len(correct_guess):
                # if list_selection and past_word == current_phrase[past_spot]:
                    dict_index += 1
                    print("incr dict_index")
                # else:
                    # correct_guess = set(temp_correct)
                    # print("assign correct_guess")
                # past_word = current_phrase[past_spot]
            # past_word = current_phrase[past_spot]
            # print("assign past word")
            correct_guess = set(temp_correct)
            print("assign correct_guess")
            char_to_guess = ""
            if spot != -1:
                # guess based on spot
                try:
                    char_to_guess, dict_index = post_letter(current_phrase[spot], dict_index)
                except KeyError:
                    char_to_guess = "+"

            if char_to_guess.isalpha():
                inorder_letters.pop(inorder_letters.index(char_to_guess))
                list_selection = True
            else:
                if char_to_guess == "+":
                    avoid.append(spot)
                    print("appended to avoid")
                print("guess from inorder_letters")
                char_to_guess = inorder_letters.pop(0)
                list_selection = False

            print("char:", char_to_guess)
            letters_guessed.add(char_to_guess)

            print("dict_index", dict_index)

            print("letters guessed:", letters_guessed)
            print("inorder_letters", inorder_letters)

            time.sleep(2)

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
        # for i in data[varb]:
            if i.isalpha():
                s += i
            if i.isspace():
                if s != "":
                    entry_to_store(s)
                    s = ""
        # Add last word to dictionary
        if s != "":
            entry_to_store(s)

        # print ("store:", dictionary)
        for a in dictionary:
            print("length bin:", a)
            for b in dictionary[a]:
                print("word val:", b.word, "frq:", b.frq)

        print("correct guesses:", correct_guess)

        varb += 1

def main():
    loop_func()
    

if __name__ == "__main__":
    main()
