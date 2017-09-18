import json
import time
import subprocess
import sys

f=open('config/miner.json','r');
miners=json.load(f);
f.close();

for i in xrange(0,len(miners['miners'])):
	print('========  Testing miner %s  =========='%miners['miners'][i]['name']);
	print(' ')
	command=miners['prefix']+'exec '+miners['miners'][i]['command'];
	process=subprocess.Popen(command,shell=True);
	time.sleep(60);
	process.terminate();
	process.wait();
	print(' ')
	print(' ')
	print(' ')

subprocess.call('stty echo',shell=True); #Restore commandline echo...