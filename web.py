import socket
import server
import other
import json
import copy
import time
players = other.Consts().players

default_data = [[], False, [None, None]]
last_data = [copy.deepcopy(default_data)] * players
timeout = 1 / server.game.consts.tick_rate / (players + 1)
sock = socket.socket()
port = 3228
sock.bind(("127.0.0.1", port)) 

sock.listen(players)

conns = []

for i in range(players):
    cur_conn = sock.accept()[0]
    cur_conn.settimeout(timeout)
    conns.append(cur_conn)
    
    print('Accepted ', i + 1)

while True:
    time_of_begin_of_tick = time.time()
    curdata = []
    for i, conn in enumerate(conns):
        try:
            data = conn.recv(1024)
            #print(data)
            data = str(data, encoding = 'ascii')
            #print(data, repr(data))
            data = json.loads(data)
            last_data[i] = copy.deepcopy(data)
            #print(data)
            
        except socket.timeout:
            #print("No data")
            data = copy.deepcopy(last_data[i])
        except ValueError:
            #print('Invalid data')
            data = copy.deepcopy(last_data[i])
        #except Exception as s:
        #    print("chto-to-poshlo-ne-tak")
            
        curdata.append(data)
    all_commands = []
    all_is_fires = []
    all_curs = []

    #all_commands, all_is_fires, all_curs = zip(*curdata)

    for data in curdata:
        all_commands.append(data[0])
        all_is_fires.append(data[1])
        all_curs.append(data[2])

    tmp = server.game.do_tick(all_commands, all_is_fires, all_curs)
    #print(tmp)
    output = json.dumps(tmp).encode()
        
    for i, conn in enumerate(conns):
        conn.send(output)
        #print('Sended', i + 1)
    time_of_end_of_tick = time.time()
    remaning_time = 1 / server.game.consts.tick_rate - (time_of_end_of_tick - time_of_begin_of_tick)
    if remaning_time < 0:
        print("wait time biger than time of 1 tick")
    else:
        time.sleep(remaning_time)
        
    
    
for i in range(players):
    conns[i].close()
