import os
import shutil
import collections

def get_region_name(region_number):

    """По номеру региона Яндекса вернуть кортеж (регион: название региона).
    Например, (223: Москва).

    https://tech.yandex.ru/xml/doc/dg/reference/regions-docpage/


    :param region_number: int
    :return: tuple
    """

    regions = {
                20: "Архангельск",
                1092: "Назрань",
                37: "Астрахань",
                30: "Нальчик",
                197: "Барнаул",
                47: "Нижний Новгород",
                4: "Белгород",
                65: "Новосибирск",
                77: "Благовещенск",
                66: "Омск",
                191: "Брянск",
                10: "Орел",
                24: "Великий Новгород",
                48: "Оренбург",
                75: "Владивосток",
                49: "Пенза",
                33: "Владикавказ",
                50:  "Пермь",
                192: "Владимир",
                25: "Псков",
                38: "Волгоград",
                39: "Ростов-на-Дону",
                21: "Вологда",
                11: "Рязань",
                193: "Воронеж",
                51: "Самара",
                1106: "Грозный",
                2: "Санкт-Петербург",
                54: "Екатеринбург",
                42: "Саранск",
                5: "Иваново",
                12: "Смоленск",
                63: "Иркутск",
                239: "Сочи",
                41: "Йошкар-Ола",
                36: "Ставрополь",
                43: "Казань",
                973: "Сургут",
                22: "Калининград",
                13: "Тамбов",
                64: "Кемерово",
                14: "Тверь",
                7: "Кострома",
                67: "Томск",
                35: "Краснодар",
                15: "Тула",
                62: "Красноярск",
                195: "Ульяновск",
                53: "Курган",
                172: "Уфа",
                8: "Курск",
                76: "Хабаровск",
                9: "Липецк",
                45: "Чебоксары",
                28: "Махачкала",
                56: "Челябинск",
                1: "Москва и Московская область",
                1104: "Черкесск",
                213: "Москва",
                16: "Ярославль",
                23: "Мурманск",
                225: "Россия",
                187: "Украина",
                149: "Беларусь",
                159: "Казахстан",
                225: "Россия",
                187: "Украина",
                149: "Беларусь",
                159: "Казахстан",
    }

    return region_number, regions[int(region_number)]


def write_phrase_to_log(phrase, write_mode, enc, full_path_to_file):
    """
    Псать в лог.

    :param phrase: str
    :param write_mode: "r", "a", "w" (https://docs.python.org/3/library/functions.html#open)
    :param enc: str
    :param full_path_to_file: str
    :return: None
    """
    with open(full_path_to_file, write_mode, encoding=enc) as f:
        # Здесь могуть возникать сключения. Например, UnicodeEncodeError.
        # Пусть взрывается - дебажить будем в каждом конкретном случае.
        f.write("{}\n".format(phrase))


def get_full_path_to_project_dir(project_name):
    """
    По названию проекта получить полный путь до каталога c инит-файлами и логом.
    :param project_name:
    :return: str
    """
    return os.path.join("/home/michael/Documents/PoiskOptim", project_name)


def get_project_paths(project_name):
    """
    У каждого проекта есть свой каталог, где располагаются каталоги с инит-файлами и логом.

    :param project_name:
    :return: project_dir, init_dir, log_dir, log_file
    """
    project_dir = os.path.join(get_full_path_to_project_dir(project_name))
    init_dir = os.path.join(project_dir, "init")
    log_dir = os.path.join(project_dir, "log")
    log_file = os.path.join(project_dir, project_name)

    return project_dir, init_dir, log_dir, log_file



def clear_files(a_dir):
    """
    Удаляем файлы. например, лога.
    :param logs_dir:
    :return: None
    """
    try:
        shutil.rmtree(a_dir)
    except FileNotFoundError:
        pass # Do nothing

    os.makedirs(a_dir)


def alert_duplicates(elements):
    duplicates = [element for element, count in collections.Counter(elements).items() if count > 1]
    if duplicates:
        str_duplicates = "\n".join(duplicates)
        raise Exception("Дубли: \n{}".format(str_duplicates))


def get_list(full_path_to_file, encoding):
    """
    Прочитать содержимое файла. Вернуть список.
    :param full_path_to_file:
    :param encoding:
    :return: list
    """

    try:
        with open(full_path_to_file, "r", encoding=encoding) as f:
            elements = f.read().splitlines()
    except FileNotFoundError:
        return []
    alert_duplicates(elements)
    return elements