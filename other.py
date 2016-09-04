class Consts:
    def __init__(self, players = 2):
        self.maxplayers = 2
        self.resp = [0 for i in range(self.maxplayers)]
        self.resp[0] = [5, 5]
        self.resp[1] = [15, 15]
        self.players = players
        self.body_length = 3 #hitbox is square
        self.tick_rate = 100
        self.human_speed = 20 #ticks, should multiple tick_rate
        self.bullet_speed = 50 #ticks, should multiple tick_rate
        self.move_cooldown = self.tick_rate // self.human_speed
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
       12: pos = [12, 34]
           vecotor = [2.2, -1.5] #length is randomly
       24: pos = [7.6, 8.3] #hitbox is [8, 8]
           vector = [2, -1]
    }
}
'''
#def get_commands
