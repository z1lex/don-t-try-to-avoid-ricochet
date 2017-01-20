from other import *
import socket

class Human:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.move_cooldown = 0
        self.shoot_cooldown = 0
        self.respawn_time = 0
    def die(self):
        self.respawn_time = game.consts.respawn_time
        self.x = game.consts.length + 1
        self.y = game.consts.width + 1
    def try_move(self, command):
        flag = True
        if command == 'w':
            for x in range(self.x, self.x + game.consts.body_length):
                if game.field[x][self.y - 1] != 0:
                    flag = False
            for i in range(game.consts.players):
                if game.humans[i].id != self.id:
                    if game.humans[i].y == self.y - game.consts.body_length:
                        if self.x - game.consts.body_length + 1 <= game.humans[i].x < self.x + game.consts.body_length:
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
                        if self.x - game.consts.body_length + 1 <= game.humans[i].x < self.x + game.consts.body_length:
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
                        if self.y - game.consts.body_length + 1 <= game.humans[i].y < self.y + game.consts.body_length:
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
                        if self.y - game.consts.body_length + 1 <= game.humans[i].y < self.y + game.consts.body_length:
                            flag = False
            if flag:
                self.x += 1
        return flag

    
    def do_move(self, commands, is_fire, cursour):
        self.move_cooldown = max(0, self.move_cooldown - 1)
        self.shoot_cooldown = max(0, self.shoot_cooldown - 1)
        if self.respawn_time > 1:
            return [None, None]
        if self.respawn_time == 1:
            self.x = game.consts.resp[self.id][0]
            self.y = game.consts.resp[self.id][1]
            return [None, 'resp']
        self.respawn_time = max(0, self.respawn_time - 1)
        new_bullets = dict()
        if self.shoot_cooldown == 0 and is_fire:
            game.bullets[game.curid] = Bullet(self.x + game.consts.body_length // 2, self.y + game.consts.body_length // 2, cursour.x, cursour.y, game.curid, self.id)
            new_bullets[game.curid] = [self.x + game.consts.body_length // 2, self.y + game.consts.body_length // 2, cursour.x, cursour.y]
            game.curid += 1
            self.shoot_cooldown = game.consts.shoot_cooldown
        move = []
        if self.move_cooldown == 0:
            if len(commands) != 0:
                for command in commands:
                    if self.try_move(command):
                        move.append(command)    
                self.move_cooldown = game.consts.move_cooldown
        return [move, new_bullets]


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
            for human in game.humans:
                if (human.x <= square.x < human.x + game.consts.body_length) and (human.y <= square.y < human.y + game.consts.body_length) and (self.creator_id != self.id):
                    return square
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
        is_destroyed = [0] #[0] - continue mooving, [1] - destroyed without effects, [2, x, y] - destroyed points arround (x, y), [3, id] - destroyed tank with id=id
        first_crossed_in_field = self.first_crossed()
        x = first_crossed_in_field.x
        y = first_crossed_in_field.y
        point_crossed_with_squares = self.first_crossed_point()
        kinetic_cost = self.kinetic_cost(self.x, self.y, point_crossed_with_squares.x, point_crossed_with_squares.y)
        time_cost = self.time_cost(self.x, self.y, point_crossed_with_squares.x, point_crossed_with_squares.y)
        if self.kinetic < kinetic_cost:
            #bullet is destroyed
            return [1], [self.kinetic_move() + Vector(self.x, self.y)]
        if remaning_time < time_cost:
            #bullet continue moving next
            ans = [Vector(self.x, self.y) + self.time_move(remaning_time)]
            self.x += self.time_move(remaning_time).x
            self.y += self.time_move(remaning_time).y
            self.kinetic -= kinetic_cost
            return [0], ans
        self.kinetic -= kinetic_cost
        remaning_time -= time_cost
        bullet_change_move = self.vector_change_on_move()
        self.x = point_crossed_with_squares.x
        self.y = point_crossed_with_squares.y
        if game.field[x][y] == 1:
            #bullet has destroyed wall
            return [2, x, y], [Vector(self.x, self.y)]
        is_self_tank = False
        if game.field[x][y] == 0:
            #bullet has destroyed human maybe
            for human in game.humans:
                if (human.x <= square.x < human.x + game.consts.body_length) and (human.y <= square.y < human.y + game.consts.body_length):
                    if (human.id != self.creator_id):
                        return [3, x, y], [Vector(self.x, self.y)]
                    else:
                        is_self_tank = True
        if self.kinetic < game.consts.bullet_ricochet_cost:
            #bullet is destroyed
            return [0], [Vector(self.x, self.y)]
        self.vector = bullet_change_move
        self.line = Line(self.x, self.y, self.x + self.vector.x, self.y + self.vector.y)
        curx = self.x
        cury = self.y
        is_destroyed, pts = self.do_move(remaning_time)
        if (is_self_tank == False):
            pts += [Vector(curx, cury)]
        return is_destroyed, pts
            
class Game:
    def __init__(self, players = Consts().players, field = Consts().start_field):
        self.consts = Consts(players)
        self.field = field #0 is free, 1 is breakable, 2 is unbreakable(ricochet wall)
        self.humans = []
        self.bullets = dict()
        self.curid = 0
        for i in range(self.consts.players):
            self.humans.append(Human(self.consts.resp[i][0], self.consts.resp[i][1], i))


    def do_tick(self, commands, is_fire, cursour):
        for i in range(game.consts.players):
            cursour[i] = Vector(cursour[i][0], cursour[i][1])
            
        #cursour = Vector(cursour[0], cursour[1])
        #commands, is_fire, cursour = convert_input(commands, is_fire, cursour)
        answer = ans_init() 
        for i in range(self.consts.players):
            ans_move, new_bullets = self.humans[i].do_move(commands[i], is_fire[i], cursour[i])
            if ans_move == None and new_bullets == None: #died
                answer['humans'][i]['move'] = []
            elif ans_move == None and new_bullets == 'resp': #already resp
                answer['humans'][i]['move'] = []
                answer['humans'][i]['is_resp'] = True
            else:
                answer['humans'][i]['move'] = ans_move
            for cur_id in new_bullets:
                answer['bullets'][cur_id] = dict()
                answer['bullets'][cur_id]['is_resp'] = True
            
        cur_bullets = list(self.bullets.keys())
        for bullet in cur_bullets:
            bullet = self.bullets[bullet]
            is_destroyed, pts = bullet.do_move(1)
            if (is_destroyed[0] != 0):
                self.bullets.pop(bullet.id)
                if (is_destroyed[0] == 3):
                    x = is_destroyed[1]
                    y = is_destroyed[2]
                    for human in self.humans:
                        if (human.x <= square.x < human.x + game.consts.body_length) and (human.y <= square.y < human.y + game.consts.body_length):
                            human.die()
                            answer['humans'][human.id]['die'] = True
                if (is_destroyed[0] == 2):
                    x = is_destroyed[1]
                    y = is_destroyed[2]
                    for i in range(x - 1, x + 1):
                        for j in range(y - 1, y + 1):
                            if (i >= 0) and (j >= 0) and (i < self.consts.length) and (j < self.consts.width) and (abs(x - i) + abs(y - j) <= 1) and (self.field[i][j] == 1):
                                answer['squares'].append([i, j, 0])
                                game.field[i][j] = 0
                if not (bullet.id in answer['bullets']):
                    answer['bullets'][bullet.id] = dict()
                answer['bullets'][bullet.id]['die'] = True
                    
            else:
                if not (bullet.id in answer['bullets']):
                    answer['bullets'][bullet.id] = dict()
                answer['bullets'][bullet.id]['pos'] = [bullet.x, bullet.y]
                answer['bullets'][bullet.id]['direction'] = [bullet.vector.x, bullet.vector.y]

                converted_points = pts[::-1]
                for i, point in enumerate(converted_points):
                    converted_points[i] = [point.x, point.y]
                    
                answer['bullets'][bullet.id]['pts'] = converted_points
                if not ('is_resp' in answer['bullets'][bullet.id]):
                    answer['bullets'][bullet.id]['is_resp'] = False
        answer['consts'] = ''
        return answer
        #return transform_ans(answer)
    
            


game = Game()


