import consts


class Snake:

    dx = {'UP': 0, 'DOWN': 0, 'LEFT': -1, 'RIGHT': 1}
    dy = {'UP': -1, 'DOWN': 1, 'LEFT': 0, 'RIGHT': 0}

    def __init__(self, game, pos, color, direction):
        self.cells = [pos]
        self.game = game
        self.game.snake = self
        self.color = color
        self.direction = direction
        self.game.get_cell(pos).set_color(color)

    def get_head(self):
        return self.cells[-1]
    def kill(self):
        for cell in self.cells:
            self.game.get_cell(cell).set_color(consts.back_color)
