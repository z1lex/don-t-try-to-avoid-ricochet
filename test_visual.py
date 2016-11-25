from tkinter import *
from random import *
from server import *
from time import *
arw_x = 0
arw_y = 0
fr = False

def motion(event):
    global fr, arw_x, arw_y
    arw_x = event.x
    arw_y = event.y
    fr = True
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1')

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
player = [out_of_create_disp[1], out_of_create_disp[3]]
root = out_of_create_disp[2]
crds = [0, game.consts.width * game.consts.pixels_on_one_square, game.consts.width * game.consts.pixels_on_one_square, 0]

def disp_tick(btns, cnv, player, lng, root, arr_of_blts, spd):
    for i in range(2):
        x = 0
        y = 0
        y1 = 0
        x1 = 0
        if 'a' in btns[i]:
            x -= lng
            x1 = 1
        if 's' in btns[i]:
            y += lng
            y1 = 1
        if 'w' in btns[i]:
            y -= lng
            y1 = -1
        if 'd' in btns[i]:
            x += lng
            x1 = 1
        cnv.move(player[i], x, y)
        #print(crds)
        crds[0] += x
        crds[2] += x
        crds[1] += y
        crds[3] += y
        root.update()

blts = []
def crt_blt(cnv, x, y, c_id):
    blts.append(cnv.create_rectangle(x, y, x + 5, y + 5, tag="", fill="red"))
    root.update()

def mv_blt(arr_vct, blts, cnv):
    for i in arr_vct.keys():
        print(i, blts)
        if len(blts) > i:
            cnv.move(blts[i], arr_vct[i]['pos'].x, arr_vct[i]['pos'].y)
    root.update()
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
        fr = False
