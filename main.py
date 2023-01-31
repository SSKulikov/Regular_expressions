from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re
from typing import List, Any
import pandas as pd

with open("phonebook_raw.csv", 'r', encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)
    new_list = []


def names_moving():
    name_pattern = r'([А-Я])'
    name_substitution = r' \1'

    for column in contacts_list[1:]:
        line = column[0] + column[1] + column[2]
        if len((re.sub(name_pattern, name_substitution, line).split())) == 3:
            column[0] = re.sub(name_pattern, name_substitution, line).split()[0]
            column[1] = re.sub(name_pattern, name_substitution, line).split()[1]
            column[2] = re.sub(name_pattern, name_substitution, line).split()[2]
        elif len((re.sub(name_pattern, name_substitution, line).split())) == 2:
            column[0] = re.sub(name_pattern, name_substitution, line).split()[0]
            column[1] = re.sub(name_pattern, name_substitution, line).split()[1]
            column[2] = ''
        elif len((re.sub(name_pattern, name_substitution, line).split())) == 1:
            column[0] = re.sub(name_pattern, name_substitution, line).split()[0]
            column[1] = ''
            column[2] = ''
    return


def phone_number_formatting():
    phone_pattern = re.compile(
        r'(\+7|8)?\s*\(?(\d{3})\)?\s*\D?(\d{3})[-\s+]?(\d{2})-?(\d{2})((\s)?\(?(доб.)?\s?(\d+)\)?)?')
    phone_substitution = r'+7(\2)\3-\4-\5\7\8\9'
    for column in contacts_list:
        column[5] = phone_pattern.sub(phone_substitution, column[5])
    return


def duplicates_combining():
    for column in contacts_list[1:]:
        first_name = column[0]
        last_name = column[1]
        for contact in contacts_list:
            new_first_name = contact[0]
            new_last_name = contact[1]
            if first_name == new_first_name and last_name == new_last_name:
                for item in range(2, 7):
                    if contact[item] == '':
                        contact[item] = column[item]

    for contact in contacts_list:
        if contact not in new_list:
            new_list.append(contact)
    return new_list

def merge_list(lst1, lst2):
    for i in lst2:
        if i not in lst1:
            lst1.append(i)
    return lst1


def result_list():
    duplicate = {'result': [], "two": []}
    list_new = [n[0] for n in new_list]
    for index, item in enumerate(new_list):
        if list_new.count(item[0]) == 1:
            duplicate['result'].append(item)
        else:
            duplicate['two'].append(item)
    duplicate['result'].append(merge_list(duplicate['two'][0], duplicate['two'][1]))
    return duplicate['result']


if __name__ == '__main__':
    names_moving()
    phone_number_formatting()
    duplicates_combining()

with open("phonebook.csv", "w", encoding='utf-8', newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(result_list())