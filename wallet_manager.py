import json
import time
import re
import subprocess
from subprocess import check_output
import sys
import os
import os.path

import constant
import config

def algo2name(coin,algo):
	if algo=='myr-gr':
		if coin=='j':
			return 'groestle';
		else:
			return 'groestl';
	elif algo=='whirl':
		return 'whirlpool';
	elif algo=='penta':
		return 'pentablake';
	elif algo=='lyra2v2':
		return 'lyra2rev2';
	elif algo=='blake2s':
		return 'blake';
	else:
		return algo;

def get_pid(name):
	try:
		return map(int,check_output(["pidof",name]).split())
	except:
		return [];

def install_vanilla(coin,url,rpcport,p2pport,nodes='',specify_algo=''):
	current_dir=os.getcwd();
	exec_path=os.path.join(current_dir,'wallet',coin,'src',constant.executable[coin]);
	if os.path.isfile(exec_path):
		return True;
	#Download
	subprocess.call('git clone %s ./wallet/%s'%(url,coin),shell=True);
	#Compile
	subprocess.call('mv ./wallet/%s/src/makefile.unix ./wallet/%s/src/Makefile'%(coin,coin),shell=True);
	subprocess.call('chmod +x ./wallet/%s/src/leveldb/build_detect_platform'%(coin),shell=True);
	if coin=='max':
		subprocess.call("sed -i 's/boost::get<const CScriptID&>(address)/boost::get<CScriptID>(address)/g' ./wallet/%s/src/rpcrawtransaction.cpp"%(coin),shell=True);
		subprocess.call("sed -i 's:/usr/lib/libminiupnpc.a:-lminiupnpc:g' ./wallet/%s/src/Makefile"%(coin),shell=True);
	elif coin=='coinonat':
		subprocess.call("sed -i 's:sudo::g' ./wallet/%s/src/leveldb/Makefile"%(coin),shell=True);
	subprocess.call('cd wallet/%s/src/;make -j20'%(coin),shell=True);
	#Prepare data folders and run commands
	algo=constant.algo_lookup[coin];
	if type(algo)==list:
		for a in algo:
			datadir='wallet-data/%s-%s'%(coin,a);
			subprocess.call('mkdir %s'%(datadir),shell=True);
	else:
		datadir='wallet-data/%s-%s'%(coin,algo);
		subprocess.call('mkdir %s'%(datadir),shell=True);
	#
	#Create run commands
	f=open('./wallet/%s/run.sh'%coin,'w');
	current_dir=os.getcwd();
	exec_path=os.path.join(current_dir,'wallet',coin,'src',constant.executable[coin]);
	if type(algo)==list:
		if specify_algo=='':
			i=0;
			for a in algo:
				datadir=os.path.join(current_dir,'wallet-data','%s-%s'%(coin,a));
				command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,algo2name(coin,a),config.wallet_username,config.wallet_password,rpcport+i,p2pport+i,nodes);
				f.write(command+'\n');
				i=i+1;
			#
		else:
			datadir=os.path.join(current_dir,'wallet-data','%s-%s'%(coin,specify_algo));
			command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,algo2name(coin,specify_algo),config.wallet_username,config.wallet_password,rpcport,p2pport,nodes);
			f.write(command+'\n');
		#
	else:
		datadir=os.path.join(current_dir,'wallet-data','%s-%s'%(coin,algo));
		command='%s --datadir=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,config.wallet_username,config.wallet_password,rpcport,p2pport,nodes);
		f.write(command+'\n');
	#
	f.close();
	subprocess.call('chmod +x ./wallet/%s/run.sh'%coin,shell=True);
	#Verify installation
	if os.path.isfile(exec_path):
		return True;
	else:
		print(coin)
		raise;
		return False;


def install(coin,url,rpcport,p2pport,nodes='',specify_algo=''):
	current_dir=os.getcwd();
	exec_path=os.path.join(current_dir,'wallet',coin,'src',constant.executable[coin]);
	if os.path.isfile(exec_path):
		return True;
	#Download
	subprocess.call('git clone %s ./wallet/%s'%(url,coin),shell=True);
	if coin=='flaxscript':
		#flaxscript test is not implemented properly
		subprocess.call('cd wallet/%s/;git checkout ca31361fd09ff36e6f68e21d1c1d034213c93f44'%(coin),shell=True);
		#subprocess.call('cd wallet/%s/;./configure --with-incompatible-bdb --disable-tests'%(coin),shell=True);
	#Compile
	subprocess.call('chmod +x wallet/%s/autogen.sh'%(coin),shell=True);
	subprocess.call('chmod +x wallet/%s/share/genbuild.sh'%(coin),shell=True);
	subprocess.call('chmod +x wallet/%s/src/leveldb/build_detect_platform'%(coin),shell=True);
	subprocess.call('cd wallet/%s/;./autogen.sh'%(coin),shell=True);
	if coin=='ftc' or coin=='btx' or coin=='rvn':
		subprocess.call('cd wallet/%s/;./configure --enable-cxx --disable-shared --with-pic --with-incompatible-bdb CXXFLAGS="-fPIC" CPPFLAGS="-fPIC"'%(coin),shell=True);
	else:
		subprocess.call('cd wallet/%s/;./configure --with-incompatible-bdb'%(coin),shell=True);
	subprocess.call('cd wallet/%s/;make -j20'%(coin),shell=True);
	#Prepare data folders and run commands
	algo=constant.algo_lookup[coin];
	if type(algo)==list:
		for a in algo:
			datadir='wallet-data/%s-%s'%(coin,a);
			subprocess.call('mkdir %s'%(datadir),shell=True);
	else:
		datadir='wallet-data/%s-%s'%(coin,algo);
		subprocess.call('mkdir %s'%(datadir),shell=True);
	#
	#Create run commands
	f=open('./wallet/%s/run.sh'%coin,'w');
	current_dir=os.getcwd();
	exec_path=os.path.join(current_dir,'wallet',coin,'src',constant.executable[coin]);
	if type(algo)==list:
		if specify_algo=='':
			i=0;
			for a in algo:
				datadir=os.path.join(current_dir,'wallet-data','%s-%s'%(coin,a));
				command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,algo2name(coin,a),config.wallet_username,config.wallet_password,rpcport+i,p2pport+i,nodes);
				f.write(command+'\n');
				i=i+1;
			#
		else:
			datadir=os.path.join(current_dir,'wallet-data','%s-%s'%(coin,specify_algo));
			command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,algo2name(coin,specify_algo),config.wallet_username,config.wallet_password,rpcport,p2pport,nodes);
			f.write(command+'\n');
		#
	else:
		datadir=os.path.join(current_dir,'wallet-data','%s-%s'%(coin,algo));
		command='%s --datadir=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,config.wallet_username,config.wallet_password,rpcport,p2pport,nodes);
		f.write(command+'\n');
	#
	f.close();
	subprocess.call('chmod +x ./wallet/%s/run.sh'%coin,shell=True);
	#Verify installation
	if os.path.isfile(exec_path):
		return True;
	else:
		print(coin)
		raise;
		return False;


def purge(coin):
	#Stop processes
	ids=get_pid(constant.executable[coin]);
	for id in ids:
		subprocess.call('kill -9 %d'%id,shell=True);
	#Remove folder (but keeps wallet)
	subprocess.call('rm -rf wallet/%s'%coin,shell=True);
	return True;

def run():
	#run compiled wallets
	m=os.listdir('wallet/');
	for f in m:
		print('launching %s'%f)
		subprocess.call('chmod +x ./wallet/%s/run.sh'%f,shell=True);
		subprocess.call('wallet/%s/run.sh'%f,shell=True);
		time.sleep(2);
	#
	return True;
			
	