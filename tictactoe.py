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
        if x_player not in ['user', 'easy'] or o_player not in ['user', 'easy']:
            print('Bad parameters!')
            continue
    else:
        print('Bad parameters!')
        continue
    table = list(starting_condition.replace('_',' '))
    display_table(table)
    first_move = next_move if x_player == 'user' else easy_move
    second_move = next_move if o_player == 'user' else easy_move
    while moves and winner(table) == ' ':
        # X's Move
        curr = 'X'
        x, y = first_move(table)
        table[x - 1 + (3 - y) * 3] = curr
        if x_player == 'easy':
            print('Making move level "easy"')
        display_table(table)
        moves -= 1
        # O's Move
        if moves and winner(table) == ' ':
            curr = 'O'
            x, y = second_move(table)
            table[x - 1 + (3 - y) * 3] = curr
            if o_player == 'easy':
                print('Making move level "easy"')
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

