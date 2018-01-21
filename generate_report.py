import re
import json
import requests
from jsonrpc import ServiceProxy
import whattomine
import constant
import config
import time
import sys

def Log(fname,str):
	print(str);
	sys.stdout.flush();
	f=open(fname,'a');
	f.write(str);
	f.close();
	return;

exchange=whattomine.exchange();
exchange.load('config/exchange.json');
exchange.update();
btc_usd=0;
try:
	coindesk_request=requests.get("http://api.coindesk.com/v1/bpi/currentprice.json",timeout=5);
	coindesk_btc=json.loads(coindesk_request.content);
	btc_usd=coindesk_btc['bpi']['USD']['rate_float'];
except:
	print('failed to get btc price');



result=[];
for port in config.scan_ports:
	access=ServiceProxy({'url':config.scan_api%port,'username':config.wallet_username,'password':config.wallet_password},timeout=5);
	try:
		info=access.help();
		for coin in constant.wallets_key:
			if info.find(constant.wallets_key[coin])>0:
				try:
					if not(coin in constant.multi_algo_coins):
						algo=constant.algo_lookup[coin];
					else:
						info2=access.getinfo();
						algo=info2['pow_algo'];
					txs=access.listtransactions('',100000000); #You won't mine more than that will you?
					txs=[tx for tx in txs if tx['category']=='generate'];
					result.append([coin,algo,txs]);
					break;
				except:
					print('Error reading wallet %s at port %d'%(coin,port));
					print('Could not generate report');
					raise;
					#error in reading wallet, very bad.
		#
	except:
		pass;

fname='report/generation_report_%d.json'%(time.time());
f=open(fname,'w');
json.dump(result,f);
f.close();

total_btc=0;
print('Report summary')
print('Pair\t\tGenerated\tHodl value(B)\tHodl value($)');
for item in result:
	subtotal=sum([tx['amount'] for tx in item[2]]);
	subtotal_btc=subtotal*exchange.tickers[item[0]];
	print('%s-%s  \t%f\t%f\t%f'%(item[0],item[1],subtotal,subtotal_btc,subtotal_btc*btc_usd));
	total_btc=total_btc+subtotal_btc;
print('Total hodl value:\t\t%f BTC'%total_btc);
print('\t\t\t\t%f USD'%(total_btc*btc_usd));
