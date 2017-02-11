import math
import sys
class Consts:
    def __init__(self, players = 1):
        self.maxplayers = 2
        self.eps = 1e-5
        self.resp = [0 for i in range(self.maxplayers)]
        self.resp[0] = [5, 5] #in decart
        self.resp[1] = [14, 14] #in decart
        self.players = players
        self.body_length = 3 #hitbox is square
        self.tick_rate = 15
        self.human_speed = 0.5 #dist per tick
        self.bullet_speed = 1.0 #dist per tick
        self.respawn_time = 200 #ticks
        self.shoot_cooldown = 1 * self.tick_rate #in ticks
        self.move_cooldown = int(1 / self.human_speed + self.eps)
        self.width = 20 #parallel OY
        self.length = 20 #parallel OX
        self.pixels_on_one_square = 20 #it is pixels in line of squere
        self.bullet_maxenergy = 500
        self.bullet_flycost = 7 #lost per tick 
        self.bullet_ricochet_cost = 88 #lost per ricochet
        self.start_field =                      [[2 * ((j <= 1) or
                                                   (i <= 1) or
                                                   (i >= self.length - 2) or
                                                   (j >= self.width - 2))
                                                for j in range(self.width)] for i in range(self.length)]
        self.index_of_fire = 0x20 #space
        self.index_of_key_w = 0x57
        self.index_of_key_s = 0x53
        self.index_of_key_a = 0x41
        self.index_of_key_d = 0x44 #this is client consts for some optimisation
        self.color = ['green', 'red', 'pink']
        self.bullet_color = 'red'
consts = Consts()
def ans_init():
    answer = dict()
    answer['humans'] = dict()
    answer['bullets'] = dict()
    answer['consts'] = None
    answer['squares'] = []
    for i in range(consts.maxplayers):
        answer['humans'][i] = dict()
        answer['humans'][i]['move'] = []
    return answer
def convert_input(commands, is_fire, cursour):
    for player in range(len(commands)):
        for command_id in range(len(commands[player])):
            if (commands[player][command_id] == 'w'):
                commands[player][command_id] = 's'
            elif (commands[player][command_id] == 's'):
                  commands[player][command_id] = 'w'
    cursour.y = consts.width - cursour.y
    return commands, is_fire, cursour
def transform_ans(answer):
    for player_id in range(len(answer['humans'])):
        for command_id in range(len(answer['humans'][player_id]['move'])):
            if (answer['humans'][player_id]['move'][command_id] == 'w'):
                answer['humans'][player_id]['move'][command_id] = 's'
            elif (answer['humans'][player_id]['move'][command_id] == 's'):
                answer['humans'][player_id]['move'][command_id] = 'w'

    for bullet_id in answer['bullets'].keys():
        answer['bullets'][bullet_id]['pos'].y = consts.width - answer['bullets'][bullet_id]['pos'].y
        answer['bullets'][bullet_id]['direction'].y *= -1
        for point_id in range(len(answer['bullets'][bullet_id]['pts'])):
            answer['bullets'][bullet_id]['pts'][point_id].y = consts.width - answer['bullets'][bullet_id]['pts'][point_id].y
    return answer
        
'''
example of answer
answer = {
    humans = {
        0:
            move = ['w', 'a'] #commands that executed
            is_resp = True
        1:
            move = []
            die = True
    }
    bullets = { #key is id
       12: pos = vector(12, 34)
           direction = vector(2.2, -1.5) #length is distanse per 1 tick
           pts = [vector(31, 44), vector(12, 34)], moving key points, points, when direction changed(or last point)
           is_resp = False
       24: pos = vector(7.6, 8.3) #hitbox is [8, 8]
           is_resp = False
           direction = vector(2, -1)
           pts = [vector(7.6, 8.3)]
           die = True
       0:  pos = vector(1, 1)
           direction = (-1.1, -2.2)
           is_resp = True
    }
    squares = [
        [1, 2, 3], # point (1, 2) converted in 3
        [x, y, d]
    ]
    field = [[0, 0, 0, 1, 0],
             [0, 1, 2, 0, 1],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 1, 0, 0]]
}
'''
#def get_commands

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def len2(self):
        return self.x * self.x + self.y * self.y


    def len(self):
        return math.sqrt(self.len2())


    def dist2(self, other):
        return (other - self).len2()


    def dist(self, other):
        return math.sqrt(self.dist2(other))

    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)


    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)


    def __mul__(self, other):
        if type(other) == int or type(other) == float:
            return Vector(self.x * other, self.y * other)
        return self.x * other.x + self.y * other.y


    def __mod__(self, other):
        return self.x * other.y - self.y * other.x

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)
    def __neg__(self):
        return Vector(-self.x, -self.y)

    def normed(self):
        return Vector(self.x / self.len(), self.y / self.len())
    def __str__(self):
        return str(self.x) + ' ' + str(self.y)

class Line:
    def __init__(self, x1, y1, x2, y2):
        self.consts = Consts()
        self.flag = False
        if (x1 == x2):
            #self.flag = True #line don't cross OY
            #self.k = None
            #self.b = x1
            x2 += Consts().eps
        else:
            self.k = (y2 - y1) / (x2 - x1)
            self.b = y1 - self.k * x1
        
        self.crossing_squares = [] #squares on a Cartesian system.
        '''
        for x in range(Consts().length):
            for y in range(Consts().width):
                cur = Vector(x, y)
                delta = Vector(0.5, 0.5)
                if self.cross_square(cur - delta, cur + delta) != []:
                    self.crossing_squares.append(cur)
        '''
        if (x1 == x2):
            for y in range(self.consts.width):
                self.crossing_squares.append(Vector(x1, y))
        else:
            for x in range(self.consts.length):
                y1 = self.k * x + self.b
                #max(0, math.floor(self.k * x + self.b))
                y2 = self.k * x + self.b + self.k
                #min(Consts().width, math.floor(self.k * x + self.b + self.k))
                ymin = max(0, math.floor(min(y1, y2)))
                ymax = min(self.consts.width, math.floor(max(y1, y2) + self.consts.eps))
                for y in range(max(ymin - 2, 0), min(ymax + 2, self.consts.width)):
                    self.crossing_squares.append(Vector(x, y))
        fixed_crossing_squares = []
        for elem in self.crossing_squares:
            if self.cross_square(Vector(elem.x - 0.5, elem.y - 0.5), Vector(elem.x + 0.5, elem.y + 0.5)):
                fixed_crossing_squares.append(elem)
        self.crossing_squares = fixed_crossing_squares
        


    def cross_square(self, p1, p2):
        if self.k == None:
            if p1.x <= self.b <= p2.x:
                return [Vector(self.b, p1.y), Vector(self.b, p2.y)]
            return []
        else:
            ans = []
            if (p1.x - self.consts.eps <= (p1.y - self.b) / self.k <= p1.x + 1 + self.consts.eps):
                ans.append(Vector((p1.y - self.b) / self.k, p1.y))
            if (p1.x - self.consts.eps <= (p1.y + 1 - self.b) / self.k <= p1.x + 1 + self.consts.eps):
                ans.append(Vector((p1.y + 1 - self.b) / self.k, p1.y + 1))
            if (p1.y - self.consts.eps <= (p1.x * self.k + self.b) <= p1.y + 1 + self.consts.eps):
                ans.append(Vector(p1.x, p1.x * self.k + self.b))
            if (p1.y - self.consts.eps <= ((p1.x + 1) * self.k + self.b) <= p1.y + 1 + self.consts.eps):
                ans.append(Vector(p1.x + 1, (p1.x + 1) * self.k + self.b))
            return ans
            
