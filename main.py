from functions import fig_choice, first_choice, players_turn, clear_board


def main():
    clear_board()
    player1, player2 = fig_choice()
    player1, player2 = first_choice(player1, player2)

    is_playing = True
    while is_playing:
        if players_turn(player1):
            if players_turn(player2):
                continue
            else:
                is_playing = False
        else:
            is_playing = False

    print('Игра окончена')
    new_game = input('Повторим? Напиши y для новой игры или n чтобы закончить: ')
    if new_game == 'y':
        main()
    else:
        print('Пока')
        return 0


if __name__ == '__main__':
    main()
