def get_dictonary(dataset):
    uniques = ''
    row = ''
    for text in dataset:
        #row = ''
        try:
           row =row + ''.join(set(text[0]))
        except:
            pass
        #uniques = uniques.join(set(row)) #append(row)

        print("row:", row)
    uniques = uniques.join(set(row))
    print("uniques:", uniques)
    #uniques = (set(uniques))
    length = len(uniques)
    print(length)
    indexes = list(range(length))

    di = dict(zip(uniques, indexes))
    return di


def convert_to_int(dataset,dictionary):
    length = 0

    int_dataset = []
    row = []
    for text in dataset:
        length += 1
        row.clear()
        try:
            for char in text[0]:
                number = dictionary[char]
                row.append(number)
        except:
            pass
        int_dataset.append(row)

    return int_dataset

dataset = [['ذَهَبَ مُحَمَّد اِلَى المدرسة صباحا'],
               ['ذَهَبَ مُحَمَّد اِلَى المدرسة ليلا'],
               ['عاد محمد من النادى']]
_dictionary = get_dictonary(dataset)
converted_dataset = convert_to_int(dataset, _dictionary)
print(converted_dataset)


