from tkinter import *
from random import *
from server import *
from time import *
import json
import socket
arw_x = 0
arw_y = 0
fr = False
sock = socket.socket()
prt = 3228
sock.connect(("127.0.0.1", prt)) 
data = b'lol'
'''
while True:
    s = input()
    if s == 'exit':
        break
    sock.send(s.encode())
    json.loads(str(sock.recv(1024), encoding = 'ascii'))
sock.close()'''

def motion(event):
    global fr, arw_x, arw_y
    arw_x = event.x
    arw_y = event.y
    fr = True

def create_disp(size, body_length, nmb_of_cells, resp):
    root = Tk()
    cnv = Canvas(root, width= size * nmb_of_cells, height = size * nmb_of_cells, bg = "white")
    cnv.pack()
    player1 = cnv.create_rectangle(resp[0][0] * nmb_of_cells, resp[0][1] * nmb_of_cells, resp[0][0] * nmb_of_cells + body_length, resp[0][1] * nmb_of_cells + body_length, tag="rect", fill="black")
    player2 = cnv.create_rectangle(resp[1][0] * nmb_of_cells, resp[1][1] * nmb_of_cells, resp[1][0] * nmb_of_cells + body_length, resp[1][1] * nmb_of_cells + body_length, tag="rect", fill="black")
    root.bind('<Button-1>', motion)
    root.update()
    return [cnv, player1, root, player2]

out_of_create_disp = create_disp(game.consts.width, game.consts.body_length * game.consts.pixels_on_one_square , game.consts.pixels_on_one_square, game.consts.resp)
cnv = out_of_create_disp[0]
players = [out_of_create_disp[1], out_of_create_disp[3]]
root = out_of_create_disp[2]
crds = [0, game.consts.width * game.consts.pixels_on_one_square, game.consts.width * game.consts.pixels_on_one_square, 0]

def disp_tick(btns, cnv, players, lng, root, blts, mst_mv, ans, all_bl):
    for k in range(8):
        for i in range(2):
            x = 0
            y = 0
            if 'a' in btns[i]:
                x -= lng
            if 's' in btns[i]:
                y += lng
            if 'w' in btns[i]:
                y -= lng
            if 'd' in btns[i]:
                x += lng
            cnv.move(players[i], x // 8, y // 8)
            root.update()
        for i in mst_mv:
            x = ans['bullets'][i]['pos']['0'] - all_bl[i]['0']
            y = ans['bullets'][i]['pos']['1'] - all_bl[i]['1']
            if k != 7:
                cnv.move(blts[i], x // 8, y // 8)
            else:
                cnv.move(blts[i], x - 7 * (x // 8), y - 7 * (y // 8))
            root.update()

blts = []
def crt_blt(cnv, x, y):
    blts.append(cnv.create_rectangle(x, y, x + 7, y + 7, tag="", fill="red"))
    root.update()

q = []
all_bl = dict()
blts = []
mx_inx = 0
ans = dict()
mst_mv = []
btn = [0, 0]
new_btns = ['s', 'a']
while 1:
    if len(q) > 0:
        for i in range(len(q)):
            all_bl[q[i][0]] = [q[i][1], q[i][2]]
            crt_blt(cnv, q[i][1], q[1][2])
        q = []
    if fr == True:
        crt_blt(cnv, 100, 100)
        fr = False
    s = json.dumps([new_btns, fr, [arw_x, arw_y]]).encode()
    if s == 'exit':
        break
    sock.send(s)
    ans = json.loads(str(sock.recv(1024), encoding = 'ascii'))
    for i in ans['bullets'].keys():
        if i in all_bt:
            mst_mv.append(i)
        else:
            q.append([i, ans['bullets'][i]['pos']['0'], ans['bullets'][i]['pos']['1']])
    btn[0], btn[1] = ans['humans']['0']['move'], ans['humans']['1']['move']
    if 'die' in ans['humans']['0'] or 'die' in ans['humans']['1']:
        break
    disp_tick(btn, cnv, players, 8, root, blts, mst_mv, ans, all_bl)
    mst_mv = []




sock.close()

'''
i = 0
crr_id = -1
while 1:
    fr_ch = fr
    if i < 20:
        new_btns = [['s'], ['w']]
    else:
        new_btns = [['d'], ['a']]
    
    ans = game.do_tick(new_btns,[fr_ch, None] , [arw_x, arw_y])
    #print(ans['humans'])
    disp_tick([ans['humans'][0]['move'], ans['humans'][1]['move']], cnv, player, game.consts.pixels_on_one_square, root, [], 0)
    print(ans['bullets'])
    mv_blt(ans['bullets'], blts, cnv)
    if fr_ch:
        crr_id += 1
        crt_blt(cnv, 50, 50, crr_id)
        print(blts)
    print(ans['bullets'])
    sleep(0.02)
    i += 1
    print(1111111111111111111111111111, fr)
    if fr_ch == True:
        fr = False'''

