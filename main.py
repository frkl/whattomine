import whattomine
import requests
import json
import time
import sys
import socket

update_exchange_every=600;
update_wallet_full_every=600;
update_wallet_every=15;
update_miner_every=15;

wallets=whattomine.wallet_manager();
wallets.load('config/wallet.json')
wallets.update('full'); 
time.sleep(0.3)


exchange=whattomine.exchange();
exchange.load('config/exchange.json');
exchange.update();
time.sleep(0.3)

miners=whattomine.miners();
miners.load('config/miner.json');
miners.compute_profitability(wallets,exchange);

#set timers
t_exchange=time.time()
t_exchange=t_exchange-t_exchange%update_exchange_every-update_exchange_every
t_wallet_full=time.time()
t_wallet_full=t_wallet_full-t_wallet_full%update_wallet_full_every-update_wallet_full_every
t_wallet=time.time()
t_wallet=t_wallet-t_wallet%update_wallet_every-update_wallet_every
t_miner=time.time()
t_miner=t_miner-t_miner%update_miner_every-update_miner_every


btc_usd=4000;
while True:
	t=time.time();
	#update exchange info
	if t>t_exchange+update_exchange_every:
		t_exchange=time.time();
		t_exchange=t_exchange-t_exchange%update_exchange_every
		exchange.load('config/exchange.json');
		exchange.update();
		time.sleep(0.3)
	
	if t>t_wallet_full+update_wallet_full_every:
		t_wallet_full=time.time()
		t_wallet_full=t_wallet_full-t_wallet_full%update_wallet_full_every
		wallets.load('config/wallet.json')
		wallets.update('full');
		time.sleep(0.3)
	
	if t>t_wallet+update_wallet_every:
		t_wallet=time.time()
		t_wallet=t_wallet-t_wallet%update_wallet_every
		wallets.update();
		time.sleep(0.3)
	
	#update miner and perform switching
	if t>t_miner+update_miner_every:
		t_miner=time.time()
		t_miner=t_miner-t_miner%update_miner_every
		miners.load('config/miner.json');
		miners.compute_profitability(wallets,exchange);
		miners.switch(wallets,exchange);
		try:
			coindesk_request=requests.get("http://api.coindesk.com/v1/bpi/currentprice/usd.json",timeout=5);
			coindesk_btc=json.loads(coindesk_request.content);
			btc_usd=coindesk_btc['bpi']['USD']['rate_float'];
		except:
			print('failed to get btc price');
		
		#Print basic stats
		print('BTC: %f'%(btc_usd))
		print('Profitability:')
		for l in miners.general_profitability:
			print('\t%s-%s\treward %f\tamount %f\ttimestamp %lu\tdiff %f\theight %d\tblock reward %f'%(l['name'],l['algo'],l['reward_btc_24h']*btc_usd,l['amount_24h'],time.time(),l['diff'],l['height'],l['block_reward']));
		
		print('Miners:')
		for l in miners.miner_profitability:
			print('\t%s\t\treward %f'%(l['name'],l['reward_btc']*btc_usd));
		
		print('Most profitable: %s\treward %f\tamount %f\ttimestamp %lu'%(miners.current['name'],miners.current['expected_reward_btc']*btc_usd,miners.current['expected_reward'][0][1],miners.current['time']));
		print('\n\n\n')
		sys.stdout.flush();
		
		#Check internet status
		net_connected='On';
		try:
			s=socket.create_connection(('8.8.8.8',53),1);
			net_connected='On';
		except:
			net_connected='Off';
		
		#keep a log of stats
		fname='report/switch_time%lue7.log'%int(miners.current['time']/10000000);
		try:
			f=open(fname,'a');
			f.write('\n')
			f.write('%s\t%f\t%f\t%lu\t%s\tverified'%(miners.current['name'],miners.current['expected_reward_btc']*btc_usd,miners.current['expected_reward'][0][1],miners.current['time'],net_connected));
			f.close();
		except:
			pass;
	
	time.sleep(1);
