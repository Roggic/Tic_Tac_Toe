import numpy as np
import subprocess

# board = [[' ', ' ', ' '],
#          [' ', ' ', ' '],
#          [' ', ' ', ' ']]

board_pic, board_num = [['']], [[0]]


def players_turn(player):
    draw_board(board_pic)
    turn_func(player)
    cls()
    is_playing = win_check()
    if not is_playing:
        draw_board(board_pic)
    return is_playing


def clear_board():
    """Пустая доска. board_num для цифр, board_pic для фигур"""
    global board_pic, board_num
    board_p = np.full((3, 3), ' ')
    board_n = np.zeros((3, 3))
    board_pic, board_num = board_p, board_n


def eng_letters(letter):
    """Если ввели русскую букву то меняю на английскую"""
    if letter == 'Х':
        letter = 'X'
    elif letter == 'О':
        letter = 'O'
    return letter


def fig_choice():
    """Выбор фигуры"""
    cls()
    fig = input('Выбери кем будешь ходить.\nНапиши X или O: ').upper()

    fig = eng_letters(fig)

    fig_tuples = {
        'X': ('X', 1),
        'O': ('O', -1)
    }

    player1 = fig_tuples[fig]
    player2 = fig_tuples['O'] if player1[0] == 'X' else fig_tuples['X']
    cls()
    return player1, player2


def first_choice(player1, player2):
    """Выбор кто ходит первым"""
    first_turn = input('Кто ходит первым?\nНапиши X или O: ').upper()
    first_turn = eng_letters(first_turn)
    if first_turn == player2[0]:  # Если первым ходит второй игрок то здесь меняю их местами
        player1, player2 = player2, player1
    return player1, player2


def draw_board(board):
    """Рисует доску в текущем её виде"""
    print('   1 | 2 | 3')
    for i, row in enumerate(board):
        print(f'{i + 1}  {row[0]} | {row[1]} | {row[2]} ')
        print('  -----------')


def turn_func(player):
    """Ход игрока"""
    turn = input(f'Игрок {player[0]}\n'
                 f'Введи координаты куда хочешь сходить: ')

    if not turn:  # Если ввели пусто
        print('Ты ввёл пустые координаты. Ещё раз.')
        turn_func(player)
    else:
        try:
            turn_row, turn_col = int(turn[1]) - 1, int(turn[0]) - 1
        except ValueError:  # Если ввели не число
            print('Координаты должны быть от 1 до 3 для ряда и колонки')
            turn_func(player)
        else:
            # Если введённое число меньше 1 либо больше 3
            if turn_row < 0 or turn_row > 2 or turn_col < 0 or turn_col > 2:
                print('Координаты должны быть от 1 до 3 для ряда и колонки')
                turn_func(player)
            # Если ячейка не свободна
            if board_num[turn_row][turn_col] != 0:
                print('Эти координаты уже заняты, выбери другие')
                turn_func(player)
            else:
                # Если всё ок то заполняем доску ходом игрока
                board_pic[turn_row][turn_col] = player[0]
                board_num[turn_row][turn_col] = player[1]


def win_check():
    """
    Проверка на победу.
    С помощью numpy суммирую по колонкам, рядам и диагоналям.
    Потом проверяю есть ли где-то 3 для победы 'X' либо -3 для победы 'O'
    В случае победы/ничьи возвращает False для переменной is_playing в main() чтобы остановить игру
    """
    axis0 = np.sum(board_num, axis=0)  # Колонки
    axis1 = np.sum(board_num, axis=1)  # Ряды
    diag1 = np.sum(board_num.diagonal())  # Диагональ1
    diag2 = np.sum(np.fliplr(board_num).diagonal())  # Диагональ2

    if np.where(axis0 == 3)[0].size + np.where(axis1 == 3)[0].size + int(diag1 == 3) + int(diag2 == 3) != 0:
        print(f'{color_str("Игрок X выиграл")}')
        return False
    elif np.where(axis0 == -3)[0].size + np.where(axis1 == -3)[0].size + int(diag1 == -3) + int(diag2 == -3) != 0:
        print(f'{color_str("Игрок O выиграл")}')
        return False
    elif 0 not in board_num:
        print(f'{color_str("Ничья")}')
        return False
    else:
        return True


def cls():
    """Очистка экрана"""
    subprocess.call('cls', shell=True)


def color_str(string):
    """Красит строку в зелёный"""
    return f'\033[92m{string}\033[0m'
""