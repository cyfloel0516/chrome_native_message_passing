# This file is an example to show the communication between chrome extension and python script.
# It also shows the message passing between python and java.
# This git repo is only the host part of example. Refer to the extension side on: 

import struct
import sys
import subprocess
import os
import time
import json
# On Windows, the default I/O mode is O_TEXT. Set this to O_BINARY
# to avoid unwanted modifications of the input/output streams.
if sys.platform == "win32":
	import os, msvcrt
	msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
	msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

# Helper function that sends a message to the webapp.
def send_message(message):
   # Write message size.
	sys.stdout.write(struct.pack('i', len(message)).decode('UTF-8'))
	# Write the message itself.
	sys.stdout.write(message)
	sys.stdout.flush()
	
# Thread that reads messages from the webapp.
def read_thread_func():
	message_number = 0
	p = subprocess.Popen(["java", "-jar", os.path.dirname(os.path.realpath(__file__)) + "/test.jar"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
	while 1:
		# Read the message length (first 4 bytes).
		text_length_bytes = sys.stdin.buffer.read(4)
		# Unpack message length as 4 byte integer.
		text_length = struct.unpack('i', text_length_bytes)[0]
		# Read the text (JSON object) of the message.
		text = sys.stdin.buffer.read(text_length).decode("UTF-8")
		request = json.loads(text)
		# In headless mode just send an echo message back.
		#request = json.loads(text)
		# p = subprocess.Popen(["java", "-jar", os.path.dirname(os.path.realpath(__file__)) + "/MessageHandler.jar"], stdout=subprocess.PIPE)
		# text = p.communicate()[0]

		# p = subprocess.Popen(["cmd"],shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		command = request["message"]

		if command == "ACTIVE":
			# active the STT application
			# receive the application response and tell the chrome extension the application is ready
			# mock
			p.stdin.write(b'ACTIVE\r\n')
			p.stdin.flush()
			result = p.stdout.readline().decode('utf-8')[0: -2]
			send_message('{"command": "%s"}' % result)

			# send_message('{"command": "%s"}' % "2")
			# text = p.communicate("asd\n")[0]
			# send_message('{"command": "%s"}' % "12345")
			# return;
			# text = p.stdout.readline()
			# text = "12345123"
			# send_message('{"command": "%s"}' % text)
		elif command == "SPEAKING":
			# mock

			p.stdin.write(b'SPEAKING\r\n')
			p.stdin.flush()
			result = p.stdout.readline().decode('utf-8')[0: -2]
			send_message('{"command": "%s", "result": "%s"}' % ("ACTION", result))
		else:
			send_message('{"command": "%s"}' % "Unknown")

def Main():
#   p = subprocess.Popen(["java", "-jar", "./NativeMessageReceiver.jar"], stdout=subprocess.PIPE)
#   text = p.communicate()[0].decode()
#   sys.stdout.write(text)
#   sys.stdout.flush()
	read_thread_func()
	sys.exit(0)

if __name__ == '__main__':
	Main()