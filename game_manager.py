import consts,pygame
from cell import Cell
from snake import Snake
import numpy as np
class GameManager:

    def __init__(self, size, sx, sy, block_cells,keys):
        pygame.init()
        pygame.display.set_caption("SnakeGame DLR")
        self.screen = pygame.display.set_mode((consts.height, consts.width))
        self.screen.fill(consts.back_color)
        self.size = size
        self.cells = []
        self.sx = sx
        self.sy = sy
        self.keys = keys
        self.n_fruits = 0
        self.fruit_pos = [5,6]
        self.frame_iteration = 0
        self.score = 0
        self.game_over = False
        for i in range(self.size):
            tmp = []
            for j in range(self.size):
                tmp.append(Cell(self.screen, sx + i * consts.cell_size, sy + j * consts.cell_size))
            self.cells.append(tmp)
        for cell in block_cells:
            self.get_cell(cell).set_color(consts.block_color)

        self.snake = Snake(self, (consts.snake['sx'], consts.snake['sy']), consts.snake['color'], consts.snake['direction'])
    def get_cell(self, pos):
        try:
            return self.cells[pos[0]][pos[1]]
        except:
            return None

    
    def reset(self):
        self.score = 0
        self.frame_iteration = 0
        self.snake = Snake(self, (consts.snake['sx'], consts.snake['sy']), consts.snake['color'], consts.snake['direction'])

    def kill(self):
        self.snake.kill()
        self.game_over = True
        self.reset(self)

    def get_next_fruit_pos(self): # returns tuple (x, y) that is the fruit location
        ret = -1, -1
        mx = -100

        for i in range(0, self.size):
            for j in range(0, self.size):

                mn = 100000000

                for x in range(0, self.size):
                    for y in range(0, self.size):
                        if self.get_cell((x, y)).color != consts.back_color:
                            mn = min(mn, int( abs(x-i) + abs(y-j) ))


                if mn > mx:
                    mx = mn
                    ret = i, j
        rand_x, rand_y = np.random.randint(self.size), np.random.randint(self.size)
        final_fruit_pos = int((rand_x + ret[0])/2) , int((rand_y + ret[1])/2)
        print("FRUIT:", final_fruit_pos)
        return final_fruit_pos
    def _rev_direction(self,direction):
        if(direction == "UP"):
            return "DOWN"
        elif(direction == "DOWN"):
            return "UP"
        elif(direction == "LEFT"):
            return "RIGHT"
        elif(direction == "RIGHT"):
            return "LEFT"
    #handles fruit spawning and snake movement
    def handle_action(self, action):
        if(self.frame_iteration > 10000):
            self.snake.kill()
            self.reset()
        if action == ord("U"):
            action = "UP"
        if action == ord("D"):
            action = "DOWN"
        if action == ord("L"):
            action = "LEFT"
        if action == ord("R"):
            action = "RIGHT"
        print("action:" , action)
        if(self.snake.direction != self._rev_direction(action)):
            self.snake.direction = action
        reward, game_over, score = self.next_move()
        self.frame_iteration += 1
        if(self.frame_iteration % 10 == 0 and self.n_fruits<1 ):
            fruit_pos = self.get_next_fruit_pos()
            self.get_cell(fruit_pos).set_color(consts.fruit_color)
            self.n_fruits += 1
            self.fruit_pos = fruit_pos
        
        return reward, game_over, score
    def val(self, x):
            if x < 0:
                x += self.size

            if x >= self.size:
                x -= self.size

            return x
    def next_move(self):
        next_cell = list()
        #finding next cell
        if self.snake.direction == "UP":
            next_cell = [self.snake.get_head()[0] , self.snake.get_head()[1] - 1]
        elif self.snake.direction == "DOWN":
            next_cell = [self.snake.get_head()[0] , self.snake.get_head()[1] + 1]
        elif self.snake.direction == "LEFT":
            next_cell = [self.snake.get_head()[0] - 1 , self.snake.get_head()[1]]
        elif self.snake.direction == "RIGHT":
            next_cell = [self.snake.get_head()[0] + 1, self.snake.get_head()[1]]
        next_cell[0] = self.val(next_cell[0])
        next_cell[1] = self.val(next_cell[1])
        next_cell_color = self.get_cell(tuple(next_cell)).color
        if next_cell_color == consts.back_color:
            self.get_cell(self.snake.cells[0]).set_color(consts.back_color)
            self.snake.cells.pop(0)
            self.snake.cells.append(tuple(next_cell))
            self.get_cell(self.snake.cells[-1]).set_color(self.snake.color)
            return 0, False, self.score
            
        elif next_cell_color == consts.fruit_color:
            self.snake.cells.append(tuple(next_cell))
            self.n_fruits -= 1
            self.score += 1
            self.get_cell(self.snake.cells[-1]).set_color(self.snake.color)
            return 10, False, self.score
        else:
            self.snake.kill()
            return -10, True, self.score

