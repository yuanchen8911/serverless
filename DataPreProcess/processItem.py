import sys
import re
import random
import json
import os


def addSynonymsToList(words, num, synonyms_list, tmp, start_idx):
    if num == 0:
        synonyms_list.append(tmp)
        return

    if start_idx >= len(words):
        return

    if tmp != "":
        addSynonymsToList(words, num - 1, synonyms_list, tmp + " " + words[start_idx], start_idx + 1)
    else:
        addSynonymsToList(words, num - 1, synonyms_list, words[start_idx], start_idx + 1)
    addSynonymsToList(words, num, synonyms_list, tmp, start_idx + 1)


def generateSynonyms(words):
    entity = words[-1]

    words.pop(-1)
    result_list = []
    for i in range(1, len(words) + 1):
        addSynonymsToList(words, i, result_list, "", 0)

    string_list = []
    for w in result_list:
        string_list.append(w + " " + entity)
    string_list.append(entity)
    return string_list


def tokenizeDoc(cur_doc):
    return re.findall('[a-z]+', cur_doc)


def main():
    filename = ''
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        print("Please provide a filename")
        exit(0)

    item_map = {}
    entity_map = {}
    number_list = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'nine', 'ten']
    with open(filename, 'r') as f:
        for line in f.readlines():
            items = line.lower().split(',')
            product_name = items[1]
            words = tokenizeDoc(product_name)
            if len(words) <= 0:
                continue

            contains_number = False
            for num in number_list:
                if num in words:
                    contains_number = True
                    break

            if contains_number:
                continue

            entity = words[-1]
            if entity.endswith('s'):
                entity = entity[0:-1]
            if len(words) <= 4 and entity not in entity_map:
                result_list = generateSynonyms(words)
                item_map[" ".join(words) + " " + entity] = result_list
                entity_map[entity] = True

    f.close()

    price_file = open('price.txt', 'w+')
    item_file = open('dialogflow_entity.txt', 'w+')
    for key, val in item_map.iteritems():
        print('"' + key + '", "' + '","'.join(val) + '"')
        item_file.write('"' + key + '", "' + '","'.join(val) + '"\n')
        price = random.random() * 20
        price_string = round(price, 2)
        price_file.write(key + "," + str(price_string) + '\n')

    price_file.close()
    item_file.close()


if __name__ == '__main__':
    main()
