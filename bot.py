import urllib.request
import json
import subprocess
import time
import os
import signal
import requests
import re
token= "287670488:AAGyEmCNxqUWAXo0r0HqV2fluhbihq_sB84"
def command(cmd,params):
	response = requests.post(
		url='https://api.telegram.org/bot{0}/{1}'.format(token, cmd),
		data=params
	).json()

def commandget(cmd,params):
	api="https://api.telegram.org/bot%s/%s?%s" % (token,cmd,params)
	r = urllib.request.urlopen(api).read()
	parsed_json = json.loads(r)
	return parsed_json

def param(params):
	return urllib.parse.urlencode(params)

def tresult(resultt):
	return resultt['message']['text']

def checkcommand(result):
	cmd=tresult(result).split(" ",1)
	return cmd

def executecmd(cmd,user):
	if cmd[0]=="/sendcommand":
		if len(cmd)>1:
			cmd2=cmd[1].split(",")
			for i in cmd2:
				execute(i,user)

def subprocesscmd(cmd,user):
	msg=[]
	start_time = time.time()
	print("subprocess",cmd)
	elapsed_time = time.time() - start_time
	try:
		proc=subprocess.Popen(cmd,stdout=subprocess.PIPE,preexec_fn=os.setsid)
		with open(cmd[0]+".txt","w") as log_file:
			while proc.poll() is None:
				line = proc.stdout.readline()
				if line:
					#print ("out: " + line.strip().decode('utf-8'))
					log_file.write(line.decode('utf-8'))
					msg.append(line.decode('utf-8'))
					elapsed_time = time.time() - start_time
					if elapsed_time > 1:
						os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
						print("matando")
			print ( ' '.join(msg))

			ansi_escape = re.compile(r'\x1b[^m]*m')
			nmsg=ansi_escape.sub('', ' '.join(msg))
			print(nmsg)
			sendmsg(nmsg,user)

	except:
		print("not a valid command")

def sendmsg(cmd,user):
	f={'chat_id':user,'text':cmd }
	msg=command('sendMessage',f)
	print(msg)

def execute(cmd,user):
	cmd=cmd.split()
	print("executando",cmd)
	if cmd[0] == "watch":
		subprocesscmd(cmd[1:],user)
		main()
	else:
		subprocesscmd(cmd,user)

def main():
	oldid=""
	while True:
		f={'allowed_updates':'message'}
		result=commandget('getUpdates',param(f))
		lastrst=result['result'][-1]
		if lastrst['update_id'] != oldid:
			if 'edited_message' not in lastrst:

				if 'entities' in lastrst['message']:
					user=lastrst['message']['from']['id']
					cmd=checkcommand(lastrst)
					executecmd(cmd,user)
					oldid=lastrst['update_id']
					print(tresult(lastrst))

main()
