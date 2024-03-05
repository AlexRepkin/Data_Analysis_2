#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys
import jsonschema


def new_human():
    """Запросить данные о человеке."""

    name = input("Name - ")
    surname = input("Surname - ")
    telephone = input("Telephone number - ")
    happy_birthday = input("Date of birth (Day.Month.Year) - ")
    # Создать словарь.
    return {
        "name": name,
        "surname": surname,
        "telephone": telephone,
        "birthday": happy_birthday
    }


def display_people(people):
    """Отобразить список людей."""

    if people:
        # Заголовок таблицы.

        line = "├-{}-⫟-{}⫟-{}-⫟-{}-⫟-{}-┤".format(
            "-" * 5, "-" * 25, "-" * 25, "-" * 25, "-" * 18)
        print(line)
        print("| {:^5} | {:^24} | {:^25} | {:^25} | {:^18} |".format(
            "№", "Name", "Surname", "Telephone", "Birthday"))
        print(line)
        for number, human in enumerate(people, 1):
            print("| {:^5} | {:<24} | {:<25} | {:<25} | {:<18} |".format(number, human.get(
                "name", ""), human.get("surname", ""),
                                                                         human.get("telephone", ""),
                                                                         human.get("birthday", "")))
        print(line)
    else:
        print("There are no people in list!")


def list_commands():
    """Список команд, доступных пользователю."""

    print("List of commands:")
    print("add - adding the human;")
    print("list - list of known people;")
    print("select 'month' - list of people, born in needed month;")
    print("help - list of commands;")
    print("exit - exit this program.")


def select_people(people, month):
    """Выбрать людей, родившихся в требуемом месяце."""

    born = []
    for human in people:
        human_month = human.get("birthday").split(".")
        if month == int(human_month[1]):
            born.append(human)
    return born


def save_people(file_name, staff):
    """Сохранить всех людей в файл JSON."""

    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установлен ensure_ascii=False
        json.dump(staff, fout, ensure_ascii=False, indent=4)


def load_people(file_name):
    """Загрузить всех людей из файла JSON."""

    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        loaded = json.load(fin)
    try:
        jsonschema.validate(loaded, schema)
        print(">>> Data is obtained!")
    except jsonschema.exceptions.ValidationError as e:
        print(">>> Data's structure is invalid. Please, check your JSON file.Error:")
        print(e.message)  # Ошибка валидацци будет выведена на экран
    return loaded


def main():
    """Главная функция программы."""

    print("Good day!, please, enter your command: ('help' will list all of them)")
    people = []
    while True:
        command = input(">>> ").lower()
        if command == "exit":
            break
        elif command == "add":
            human = new_human()
            people.append(human)
            # Сортировка идёт по фамилиям. Если фамилии одинаковые, то рассматриваются имена
            people.sort(key=lambda person: (person.get(
                "surname", ""), person.get("name", "")))
        elif command == "list":
            display_people(people)
        elif command.startswith("select "):
            which_month = command.split(" ", maxsplit=1)
            user_month = int(which_month[1])
            same_month = select_people(people, user_month)
            display_people(same_month)
        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Сохранить данные в файл с заданным именем.
            save_people(parts[1], people)
        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Сохранить данные в файл с заданным именем.
            people = load_people(parts[1])
        elif command == "help":
            list_commands()
        else:
            print(f"Unknown command! - {command}", file=sys.stderr)


if __name__ == "__main__":
    schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "surname": {"type": "string"},
                "telephone": {"type": "string"},
                "birthday": {"type": "string"}
            },
            "required": ["name", "surname", "telephone", "birthday"]
        }
    }
    main()
