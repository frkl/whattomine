import re
import json
import requests
from jsonrpc import ServiceProxy
import whattomine
import constant
import config
import time
import sys
import os
import os.path

#Time
#24h 7d 30d 90d YTD
#
#Entries
#Total estimate/total actual
#Estimate/actual reward
#Entrance point/total duration
#payoff by duration stats

#Without BTC stats

#Read 

print('Reading report')
expected=[];
files=os.listdir('report/');
for fname in files:
	if fname.find('.log')>0:
		f=open(os.path.join('report/',fname),'r');
		for line in f:
			data=line.rstrip('\n').rstrip('\r').split('\t');
			if len(data)>0 and data[-1]=='verified':
				expected.append({'wallet':data[0],'usd_24h':float(data[1]),'amount_24h':float(data[2]),'time':int(data[3]),'net':data[4]});
		f.close();

expected=sorted(expected,key=lambda data:data['time']);


print('Loading wallet');
mined=[];
err=False;
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
					for tx in txs:
						 if tx['category']=='generate':
							mined.append({'wallet':'%s-%s'%(coin,constant.aliases(algo,coin)),'amount':float(tx['amount']),'time':int(tx['time'])});
					break;
				except:
					print('Error reading wallet %s at port %d'%(coin,port));
					print('Could not generate report');
					err=True;
					#error in reading wallet, very bad. Wallet is probably corrupted
		#
	except:
		pass;

if err:
	raise;

mined=sorted(mined,key=lambda data:data['time']);

print('Analyzing');

t0=max(mined[0]['time'],expected[0]['time']); #locate the first recording
#assign mint value to nearest record
exp_id=0;
for data in mined:
	if data['time']>t0:
		while expected[exp_id]['time']<data['time']:
			exp_id=exp_id+1;
		j=0;
		while j<10 and j>-10:
			if exp_id+j>=0 and exp_id+j<len(expected):
				if expected[exp_id+j]['wallet']==data['wallet']:
					break;
			if j>0:
				j=-j;
			else:
				j=-j+1;
		if not(expected[exp_id+j]['wallet']==data['wallet']):
			#This means mined coins in wallet somehow do not have corresponding mining reward records
			print('Could not register mined coins for %s'%data['wallet']);
		data['usd']=data['amount']/expected[exp_id+j]['amount_24h']*expected[exp_id+j]['usd_24h'];
#
tx=time.time();
result=dict();
#Total est
#Total register
for data in mined:
	if data['time']>t0:
		if not (data['wallet'] in result):
			result[data['wallet']]=dict();
			result[data['wallet']]['expected_usd_1d']=0;
			result[data['wallet']]['expected_usd_7d']=0;
			result[data['wallet']]['expected_usd_30d']=0;
			result[data['wallet']]['expected_usd_365d']=0;
			#
			result[data['wallet']]['usd_1d']=0;
			result[data['wallet']]['usd_7d']=0;
			result[data['wallet']]['usd_30d']=0;
			result[data['wallet']]['usd_365d']=0;
			#
			result[data['wallet']]['work_1d']=1e-7;
			result[data['wallet']]['work_7d']=1e-7;
			result[data['wallet']]['work_30d']=1e-7;
			result[data['wallet']]['work_365d']=1e-7;
		#
		if data['time']>tx-86400:
			result[data['wallet']]['usd_1d']+=data['usd'];
		if data['time']>tx-7*86400:
			result[data['wallet']]['usd_7d']+=data['usd'];
		if data['time']>tx-30*86400:
			result[data['wallet']]['usd_30d']+=data['usd'];
		if data['time']>tx-365*86400:
			result[data['wallet']]['usd_365d']+=data['usd'];


for i in range(0,len(expected)-1):
	data=expected[i];
	if data['time']>t0 and data['net']=='On':
		if not (data['wallet'] in result):
			result[data['wallet']]=dict();
			result[data['wallet']]['expected_usd_1d']=0;
			result[data['wallet']]['expected_usd_7d']=0;
			result[data['wallet']]['expected_usd_30d']=0;
			result[data['wallet']]['expected_usd_365d']=0;
			#
			result[data['wallet']]['usd_1d']=0;
			result[data['wallet']]['usd_7d']=0;
			result[data['wallet']]['usd_30d']=0;
			result[data['wallet']]['usd_365d']=0;
			#
			result[data['wallet']]['work_1d']=1e-7;
			result[data['wallet']]['work_7d']=1e-7;
			result[data['wallet']]['work_30d']=1e-7;
			result[data['wallet']]['work_365d']=1e-7;
		#
		work=expected[i+1]['time']-expected[i]['time'];
		if work>300:
			work=0;
		if data['time']>tx-86400:
			result[data['wallet']]['work_1d']+=work;
			result[data['wallet']]['expected_usd_1d']+=data['usd_24h']*work/86400.0;
		if data['time']>tx-7*86400:
			result[data['wallet']]['work_7d']+=work;
			result[data['wallet']]['expected_usd_7d']+=data['usd_24h']*work/86400.0;
		if data['time']>tx-30*86400:
			result[data['wallet']]['work_30d']+=work;
			result[data['wallet']]['expected_usd_30d']+=data['usd_24h']*work/86400.0;
		if data['time']>tx-365*86400:
			result[data['wallet']]['work_365d']+=work;
			result[data['wallet']]['expected_usd_365d']+=data['usd_24h']*work/86400.0;

print('1d');
print('Wallet  \tExpected\tActual\tUtilization(%)\tAverage Rate');
usd=0;
expected_usd=0;
work=0;
for wallet in result:
	usd=usd+result[wallet]['usd_1d'];
	expected_usd=expected_usd+result[wallet]['expected_usd_1d'];
	work=work+result[wallet]['work_1d'];
	print('%s \t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(wallet,result[wallet]['expected_usd_1d'],result[wallet]['usd_1d'],result[wallet]['work_1d']*100/86400.0,result[wallet]['expected_usd_1d']/result[wallet]['work_1d']*86400));
print('===============================================================')
print('subtotal\t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(expected_usd,usd,work*100/86400.0,expected_usd/work*86400));

print('\n')
print('7d');
print('Wallet  \tExpected\tActual\tUtilization(%)\tAverage Rate');
usd=0;
expected_usd=0;
work=0;
for wallet in result:
	usd=usd+result[wallet]['usd_7d'];
	expected_usd=expected_usd+result[wallet]['expected_usd_7d'];
	work=work+result[wallet]['work_7d'];
	print('%s \t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(wallet,result[wallet]['expected_usd_7d'],result[wallet]['usd_7d'],result[wallet]['work_7d']*100/86400.0/7,result[wallet]['expected_usd_7d']/result[wallet]['work_7d']*86400));
print('===============================================================')
print('subtotal\t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(expected_usd,usd,work*100/86400.0/7,expected_usd/work*86400));

print('\n')
print('30d');
print('Wallet  \tExpected\tActual\tUtilization(%)\tAverage Rate');
usd=0;
expected_usd=0;
work=0;
for wallet in result:
	usd=usd+result[wallet]['usd_30d'];
	expected_usd=expected_usd+result[wallet]['expected_usd_30d'];
	work=work+result[wallet]['work_30d'];
	print('%s \t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(wallet,result[wallet]['expected_usd_30d'],result[wallet]['usd_30d'],result[wallet]['work_30d']*100/86400.0/30,result[wallet]['expected_usd_30d']/result[wallet]['work_30d']*86400));
print('===============================================================')
print('subtotal\t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(expected_usd,usd,work*100/86400.0/30,expected_usd/work*86400));

print('\n')
print('365d');
print('Wallet  \tExpected\tActual\tUtilization(%)\tAverage Rate');
usd=0;
expected_usd=0;
work=0;
for wallet in result:
	usd=usd+result[wallet]['usd_365d'];
	expected_usd=expected_usd+result[wallet]['expected_usd_365d'];
	work=work+result[wallet]['work_365d'];
	print('%s \t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(wallet,result[wallet]['expected_usd_365d'],result[wallet]['usd_365d'],result[wallet]['work_365d']*100/86400.0/365,result[wallet]['expected_usd_365d']/result[wallet]['work_365d']*86400));
print('===============================================================')
print('subtotal\t%.02f\t\t%.02f\t%.02f\t\t%.02f'%(expected_usd,usd,work*100/86400.0/365,expected_usd/work*86400));