import random
def split_data(test_set_index, fileName, output):
    with open(fileName) as file:
        data = file.readlines();

    translated_data_output = [output] * len(data)

    test_set_size = int(len(data) * 0.1)
    test_set = []
    for index in range(0, test_set_size):
        test_sample_index = random.randint(0, len(data) - 1)
        test_set.append(data[test_sample_index])
        del data[test_sample_index]

    return (test_set, data)

def generate_train_and_test_files():
    female_names = split_data(0.1, 'female.txt', 0)

    with open('femaleTest.txt', 'w') as female_test_file:
        for name in female_names[0]:
            female_test_file.write(name)

    with open('femaleTrain.txt', 'w') as female_train_file:
        for name in female_names[1]:
            female_train_file.write(name)


    male_names = split_data(0.1, 'male.txt', 1)

    with open('maleTest.txt', 'w') as male_test_file:
        for name in male_names[0]:
            male_test_file.write(name)

    with open('maleTrain.txt', 'w') as male_train_file:
        for name in male_names[1]:
            male_train_file.write(name)
