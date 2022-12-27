from pprint import pprint
import re
# читаем адресную книгу в формате CSV в список contacts_list
import csv

with open("phonebook_raw.csv") as f:
    rows = csv.reader(f, delimiter=',')
    contacts_list = list(rows)
# pprint(contacts_list)

# TODO 1: выполните пункты 1-3 ДЗ
pattern = r'(\w+)'
pattern_number_search = r'(\+7|8)\s*\(?(\d{3})\)?\s*\-?(\d{3})\-?(\d{2})\-?(\d{2})\s?\(?([А-ё]+\.)?\s?(\d{4})?\)?'
pattern_number_sub = r'+7(\2)\3-\4-\5 \6\7'


def raw_transformations(contacts_list):
    new_contacts_list = []
    for contact_list in contacts_list:
        record = []
        full_name = re.findall(pattern, ' '.join((contact_list[:3])))
        if len(full_name) < 3:
            full_name.append('')
        record += full_name
        record.append(contact_list[3])
        record.append(contact_list[4])
        record.append(re.sub(pattern_number_search, pattern_number_sub, contact_list[5]).strip())
        record.append(contact_list[6])
        new_contacts_list.append(record)
    return new_contacts_list


def merge_doubles(record_one, record_two):
    result = []
    for index in range(len(record_one)):
        result.append(record_one[index]) if record_one[index] else result.append(record_two[index])
    return result


def finish_contact_list(new_contacts_list):
    result = {}
    for item in new_contacts_list:
        result[item[0]] = merge_doubles(item, result[item[0]]) if item[0] in result else item
    return result.values()


new_contacts_list = raw_transformations(contacts_list)
result = finish_contact_list(new_contacts_list)


# TODO 2: сохраните получившиеся данные в другой файл
# код для записи файла в формате CSV
with open('phonebook.csv', 'w') as f:
    datawriter = csv.writer(f, delimiter=',')
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(result)


