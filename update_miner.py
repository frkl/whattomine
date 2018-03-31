import json
from jsonrpc import ServiceProxy
import config
import constant


#Prefix of commands and clocking
miners=dict();
miners['prefix']=config.gpuinfo;
miners['global_efficiency']=config.miner_efficiency;
miners['hashrate']=config.hashrate;
miners['miners']=list();

#Pool miners
for miner in config.pool_miners:
	miners['miners'].append(miner);

#Sniff wallets for automatic miners
def if_string_in(key,d):
	if isinstance(d,dict):
		if key in d:
			return d[key];
		else:
			return '';
	else:
		if key<len(d):
			return d[key];
		else:
			return '';

registered=dict();
for port in config.scan_ports:
	access=ServiceProxy({'url':config.scan_api%port,'username':config.wallet_username,'password':config.wallet_password},timeout=1);
	try:
		info=access.help();
		for pair in config.I_wallet_mine:
			if info.find(constant.wallets_key[pair[0]])>=0:
				if (pair[0],pair[1]) in registered:
					continue;
				if not(pair[0] in constant.multi_algo_coins):
					miners['miners'].append({'name':pair[0]+'-'+pair[1],'command':pair[2]%(pair[1],config.scan_api%port,config.wallet_username,config.wallet_password)+' '+if_string_in(3,pair),'pairs':[[pair[0],pair[1],config.hashrate[pair[1]]]]});
					registered[(pair[0],pair[1])]=1;
					break;
				else:
					info2=access.getinfo();
					if constant.aliases(info2['pow_algo'],pair[0])==constant.aliases(pair[1],pair[0]):
						miners['miners'].append({'name':pair[0]+'-'+pair[1],'command':pair[2]%(pair[1],config.scan_api%port,config.wallet_username,config.wallet_password)+' '+if_string_in(3,pair),'pairs':[[pair[0],pair[1],config.hashrate[pair[1]]]]});
						registered[(pair[0],pair[1])]=1;
						break;
		
	except:
		pass;


for miner in miners['miners']:
	print('Added miner for: %s'%(miner['name']));

f=open('config/miner.json','w');
json.dump(miners,f);
f.close();
