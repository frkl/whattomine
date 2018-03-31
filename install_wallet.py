import wallet_manager
import subprocess
import sys
import os
import os.path


def install_vanilla(coin,url,exec_name,rpcport,p2pport,nodes='',specify_algo=''):
	#download
	subprocess.call('git clone %s ./%s'%(url,coin),shell=True);
	#compile
	subprocess.call('mv ./%s/src/makefile.unix ./%s/src/Makefile'%(coin,coin),shell=True);
	subprocess.call('chmod +x ./%s/src/leveldb/build_detect_platform'%(coin),shell=True);
	if coin=='solariscoin':
		subprocess.call('cd ./%s/src/leveldb/;make -j8'%(coin),shell=True);
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
		elif line.find('extern uint64_t nHashesPerSec;')>=0:
			#marker 1 v2 : add patch
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
 
#git remote set-url origin https://github.com/frkl/REPOSITORY.git
#git add -A
#git -c user.name='frkl' -c user.email='name@example.org' commit -m 'getwork'
#git push


wallet_manager.install_vanilla('log','https://github.com/funkshelper/woodcoin',6001,8001);
wallet_manager.install('aur','https://github.com/aurarad/Auroracoin',6011,8011);
wallet_manager.install_vanilla('spr','https://github.com/spreadcoin/spreadcoin',6021,8021);
wallet_manager.install_vanilla('orb','https://github.com/Orbitcoin/Orbitcoin',6031,8031);
wallet_manager.install('chc','https://github.com/chaincoin-legacy/chaincoin',6051,8051);
wallet_manager.install_vanilla('j','https://github.com/pallas1/joincoin',6061,8061,'-addnode=drtevq326tweby2k.onion:17941 -addnode=bfyswf2wu5ofqxyb.onion:17941 -addnode=gdhtrc7qoh3qowvf.onion:17941 -addnode=jzxs646bc3rajr3u.onion:17941 -addnode=p44az425ct7rhen6.onion:17941 -addnode=eldi5al5je6gw24u.onion:17941 -addnode=53zy47p5wly5penk.onion:17941 -addnode=vcn4cz4mhs4acnqd.onion:17941','keccak');
subprocess.call('mkdir ~/.joincoin',shell=True);

wallet_manager.install_vanilla('boat','https://github.com/OBAViJEST/boatcoinfinal',6081,8081);
wallet_manager.install('grs','https://github.com/frkl/groestlcoin',6091,8091);
wallet_manager.install('mac','https://github.com/frkl/machinecoin-core',6111,8111);

wallet_manager.install('ftc','https://github.com/frkl/Feathercoin',6101,8101); #lbry patch, not tested
wallet_manager.install('mona','https://github.com/frkl/monacoin',6121,8121); #not tested

wallet_manager.install('flax','https://github.com/thegreatoldone/flaxscript',6131,8131,' -addnode=107.191.104.244 -addnode=108.61.187.95 -addnode=13.228.216.184 -addnode=130.255.12.2 -addnode=130.255.12.3 -addnode=139.59.69.63 -addnode=158.69.248.93 -addnode=173.255.213.93 -addnode=184.164.129.202 -addnode=188.23.226.48 -addnode=192.155.85.40 -addnode=193.27.209.115 -addnode=42.3.86.79 -addnode=45.32.161.111 -addnode=45.50.48.252 -addnode=45.77.114.184 -addnode=45.79.68.185 -addnode=5.228.233.54 -addnode=51.15.162.15 -addnode=51.15.162.24 -addnode=61.92.170.78 -addnode=66.172.10.28 -addnode=69.202.152.251 -addnode=73.10.255.44 -addnode=76.74.178.146 -addnode=80.220.152.209'); 

wallet_manager.install('lbc','https://github.com/frkl/lbrycrd',6141,8141) #not tested
wallet_manager.install('sib','https://github.com/ivansib/sibcoin',6151,8151);
wallet_manager.install('dgb','https://github.com/frkl/digibyte',6161,8161); #not tested
wallet_manager.install('bsd','https://github.com/frkl/BitSend',6181,8181); #surprisingly low efficiency

wallet_manager.install_vanilla('hsr','https://github.com/HcashOrg/Hshare',6191,8191);
wallet_manager.install('xlr','https://github.com/frkl/Solaris',6201,8201,' -reindex');

wallet_manager.install_vanilla('max','https://github.com/Max-Coin/maxcoin',6221,8221,' -addnode=54.37.16.147:8668 -addnode=82.36.184.73:8668 -addnode=85.113.227.175:8668 -addnode=185.31.160.214:8668 -addnode=81.152.255.255:8668 -addnode=138.68.185.184:8668 -addnode=198.98.61.77:8668 -addnode=109.208.184.255:8668 -addnode=73.42.67.247:8668 -addnode=87.98.243.61:8668');

wallet_manager.install('xre','https://github.com/frkl/revolvercoin',6231,8231); 
wallet_manager.install('btx','https://github.com/frkl/BitCore',6241,8241);
#install_vanilla('denarius','https://github.com/carsenk/denarius','denariusd',6251,8251); #severe sync problems.
#install_vanilla('trezarcoin','https://github.com/TrezarCoin/TrezarCoin','trezarcoind',6261,8261);
#install('creativecoin','https://github.com/creativechain/creativechain-core','creativecoind',6281,8281,'',getwork_patch='btc');

wallet_manager.install('rvn','https://github.com/frkl/Ravencoin',6291,8291,' -reindex');
#./configure --enable-cxx --disable-shared --with-pic --prefix=$BDB_PREFIX CXXFLAGS="-fPIC" CPPFLAGS="-fPIC"
wallet_manager.install('nort','https://github.com/frkl/Northern',6301,8301,' -reindex');
wallet_manager.install('ifx','https://github.com/frkl/infinex',6311,8311);
