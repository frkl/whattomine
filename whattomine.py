import requests
import json
import time
import re
from jsonrpc import ServiceProxy
import subprocess
import sys


def alias(orig,see,replace,name='',cond=''):
	if orig==see and name==cond:
		return replace;
	else:
		return orig;

#Query wallets, read latest difficulty and record latest rewards
class wallet:
	url=None;
	name='';
	algorithm='';
	K=100;
	access=None;
	reward_history_limit=10;
	
	height=0;
	reward_history=list();
	difficulty=dict();
	
	def __init__(self,conf):
		self.name=conf['name'];
		self.url=conf['url'];
		if 'algorithm' in conf:
			self.algorithm=conf['algorithm'];
		if 'K' in conf:
			self.K=conf['K'];
		self.access=ServiceProxy(self.url,timeout=5);
		self.reward_history=list();
		self.difficulty=dict();
	
	def getDifficulty(self,algo=''):
		try:
			if algo=='':
				return self.difficulty[self.algorithm];
			else:
				return self.difficulty[algo];
		except:
			return 1e10;
	
	def getReward(self):
		try:
			average_reward=sum([r[1] for r in self.reward_history])/len(self.reward_history);
			return average_reward;
		except:
			return 0;
	
	def getHeight(self):
		return self.height;
	
	
	def update(self,method='quick'):
		#Update info
		try:
			info=self.access.getinfo();
			
			#Load height
			height=info['blocks'];
			prev_height=self.height;
			self.height=height;
			
			#Load difficulty
			if isinstance(self.algorithm,basestring):
				#single algo wallet
				if 'difficulty' in info and isinstance(info['difficulty'],(int, long, float, complex)):
					self.difficulty[self.algorithm]=info['difficulty'];
				else:
					#work around for orbitcoin
					diff=self.access.getdifficulty();
					self.difficulty[self.algorithm]=diff['proof-of-work'];
			else:
				for algo in self.algorithm:
					try:
						key=algo;
						#handle aliases
						key=alias(key,'myr-gr','groestle','j',self.name);
						key=alias(key,'myr-gr','groestl');
						key=alias(key,'whirl','whirlpool');
						key=alias(key,'penta','pentablake');
						key=alias(key,'lyra2v2','lyra2re');
						key=alias(key,'blake2s','blake');
						key='difficulty_%s'%key;
						self.difficulty[algo]=info[key];
					except:
						print('Wallet %s: cannot find difficulty'%(self.name));
		
		except:
			print('Wallet %s: network error'%(self.name));
			return;
		
		if method!='quick':
			#Load blocks and compute block reward history
			i=max([0,height-self.K+1,prev_height+1]) #starts reading from 0, or current block, or K blocks before current
			while i<=height:
				try:
					hash=self.access.getblockhash(i);
					block=self.access.getblock(hash);
					
					if 'flags' in block and block['flags']=='proof-of-stake':
						#work around for hybrid POS/POW coins such as xlr
						pass;
					else:
						for txid in block['tx']:
							try:
								txhash=self.access.getrawtransaction(txid);
								tx=self.access.decoderawtransaction(txhash);
								coinbase_tx_cnt=sum([1 for vin in tx['vin'] if 'coinbase' in vin]);
								if coinbase_tx_cnt>0:
									#Read reward as sum of all coinbase transactions
									#Does not really work for coins with dev fees
									reward=sum([vout['value'] for vout in tx['vout']]);
									self.reward_history.append((i,reward));
									if len(self.reward_history)>self.reward_history_limit:
										self.reward_history.pop(0);
							except:
								#If such transaction was not in the wallet, it would be impossible to read the transaction
								#print('Wallet %s: error reading tx %s'%(self.name,txid));
								pass
					
				except:
					#print('Wallet %s: failed to read block hash %d/%d'%(self.name,i,height));
					return;
				
				i=i+1;
		
		return;

class whattomine:
	url=None;
	name='';
	algorithm='';
	
	height=0;
	reward=0;
	difficulty=None;
	def __init__(self,conf):
		self.name=conf['name'];
		self.url=conf['url'];
		self.algorithm=conf['algorithm'];
		self.difficulty=dict();
	
	def getDifficulty(self,algo=''):
		try:
			if algo=='':
				return self.difficulty[self.algorithm];
			else:
				return self.difficulty[algo];
		except:
			return 1e10;
	
	def getReward(self):
		return self.reward;
	
	def getHeight(self):
		return self.height;
	
	def update(self,method='quick'):
		blocks=dict();
		try:
			page=requests.get(self.url,timeout=5);
			#wait to reduce polling frequency
			time.sleep(1);
			data=json.loads(page.content);
			self.height=data['last_block'];
			self.reward=data['block_reward24'];
			if self.name=='kmd':
				#komodo work around
				self.difficulty[self.algorithm]=data['difficulty']/pow(2,41);
			elif self.name=='dmd' or self.name=='pasc' or self.name=='grs' or self.name=='xzc':
				#dmd work around
				self.difficulty[self.algorithm]=data['difficulty']/pow(2,0);
			else:
				self.difficulty[self.algorithm]=data['difficulty']/pow(2,32);
			
		except:
			print('Wallet %s: network error'%(self.name));
		return;

class wallet_manager:
	wallets=dict();
	def load(self,fname):
		try:
			f=open(fname,'r');
			data=json.load(f);
			f.close();
			#process wallets
			for name in data:
				if name in self.wallets and json.dumps(data[name]['url'])==json.dumps(self.wallets[name].url) and json.dumps(data[name]['algorithm'])==json.dumps(self.wallets[name].algorithm):
					pass;
				else:
					if data[name]['type']=='whattomine':
						self.wallets[name]=whattomine(data[name]);
					elif data[name]['type']=='wallet':
						self.wallets[name]=wallet(data[name]);
			
			#remove wallets that are not mentioned
			for name in self.wallets:
				if not (name in data):
					self.wallets.pop(name);
			
		except:
			print('Failed to load wallet info');
		return;
	
	def update(self,method='quick'):
		for name in self.wallets:
			self.wallets[name].update(method);
		return;

class chainz:
	url='http://chainz.cryptoid.info/explorer/api.dws?q=summary'
	name='';
	algorithm='';
	
	height=0;
	reward=0;
	difficulty=dict();
	def __init__(self,conf):
		self.name=conf['name'];
		self.reward=conf['reward'];
		self.algorithm=conf['algorithm'];
		self.difficulty=dict();
	
	def getDifficulty(self,algo=''):
		if algo=='':
			return self.difficulty[self.algorithm];
		else:
			return self.difficulty[algo];
	
	def getReward(self):
		return self.reward;
	
	def getHeight(self):
		return self.height;
	
	def update(self,method='quick'):
		try:
			page=requests.get(self.url,timeout=5);
			data=json.loads(unicode(page.content,errors='ignore'));
			self.height=data[self.name]['height'];
			self.difficulty[self.algorithm]=data[self.name]['diff'];
		except:
			print('Wallet %s: network error'%(self.name));
		return;

#Query exchanges, read price tags for coins of interest
class exchange:
	coins=dict();
	tickers=dict();
	bittrex_api='https://bittrex.com/api/v1.1/public/getmarketsummaries'
	poloniex_api='https://poloniex.com/public?command=returnTicker';
	ccex_api='https://c-cex.com/t/prices.json';
	cryptopia_api='https://www.cryptopia.co.nz/api/GetMarkets';
	yobit_api='https://yobit.net/api/3/ticker/';
	novaexchange_api='https://novaexchange.com/remote/v2/markets/';
	def __init__(self):
		self.tickers=dict();
		self.coins=dict();
	
	def load(self,fname):
		try:
			f=open(fname,'r');
			data=json.load(f);
			f.close();
			self.coins=data;
			#process into tuples
			for i in self.coins:
				self.coins[i]=tuple(self.coins[i]);
			
		except:
			print('Failed to load exchange info');
		return;
	
	def update(self):
		#Build a market to coin translation table
		tocoin=dict();
		for c in self.coins:
			if not (c in self.tickers):
				self.tickers[c]=0;
			tocoin[self.coins[c]]=c;
		
		
		#Bittrex
		try:
			r=requests.get(self.bittrex_api,timeout=5);
			tickers=json.loads(r.content);
			for t in tickers['result']:
				if ('bittrex',t['MarketName']) in tocoin:
					c=tocoin[('bittrex',t['MarketName'])];
					self.tickers[c]=t['Bid'];
			
		except:
			print('Exchange: error getting price from bittrex');
		
		#Poloniex
		try:
			r=requests.get(self.poloniex_api,timeout=5);
			tickers=json.loads(r.content);
			for market in tickers:
				if ('poloniex',market) in tocoin:
					c=tocoin[('poloniex',market)];
					self.tickers[c]=float(tickers[market]['highestBid']);
			
		except:
			print('Exchange: error getting price from poloniex');
		
		#C-Cex
		try:
			r=requests.get(self.ccex_api,timeout=5);
			tickers=json.loads(r.content);
			for market in tickers:
				if ('ccex',market) in tocoin:
					c=tocoin[('ccex',market)];
					self.tickers[c]=tickers[market]['buy'];
			
		except:
			print('Exchange: error getting price from ccex');
		
		#Cryptopia
		try:
			r=requests.get(self.cryptopia_api,timeout=5);
			tickers=json.loads(r.content);
			for t in tickers['Data']:
				if ('cryptopia',t['Label']) in tocoin:
					c=tocoin[('cryptopia',t['Label'])];
					self.tickers[c]=t['BidPrice'];
			
		except:
			print('Exchange: error getting price from cryptopia');
		
		#NovaExchange
		try:
			r=requests.get(self.novaexchange_api,timeout=10);
			tickers=json.loads(r.content);
			for t in tickers['markets']:
				if ('nova',t['marketname']) in tocoin:
					c=tocoin[('nova',t['marketname'])];
					self.tickers[c]=float(t['bid']);
			
		except:
			print('Exchange: error getting price from novaexchange');
		
		#Yobit
		#First craft the url
		yobit_url=self.yobit_api;
		n=0;
		for m in tocoin:
			if m[0]=='yobit':
				if n==0:
					yobit_url=yobit_url+m[1];
				else:
					yobit_url=yobit_url+'_'+m[1];
				n=n+1;
		
		print(yobit_url);
		#Now query website
		if n>0:
			try:
				r=requests.get(yobit_url,timeout=5);
				tickers=json.loads(r.content);
				for market in tickers:
					if ('yobit',market) in tocoin:
						c=tocoin[('yobit',market)];
						self.tickers[c]=tickers[market]['buy'];
				
			except:
				print('Exchange: error getting price from yobit');
		
		return;

class miners:
	prefix='';
	global_efficiency=1;
	hashrate=dict();
	miners=list();
	miner_profitability=list();
	general_profitability=list();
	current={'name':'','command':'','process':None,'time':-1,'expected_reward':[]};
	history=list();
	def __init__(self):
		self.hashrate=dict();
		self.miners=list();
		self.miner_profitability=list();
		self.general_profitability=list();
		self.history=list();
		self.current={'name':'','command':'','process':None,'time':-1,'expected_reward':[]};
	
	def load(self,fname):
		try:
			f=open(fname,'r');
			data=json.load(f);
			f.close();
			self.prefix=data['prefix'];
			self.global_efficiency=data['global_efficiency'];
			self.miners=data['miners'];
			self.hashrate=data['hashrate'];
			
		except:
			print('Failed to load miner info');
		return
	
	def compute_profitability(self,wallets,exchange):
		pairs=list();
		for coin in wallets.wallets:
			if isinstance(wallets.wallets[coin].algorithm,basestring):
				pairs.append((coin,wallets.wallets[coin].algorithm));
			else:
				for algo in wallets.wallets[coin].algorithm:
					pairs.append((coin,algo));
		
		profit=list();
		for p in pairs:
			hashrate=self.hashrate[p[1]];
			height=wallets.wallets[p[0]].getHeight();
			diff=wallets.wallets[p[0]].getDifficulty(p[1]);
			block_reward=wallets.wallets[p[0]].getReward();
			amount_24h=86400.0*hashrate/diff/float(pow(2,12))*block_reward;
			reward_btc_24h=amount_24h*exchange.tickers[p[0]];
			
			profit.append({'name':p[0],'algo':p[1],'amount_24h':amount_24h,'reward_btc_24h':reward_btc_24h,'diff':diff,'height':height,'block_reward':block_reward});
		
		profit=sorted(profit,key=lambda x:x['reward_btc_24h'],reverse=True);
		self.general_profitability=profit;
		return;
	
	def switch(self,wallets,exchange):
		profit=list();
		for m in self.miners:
			reward_btc=0;
			rewards=list();
			for p in m['pairs']:
				hashrate=p[2];
				try:
					diff=wallets.wallets[p[0]].getDifficulty(p[1]);
					block_reward=wallets.wallets[p[0]].getReward();
				except:
					#wallet does not exist
					diff=-1;
					block_reward=0;
				
				amount_24h=86400.0*hashrate/diff/float(pow(2,12))*block_reward*self.global_efficiency;
				reward_btc_24h=amount_24h*exchange.tickers[p[0]];
				rewards.append((p[0],amount_24h));
				reward_btc=reward_btc+reward_btc_24h;
			
			profit.append({'command':m['command'],'reward_btc':reward_btc,'name':m['name'],'rewards':rewards});
		
		profit=sorted(profit,key=lambda x:x['reward_btc'],reverse=True);
		self.miner_profitability=profit;
		most_profitable=profit[0];
		
		command=self.prefix+'exec ' + most_profitable['command'] + ' >miner.log 2>&1';
		if self.current['command']==command and self.current['process']!=None and self.current['process'].poll()==None:
			self.current['expected_reward']=most_profitable['rewards'];
			self.current['expected_reward_btc']=most_profitable['reward_btc'];
			self.current['time']=time.time();
		else:
			if not (self.current['process'] is None):
				try:
					self.current['process'].terminate();
					tmp=time.time();
					self.current['process'].wait();
					print(time.time()-tmp);
				except:
					print('failed to kill process...');
					self.current['process']=None;
			
			#Store history of the previous session
			#if self.current['command']!='':
			#	self.current['process']='';
			#	self.history.append(self.current);
			
			self.current=dict();
			self.current['process']=subprocess.Popen(command,stdout=subprocess.PIPE,shell=True);
			self.current['name']=most_profitable['name'];
			self.current['command']=command;
			self.current['expected_reward']=most_profitable['rewards'];
			self.current['expected_reward_btc']=most_profitable['reward_btc'];
			self.current['time']=time.time();
		
		return;