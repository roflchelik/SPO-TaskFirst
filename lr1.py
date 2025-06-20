import re  # импорт регулярных выражений для python


number = r"^[0-9A-Fa-f]+$"  # регулярка для чисел
operator = ['|', '&', '^', '!']  # логические операторы (OR, AND, XOR, NOT)
assignment = ':='  # знак присваивания
space = ' '
hex_number = ['a', 'b', 'c', 'd', 'e', 'f', 'A', 'B', 'C', 'E', 'F']  # для 16-ричных чисел
brackets = ['(', ')']

out_list = []


def read(text):
    state = 'a'  # начальное состояние
    i: int = -1  # переменная цикла перебора символов
    token = ''  # хранит текущую лексему
    token_type = 'token type'  # хранит тип лексемы

    while i < len(text) - 1:  # начало перебора символов (элементарных лексем)
        i += 1
        current_char = text[i]  # текущий символ строки
        token += current_char  # считываем лексему целиком (посимвольно)

        if state == 'a':  # начальное состояние А
            if current_char.isdigit():  # проверка символа: цифра или нет
                state = 'b'
            elif current_char.isalpha():  # проверка символа: буква алфавита или нет
                state = 'c'
            elif current_char == ':':  # проверка: оператор присваивания или нет
                state = 'd'
            elif current_char == '#':  # проверка: начинается комментарий или нет
                state = 'e'
                token_type = 'comment'
            elif current_char in operator:  # Проверка: логич. Оператор или нет
                token_type = 'logical sign'
                state = 'f'
            elif current_char == ';':  # конец строки кода или нет
                token_type = 'separator'
                state = 'f'
            elif current_char in brackets:  # скобка или нет
                token_type = 'bracket'
                state = 'f'
            elif current_char == space:  # пробел или нет
                token = token[:-1]
            else:  # иначе символ не распознан -> состояние ошибки
                state = 'g'
            continue

        elif state == 'b':  # состояние для проверки на шестнадцатеричное число
            if current_char.isdigit() or current_char in hex_number:  # число продолжается
                state = 'b'
            # ниже происходит проверка: если число закончилось, и дальше идет след. лексема алфавита, то проверь число
            # по регулярному выражению на шестнадцатеричность
            elif current_char == ';' or current_char == space or current_char in operator or current_char in brackets:
                if re.fullmatch(number, token[:-1].strip()):
                    token_type = 'hexadecimal number'
                state = 'f'
            else:  # иначе состояние ошибки
                state = 'g'

        elif state == 'c':  # состояние для проверки на имя переменной (идентификатор)
            if current_char.isalnum():  # метод проверки: цифра или буква алфавита
                state = 'c'
            # ниже происходит проверка: если после имени переменной идет след. лексема алфавита, то текущая лексема - переменная
            elif current_char == ';' or current_char == space or current_char == ':' or current_char in operator or current_char in brackets:
                token_type = 'identifier'
                state = 'f'
            else:  # иначе состояние ошибки: символ не распознан
                state = 'g'

        elif state == 'd':  # состояние проверки на оператор присваивания
            token_type = 'assignment operator'
            if current_char == '=':
                token = token.strip()
                state = 'f'
            else:  # если не оператор присваивания - ошибка
                state = 'g'
            continue

        elif state == 'e':  # состояние проверки на комментарий
            if current_char != '#':
                state = 'e'
            else:
                out_list.append((token[:-1].strip(), token_type))
                state = 'a'
                token = ''
            continue

        elif state == 'g':  # состояние для выделения неизвестных лексем
            out_list.append((token[:-1].strip(), token_type))
            token_type = 'error'
            state = 'a'
            i -= 1
            token = ''
            continue

        # ниже последнее состояние, здесь выводится результат анализа типа лексемы
        # если это не ошибка и не комментарий
        if state == 'f':
            if token.strip() != '':
                out_list.append((token[:-1].strip(), token_type))
            state = 'a'
            i -= 1
            token = ''


def read_file():
    out_list.clear()
    file = open('text.txt')  # открываем файл
    # ниже читаю файл построчно
    for string in file:
        read(string)
    # затем закрываю файл после проведенного анализа
    file.close()
    return out_list


def read_first():
    with open('text.txt', 'r') as file:  # открываем файл
        first_string = file.readline()
    # затем закрываю файл после проведенного анализа
    return first_string
