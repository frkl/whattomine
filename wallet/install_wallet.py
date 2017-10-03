
import subprocess
import sys
import os
import os.path

wallet_username='grrr'
wallet_password='13457';
port=6001;
wallet_commands=list();

def install_vanilla(coin,url,exec_name,rpcport,p2pport,nodes='',specify_algo=''):
	#download
	subprocess.call('git clone %s ./%s'%(url,coin),shell=True);
	#compile
	subprocess.call('mv ./%s/src/makefile.unix ./%s/src/Makefile'%(coin,coin),shell=True);
	subprocess.call('chmod +x ./%s/src/leveldb/build_detect_platform'%(coin),shell=True);
	if coin=='solariscoin':
		subprocess.call('cd ./%s/src/leveldb/;make -j8'%(coin),shell=True);
	if coin=='veltor':
		subprocess.call('mkdir ./%s/src/obj'%(coin),shell=True);
		subprocess.call('cp ./Makefile_veltor ./%s/src/Makefile'%(coin),shell=True);
		subprocess.call('cp ./net_cpp_veltor ./%s/src/net.cpp'%(coin),shell=True);
		subprocess.call('cd %s/src/;make clean'%(coin),shell=True);
	subprocess.call('cd %s/src/;make -j8'%(coin),shell=True);
	#prepare command to run the coin
	current_dir=os.getcwd();
	exec_path=os.path.join(current_dir,coin,'src',exec_name);
	if coin in multi_algo and specify_algo=='':
		i=0;
		for algo in multi_algo[coin]:
			datadir=os.path.join(current_dir,coin,'data_%s'%algo);
			subprocess.call('mkdir %s'%(datadir),shell=True);
			command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,algo,wallet_username,wallet_password,rpcport+i,p2pport+i,nodes);
			wallet_commands.append(command);
			i=i+1;
	
	elif coin in multi_algo:
		datadir=os.path.join(current_dir,coin,'data');
		subprocess.call('mkdir %s'%(datadir),shell=True);
		command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,specify_algo,wallet_username,wallet_password,rpcport,p2pport,nodes);
		wallet_commands.append(command);
	else:
		datadir=os.path.join(current_dir,coin,'data');
		subprocess.call('mkdir %s'%(datadir),shell=True);
		command='%s --datadir=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,wallet_username,wallet_password,rpcport,p2pport,nodes);
		wallet_commands.append(command);
	
	return;

def patch_getwork(fname,patch_fname):
	subprocess.call('mv %s %s_'%(fname,fname),shell=True);
	source=open('%s_'%fname,'r');
	target=open('%s'%fname,'w');
	patch=open(patch_fname,'r');
	patched=0;
	for line in source:
		target.write(line);
		if line.find('using namespace std')>=0:
			#marker 1 : add patch
			for line_patch in patch:
				target.write(line_patch);
			patched=patched+1;
		elif line.find('&getblocktemplate')>=0:
			#marker 2 : add getwork RPC command
			if line.find('template_request')>=0:
				#new bitcoin code
				target.write('    { "mining",             "getwork",                &getwork,                true ,  {"template_request"} },\n');
			else:
				#old bitcoin code
				target.write('    { "mining",             "getwork",                &getwork,                true },\n');
			patched=patched+1;
	source.close();
	target.close();
	patch.close();
	if patched<2:
		raise Exception('Failed to install getwork patch on %s'%fname);
	return;

def install(coin,url,exec_name,rpcport,p2pport,nodes='',specify_algo='',getwork_patch=''):
	#download
	subprocess.call('git clone %s ./%s'%(url,coin),shell=True);
	current_dir=os.getcwd();
	if getwork_patch=='lbry':
		patch_getwork(os.path.join(current_dir,coin,'src','rpc','mining.cpp'),'getwork_patch_lbry_v1.cpp');
	elif getwork_patch=='btc':
		patch_getwork(os.path.join(current_dir,coin,'src','rpc','mining.cpp'),'getwork_patch_v2.cpp');
	elif getwork_patch=='digibyte':
		patch_getwork(os.path.join(current_dir,coin,'src','rpc','mining.cpp'),'getwork_patch_digibyte_v1.cpp');
	#compile
	subprocess.call('chmod +x ./%s/src/leveldb/build_detect_platform'%(coin),shell=True);
	subprocess.call('cd %s/;./autogen.sh'%(coin),shell=True);
	subprocess.call('cd %s/;./configure --with-incompatible-bdb'%(coin),shell=True);
	subprocess.call('cd %s/;make -j8'%(coin),shell=True);
	#prepare command to run the coin
	exec_path=os.path.join(current_dir,coin,'src',exec_name);
	if coin in multi_algo and specify_algo=='': #joincoin doesn't allow mining multiple instances.
		i=0;
		for algo in multi_algo[coin]:
			datadir=os.path.join(current_dir,coin,'data_%s'%algo);
			subprocess.call('mkdir %s'%(datadir),shell=True);
			command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,algo,wallet_username,wallet_password,rpcport+i,p2pport+i,nodes);
			wallet_commands.append(command);
			i=i+1;
	
	elif coin in multi_algo:
		datadir=os.path.join(current_dir,coin,'data');
		subprocess.call('mkdir %s'%(datadir),shell=True);
		command='%s --datadir=%s -algo=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,specify_algo,wallet_username,wallet_password,rpcport,p2pport,nodes);
		wallet_commands.append(command);
	else:
		datadir=os.path.join(current_dir,coin,'data');
		subprocess.call('mkdir %s'%(datadir),shell=True);
		command='%s --datadir=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,wallet_username,wallet_password,rpcport,p2pport,nodes);
		wallet_commands.append(command);
	
	return;

multi_algo=dict();
multi_algo['joincoin']=['groestle','skein','luffa','penta','bastion','nist5']
multi_algo['auroracoin']=['groestl','skein'];
multi_algo['digibyte']=['groestl','skein'];
multi_algo['myriadcoin']=['groestl','skein'];
multi_algo['verge']=['groestl','lyra2rev2','x17']

install_vanilla('woodcoin','https://github.com/funkshelper/woodcoin','woodcoind',6001,8001);
install('auroracoin','https://github.com/aurarad/Auroracoin','auroracoind',6011,8011);
install_vanilla('spreadcoin','https://github.com/spreadcoin/spreadcoin','spreadcoind',6021,8021);
install_vanilla('solariscoin','https://github.com/solariscoin/solariscoin','solariscoind',6031,8031);
install_vanilla('veltor','https://github.com/veltor/veltor-old','veltord',6041,8041);
install('chaincoin','https://github.com/chaincoin/chaincoin','chaincoind',6051,8051);
install_vanilla('joincoin','https://github.com/pallas1/joincoin','joincoind',6061,8061,'-addnode=drtevq326tweby2k.onion:17941 -addnode=bfyswf2wu5ofqxyb.onion:17941 -addnode=gdhtrc7qoh3qowvf.onion:17941 -addnode=jzxs646bc3rajr3u.onion:17941 -addnode=p44az425ct7rhen6.onion:17941 -addnode=eldi5al5je6gw24u.onion:17941 -addnode=53zy47p5wly5penk.onion:17941 -addnode=vcn4cz4mhs4acnqd.onion:17941','groestle');
subprocess.call('mkdir ~/.joincoin',shell=True);

#install_vanilla('signatum','https://github.com/signatumd/source','signatumd',6071,8071); --verified broken
install_vanilla('boatcoin','https://github.com/OBAViJEST/boatcoinfinal','doubloond',6081,8081);



install('groestlcoin','https://github.com/Groestlcoin/groestlcoin','groestlcoind',6091,8091,'',getwork_patch='btc');
install('feathercoin','https://github.com/FeatherCoin/Feathercoin','feathercoind',6101,8101,''); #not tested
install('machinecoin','https://github.com/machinecoin-project/machinecoin-core','machinecoind',6111,8111,'',getwork_patch='btc');
install('monacoin','https://github.com/monacoinproject/monacoin','monacoind',6121,8121,'',getwork_patch='btc'); #not tested
install('vertcoin','https://github.com/vertcoin/vertcoin','vertcoind',6131,8131,'',getwork_patch='btc'); #not tested
install('lbry','https://github.com/lbryio/lbrycrd','lbrycrdd',6141,8141,'',getwork_patch='lbry'); #not tested
install('sibcoin','https://github.com/ivansib/sibcoin','sibcoind',6151,8151,'');
install('digibyte','https://github.com/digibyte/digibyte','digibyted',6161,8161,'',getwork_patch='digibyte'); #not tested
install('verge','https://github.com/vergecurrency/VERGE','VERGEd',6171,8171); #need to download blockchain manually

run_file=open('run_wallet.sh','w');
for command in wallet_commands:
	run_file.write(command+'\n');
run_file.close();
subprocess.call('chmod +x ./run_wallet.sh',shell=True);
