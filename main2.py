import random
import socket

UDP_IP = "127.0.0.1"

peers_ports = []


def main():
    peer_id = input("Enter ID for yourself : ")

    while True:
        side = input("a) send\n"
                     "b) receive\n"
                     "c) finish  \n ")
        port = random.randint(5000, 5500)
        if side == "a":
            with open('peers_ports.txt', 'a') as ports:
                ports.write(f'{port}\n')
                ports.close()
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((UDP_IP, port))
            fname = input("Enter your file name : ")
            path = input("Enter your file path : ")
            with open(path) as f:
                lines = f.readlines()
            while True:
                print("listening .........")
                data, addr = sock.recvfrom(1024)
                print(f'request for sending from port : {addr[1]}')
                req = (data.decode('utf-8')).split(" ")
                print(req)
                if fname == req[1]:
                    seqnum = 0
                    for line in lines:
                        line = line.split(" ")
                        for l in line:
                            packet = f'{l} {seqnum}'
                            seqnum += 1
                            line1 = packet.encode('utf-8')
                            sock.sendto(line1, addr)
                    finish = "finished"
                    sock.sendto(finish.encode('utf-8'), addr)
                    print("finished")
                    break
        if side == "b":
            with open('peers_ports.txt', 'r') as portsin:
                reads = portsin.readlines()
                for i in reads:
                    peers_ports.append(int(str(i.strip())))
                portsin.close()
            fname = input("give your file name : ")
            message = f'req {fname}'
            message = message.encode('utf-8')
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.bind((UDP_IP, port))
            print(f'socket built on port :  {port}')
            for peer in peers_ports:
                sock.sendto(message, (UDP_IP, peer))
            main_part = [0] * 100
            while True:
                data, addr = sock.recvfrom(1024)
                data1 = data.decode('utf-8')
                if data1 == "finished":
                    print("inja finish")
                    with open(f'P{peer_id}-{fname}.txt', 'w') as f:
                        for i in main_part:
                            if i != 0:
                                f.write(i)
                                f.write(" ")
                        f.close()
                        print("receiving finished")
                    break
                else:
                    data2 = data1.split(" ")
                    seq = int(data2[1])
                    main_part[seq] = data2[0]
        if side == "c":
            print("by by")
            break



if __name__ == '__main__':
    main()
