#-----------------WALLETS-----------------
#Assuming username/password are the same for all wallets
#This is my username/password, Change them to yours
wallet_username='grrr';
wallet_password='13457';

#Automatically scan ports for wallets
#For each port, call wallet jsonrpc API to decide if 
#  - There's a wallet using that port
#  - Which wallet it is
#Define which ports to scan here
scan_api='http://127.0.0.1:%d';
scan_ports=range(6000,12000);

#For coins not suitable for wallet mining, check whattomine.com for blockchain status
#Specify which coins to monitor here
whattomine=['zec','eth','dcr','sc','xzc'];

#Specify non-local wallets, if any
remote_wallets=dict();
#Format: remote_wallets['coin']={'name':'coin','url':{'url':'http://ip.ip.ip.ip:port','username':'user','password':'pass'},'algorithm':'algo','type':'wallet'};


#-----------------EXCHANGE-----------------
#Which exchange addresses to send the coins to
#Create accounts on Bittrex, Cryptopia, C-Cex, Yobit, NovaExchange and Poloniex and create exchange addresses
#Remove lines coins which you are not sending to exchanges or you wish to do so manually
#TODO: Change my exchange addresses to your exchange addresses
exchange_addr=dict();
exchange_addr['aur']='ASqG874uv2PCo64AZhqR4uU1xopFbzGePa'
exchange_addr['orb']='oWrBy3xB2EAL6DcwCPz3bDCtkFcWG1dKqR'
exchange_addr['dgb']='DAVbWb3Ao72CkumCwaJLnPJYqxpn41F7qd'
exchange_addr['chc']='CYa38GJZbW6oq9cNT3GhtSUfafYFXEKVKV'
exchange_addr['skc']='Sj5NefeFu85A7K9nyKm3HkM5ir4zm6ZGDP'
exchange_addr['xvg']='DDAXvooye47NhbygoC418Hyw8CrMGmHH1m'
exchange_addr['spr']='SQgL2kP26jxACNFiDiiLkFyLEwSjMuPwRH'
exchange_addr['j']='JdXaXyxudbPsjxX6kyU5qW37j5odvWtk6P'
exchange_addr['log']='WR3EKWvGWkg9MNsR1Nknvk6iHM5MUW2f6i'
exchange_addr['vlt']='VbueM3wkqhVsjfm57XmHBTNAmmLgAwU1kF'
exchange_addr['ftc']='6pnrgffpoWsDp6Uf4C5gTvLGqcdbgmAYvS'
exchange_addr['boat']='BLihpqwt8wGPYLnFS7r3V1kC47qscXyDtc'
exchange_addr['grs']='FX7G6oaDMvvKyuZrDPF9UWzvgiJRhKDc1B'
exchange_addr['bsd']='iQFX64efzJwNZ5DjPHmXeXHhc3T3RXopzh'
exchange_addr['mac']='MREqeDeaMqhnUqF2WAcyH9tbzDJsPLhiG6'
exchange_addr['sib']='SZRS3oGYCzmvPnv28t8KapVBofEaecKnaG'
exchange_addr['xlr']='sMvt4bTZyWHYo8MfkMMCNjr2dq9YvoV8oh'
exchange_addr['xlrx']='SbMNqBPPt63uaVBr33jCwQutKpPqmcq4Go'



#----------------MINERS-----------------
gpuinfo='export CUDA_VISIBLE_DEVICES=0,1,2,3;'
miner_efficiency=1;
#TODO: Benchmark all algorithms using corresponding miners and fill in your hashrates. 
#Enter hashrate in Mh/s
#Hashrates below are for 4x 1080Ti.
hashrate=dict();
hashrate['timetravel']=150						#tpruvot 
hashrate['tribus']=400							#tpruvot 
hashrate['cryptonight']=3100/pow(2.0,20)		#tpruvot H/s->MH/s
hashrate['neoscrypt']=5.75						#tpruvot 
hashrate['lyra2v2']=285							#alexis
hashrate['skein']=3850							#alexis
hashrate['myr-gr']=490							#alexis
hashrate['groestl']=268							#tpruvot
hashrate['spread']=44.5							#sp-spread
hashrate['nist5']=340							#alexis
hashrate['whirl']=330							#alexis
hashrate['luffa']=1920							#tpruvot
hashrate['penta']=760							#sp-penta 
hashrate['bastion']=76.5						#tpruvot 
hashrate['keccak']=5400							#alexis
hashrate['x15']=79								#alexis
hashrate['skein2']=3350							#alexis
hashrate['lbry']=2000							#alexis
hashrate['yescrypt']=0
hashrate['xevan']=24
hashrate['lyra2z']=11							#tpruvot 
hashrate['eqhash']=2950/pow(2.0,21);			#ewbf sol/s->MH/s 
hashrate['ethash']=118;							#claymore
hashrate['decred-dual']=7100					#claymore
hashrate['sia-dual']=7100						#claymore
hashrate['sia']=12700							#alexis
hashrate['decred']=20000						#alexis
hashrate['skunk']=204							#tpruvot 
hashrate['hmq1725']=30							#tpruvot 
hashrate['x11evo']=90							#alexis
hashrate['blake2s']=29000						#alexis
hashrate['x17']=78								#alexis
hashrate['c11']=120								#alexis 
hashrate['sib']=90								#alexis
hashrate['veltor']=230							#alexis
hashrate['m7']=0
hashrate['pascal']=0
hashrate['bitcore']=104							#tpruvot
hashrate['hsr']=60							#tpruvot
hashrate['phi']=130							#tpruvot

#Wallet miners (algo,stratum,user,pass)
alexis='./miner/ccminer-alexis/ccminer -a %s -o %s -u %s -p %s'
tpruvot='./miner/ccminer-tpruvot/ccminer -a %s -o %s -u %s -p %s'
spread='wine ./miner/ccminer-sp-spread9/spreadminer.exe %.0s -o %s -u %s -p %s'
penta='wine ./miner/ccminer-sp-penta/ccminer.exe -a %s -o %s -u %s -p %s'
krnlx='./miner/ccminer-krnlx-xevan/ccminer -a %s -o %s -u %s -p %s'

#Specify which (coin,algorithm,miner) you use for wallet mining
#Make sure you 
#  -- Have that wallet
#  -- The wallet is synced
#Or you'll encounter errors
I_wallet_mine=list();
I_wallet_mine.append(['log','skein2',alexis,'-i 27.13']);
I_wallet_mine.append(['aur','myr-gr',alexis,'-i 23.13']);
I_wallet_mine.append(['aur','skein',alexis,'-i 23.13']);
I_wallet_mine.append(['spr','spread',spread,' -x 15']);
I_wallet_mine.append(['chc','c11',alexis,'-i 22']);
#I_wallet_mine.append(['xlr','nist5',alexis,'-i 21.13']);
I_wallet_mine.append(['vlt','veltor',alexis,'-i 25.13']);
I_wallet_mine.append(['boat','hmq1725',tpruvot,'-i 19.13']);
I_wallet_mine.append(['j','penta',penta]);
I_wallet_mine.append(['sib','sib',alexis,'-i 22.13']);
I_wallet_mine.append(['lbc','lbry',alexis,'-i 28.13']);
I_wallet_mine.append(['grs','groestl',tpruvot,'-i 19.13']);
I_wallet_mine.append(['mac','timetravel',tpruvot,'-i 20.13']);
I_wallet_mine.append(['ftc','neoscrypt',tpruvot,'-i 21.13']);
I_wallet_mine.append(['vtc','lyra2v2',alexis,'-i 22.13']);
I_wallet_mine.append(['mona','lyra2v2',alexis,'-i 22.13']);
I_wallet_mine.append(['dgb','myr-gr',alexis,'-i 23.13']);
I_wallet_mine.append(['dgb','skein',alexis,'-i 27.13']);
I_wallet_mine.append(['xvg','myr-gr',alexis,'-i 23.13']);
#I_wallet_mine.append(['xvg','x17',alexis]);
I_wallet_mine.append(['xvg','lyra2v2',alexis,'-i 22.13']);
I_wallet_mine.append(['bsd','xevan',krnlx,'-i 20.13']);
I_wallet_mine.append(['xlrx','xevan',krnlx,'-i 20.13']);
#I_wallet_mine.append(['lux','phi',tpruvot]);


#Pool miners
#Specify your pool mining commands and accounts.
#Register accounts on pools
#It's not that complicated but for fool-proof version, I have them disabled. 
#Pools are often dishonest anyway

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

claymore_dual_dcr='./miner/claymore-dual/ethdcrminer64 -epool %s -esm 1 -ewal %s -epsw x -dpool %s -dwal %s -dcoin dcr -dcri %d'%(eth_pool,eth_addr,dcr_pool,dcr_addr,i_decred);
claymore_dual_sia='./miner/claymore-dual/ethdcrminer64 -epool %s -esm 1 -ewal %s -epsw x -dpool %s -dwal %s -dcoin sia -dcri %d'%(eth_pool,eth_addr,sia_pool,sia_addr,i_sia);
ewbf_zec='./miner/ewbf-eqhash/miner --server %s --user %s --pass x'%(zec_pool,zec_addr)
tpruvot_xzc=tpruvot%('lyra2z','stratum+tcp://us-east.lyra2z-hub.miningpoolhub.com:20581','grrrbot.grrr3','13457')

pool_miners=list();
#pool_miners.append({'name':'eth-sc','command':claymore_dual_sia,'pairs':[['eth','ethash',hashrate['ethash']],['sc','sia',hashrate['sia-dual']]]});
#pool_miners.append({'name':'eth-dcr','command':claymore_dual_dcr,'pairs':[['eth','ethash',hashrate['ethash']],['dcr','decred',hashrate['decred-dual']]]});
#pool_miners.append({'name':'xzc-lyra2z','command':tpruvot_xzc,'pairs':[['xzc','lyra2z',hashrate['lyra2z']]]});
#pool_miners.append({'name':'zec-eqhash','command':ewbf_zec,'pairs':[['zec','eqhash',hashrate['eqhash']]]});
