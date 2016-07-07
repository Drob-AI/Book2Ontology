import fuzzy
import numpy as np

special_english_sounds = ['mm', 'nn', 'rr','ll','dth','tt', 'ri', 'ch', 'sh', 'th', 'wh' ,
'ng', 'nk', 'oi', 'ow', 'oo','ur' , 'ar' , 'or'
'aw' 'zh', 'gl', 'pl', 'br', 'cr', 'dr', 'fr',
'gr', 'pr', 'tr', 'sk', 'sl', 'sp', 'st', 'sw' , 'spr' , 'str']
vowels = ['a', 'e', 'i', 'o', 'u']

def postions_with_charcode(features, name):
    features += [0] * 27
    for position, char_code in enumerate([ord(char) - 96 for char in name]):
        if char_code < 0:
            char_code = 0
        features[char_code] += (position + 1) * char_code

def soundex_feature(features, name):
    soundex = fuzzy.Soundex(7)
    name_soundex = soundex(name)
    features_soundex = [ord(name_soundex[0].lower()) - 96 if char.isalpha() else int(char) for char in name_soundex]
    features = features + features_soundex

def bigrams_feature(features, name):
    features += [0] * 14
    char_codes = [ord(char) - 96 for char in name]
    for position, char_code in enumerate(char_codes):
        if char_code < 0:
            char_code = 0
        if position > 0:
            features[position - 1] = int(str(char_codes[position - 1]) + str(char_code))

def is_last_letter(features, name, letter):
    features.append((1 if name[-1] == letter else 0))

def has_pair_letters(features, name, pair):
    features.append((1 if pair in name else 0))


def number_of_vowels(features, name):
    features.append(len(filter(lambda char: char in vowels, list(name))))

def ends_with_vowels(features, name):
    features.append(name[-1] in ['a', 'e', 'i', 'o', 'u'])

def starts_with_vovel(features, name):
    features.append(name[0] in ['a', 'e', 'i', 'o', 'u'])

def number_of_double_letters(features, name):
    features.append(0)
    name_as_list = list(name)
    for index, char in enumerate(name_as_list):
        if index > 0 and char == name_as_list[index - 1]:
            features[-1] += 1

def vowels_to_nonvowels(features, name):
    number_of_vowels = len(filter(lambda char: char in vowels, list(name)))
    features.append( float(number_of_vowels) / len(name))

def name_size(features, name):
    features.append(len(name))

def name_count(features, name):
    arr = [0] * 27
    for ind, x in enumerate(name):
        index = ord(x)-ord('a')
        if index > 0:
            arr[ord(x)-ord('a')] += 1
    features += arr

def letter_positions(features, name, letter):

    features.append(0)
    for ind, x in enumerate(name):
        if x == letter:
            features[-1] += ind+1;

def longest_nonvowels_seq(features, name):
    features.append(0)
    current_seq_size = 0

    for char in name:
        if char in vowels:
            if features[-1] < current_seq_size:
                features[-1] = current_seq_size
            current_seq_size = 0
        else:
            current_seq_size += 1

    if features[-1] < current_seq_size:
                features[-1] = current_seq_size

def translate_name_in_array(name):
    name = name[0:-1]
    features = []

    postions_with_charcode(features, name)

    is_last_letter(features, name, 'a')
    is_last_letter(features, name, 'n')
    is_last_letter(features, name, 'y')

    letter_positions(features, name, 'a')
    letter_positions(features, name, 'e')
    letter_positions(features, name, 'i')
    letter_positions(features, name, 'y')
    letter_positions(features, name, 'l')

    ends_with_vowels(features, name)
    starts_with_vovel(features, name)
    number_of_double_letters(features, name)

    has_pair_letters(features, name, 'ie')
    for sound in special_english_sounds:
        has_pair_letters(features, name, sound)

    longest_nonvowels_seq(features, name)
    name_count(features, name)
    soundex_feature(features, name)
    bigrams_feature(features, name)

    name_size(features, name)
    number_of_vowels(features, name)

    # features[-2] = ord(name[-1])-ord('a')
    # features[-1] = ord(name[-2])-ord('a')

    return np.array(features)

def translate_name_in_array_1(name):
    name = name[0:-1]
    features = [0] * 15
    for position, char_code in enumerate([ord(char) - 96 for char in name]):
        if char_code < 0:
            char_code = 0
        features[position] = char_code


    is_last_letter(features, name, 'a')
    is_last_letter(features, name, 'y')

    ends_with_vowels(features, name)

    # has_pair_letters(features, name, 'ie')
    # for sound in special_english_sounds:
    #     has_pair_letters(features, name, sound)

    longest_nonvowels_seq(features, name)
    # soundex_feature(features, name)
    # bigrams_feature(features, name)
    # vowels_to_nonvowels(features, name)
    # name_size(features, name)
    # number_of_vowels(features, name)

    return features

def translate_name_in_svm_array(name):
    name = name[0:-1]
    features = []
    postions_with_charcode(features, name)

    is_last_letter(features, name, 'a')
    is_last_letter(features, name, 'n')
    is_last_letter(features, name, 'g')
    is_last_letter(features, name, 'l')
    is_last_letter(features, name, 'y')

    ends_with_vowels(features, name)
    starts_with_vovel(features, name)
    number_of_double_letters(features, name)

    has_pair_letters(features, name, 'ie')
    for sound in special_english_sounds:
        has_pair_letters(features, name, sound)

    longest_nonvowels_seq(features, name)
    soundex_feature(features, name)
    bigrams_feature(features, name)
    vowels_to_nonvowels(features, name)
    name_size(features, name)
    number_of_vowels(features, name)
    return features
