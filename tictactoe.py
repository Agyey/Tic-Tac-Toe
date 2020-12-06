import random

# Display Table
def display_table(table):
    print('---------')
    print('|', " ".join(table[:3]), '|')
    print('|', " ".join(table[3:6]), '|')
    print('|', " ".join(table[6:]), '|')
    print('---------')


# Get Coordinates from user if move is valid
def next_move(table):
    valid_move = False
    while not valid_move:
        try:
            x, y = map(int, input('Enter the coordinates:').strip().split())
            valid_move = True
        except:
            print('You should enter numbers!')
            valid_move = False
        if valid_move:
            if 0 < x < 4 and 0 < y < 4:
                if table[x - 1 + (3 - y) * 3] != ' ':
                    print('This cell is occupied! Choose another one!')
                    valid_move = False
                else:
                    valid_move = True
            else:
                print('Coordinates should be from 1 to 3!')
                valid_move = False
    return x, y


# Check Win Status
def winner(table):
    # Top Left Corner
    if table[0] == table[1] and table[1] == table[2]:
        return table[0]
    elif table[0] == table[4] and table[4] == table[8]:
        return table[0]
    elif table[0] == table[3] and table[3] == table[6]:
        return table[0]
    # Top Middle
    elif table[1] == table[4] and table[4] == table[7]:
        return table[1]
    # Top Right Corner
    elif table[2] == table[5] and table[5] == table[8]:
        return table[2]
    elif table[2] == table[4] and table[4] == table[6]:
        return table[2]
    # Middle Left
    elif table[3] == table[4] and table[4] == table[5]:
        return table[3]
    # Bottom Left
    elif table[6] == table[7] and table[7] == table[8]:
        return table[6]
    else:
        return ' '


# Easy Mode (Random Move)
def easy_move(table):
    valid_move = False
    while not valid_move:
        x = random.randint(1, 3)
        y = random.randint(1, 3)
        if table[x - 1 + (3 - y) * 3] != ' ':
            valid_move = False
        else:
            valid_move = True
    return x, y


# Medium Mode (If win or block in one move then do it else random)
def medium_move(table):
    # Top Left Corner
    if table[:3].count(' ') == 1 and (table[:3].count('X') == 2 or table[:3].count('O') == 2):
        return table[:3].index(' ')+1, 3
    elif table[::4].count(' ') == 1 and (table[::4].count('X') == 2 or table[::4].count('O') == 2):
        return table[::4].index(' ') + 1, 3 - table[::4].index(' ')
    elif table[::3].count(' ') == 1 and (table[::3].count('X') == 2 or table[::3].count('O') == 2):
        return 1, 3 - table[::3].index(' ')
    # Top Middle
    elif table[1::3].count(' ') == 1 and (table[1::3].count('X') == 2 or table[1::3].count('O') == 2):
        return 2, 3 - table[1::3].index(' ')
    # Top Right Corner
    elif table[2::3].count(' ') == 1 and (table[2::3].count('X') == 2 or table[2::3].count('O') == 2):
        return 3, 3 - table[2::3].index(' ')
    elif table[2::2].count(' ') == 1 and (table[2::2].count('X') == 2 or table[2::2].count('O') == 2):
        return 3 - table[2::2].index(' '), 3 - table[2::2].index(' ')
    # Middle Left
    elif table[3:6].count(' ') == 1 and (table[3:6].count('X') == 2 or table[3:6].count('O') == 2):
        return table[3:6].index(' ') + 1, 2
    # Bottom Left
    elif table[6:9].count(' ') == 1 and (table[6:9].count('X') == 2 or table[6:9].count('O') == 2):
        return table[6:9].index(' ') + 2, 1
    else:
        return easy_move(table)


# Best Move Possible
def best_move(table, ai):
    moves = list()
    player = 'X' if table.count('X') == table.count('O') else 'O'
    if table.count(' ') == 0:
        if winner(table) == ai:
            return {'score': 10}
        elif winner(table) == ' ':
            return {'score': 0}
        else:
            return {'score': -10}
    for position in range(len(table)):
        # If position is not occupied
        if table[position] not in ['X', 'O']:
            # Set move position
            move = dict()
            move['position'] = position
            # Set current position to Player's Mark
            table[position] = player
            # Call hard_move on the current position
            move['score'] = best_move(table, ai)['score']
            # Reset table
            table[position] = ' '
            moves.append(move)
    if player == ai:
        return max(moves, key=lambda x: x['score'])
    else:
        return max(moves, key=lambda x: -x['score'])


# Hard Mode (Tries to Win Everytime)
def hard_move(table):
    ai = 'X' if table.count('X') == table.count('O') else 'O'
    index = best_move(table, ai)['position']
    return index % 3 + 1, 3 - index // 3


# Initialisation
starting_condition = "_________"
x_moves = starting_condition.lower().count('x')
o_moves = starting_condition.lower().count('o')
moves = starting_condition.lower().count('_')
command = ''
x = 'easy'
o = 'easy'

# Ask user to start
while command != 'exit':
    command = input('Input command: ')
    if command == 'exit':
        break
    elif command.startswith('start'):
        try:
            x_player, o_player = command.split()[-2:]
        except:
            print('Bad parameters!')
            continue
        options = {
            'user': next_move,
            'easy': easy_move,
            'medium': medium_move,
            'hard': hard_move}
        if x_player not in options or o_player not in options:
            print('Bad parameters!')
            continue
    else:
        print('Bad parameters!')
        continue
    table = list(starting_condition.replace('_',' '))
    display_table(table)
    first_move = options[x_player]
    second_move = options[o_player]
    while moves and winner(table) == ' ':
        # X's Move
        curr = 'X'
        x, y = first_move(table)
        table[x - 1 + (3 - y) * 3] = curr
        if x_player != 'user':
            print(f'Making move level "{x_player}"')
        display_table(table)
        moves -= 1
        # O's Move
        if moves and winner(table) == ' ':
            curr = 'O'
            x, y = second_move(table)
            table[x - 1 + (3 - y) * 3] = curr
            if o_player != 'user':
                print(f'Making move level "{o_player}"')
            display_table(table)
            moves -= 1
    win = winner(table)
    if win != ' ':
        print(f'{win} wins')
    elif moves == 0:
        print('Draw')
    else:
        print('Game not finished')
    break

