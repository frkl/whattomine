

import re
import json
import requests
from jsonrpc import ServiceProxy
import whattomine
import constant
import config


exchange=whattomine.exchange();
exchange.load('config/exchange.json');
exchange.update();


f=open('log.txt','r');
rewards=list();
for line in f:
	tmp=re.findall(r'Most profitable: ([^-]+)-(.+)\treward ([0-9.]+)\tamount ([0-9.]+)\ttimestamp ([0-9]+)',line);
	if len(tmp)==1:
		rewards.append(tmp[0]);

f.close();

if len(rewards)>0:
	d=dict();
	d_usd=dict();
	for i in range(0,len(rewards)-1):
		if not((rewards[i][0],rewards[i][1]) in d):
			d[(rewards[i][0],rewards[i][1])]=0;
			d_usd[(rewards[i][0],rewards[i][1])]=0;
		
		d[(rewards[i][0],rewards[i][1])]=d[(rewards[i][0],rewards[i][1])]+float(int(rewards[i+1][4])-int(rewards[i][4]))/86400*float(rewards[i][3]);
		d_usd[(rewards[i][0],rewards[i][1])]=d_usd[(rewards[i][0],rewards[i][1])]+float(int(rewards[i+1][4])-int(rewards[i][4]))/86400*float(rewards[i][2]);
	
	if len(rewards)>1:
		print('total %d seconds'%(int(rewards[len(rewards)-1][4])-int(rewards[0][4])));
		total_rewards=0;
		for c in d:
			print('%s-%s: %f\t%f'%(c[0],c[1],d[c],d_usd[c]));
			total_rewards=total_rewards+d_usd[c];
		
		print('Rewards so far: %f'%(total_rewards));
		print('Estimated 24h rewards: %f'%(total_rewards/float(int(rewards[len(rewards)-1][4])-int(rewards[0][4]))*86400));


total_balance_btc=0;
print('wallet balance');
for port in config.scan_ports:
	access=ServiceProxy({'url':config.scan_api%port,'username':config.wallet_username,'password':config.wallet_password},timeout=1);
	try:
		info=access.help();
		for coin in constant.wallets_key:
			if info.find(constant.wallets_key[coin])>0:
				if not(coin in constant.multi_algo_coins):
					v=access.getbalance();
					print('%s: %f'%(coin,v));
					total_balance_btc=total_balance_btc+v*exchange.tickers[coin];
					break;
				else:
					info2=access.getinfo();
					v=access.getbalance();
					print('%s-%s: %f'%(coin,info2['pow_algo'],v));
					total_balance_btc=total_balance_btc+v*exchange.tickers[coin];
		
	except:
		pass;


btc_usd=0;
try:
	coindesk_request=requests.get("http://api.coindesk.com/v1/bpi/currentprice.json",timeout=5);
	coindesk_btc=json.loads(coindesk_request.content);
	btc_usd=coindesk_btc['bpi']['USD']['rate_float'];
except:
	print('failed to get btc price');
print('Total net worth:\t\t%f BTC'%total_balance_btc);
print('\t\t\t\t%f USD'%(total_balance_btc*btc_usd));
