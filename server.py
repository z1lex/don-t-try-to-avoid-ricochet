from other import *


class Human:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.move_cooldown = 0
    def try_move(self, command):
        flag = True
        if command == 'w':
            for x in range(self.x, self.x + game.consts.body_length):
                if game.field[x][self.y - 1] != 0:
                    flag = False
            if flag:
                self.y -= 1
        if command == 's':
            for x in range(self.x, self.x + game.consts.body_length):
                if game.field[x][self.y + game.consts.body_length] != 0:
                    flag = False
            if flag:
                self.y += 1
        if command == 'a':
            for y in range(self.y, self.y + game.consts.body_length):
                if game.field[self.x - 1][y] != 0:
                    flag = False
            if flag:
                self.x -= 1
        if command == 'd':
            for y in range(self.y, self.y + game.consts.body_length):
                if game.field[self.x + game.consts.body_length][y] != 0:
                    flag = False
            if flag:
                self.x += 1
        return flag
    def do_move(self, commands):
        move = []
        if self.move_cooldown == 0:
            if len(commands) != 0:
                for command in commands:
                    if self.try_move(command):
                        move.append(command)    
                self.move_cooldown = game.consts.move_cooldown
        else:
            self.move_cooldown -= 1
        return move
class Game:
    def __init__(self, players = 2, field = [[0 for j in range(20)] for i in range(20)]):
        self.consts = Consts(players)
        self.field = field
        self.humans = []
        for i in range(self.consts.players):
            self.humans.append(Human(self.consts.resp[i][0], self.consts.resp[i][1], i))
    def do_tick(self, commands):
        answer = ans_init()
        for i in range(self.consts.players):
            answer['humans'][i]['move'] = self.humans[i].do_move(commands[i])
        return answer
    
            


game = Game()
