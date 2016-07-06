from sklearn import svm
from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.ensemble import RandomForestClassifier


import json
import numpy as np
import random
import features as translators
import data_operations as dataAPI
import os

cur_dir = os.path.dirname(os.path.realpath(__file__))

def diff(a, b):
    b = set(b)
    return [aa for aa in a if aa not in b]


def test_classifier(clf):
    with open(cur_dir + '/femaleTest.txt') as data_female:
        test_data_female = data_female.readlines()
    with open(cur_dir + '/maleTest.txt') as data_male:
        test_data_male = data_male.readlines()

    female_succes_rate = 0
    for female_name in test_data_female:
        if clf.predict([translators.translate_name_in_array(female_name)])[0] == 0:
            female_succes_rate += 1
    print('female:', female_succes_rate, len(test_data_female))
    female_succes_rate1 = float(female_succes_rate) / len(test_data_female)

    male_succes_rate = 0
    for male_name in test_data_male:
        if clf.predict([translators.translate_name_in_array(male_name)])[0] == 1:
            male_succes_rate += 1

    print('male: ', male_succes_rate, len(test_data_male))
    male_succes_rate1 = float(male_succes_rate) / len(test_data_male)
    # print(float((male_succes_rate + female_succes_rate)) / (len(test_data_male) + len(test_data_female)))
    return float((male_succes_rate + female_succes_rate)) / (len(test_data_male) + len(test_data_female))


def test_classifier_with_sets(number_of_test_sets, clf):
    sum_rate = 0
    for i in range(number_of_test_sets):
        dataAPI.generate_train_and_test_files()
        train_name_classifier(clf)
        sum_rate = np.add(sum_rate, test_classifier(clf))
    return np.divide(sum_rate, number_of_test_sets)


def translate_to_classname(class_val):
    if class_val == 1:
        return 'male'
    else:
        return 'female'


def train_name_classifier(clf, female_names_file=cur_dir + '/femaleTrain.txt', male_names_file=cur_dir + '/maleTrain.txt'):
    print(cur_dir)
    with open(female_names_file) as data_female:
        data_female = data_female.readlines()
    with open(male_names_file) as data_male:
        data_male = data_male.readlines()

    data_male = diff(data_male, data_female)
    data_female = diff(data_female, data_male)

    data = data_male + data_female
    translated_data = [
        translators.translate_name_in_array(name.lower()) for name in data]
    translated_data_output = [1] * len(data_male) + [0] * len(data_female)

    # max_depth=11
    # n estim = 6
    # clf = RandomForestClassifier(n_estimators=180, min_samples_split=25, random_state=3)
    clf = clf.fit(translated_data, translated_data_output)


def test_with_hary_potter_names(clf):
    with open('harry-poter-names.txt') as hary_potter_names:
        data = hary_potter_names.readlines()

    with open('hary-potter-names-with-gender.txt', 'w') as classified:
        for name in data:
            prediction = clf.predict(
                [translators.translate_name_in_array(name)])[0]

            gender = translate_to_classname(prediction)

            line = name + ' ' + gender + '\n'
            classified.write(line)

# dataAPI.generate_train_and_test_files()
# 0.786247086247

# clf = KNeighborsClassifier(n_neighbors=15, p = 1)
# clf = tree.DecisionTreeClassifier(max_depth=9,random_state=3)
clf = RandomForestClassifier(n_estimators=180,
                             min_samples_split=25,
                             random_state=3,)
# train_name_classifier(clf)
# print(test_classifier(clf))

# from sklearn.externals import joblib
# joblib.dump(clf, 'my_model.pkl', compress=9)
# test_with_hary_potter_names(clf)
# print(test_classifier_with_sets(1, clf))
