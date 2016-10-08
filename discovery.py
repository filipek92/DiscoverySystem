#!/usr/bin/env python3

import socket
import click
import traceback

class Server:
    def __init__(self, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sock.bind(("0.0.0.0", port))
        self.services = [];

    def run(self):
        print("Starting server")
        self.list()
        while True:
            data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
            print("Proccesing request {} from {}:{}".format(data, *addr))
            try:
                self.request(addr[0], addr[1], data.decode())
            except KeyboardInterrupt:
                print("CTRL+C")
                break
            except Exception as e:
                print(e)
                traceback.print_exc()
                continue


    def request(self, address, port, request):
        cmd, *args = request.split(" ");
        getattr(self,cmd)(*args, port=port, address=address) 

    def list(self, address=None, port=None):
        print("Advertising these services:")
        reply = "List of services\n";
        for name, port in self.services:
            print(" {} at {}".format(name, port))
            reply += "{}\t{}\n".format(name, port);
        if not self.services:
            print(" No services available");
        if address and port:
            print("Sending reply");
            self.sock.sendto(reply.encode(), (address, port))

    def add(self, name, port):
        self.services.append((name, port));     
        

def discover(port, request):
    print("Sendind request {}".format(request))
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 25000))
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(request.encode(), ("255.255.255.255", port))
    print("Waiting for reply")
    data, addr = sock.recvfrom(1024)
    print("Reply {} from {}:{}".format(data, *addr))
        

@click.command()
@click.option("-s","--server", is_flag=True, default=False)
@click.option("-p","--port", default=5005)
@click.option("-m","--message", default="No message")
@click.option("-a","--add-service", type=(str, int), multiple=True)
def main(server, port, message, add_service):
    if server:
        s = Server(port);
        for service in add_service:
            s.add(*service)
        s.run();
    else:
        print("message:", message)
        discover(port, message)


if __name__ == '__main__':
    main()
