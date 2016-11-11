from other import *


class Human:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.move_cooldown = 0
        self.shoot_cooldown = 0


    
    def try_move(self, command):
        flag = True
        if command == 'w':
            for x in range(self.x, self.x + game.consts.body_length):
                if game.field[x][self.y - 1] != 0:
                    flag = False
            for i in range(game.consts.players):
                if game.humans[i].id != self.id:
                    if game.humans[i].y == self.y - game.consts.body_length:
                        if self.x <= game.humans[i].x < self.x + game.consts.body_length:
                            flag = False
            if flag:
                self.y -= 1
        if command == 's':
            for x in range(self.x, self.x + game.consts.body_length):
                if game.field[x][self.y + game.consts.body_length] != 0:
                    flag = False
            for i in range(game.consts.players):
                if game.humans[i].id != self.id:
                    if game.humans[i].y == self.y + game.consts.body_length:
                        if self.x <= game.humans[i].x < self.x + game.consts.body_length:
                            flag = False
            if flag:
                self.y += 1
        if command == 'a':
            for y in range(self.y, self.y + game.consts.body_length):
                if game.field[self.x - 1][y] != 0:
                    flag = False
            for i in range(game.consts.players):
                if game.humans[i].id != self.id:
                    if game.humans[i].x == self.x - game.consts.body_length:
                        if self.y <= game.humans[i].y < self.y + game.consts.body_length:
                            flag = False
            if flag:
                self.x -= 1
        if command == 'd':
            for y in range(self.y, self.y + game.consts.body_length):
                if game.field[self.x + game.consts.body_length][y] != 0:
                    flag = False
            for i in range(game.consts.players):
                if game.humans[i].id != self.id:
                    if game.humans[i].x == self.x + game.consts.body_length:
                        if self.y <= game.humans[i].y < self.y + game.consts.body_length:
                            flag = False
            if flag:
                self.x += 1
        return flag

    
    def do_move(self, commands, is_fire, cursour):
        self.move_cooldown = max(0, self.move_cooldown - 1)
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        new_bullets = dict()
        if self.shoot_cooldown == 0 and is_fire:
            game.bullets[game.curid] = Bullet(self.x, self.y, cursour.x, cursour.y, self.id)
            new_bullets[game.curid] = [self.x, self.y, cursour.x, cursour.y]
            self.shoot_cooldown = game.consts.shoot_cooldown
        move = []
        if self.move_cooldown == 0:
            if len(commands) != 0:
                for command in commands:
                    if self.try_move(command):
                        move.append(command)    
                self.move_cooldown = game.consts.move_cooldown
        return move, new_bullets


class Bullet:
    def __init__(self, x, y, vector_x, vector_y, curid, creator_id):
        self.x = x
        self.y = y
        self.id = curid
        self.creator_id = creator_id
        self.vector = Vector(vector_x, vector_y).normed()
        self.move_cooldown = 0
        self.line = Line(x, y, x + vector_x, y + vector_y)
        self.kinetic = game.consts.bullet_maxenergy


    def first_crossed(self):
        if self.vector.x < 0:
            indexacya = -1
        else:
            indexacya = 1
        for square in self.line.crossing_squares[::indexacya]:
            if (square.x + 1 <= self.x) and self.vector.x >= 0:
                continue
            if (square.x >= self.x) and self.vector.x <= 0:
                continue
            if game.field[square.x][square.y] != 0:
                if self.x < square.x or self.x > square.x + 1 or self.y < square.y or self.y > square.y + 1:
                    return square
                else:
                    continue
        return None


    def first_crossed_point(self):
        pts = self.line.cross_square(self.first_crossed(), self.first_crossed() + Vector(1, 1))
        if len(pts) == 0:
            return None
        ans = pts[0]
        mn = Vector(self.x, self.y).dist2(pts[0])
        for point in pts:
            if mn > Vector(self.x, self.y).dist2(point):
                mn = Vector(self.x, self.y).dist2(point)
                ans = point
        return ans
    def is_int(self, x):
        return (abs(x - int(x)) <= game.consts.eps)

    def vector_change_on_move(self):
        pt = self.first_crossed_point()
        if self.is_int(pt.x):
            return Vector(-self.vector.x, self.vector.y)
        else:
            return Vector(self.vector.x, -self.vector.y)

    def kinetic_cost(self, x1, y1, x2, y2):
        return (Vector(x2, y2) - Vector(x1, y1)).len() / game.consts.bullet_speed * game.consts.bullet_flycost

    def time_cost(self, x1, y1, x2, y2):
        return (Vector(x2, y2) - Vector(x1, y1)).len() / game.consts.bullet_speed

    def kinetic_move(self):
        return self.vector * (self.kinetic / game.consts.bullet_flycost * game.consts.bullet_speed / self.vector.len())

    def time_move(self, time): #time in ticks
        return self.vector * (time * game.consts.bullet_speed)

    def do_move(self, remaning_time): #time in ticks
        point_crossed_with_squares = self.first_crossed_point()
        kinetic_cost = self.kinetic_cost(self.x, self.y, point_crossed_with_squares.x, point_crossed_with_squares.y)
        time_cost = self.time_cost(self.x, self.y, point_crossed_with_squares.x, point_crossed_with_squares.y)
        if self.kinetic < kinetic_cost:
            #bullet is destroyed
            return [self.kinetic_move() + Vector(self.x, self.y)]
        if remaning_time < time_cost:
            #bullet continue moving next
            ans = [Vector(self.x, self.y) + self.time_move(remaning_time)]
            self.x += self.time_move(remaning_time).x
            self.y += self.time_move(remaning_time).y
            self.kinetic -= kinetic_cost
            return ans
        self.kinetic -= kinetic_cost
        remaning_time -= time_cost
        bullet_change_move = self.vector_change_on_move()
        self.x = point_crossed_with_squares.x
        self.y = point_crossed_with_squares.y
        if self.kinetic < game.consts.bullet_ricochet_cost:
            #bullet is destroyed
            return [Vector(self.x, self.y)]
        self.vector = bullet_change_move
        self.line = Line(self.x, self.y, self.x + self.vector.x, self.y + self.vector.y)
        curx = self.x
        cury = self.y
        pts = self.do_move(remaning_time) + [Vector(curx, cury)]
        return pts
            
class Game:
    def __init__(self, players = 2, field = [[2 * ((j == 0) or (i == 0)) for j in range((Consts().width))] for i in range(Consts().length)]):
        self.consts = Consts(players)
        self.field = field #0 is free, 1 is breakable, 2 is unbreakable(ricochet wall)
        self.humans = []
        self.bullets = dict()
        self.curid = 0
        for i in range(self.consts.players):
            self.humans.append(Human(self.consts.resp[i][0], self.consts.resp[i][1], i))


    def do_tick(self, commands, is_fire, cursour):
        cursour = Vector(cursour[0], cursour[1])
        commands, is_fire, cursour = convert_input(commands, is_fire, cursour)
        answer = ans_init()
        commands, is_fire, cursour = transform_input(commands, is_fire, cursour)
        for i in range(self.consts.players):
            ans_move, new_bullets = self.humans[i].do_move(commands[i], is_fire[i], cursour)
            answer['humans'][i]['move'] = ans_move
            for cur_id in new_bullets:
                answer['bullets'][cur_id]['is_resp'] = True
        for bullet in self.bullets:
            pts = bullet.do_move(1)
            answer['bullets'][bullet.id]['pos'] = Vector(bullet.x, bullet.y)
            answer['bullets'][bullet.id]['direction'] = bullet.vector
            answer['bullets'][bullet.id]['pts'] = pts[::-1]
            if not ('is_resp' in answer['bullets'][bullet.id]):
                answer['bullets'][bullet.id] = False
        answer['consts'] = game.consts
        return transform_ans(answer)
    
            


game = Game()
