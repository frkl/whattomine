
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
	elif coin=='veltor':
		subprocess.call('mkdir ./%s/src/obj'%(coin),shell=True);
		subprocess.call('cp ./Makefile_veltor ./%s/src/Makefile'%(coin),shell=True);
		subprocess.call('cp ./net_cpp_veltor ./%s/src/net.cpp'%(coin),shell=True);
		subprocess.call('cd %s/src/;make clean'%(coin),shell=True);
	elif coin=='maxcoin':
		subprocess.call("sed -i 's/boost::get<const CScriptID&>(address)/boost::get<CScriptID>(address)/g' ./%s/src/rpcrawtransaction.cpp"%(coin),shell=True);
		subprocess.call("sed -i 's:/usr/lib/libminiupnpc.a:-lminiupnpc:g' ./%s/src/Makefile"%(coin),shell=True);
	elif coin=='coinonat':
		subprocess.call("sed -i 's:sudo::g' ./%s/src/leveldb/Makefile"%(coin),shell=True);
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
	elif coin=='altcommunity':
		#This coin doesn't like datadir. It defaults to ~/.
		command='%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,wallet_username,wallet_password,rpcport,p2pport,nodes);
		wallet_commands.append(command);
	else:
		datadir=os.path.join(current_dir,coin,'data');
		subprocess.call('mkdir %s'%(datadir),shell=True);
		command='%s --datadir=%s -server=1 -rpcuser=%s -rpcpassword=%s -rpcport=%d -port=%d %s &'%(exec_path,datadir,wallet_username,wallet_password,rpcport,p2pport,nodes);
		wallet_commands.append(command);
	#
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
	if coin=='flaxscript':
		#flaxscript test is not implemented properly
		subprocess.call('cd %s/;git checkout ca31361fd09ff36e6f68e21d1c1d034213c93f44'%(coin),shell=True);
		#subprocess.call('cd %s/;./configure --with-incompatible-bdb --disable-tests'%(coin),shell=True);
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
install_vanilla('orbitcoin','https://github.com/Orbitcoin/Orbitcoin','orbitcoind',6031,8031);
install_vanilla('veltor','https://github.com/veltor/veltor-old','veltord',6041,8041,' -addnode=2a01:4f8:201:6211::2101 -addnode=78.94.32.195 -addnode=2001:41d0:8:250e:: -addnode=veltor.suprnova.cc -addnode=178.33.228.14 -addnode=144.76.237.39 ');
install('chaincoin','https://github.com/chaincoin/chaincoin','chaincoind',6051,8051);
install_vanilla('joincoin','https://github.com/pallas1/joincoin','joincoind',6061,8061,'-addnode=drtevq326tweby2k.onion:17941 -addnode=bfyswf2wu5ofqxyb.onion:17941 -addnode=gdhtrc7qoh3qowvf.onion:17941 -addnode=jzxs646bc3rajr3u.onion:17941 -addnode=p44az425ct7rhen6.onion:17941 -addnode=eldi5al5je6gw24u.onion:17941 -addnode=53zy47p5wly5penk.onion:17941 -addnode=vcn4cz4mhs4acnqd.onion:17941','groestle');
subprocess.call('mkdir ~/.joincoin',shell=True);

install_vanilla('altcommunity','https://github.com/altcommunitycoin/altcommunitycoin-skunk/','altcommunitycoind',6071,8071);
install_vanilla('boatcoin','https://github.com/OBAViJEST/boatcoinfinal','doubloond',6081,8081);



install('groestlcoin','https://github.com/Groestlcoin/groestlcoin','groestlcoind',6091,8091,'',getwork_patch='btc');
install('feathercoin','https://github.com/FeatherCoin/Feathercoin','feathercoind',6101,8101,''); 
install('machinecoin','https://github.com/machinecoin-project/machinecoin-core','machinecoind',6111,8111,'',getwork_patch='btc');
install('monacoin','https://github.com/monacoinproject/monacoin','monacoind',6121,8121,''); #not tested
install('flaxscript','https://github.com/thegreatoldone/flaxscript','flaxscriptd',6131,8131,' -addnode=107.191.104.244 -addnode=108.61.187.95 -addnode=13.228.216.184 -addnode=130.255.12.2 -addnode=130.255.12.3 -addnode=139.59.69.63 -addnode=158.69.248.93 -addnode=173.255.213.93 -addnode=184.164.129.202 -addnode=188.23.226.48 -addnode=192.155.85.40 -addnode=193.27.209.115 -addnode=42.3.86.79 -addnode=45.32.161.111 -addnode=45.50.48.252 -addnode=45.77.114.184 -addnode=45.79.68.185 -addnode=5.228.233.54 -addnode=51.15.162.15 -addnode=51.15.162.24 -addnode=61.92.170.78 -addnode=66.172.10.28 -addnode=69.202.152.251 -addnode=73.10.255.44 -addnode=76.74.178.146 -addnode=80.220.152.209'); 
install('lbry','https://github.com/lbryio/lbrycrd','lbrycrdd',6141,8141,'',getwork_patch='lbry'); #not tested
install('sibcoin','https://github.com/ivansib/sibcoin','sibcoind',6151,8151,'');
install('digibyte','https://github.com/digibyte/digibyte','digibyted',6161,8161,'',getwork_patch='digibyte');
install('bitsend','https://github.com/LIMXTEC/BitSend','bitsendd',6181,8181,getwork_patch='btc'); 
install_vanilla('hshare','https://github.com/HcashOrg/Hshare','hshared',6191,8191);
install('solaris-xevan','https://github.com/frkl/Solaris','solarisd',6201,8201);
install_vanilla('berncash','https://github.com/BERNiecoin/BERNcash','BERNd',6211,8211);
install_vanilla('maxcoin','https://github.com/Max-Coin/maxcoin','maxcoind',6221,8221,' -addnode=54.37.16.147:8668 -addnode=82.36.184.73:8668 -addnode=85.113.227.175:8668 -addnode=185.31.160.214:8668 -addnode=81.152.255.255:8668 -addnode=138.68.185.184:8668 -addnode=198.98.61.77:8668 -addnode=109.208.184.255:8668 -addnode=73.42.67.247:8668 -addnode=87.98.243.61:8668');

install('revolvercoin','https://github.com/frkl/revolvercoin','revolvercoind',6231,8231,''); 
install('bitcore','https://github.com/LIMXTEC/BitCore','bitcored',6241,8241,'',getwork_patch='btc');
install_vanilla('denarius','https://github.com/carsenk/denarius','denariusd',6251,8251);
install_vanilla('trezarcoin','https://github.com/TrezarCoin/TrezarCoin','trezarcoind',6261,8261);
install('creativecoin','https://github.com/creativechain/creativechain-core','creativecoind',6281,8281,'',getwork_patch='btc');




run_file=open('run_wallet.sh','a');
for command in wallet_commands:
	print(command);
	run_file.write(command+'\n');
run_file.close();
subprocess.call('chmod +x ./run_wallet.sh',shell=True);
