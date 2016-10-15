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
        if self.move_cooldown == 0 and is_fire:
            game.bullets[game.curid] = Bullet(self.x, self.y, cursour.x, cursour.y)
            self.move_cooldown = game.consts.move_cooldown
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


class Bullet:
    def __init__(self, x, y, vector_x, vector_y, curid, creator_id):
        self.x = x
        self.y = y
        self.id = curid
        self.creator_id = creator_id
        self.vector = Vector(vector_x, vector_y)
        self.move_cooldown = 0
        self.line = Line(x, y, x + vector_x, y + vector_y)
        self.kinetic = game.consts.bullet_maxenergy


    def first_crossed(self):
        for square in self.line.crossing_squares:
            if (-self.vector) * (square - (Vector(self.x, self.y) + self.vector)) < 0:
                continue
            if (self.vector) * (square + Vector(1, 1) - (Vector(self.x, self.y))) < 0:
                continue
            if game.field[square.x][square.y] != 0:
                return square


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
    def is_int(x):
        return (abs(x - int(x)) <= game.consts.eps)

    def vector_change_on_move(self):
        pt = self.firstcrossed_point()
        if is_int(pt.x):
            return Vector(-pt.x, pt.y)
        else:
            return Vector(pt.x, -pt.y)

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
        time_cost = self.time_cost(self.x, self.y, points_crossed_with_squares.x, points_crossed_with_squares.y)
        if self.kinetic < kinetic_cost:
            #bullet is destroyed
            return [self.kinetic_move() + Vector(self.x, self.y)]
        if remaning_time < time_cost:
            #bullet is destroyed
            return [self.time_move(remaning_time)]
        self.kinetic -= kinetic_cost
        remaning_time -= time_cost
        bullet_change_move = self.vector_change_move()
        self.x = point_crossed_with_squares.x
        self.y = point_crossed_with_squares.y
        if self.kinetic < game.consts.ricochet_cost:
            #bullet is destroyed
            return [Vector(self.x, self.y)]
        self.vector = bullet_change_move
        curx = self.x
        cury = self.y
        pts = do_move(remaning_time)
        pts.append(Vector(curx, cury))
        return pts
            
class Game:
    def __init__(self, players = 2, field = [[0 for j in range(20)] for i in range(20)]):
        self.consts = Consts(players)
        self.field = field #0 is free, 1 is breakable, 2 is unbreakable(ricochet wall)
        self.humans = []
        self.bullets = dict()
        self.curid = 0
        for i in range(self.consts.players):
            self.humans.append(Human(self.consts.resp[i][0], self.consts.resp[i][1], i))


    def do_tick(self, commands, is_fire, cursour):
        answer = ans_init()
        for i in range(self.consts.players):
            answer['humans'][i]['move'] = self.humans[i].do_move(commands[i], curid)
        for bullet in bullets:
            pts = bullet.do_move(1)
            answer['bullets'][bullet.id]['pos'] = Vector(bullet.x, bullet.y)
            answer['bullets'][bullet.id]['direction'] = bullet.vector
            answer['bullets'][bullet.id]['pts'] = pts[::-1]
        return answer
    
            


game = Game()
