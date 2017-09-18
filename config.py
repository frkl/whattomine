#-----------------WALLETS-----------------
#Common username/password for wallets
wallet_username='user';
wallet_password='pass';
scan_api='http://127.0.0.1:%d';
scan_ports=range(6000,12000);  #Which ports to scan for wallets jsonrpc

#Which coins to monitor at whattomine.com
whattomine=['zec','eth','dcr','sc','grs','xzc'];

#Specify remote wallets, if any
remote_wallets=dict();
#remote_wallets['coin']={'name':'coin','url':{'url':'http://ip.ip.ip.ip:port','username':'user','password':'pass'},'algorithm':'algo','type':'wallet'};



#-----------------EXCHANGE-----------------
#Which exchange addresses to send the coins to
exchange_addr=dict();
exchange_addr['aur']='AHNs7BiKkyUzQDgeomRoYxGoekBfGCeQbn'
exchange_addr['orb']='oYMJbeLdpMf5TBoYTF1JQ7Ahbi3bqMSKpL'
exchange_addr['dgb']='DMHTQ5MJoYgMRSk3XeL5frmpujDpwtmip1'
exchange_addr['chc']='CYa38GJZbW6oq9cNT3GhtSUfafYFXEKVKV'
exchange_addr['skc']='Sj5NefeFu85A7K9nyKm3HkM5ir4zm6ZGDP'
exchange_addr['xvg']='D7gdSJaPSF7p4MqXh8ioWNtHD7UhApPLK2'
exchange_addr['spr']='SVihb9U6aeegNqxFAiEXGjvuG5VvDz4uov'
exchange_addr['j']='JeHuqWdCoYRgW4b9cuEzgLuLjDdXSQA6qU'
exchange_addr['log']='WR3EKWvGWkg9MNsR1Nknvk6iHM5MUW2f6i'
exchange_addr['vlt']='VbueM3wkqhVsjfm57XmHBTNAmmLgAwU1kF'
exchange_addr['ftc']='72PUW7PT5L5aJJPW7LrngXi98xDTQWEsag'
exchange_addr['xlr']='sXijWryVFygAaNc1vgscfEMKpUiB6U5QBw'
exchange_addr['boat']='BJUVhBYnFDu3rpsWWE7bjfyXS5SRWPfFxP'




#----------------MINERS-----------------
gpuinfo='export CUDA_VISIBLE_DEVICES=1,2,3;';
miner_efficiency=1;
#hashrate
hashrate=dict();
hashrate['tribus']=300							#tpruvot 
hashrate['cryptonight']=2150/pow(2.0,32)		#tpruvot 
hashrate['neoscrypt']=4.2						#tpruvot 
hashrate['lyra2v2']=210							#alexis
hashrate['skein']=2860							#alexis
hashrate['myr-gr']=380							#alexis
hashrate['groestl']=190							#Klaust
hashrate['spread']=37.6							#sp-spread
hashrate['nist5']=260							#alexis
hashrate['whirl']=240							#alexis
hashrate['luffa']=0							#tpruvot
hashrate['penta']=0							#tpruvot 
hashrate['bastion']=58						#tpruvot 
hashrate['keccak']=4000							#alexis
hashrate['x15']=58							#alexis
hashrate['skein2']=2430							#alexis
hashrate['lbry']=1560							#alexis
hashrate['yescrypt']=0
hashrate['xevan']=0
hashrate['lyra2z']=8.1							#tpruvot 
hashrate['eqhash']=2020/pow(2.0,33);			#ewbf sol/s->h/s 
hashrate['ethash']=80;							#claymore
hashrate['decred-dual']=4800/pow(2.0,32)		#claymore
hashrate['sia-dual']=4800						#claymore
hashrate['sia']=9400							#alexis
hashrate['decred']=14800/pow(2.0,32)			#alexis
hashrate['skunk']=147							#tpruvot 
hashrate['hmq1725']=22							#tpruvot 
hashrate['x11evo']=68.0							#alexis
hashrate['blake2s']=21400						#alexis
hashrate['x17']=57								#alexis
hashrate['c11']=86/8.0*6.0						#alexis adjusting for chaincoin coin distribution
hashrate['sib']=65								#alexis
hashrate['veltor']=172							#alexis
hashrate['m7']=0
hashrate['pascal']=0
hashrate['bitcore']=75							#tpruvot

#Wallet miners (algo,stratum,user,pass)
alexis='../ccminer-alexis-oct2016/ccminer -a %s -o %s -u %s -p %s'
tpruvot='../ccminer-tpruvot-mar2017/ccminer -a %s -o %s -u %s -p %s'
spread='wine ../ccminer-sp-spread9/spreadminer.exe %.0s -o %s -u %s -p %s'

I_wallet_mine=list();
I_wallet_mine.append(['log','skein2',alexis]);
I_wallet_mine.append(['aur','myr-gr',alexis]);
I_wallet_mine.append(['aur','skein',alexis]);
I_wallet_mine.append(['spr','spread',spread,' -x 15']);
I_wallet_mine.append(['chc','c11',alexis]);
I_wallet_mine.append(['xlr','nist5',alexis]);
I_wallet_mine.append(['vlt','veltor',alexis]);
I_wallet_mine.append(['boat','hmq1725',tpruvot]);
I_wallet_mine.append(['j','myr-gr',alexis]);


#Pool miners
eth_pool='us1.ethermine.org:4444'
dcr_pool='stratum+tcp://yiimp.ccminer.org:3252'
sia_pool='stratum+tcp://sia-us-east1.nanopool.org:7777'
zec_pool='us1-zcash.flypool.org --port 13333'

eth_addr='0xd1fede8eaa0e3c4e2f1ebcd069dc6f8abe9abf2f.x'
dcr_addr='DsmJdGd8JtQNijg66JhUbC6BNwLVZnoUWnJ';
sia_addr='9ff06bc95bcf5d409514f9ae20a73b63653ce0c5f7fabef043fe749a8013905b1a91e1131830/x';
zec_addr='t1TDtxcYDrrWXsWHvr2s8LxFEsFCuCQzYeW.x'

i_decred=180;
i_sia=180;

claymore_dual_dcr='../claymore-dual-9.2/ethdcrminer64 -epool %s -esm 1 -ewal %s -epsw x -dpool %s -dwal %s -dcoin dcr -dcri %d'%(eth_pool,eth_addr,dcr_pool,dcr_addr,i_decred);
claymore_dual_sia='../claymore-dual-9.2/ethdcrminer64 -epool %s -esm 1 -ewal %s -epsw x -dpool %s -dwal %s -dcoin sia -dcri %d'%(eth_pool,eth_addr,sia_pool,sia_addr,i_sia);
ewbf_zec='../eqhash-ewbf-v0.33/miner --server %s --user %s --pass x'%(zec_pool,zec_addr)
tpruvot_xzc=tpruvot%('lyra2z','stratum+tcp://us-east.lyra2z-hub.miningpoolhub.com:20581','user.miner','pass')

pool_miners=list();
pool_miners.append({'name':'eth-sc','command':claymore_dual_sia,'pairs':[['eth','ethash',hashrate['ethash']],['sc','sia',hashrate['sia-dual']]]});
pool_miners.append({'name':'eth-dcr','command':claymore_dual_dcr,'pairs':[['eth','ethash',hashrate['ethash']],['dcr','decred',hashrate['decred-dual']]]});
pool_miners.append({'name':'xzc-lyra2z','command':tpruvot_xzc,'pairs':[['xzc','lyra2z',hashrate['lyra2z']]]});
#pool_miners.append({'name':'zec-eqhash','command':ewbf_zec,'pairs':[['zec','eqhash',hashrate['eqhash']]]});
