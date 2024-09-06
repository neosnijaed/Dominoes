import random
import operator


# return a full domino set. Each domino is represented as a list of two numbers. A full domino set is a list of 28
# unique dominoes.
def generate_domino_set() -> list[list[int]]:
    return [[i, j] for i in range(7) for j in range(i, 7)]


# split the full domino set between the players and the stock by random
def split_dominos(domino_set: list[list[int]]) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    stock_pieces = domino_set[:14]
    computer_pieces = domino_set[14:21]
    player_pieces = domino_set[21:]
    return stock_pieces, computer_pieces, player_pieces


# determine the starting piece and who starts first
def determine_starting_domino(computer_pieces: list[list[int]], player_pieces: list[list[int]]) \
        -> tuple[str, list[list[int]]]:
    highest_double = max(max(computer_pieces), max(player_pieces))
    if highest_double[0] == highest_double[1]:
        if highest_double in computer_pieces:
            computer_pieces.remove(highest_double)
            status = 'player'
        else:
            player_pieces.remove(highest_double)
            status = 'computer'
        # double_snake is in nested list which becomes longer with more dominos as lists; datatype: list[list[int]]
        double_snake = [highest_double]
    else:
        status = None
        double_snake = None

    return status, double_snake


def verify_legal_domino(domino_index: int, domino_snake: list[list[int]], computer_pieces: list[list[int]],
                        player_pieces: list[list[int]], status: str):
    if domino_index > 0 and status == 'player':
        for num in player_pieces[domino_index - 1]:
            if num == domino_snake[-1][1]:
                return True
        return False
    if domino_index < 0 and status == 'player':
        for num in player_pieces[abs(domino_index) - 1]:
            if num == domino_snake[0][0]:
                return True
        return False
    if status == 'computer' and domino_index > 0:
        for num in computer_pieces[domino_index - 1]:
            if num == domino_snake[-1][1]:
                return True
        return False
    if status == 'computer' and domino_index < 0:
        for num in computer_pieces[abs(domino_index) - 1]:
            if num == domino_snake[0][0]:
                return True
        return False


def calculate_computer_domino(computer_pieces: list[list[int]], domino_snake: list[list[int]]) \
        -> dict[tuple[int, int], int]:
    # count numbers in dominos of computer and snake
    computer_snake_pieces = computer_pieces + domino_snake
    num_count = dict.fromkeys([0, 1, 2, 3, 4, 5, 6], 0)
    for domino in computer_snake_pieces:
        num_count[domino[0]] += 1
        num_count[domino[1]] += 1

    # score each computer domino and sort scores from high to low
    score = {(domino[0], domino[1]): num_count[domino[0]] + num_count[domino[1]] for domino in computer_pieces}
    score_sorted = dict(sorted(score.items(), key=operator.itemgetter(1), reverse=True))

    return score_sorted


def determine_valid_input(domino_snake: list[list[int]], computer_pieces: list[list[int]],
                          player_pieces: list[list[int]], status: str) -> int:
    if status == 'player':
        print('\nStatus: It\'s your turn to make a move. Enter your command.')
        while True:
            try:
                domino_index = int(input())
            except ValueError:
                print('Invalid input. Please try again.')
            else:
                if abs(domino_index) > len(player_pieces):
                    print('Invalid input. Please try again.')
                elif verify_legal_domino(domino_index, domino_snake, computer_pieces, player_pieces, status) is False:
                    print('Illegal move. Please try again.')
                else:
                    break
    else:
        print('\nStatus: Computer is about to make a move. Press Enter to continue...')
        while True:
            domino_index = input()
            if domino_index == '':
                computer_scores = calculate_computer_domino(computer_pieces, domino_snake)
                # check if domino fits in the end of the snake
                for domino in computer_scores.keys():
                    if verify_legal_domino(computer_pieces.index(list(domino)) + 1, domino_snake, computer_pieces,
                                           player_pieces, status) is True:
                        return computer_pieces.index(list(domino)) + 1
                # check if domino fits in the beginning of the snake
                for domino in computer_scores.keys():
                    if verify_legal_domino(-computer_pieces.index(list(domino)) - 1, domino_snake, computer_pieces,
                                           player_pieces, status) is True:
                        return -computer_pieces.index(list(domino)) - 1
                # if nothing fits computer shall draw a domino from stock and pass turn; if stock empty just pass turn
                return 0
            else:
                print('Invalid input. Please try again.')

    return domino_index


def orientate_placing_domino(side: str, next_domino: list[int], domino_snake: list[list[int]]):
    if side == 'right' and domino_snake[-1][1] == next_domino[0]:
        return next_domino
    elif side == 'left' and domino_snake[0][0] == next_domino[1]:
        return next_domino
    else:
        num = next_domino[0]
        next_domino[0] = next_domino[1]
        next_domino[1] = num
        return next_domino


def extend_domino_snake(stock_pieces: list[list[int]], domino_snake: list[list[int]], next_piece_index: int,
                        computer_pieces: list[list[int]], player_pieces: list[list[int]], status: str) -> str:
    if status == 'player':
        if next_piece_index > 0:
            next_piece = orientate_placing_domino('right', player_pieces[next_piece_index - 1], domino_snake)
            domino_snake.append(next_piece)
            player_pieces.pop(next_piece_index - 1)
        elif next_piece_index < 0:
            next_piece = orientate_placing_domino('left', player_pieces[abs(next_piece_index) - 1], domino_snake)
            domino_snake.insert(0, next_piece)
            player_pieces.pop(abs(next_piece_index) - 1)
        else:
            if next_piece_index == 0 and len(stock_pieces) == 0:
                return 'computer'
            else:
                player_choice = random.choice(stock_pieces)
                player_pieces.append(player_choice)
                stock_pieces.remove(player_choice)
        return 'computer'
    else:
        if next_piece_index > 0:
            next_piece = orientate_placing_domino('right', computer_pieces[next_piece_index - 1], domino_snake)
            domino_snake.append(next_piece)
            computer_pieces.pop(next_piece_index - 1)
        elif next_piece_index < 0:
            next_piece = orientate_placing_domino('left', computer_pieces[abs(next_piece_index) - 1], domino_snake)
            domino_snake.insert(0, next_piece)
            computer_pieces.pop(abs(next_piece_index) - 1)
        else:
            if next_piece_index == 0 and len(stock_pieces) == 0:
                return 'player'
            else:
                computer_choice = random.choice(stock_pieces)
                computer_pieces.append(computer_choice)
                stock_pieces.remove(computer_choice)
        return 'player'


def print_interface(stock_pieces: list[list[int]], computer_pieces: list[list[int]], player_pieces: list[list[int]],
                    domino_snake: list[list[int]]) -> str:
    print('=' * 70)
    print('Stock size:', len(stock_pieces))
    print('Computer pieces:', len(computer_pieces), '\n')

    # print whole snake if less than 8 dominos; else just 6 dominos with ... inbetween
    if len(domino_snake) < 7:
        for domino in domino_snake:
            print(domino, end='')
    else:
        print(f'{domino_snake[0]}{domino_snake[1]}{domino_snake[2]}...{domino_snake[-3]}{domino_snake[-2]}'
              f'{domino_snake[-1]}', end='')

    print('\n')
    print('Your pieces:')
    for i, player_piece in enumerate(player_pieces):
        print(f'{i + 1}:{player_piece}')

    # game decider
    if len(player_pieces) == 0:
        return 'player won'
    elif len(computer_pieces) == 0:
        return 'computer won'
    # snake begins and ends with same number and this number appears 8 times
    elif domino_snake[0][0] == domino_snake[-1][1]:
        result = 0
        for num in domino_snake:
            result += num.count(domino_snake[0][0])
            if result >= 8:
                return 'draw'
    return 'noone won'


def main() -> None:
    # if computer and player have no doubles continue this loop
    while True:
        all_dominos = generate_domino_set()
        random.shuffle(all_dominos)
        stock_dominos, computer_dominos, player_dominos = split_dominos(all_dominos)
        game_status, domino_snake = determine_starting_domino(computer_dominos, player_dominos)
        if game_status is None and domino_snake is None:
            continue
        else:
            # if game isn't decided continue this loop
            while True:
                who_won = print_interface(stock_dominos, computer_dominos, player_dominos, domino_snake)
                if who_won == 'noone won':
                    next_domino_index = determine_valid_input(domino_snake, computer_dominos, player_dominos,
                                                              game_status)
                    game_status = extend_domino_snake(stock_dominos, domino_snake, next_domino_index, computer_dominos,
                                                      player_dominos, game_status)
                elif who_won == 'computer won':
                    print('Status: The game is over. The computer won!')
                    break
                elif who_won == 'player won':
                    print('\nStatus: The game is over. You won!')
                    break
                elif who_won == 'draw':
                    print('\nStatus: The game is over. It\'s a draw!')
                    break
        break


if __name__ == '__main__':
    main()
