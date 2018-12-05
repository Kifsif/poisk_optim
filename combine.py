from config import READ_ENCODING, WRITE_ENCODING
import os
import glob
import codecs


def combine_all(source_files_dir, first_column_only, encoding):
    source_files_mask = os.path.join(source_files_dir, "*.csv")
    result_file = os.path.join(source_files_dir, 'result.csv')
    file_list = glob.glob(source_files_mask)

    if first_column_only:
        counter = 1
        for a_file in file_list:
            with codecs.open(a_file, 'r', encoding) as r_file:
                while True:
                    try:
                        line = r_file.readline()
                    except UnicodeDecodeError:
                        continue  # Встретилась строка не в той кодировке. Например, Букварикс может поместить такие строки в конце.
                    if (not line):
                        break
                    try:
                        start_pos = line.index('"')
                        end_pos = line.index('"', start_pos + 1)
                    except ValueError:
                        continue  # Кавычка не найдена.

                    with codecs.open(result_file, 'a', encoding=WRITE_ENCODING) as w_file:
                        phrase = line[start_pos + 1:end_pos]
                        w_file.write("{}\n".format(phrase))
                        print("{}:{}".format(counter, phrase))
                        counter += 1

    else:

        for a_file in file_list:
            with codecs.open(a_file, 'r', encoding=READ_ENCODING) as file:
                try:
                    lines = file.read()
                except UnicodeDecodeError:
                    continue

            with codecs.open(result_file, 'a', encoding=WRITE_ENCODING) as file:
                try:
                    file.write(lines)
                except UnicodeEncodeError:
                    pass  # Поставить точку останова и смотреть в каждом конкретном случае.
    print("Готово")

def combine():
    source_files_dir = input("Введите каталог: ")

    while True:
        first_column_only = input("Только первая колонка(y/n)? ").lower()

        if first_column_only in ["y", "n"]:
            break

    if first_column_only == "y":
        first_column_only = True
    else:
        first_column_only = False

    while True:
        encoding = input("Кодировка (u/w): ").lower()

        if encoding in ["u", "w"]:
            break

    if encoding == "u":
        encoding = 'utf-8'
    else:
        encoding = 'windows-1251'


    combine_all(source_files_dir, first_column_only, encoding)




