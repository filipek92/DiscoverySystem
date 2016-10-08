#!/usr/bin/env python3

import socket
import click

class Server:
	def __init__(self, port):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
		self.sock.bind(("", port))
		print("Starting server")
	def run(self):
		while True:
		    data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
		    print("received message:", data)		
		

def discover(server, port, message):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
	sock.sendto(message.encode(), (server, port))
		

@click.command()
@click.option("-s","--server", is_flag=True, default=False)
@click.option("-h","--host", default="10.2.0.10")
@click.option("-p","--port", default=5005)
@click.option("-m","--message", default="No message")
def main(server, host, port, message):
	if server:
		Server(port).run();
	else:
		print("UDP target: {}:{}".format(host, port))
		print("message:", message)
		discover(host, port, message);


if __name__ == '__main__':
	main()
