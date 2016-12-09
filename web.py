import socket
import server
import other
import json
players = 2
default_data = [[], False, [None, None]]
timeout = 5
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
    curdata = []
    for conn in conns:
        try:
            data = conn.recv(1024)
            #print(data)
            data = str(data, encoding = 'ascii')
            #print(data, repr(data))
            data = json.loads(data)
            #print(data)    
        except socket.timeout:
            print("No data")
            data = default_data
        except ValueError:
            print('Invalid data')
            data = default_data
        #except Exception as s:
        #    print("chto-to-poshlo-ne-tak")
            
        curdata.append(data)
    #all_commands = []
    #all_is_fires = []
    #all_curs = []

    all_commands, all_is_fires, all_curs = zip(*curdata)

    '''for data in curdata:
        all_commands.append(data[0])
        all_is_fires.append(data[1])
        all_is_fires.append(data[2])'''

    tmp = server.game.do_tick(all_commands, all_is_fires, all_curs)
    print(tmp)
    output = json.dumps(tmp).encode()
        
    for i, conn in enumerate(conns):
        conn.send(output)
        print('Sended', i + 1)
        
        
    
    
for i in range(players):
    conns[i].close()
