from random import random

def all_neighboring_positions(pos):
    col, row = pos

    return [
        (col - 1, row - 1),
        (col - 1, row),
        (col - 1, row + 1),
        (col, row + 1),
        (col, row - 1),
        (col + 1, row - 1),
        (col + 1, row),
        (col + 1, row + 1)
    ]

def cardinal_neighboring_positions(pos):
    col, row = pos

    return [
        (col - 1, row),
        (col, row + 1),
        (col, row - 1),
        (col + 1, row),
    ]

class Cell(object):
    """docstring for Cell"""
    def __init__(self):
        super(Cell, self).__init__()

        self.shown = False

        self.is_mine = False
        self.mine_count = 0

        self.flagged = False

    def pr(self):
        return '*' if self.is_mine else str(self.mine_count)

    def __str__(self):
        if not self.shown and self.flagged:
            return 'F'
        elif not self.shown:
            return ' '
        elif self.is_mine:
            return '*'
        elif self.mine_count > 0:
            return str(self.mine_count)
        else:
            return '-'

    def __repr__(self):
        return repr(str(self))

class Board(object):
    """docstring for Board"""
    def __init__(self, size):
        super(Board, self).__init__()
        self.size = size
        self.mine_count = 0
        self.cells = []

        for row in range(size):
            row_cells = []
            for col in range(size):
                cell = Cell()

                cell.is_mine = random() > .9
                cell.shown = False

                if cell.is_mine:
                    self.mine_count += 1

                row_cells.append(cell)

            self.cells.append(row_cells)

        for col in range(self.size):
            for row in range(self.size):
                neighbors = all_neighboring_positions((col, row))

                # check how many neighbors are mines
                for neighbor in neighbors:
                    if (neighbor[0] < 0 or neighbor[0] >= self.size
                        or neighbor[1] < 0 or neighbor[1] >= self.size):
                        continue

                    if self.cells[neighbor[0]][neighbor[1]].is_mine:
                        self.cells[col][row].mine_count += 1



    def __str__(self):
        string = ''
        sep = '+-----'
        sep2 = '+====='

        for col_idx in range(self.size):
            sep += '+---'

        for col_idx in range(self.size):
            sep2 += '+==='

        sep += '+\n'
        sep2 += '+\n'

        string += sep

        for col_idx in range(self.size + 1):
            string += '| ' + ('   ' if col_idx == 0 else str(col_idx)) + ' '

        string += '|\n'

        string += sep2

        for row_idx in range(self.size + 1):
            if row_idx == 0:
                continue

            row_string = ''

            for col_idx in range(self.size + 1):
                if col_idx == 0:
                    row_string += '| ' + str(row_idx) + ('  |' if row_idx < 10 else ' |')
                else:
                    row_string += '| ' + str(self.cells[row_idx - 1][col_idx - 1]) + ' '
                    


            string += row_string + '|\n' + sep

        return string

    def show_neighbors(self, pos):
        self.cells[pos[1]][pos[0]].shown = True

        to_visit = all_neighboring_positions(pos)
        visited = [pos]

        while len(to_visit) > 0:
            next_pos = to_visit[0]
            to_visit = to_visit[1:]

            if (next_pos[0] < 0 or next_pos[0] >= self.size or
                next_pos[1] < 0 or next_pos[1] >= self.size):
                continue

            visited.append(next_pos)

            self.cells[next_pos[1]][next_pos[0]].shown = True

            if self.cells[next_pos[1]][next_pos[0]].mine_count == 0:
                for n in all_neighboring_positions(next_pos):
                    if n not in visited:
                        to_visit.append(n)



class Game(object):
    """docstring for Game"""
    def __init__(self):
        super(Game, self).__init__()
        
        self.board = Board(10)
        self.game_over = False

    def move(self, mv):
        parts = mv.split(' ')
        col = int(parts[1]) - 1
        row = int(parts[2]) - 1

        if parts[0] == 'u':
            self.board.cells[row][col].shown = True

            if self.board.cells[row][col].is_mine:
                self.game_over = True

            if self.board.cells[row][col].mine_count == 0:
                self.board.show_neighbors((col, row))


        elif parts[0] == 'f':
            self.board.cells[row][col].flagged = True

    def won(self):
        for row in self.board.cells:
            for cell in row:
                if cell.is_mine and not cell.flagged:
                    return False

        return True


    def run(self):
        while not self.game_over:
            for c in self.board.cells:
                r = ''
                for cell in c:
                    r += cell.pr() + ' '
                print r

            print self.board

            move = raw_input('--> ')
            self.move(move)

            if self.won():
                self.game_over = True
                print 'YOU WON'
                return

        print 'YOU LOST'


def main():
    g = Game()
    g.run()

    # b = Board(10)
    # print b


if __name__ == '__main__':
    main()
        