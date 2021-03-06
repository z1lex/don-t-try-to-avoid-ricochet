import socket
import tkinter as tk
import time
import other
import json
import win32api
import copy

#just sorry for global var, it will fixed late
port = 3228
consts = other.Consts()
root = tk.Tk()
canvas = tk.Canvas(root,
                   width = consts.length * consts.pixels_on_one_square,
                   height = consts.length * consts.pixels_on_one_square,
                   bg = 'green')


class Player:
    def __init__(self, number_of_player):
        pixels = consts.pixels_on_one_square #for next line
        resp_x = consts.resp[number_of_player][0]
        resp_y = consts.resp[number_of_player][1]
        cur_player = canvas.create_rectangle(resp_x * consts.pixels_on_one_square,
                                         resp_y * consts.pixels_on_one_square,
                                         (resp_x + consts.body_length) * consts.pixels_on_one_square,
                                         (resp_y + consts.body_length) * consts.pixels_on_one_square,
                                         fill = 'blue', outline = 'blue')
        canvas.update()
        self.object = cur_player
        self.x = resp_x
        self.y = resp_y
    def do_move(self, commands): #player in list of players [a, x, y]
        change_x = 0
        change_y = 0
        for command in commands:
            if command == 'w':
                change_y -= consts.pixels_on_one_square
            if command == 's':
                change_y += consts.pixels_on_one_square
            if command == 'a':
                change_x -= consts.pixels_on_one_square
            if command == 'd':
                change_x += consts.pixels_on_one_square
        canvas.move(self.object, change_x, change_y)
        


class Square:
    def __init__(self, x, y, value):
        self.object = canvas.create_rectangle(x * consts.pixels_on_one_square,
                                       y * consts.pixels_on_one_square,
                                       (x + 1) * consts.pixels_on_one_square,
                                       (y + 1) * consts.pixels_on_one_square,
                                       fill = consts.color[value], outline = consts.color[value])
        self.value = value
        self.x = x
        self.y = y
        canvas.update()
    def change(self, new_value):
        canvas.delete(self.object)
        self.object = canvas.create_rectangle(x * consts.pixels_on_one_square,
                                       y * consts.pixels_on_one_square,
                                       (x + 1) * consts.pixels_on_one_square,
                                       (y + 1) * consts.pixels_on_one_square,
                                       fill = consts.color[new_value], outline = consts.color[new_value])

class Bullet:
    def __init__(self, index, x, y):
        self.x = x
        self.y = y
        self.index = index
        self.object = canvas.create_rectangle(x * consts.pixels_on_one_square,
                                       y * consts.pixels_on_one_square,
                                       (x + 1) * consts.pixels_on_one_square,
                                       (y + 1) * consts.pixels_on_one_square, fill = consts.bullet_color, outline = consts.bullet_color)
    def do_move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y
        x = self.x
        y = self.y
        canvas.delete(self.object)
        self.object = canvas.create_rectangle(x * consts.pixels_on_one_square,
                                       y * consts.pixels_on_one_square,
                                       (x + 1) * consts.pixels_on_one_square,
                                       (y + 1) * consts.pixels_on_one_square, fill = consts.bullet_color, outline = consts.bullet_color)
    def delete(self):
        canvas.delete(self.object)
def is_enable(key_index):
    return (win32api.GetKeyState(key_index) < 0)

def get_buttons():
    answer = []
    is_fire = False
    forward_flag = False
    strafe_flag = False
    if is_enable(consts.index_of_key_w):
        answer.append('w')
        forward_flag = True
    
    if is_enable(consts.index_of_key_s):
        if (forward_flag):
            answer.pop() #if w and s has preesed, we don't need to consider it
        else:
            answer.append('s')
    
    if is_enable(consts.index_of_key_a):
        answer.append('a')
        strafe_flag = True
    
    if is_enable(consts.index_of_key_d):
        if (strafe_flag):
            answer.pop() #if d and a has preesed, we don't need to consider it
        else:
            answer.append('d')
    if is_enable(consts.index_of_fire):
        is_fire = True
    return answer, is_fire



players = [] # elem is [a, x, y], a - his canvas object; x,y - his coords
field = copy.deepcopy(consts.start_field)
bullets = dict()
for x in range(len(field)):
    for y in range(len(field[x])):
        field[x][y] = Square(x, y, field[x][y])






canvas.pack()







for number in range(consts.players):
    players.append(Player(number))
    

sock = socket.socket()
sock.connect(("127.0.0.1", port))
while True:
    time_of_begin_of_tick = time.time()
    current_buttons, is_fire = get_buttons()
    #print(is_fire)
    client_answer = [current_buttons, is_fire, [0.72141, 0.51252]]
    sock.send(json.dumps(client_answer).encode())
    try:
    #if 1:
        server_answer = json.loads(str(sock.recv(1024), encoding = 'ascii'))
        for player in range(consts.players):
            players[player].do_move(server_answer['humans'][str(player)]['move'])
        del_bullets = []
        new_bullets = [] # elem is [id, x, y]
        for key in server_answer['bullets'].keys():
            action_flag = False
            if ('is_resp' in server_answer['bullets'][key]) and (server_answer['bullets'][key]['is_resp']):
                new_bullets.append([key, server_answer['bullets'][key]['pos'][0], server_answer['bullets'][key]['pos'][1]])
                action_flag = True
            if ('die' in server_answer['bullets'][key]) and (server_answer['bullets'][key]['die'] == True):
                del_bullets.append(key)
                action_flag = True
            if (not action_flag):
                x = server_answer['bullets'][key]['pos'][0]
                y = server_answer['bullets'][key]['pos'][1]
                bullets[key].do_move(x, y)
        for bullet in new_bullets:
            index = bullet[0]
            x = bullet[1]
            y = bullet[2]
            bullets[index] = Bullet(index, x, y)
        for index in del_bullets:
            bullets[index].delete()
            bullets.pop(index)
            
            
            
        
    except:
        pass
    time_of_end_of_tick = time.time()
    remaning_time = 1/consts.tick_rate - (time_of_end_of_tick - time_of_begin_of_tick)
    canvas.update()
    if (remaning_time < 0):
        print("some wrong")
    else:
        time.sleep(remaning_time)


root.mainloop()
sock.close()


