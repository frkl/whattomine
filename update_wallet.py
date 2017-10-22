import json
from jsonrpc import ServiceProxy
import constant
import config

wallets=dict();
#Add whattomine wallets
for coin in config.whattomine:
	wallets[coin]=constant.whattomine_lookup[coin];
	wallets[coin]['type']='whattomine';
	print('Added whattomine.com wallet for %s'%(coin));

#Add remote wallets
for coin in config.remote_wallets:
	wallets[coin]=config.remote_wallets[coin];
	print('Added remote wallet for %s'%(coin));


#Scan for local wallets
print('Scanning local wallets...');
cnt=0;
for port in config.scan_ports:
	access=ServiceProxy({'url':config.scan_api%port,'username':config.wallet_username,'password':config.wallet_password},timeout=5);
	try:
		info=access.help();
		identified=False;
		for coin in constant.wallets_key:
			if info.find(constant.wallets_key[coin])>0:
				identified=True;
				if not(coin in wallets):
					try:
						print('Found %s wallet at port %d'%(coin,port));
						wallets[coin]={'name':coin,'url':{'url':config.scan_api%port,'username':config.wallet_username,'password':config.wallet_password},'algorithm':constant.algo_lookup[coin],'type':'wallet'};
					except:
						print('error adding wallet');
		
		if not identified:
			print('Unidentified wallet: %s'%info);
		
	except:
		pass;
	cnt=cnt+1;
	#if (cnt*10)%len(config.scan_ports)==0:
	#	print('Progress: %d %%'%((cnt*100)/len(config.scan_ports)));

f=open('config/wallet.json','w');
json.dump(wallets,f);
f.close();
