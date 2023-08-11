from termcolor import colored as clr
from random import randint, choice
from time import sleep

N = 3

class Board:
    def __init__(self):
        self.player_turn = 'X'
        self.states = [['.' for _ in range(N)] for _ in range(N)]
        self.indices = [(j, i) for j in range(N) for i in range(N)]

        self.val = (4 * N) + (N - 1)
        print('=' * self.val)
        print(f'{"TIC TAC TOE": ^{self.val}}')
        print('=' * self.val)
        if N > 3:
            print(f'{"1. EASY | 2. HARD": ^{self.val}}')
        else:
            print(f'{"EASY | HARD": ^{self.val}}')
        print('=' * self.val)

    def draw_board(self, move_coords, win_coords):
        num = 1
        for i in range(N):
            print(' ', end='')
            for j in range(N):
                val = self.states[i][j]
                if win_coords and (i, j) in win_coords:
                    print(clr(f' {val:2}', 'cyan'), end='')
                elif (i, j) == move_coords:
                    print(clr(f' {val:2}', 'yellow'), end='')
                else:
                    if val == 'X':
                        print(clr(f' {val:2}', 'green'), end='')
                    elif val == 'O':
                        print(clr(f' {val:2}', 'red'), end='')
                    else:
                        print(clr(f'{num:2} ', 'magenta'), end='')

                num += 1
                if j < N - 1: print('| ', end='')

            print('\n' + '|'.join(['----'] * N) if i < N - 1 else '')
        print()

    def all_marked(self, marked):
        if marked == ['X'] * N: return 'X'
        if marked == ['O'] * N: return 'O'

        return None

    def eval(self, term):
        winning_possibility = 0

        for i in range(N):
            if term not in self.states[i]:
                winning_possibility += 1

            if term not in [self.states[j][i] for j in range(N)]:
                winning_possibility += 1

        if term not in [self.states[i][i] for i in range(N)]:
            winning_possibility += 1

        if term not in [self.states[i][N - 1 - i] for i in range(N)]:
            winning_possibility += 1

        return winning_possibility

    def better_AI_move(self, vals):
        return vals.count('.') and 'X' not in vals and vals.count('O') >= N // 2

    def possible_won(self):
        better_move = None

        for i in range(N):
            vals = self.states[i]
            if vals.count('.') and vals.count('X') == N - 1:
                return i, vals.index('.')
            if self.better_AI_move(vals):
                better_move = i, vals.index('.')

            vals = [self.states[j][i] for j in range(N)]
            if vals.count('.') and vals.count('X') == N - 1:
                return vals.index('.'), i
            if self.better_AI_move(vals):
                better_move = i, vals.index('.')

        vals = [self.states[i][i] for i in range(N)]
        if vals.count('.') and vals.count('X') == N - 1:
            i = vals.index('.')
            return i, i
        if self.better_AI_move(vals):
            i = vals.index('.')
            better_move = i, i

        vals = [self.states[i][N - 1 - i] for i in range(N)]
        if vals.count('.') and (vals.count('X') == N - 1):
            i = vals.index('.')
            return i, N - 1 - i
        if self.better_AI_move(vals):
            i = vals.index('.')
            better_move = i, N - 1 - i

        return better_move

    def check_winner(self):
        for i in range(N):
            val = self.all_marked(self.states[i])
            if val: return val, [(i, j) for j in range(N)]

            val = self.all_marked([self.states[j][i] for j in range(N)])
            if val: return val, [(j, i) for j in range(N)]

        val = self.all_marked([self.states[i][i] for i in range(N)])
        if val: return val, [(i, i) for i in range(N)]

        val = self.all_marked([self.states[i][N - 1 - i] for i in range(N)])
        if val: return val, [(i, N - 1 - i) for i in range(N)]

        for row in self.states:
            if '.' in row: return None, None

        return '.', None

class AlphaBeta:
    def max_ab(self, alpha, beta):
        result, _ = self.check_winner()
        if result: return self.outcomes[result]

        max_val = alpha
        x, y = None, None

        for i in range(N):
            for j in range(N):
                if self.states[i][j] == '.':
                    self.states[i][j] = 'X'
                    val, _, _ = self.min_ab(alpha, beta)
                    self.states[i][j] = '.'

                    if val > max_val:
                        max_val = val
                        x, y = i, j

                    if max_val >= beta:
                        return max_val, x, y

                    alpha = max(max_val, alpha)

        return max_val, x, y

    def min_ab(self, alpha, beta):
        result, _ = self.check_winner()
        if result: return self.outcomes[result]

        min_val = beta
        x, y = None, None

        for i in range(N):
            for j in range(N):
                if self.states[i][j] == '.':
                    self.states[i][j] = 'O'
                    val, _, _ = self.max_ab(alpha, beta)
                    self.states[i][j] = '.'

                    if val < min_val:
                        min_val = val
                        x, y = i, j

                    if min_val <= alpha:
                        return min_val, x, y

                    beta = min(min_val, beta)

        return min_val, x, y


class Game(Board, AlphaBeta):
    def __init__(self):
        super().__init__()
        self.steps = 0
        self.is_easy = False

        self.outcomes = {
            '.': (0, 0, 0),
            'X': (1, 0, 0),
            'O': (-1, 0, 0)
        }

        self.end_msg = {
            'X': 'YOU WON! 😀',
            'O': 'AI WON! 🤖',
            '.': 'TIE! 😐'
        }

    def estimated_move(self):
        coords = self.possible_won()
        if coords and choice([True, False, True]):
            return coords

        if self.is_easy and choice([True, False]):
            while True:
                x, y = self.indices[randint(1, N * N) - 1]
                if self.states[x][y] != '.': continue
                return x, y

        move = None
        for i in range(N):
            for j in range(N):
                if self.states[i][j] != '.': continue

                self.states[i][j] = 'O'
                e = self.eval('O') - self.eval('X')
                move = min(move, (e, (i, j))) if move else (e, (i, j))
                self.states[i][j] = '.'

        return move[1]

    def should_estimate(self):
        return self.steps <= (N * N) - 10 or (self.is_easy and choice([True, False]))

    def play(self):
        move_coords = (None, None)
        while True:
            winner, win_coords = self.check_winner()
            self.draw_board(move_coords, win_coords)

            if winner:
                sleep(0.5)
                print('-' * self.val)
                print(f'{f"{self.end_msg[winner]}": ^{self.val}}')
                print('-' * self.val)
                return

            if self.player_turn == 'X':
                while True:
                    try:
                        x, y = self.indices[int(input('Your move: ')) - 1]
                        if self.states[x][y] != '.': raise IndexError

                        self.states[x][y] = 'X'
                        self.player_turn = 'O'
                        break
                    except (ValueError, IndexError):
                        print(clr('Invalid move! Try again.', 'red'))
                    except KeyboardInterrupt:
                        print('Quit\n' + '-' * self.val)
                        print(f'{"LOSER!!😅": ^{self.val}}')
                        print('-' * self.val)
                        raise SystemExit
                    except SystemExit:
                        pass
            else:
                sleep(0.5)
                if self.should_estimate():
                    x, y = self.estimated_move()
                    print('Estimated', end=' ')
                else:
                    print('Evaluated', end=' ')
                    _, x, y = self.min_ab(-100, 100)

                self.states[x][y] = 'O'
                self.player_turn = 'X'
                print('AI move:')

            move_coords = (x, y)
            self.steps += 1


if __name__ == "__main__":
    g = Game()
    if input('Select mode: ').lower() in ['1', 'easy']:
        g.is_easy = True
        print('Mode:', clr('Easy\n', 'green'))
    else:
        print('Mode:', clr('Hard\n', 'red'))
    g.play()
