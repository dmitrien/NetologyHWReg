import csv
import re
import operator
import itertools
from tools import logger

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def read_csv_to_dict():
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
        contacts_dict = []
        keys = contacts_list[0]
        values = contacts_list[1:]
        for num, vals in enumerate(values):
            contacts_dict.append({})
            for key, val in zip(keys, vals):
                contacts_dict[num].update({key: val})

        return contacts_dict

@logger
def decoding_info_result():
    actual_list = []
    result_list = []

    for refactor_list in contacts_list:
        not_hull_list = [number for number in refactor_list if number]
        actual_list.append(not_hull_list)

    actual_list.pop(0)

    mob_number_pattern = r"(\+7|8)\D*(\d{1,3})\D*(\d{3})\D*(\d{2})\D*(\d{2})(?:\D*(доб\.\s*(\d{4}))\D*)?"
    mail_pattern = r"[A-z-\.\d]*\W*@[A-z]+\.ru"
    sub_mob_number_pattern = r"+7(\2)\3-\4-\5 \6"
    find_numbers = r"(\+7|8)(\(\d{1,3}\))(\d{3})(\-\d{2})(\-\d{2})(?:\D*(доб\.)\s*(\d{4}))?"
    find_users_pattern = r"[А-ЯЁ][а-яё]+\s+[А-ЯЁ][а-яё]+(?:\s+[А-ЯЁ][а-яё]+)?"

    for user_list in actual_list:
        user_info = []
        dict_info = {}

        actual_text = " ".join(user_list)
        mob_number_sub = re.sub(mob_number_pattern, sub_mob_number_pattern, actual_text)

        mail_user = "".join(re.findall(mail_pattern, actual_text))
        fio_user = " ".join(re.findall(find_users_pattern, mob_number_sub))
        fio_user = fio_user.split()
        user_info.extend(fio_user)

        number_user = re.findall(find_numbers, mob_number_sub)
        user_info.append(number_user)
        user_info.append(mail_user)

        dict_info['lastname'] = fio_user[0]
        dict_info['firstname'] = fio_user[1]
        if len(fio_user) > 2:
            dict_info['surname'] = fio_user[2]
        dict_info['phone'] = user_info[-2]
        dict_info['email'] = user_info[-1]

        fix_phone = dict_info.get("phone")
        if fix_phone:
            number = "".join(fix_phone[0]).replace("доб.", " доб.")
        dict_info['phone'] = number

        result_list.append(dict_info)

    return result_list

def combining_dictionaries():
    result_list = []
    fix_list = decoding_info_result()
    false_list = read_csv_to_dict()
    for i, dict in enumerate(false_list):
        dix_dict = dict | fix_list[i]
        result_list.append(dix_dict)

    return result_list

def fixed_duble():
    list_dict = combining_dictionaries()
    group_list = ['firstname', 'lastname']
    group = operator.itemgetter(*group_list)
    list_dict.sort(key=group)
    grouped = itertools.groupby(list_dict, group)

    merge_data = []
    for (firstname, lastname), g in grouped:
        merge_data.append({'lastname': lastname, 'firstname': firstname})
        for gr in g:
            d1 = merge_data[-1]
            for k, v in gr.items():
                if k not in d1 or d1[k] == '':
                    d1[k] = v

    return merge_data

def write_result_to_file(result):
    keys = list(result[0].keys())
    with open("phonebook.csv", "w", encoding="utf8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerow(keys)
        for d in result:
            datawriter.writerow(d.values())

if __name__ == '__main__':
    result = fixed_duble()
    write_result_to_file(result)
