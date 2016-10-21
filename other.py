import math
import sys
class Consts:
    def __init__(self, players = 2):
        self.maxplayers = 2
        self.eps = 1e-5
        self.resp = [0 for i in range(self.maxplayers)]
        self.resp[0] = [5, 5]
        self.resp[1] = [15, 15]
        self.players = players
        self.body_length = 3 #hitbox is square
        self.tick_rate = 100
        self.human_speed = 0.2 #dist per tick
        self.bullet_speed = 0.5 #dist per tick
        self.shoot_cooldown = 1 * self.tick_rate #in ticks
        self.move_cooldown = int(1 / self.human_speed + self.eps)
        self.width = 20 #parallel OY
        self.length = 20 #parallel OX
        self.pixels_on_one_square = 8
        self.bullet_maxenergy = 504
        self.bullet_flycost = 14 #lost per tick 
        self.bullet_ricochet_cost = 88 #lost per ricochet
consts = Consts()
def ans_init():
    answer = dict()
    answer['humans'] = dict()
    answer['bullets'] = dict()
    for i in range(consts.maxplayers):
        answer['humans'][i] = dict()
        answer['humans'][i]['move'] = []
    return answer
'''
example of answer
answer = {
    humans = [
        0:
            move = ['w', 'a'] #commands that executed
        1:
            move = []
    ]
    bullets = { #key is id
       12: pos = vector(12, 34)
           direction = vector(2.2, -1.5) #length is distanse per 1 tick
           pts = [vector(31, 44), vector(12, 34)], moving key points, points, when direction changed(or last point)
       24: pos = vector(7.6, 8.3) #hitbox is [8, 8]
           direction = vector(2, -1)
           pts = [vector(7.6, 8.3)]
    } 
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
        if (x1 == x2):
            for y in range(Consts().width + 1):
                self.crossing_squares.append(Vector(x1, y))
        else:
            for x in range(Consts().length + 1):
                y1 = self.k * x + self.b
                #max(0, math.floor(self.k * x + self.b))
                y2 = self.k * x + self.b + self.k
                #min(Consts().width, math.floor(self.k * x + self.b + self.k))
                ymin = max(0, math.floor(min(y1, y2)))
                ymax = min(Consts().width, math.floor(max(y1, y2) + Consts().eps))
                for y in range(ymin, ymax + 1):
                    self.crossing_squares.append(Vector(x, y))


    def cross_square(self, p1, p2):
        if self.k == None:
            if p1.x <= self.b <= p2.x:
                return [Vector(self.b, p1.y), Vector(self.b, p2.y)]
            return []
        else:
            ans = []
            if (p1.x <= (p1.y - self.b) / self.k <= p1.x + 1):
                ans.append(Vector((p1.y - self.b) / self.k, p1.y))
            if (p1.x <= (p1.y + 1 - self.b) / self.k <= p1.x + 1):
                ans.append(Vector((p1.y + 1 - self.b) / self.k, p1.y + 1))
            if (p1.y <= (p1.x * self.k + self.b) <= p1.y + 1):
                ans.append(Vector(p1.x, p1.x * self.k + self.b))
            if (p1.y <= ((p1.x + 1) * self.k + self.b) <= p1.y + 1):
                ans.append(Vector(p1.x + 1, (p1.x + 1) * self.k + self.b))
            return ans
            
