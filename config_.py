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
whattomine=['zec','eth','xzc'];

#Specify non-local wallets, if any
remote_wallets=dict();
#Format: remote_wallets['coin']={'name':'coin','url':{'url':'http://ip.ip.ip.ip:port','username':'user','password':'pass'},'algorithm':'algo','type':'wallet'};


#-----------------EXCHANGE-----------------
#Which exchange addresses to send the coins to
#Create accounts on Bittrex, Cryptopia, C-Cex, Yobit, NovaExchange and Poloniex and create exchange addresses
#Remove lines coins which you are not sending to exchanges or you wish to do so manually
#TODO: Change my exchange addresses to your exchange addresses
exchange_addr=dict();
exchange_addr['aur']=''
exchange_addr['orb']=''
exchange_addr['dgb']=''
exchange_addr['chc']=''
exchange_addr['skc']=''
exchange_addr['xvg']=''
exchange_addr['spr']=''
exchange_addr['j']=''
exchange_addr['log']=''
exchange_addr['vlt']=''
exchange_addr['ftc']=''
exchange_addr['boat']=''
exchange_addr['grs']=''
exchange_addr['bsd']=''
exchange_addr['mac']=''
exchange_addr['sib']=''
exchange_addr['xlr']=''
exchange_addr['xre']=''
exchange_addr['bern']=''
exchange_addr['flax']=''
exchange_addr['tzc']=''
exchange_addr['dnr']=''
exchange_addr['crea']=''
exchange_addr['altcom']=''
exchange_addr['max']=''
exchange_addr['btx']=''




#----------------MINERS-----------------
gpuinfo='export CUDA_VISIBLE_DEVICES=0,1,2,3;'
miner_efficiency=1;
#TODO: Benchmark all algorithms using corresponding miners and fill in your hashrates. 
#Enter hashrate in Mh/s
#Hashrates below are for 4x 1070.

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
hashrate['penta']=690							#tpruvot 
hashrate['bastion']=76.5						#tpruvot 
hashrate['keccak']=5400							#alexis
hashrate['keccakc']=5350                                                #tpruvot
hashrate['x15']=79								#alexis
hashrate['x14']=85.9                                                      #alexis
hashrate['skein2']=3350							#alexis
hashrate['lbry']=2000							#alexis
hashrate['xevan']=24
hashrate['lyra2z']=11							#tpruvot 
hashrate['eqhash']=2950/pow(2.0,21);			#ewbf sol/s->MH/s 
hashrate['ethash']=130;							#claymore
hashrate['sia']=12700							#alexis
hashrate['decred']=20000						#alexis
hashrate['skunk']=204							#tpruvot 
hashrate['hmq1725']=30							#tpruvot 
hashrate['x11evo']=90							#alexis
hashrate['blake2s']=29000						#alexis
hashrate['x17']=78								#alexis
hashrate['x16r']=50							#ocminer/enemy 
hashrate['c11']=120								#alexis 
hashrate['sib']=90								#alexis
hashrate['veltor']=230							#alexis
hashrate['pascal']=0
hashrate['bitcore']=104							#tpruvot
hashrate['hsr']=60							#tpruvot

#Wallet miners (algo,stratum,user,pass)
alexis='./miner/ccminer-alexis/ccminer -a %s -o %s -u %s -p %s  --scantime=5'
tpruvot='./miner/ccminer-tpruvot/ccminer -a %s -o %s -u %s -p %s  --scantime=5'
djm34='./miner/ccminer-djm34/ccminer -a %s -o %s -u %s -p %s'
spread='wine ./miner/ccminer-sp-spread9/spreadminer.exe %.0s -o %s -u %s -p %s'
penta='wine ./miner/ccminer-sp-penta/ccminer.exe -a %s -o %s -u %s -p %s'
krnlx='./miner/ccminer-krnlx/ccminer -a %s -o %s -u %s -p %s  --scantime=5'
msft='./miner/ccminer_MSFT/ccminer -a %s -o %s -u %s -p %s  --scantime=5'

#Specify which (coin,algorithm,miner) you use for wallet mining
#Make sure you 
#  -- Have that wallet
#  -- The wallet is synced
#Or you'll encounter errors
I_wallet_mine=list();
I_wallet_mine.append(['dgb','myr-gr',alexis]);
I_wallet_mine.append(['dgb','skein',alexis]);
I_wallet_mine.append(['mona','lyra2v2',alexis]);
I_wallet_mine.append(['ftc','neoscrypt',tpruvot]);
I_wallet_mine.append(['sib','sib',alexis]);
I_wallet_mine.append(['aur','myr-gr',alexis]);
I_wallet_mine.append(['aur','skein',alexis]);
#I_wallet_mine.append(['spr','spread',spread,' -x 15']);
I_wallet_mine.append(['chc','c11',alexis]);
I_wallet_mine.append(['log','skein2',alexis]);
I_wallet_mine.append(['grs','groestl',tpruvot]);
I_wallet_mine.append(['j','keccak',alexis]);
I_wallet_mine.append(['xlr','xevan',krnlx]);
#I_wallet_mine.append(['vlt','veltor',alexis]);
I_wallet_mine.append(['orb','neoscrypt',tpruvot]);
I_wallet_mine.append(['xre','x11evo',alexis]);
I_wallet_mine.append(['mac','timetravel',tpruvot]);
#I_wallet_mine.append(['boat','hmq1725',tpruvot]);
I_wallet_mine.append(['bsd','xevan',krnlx]);
#I_wallet_mine.append(['altcom','skunk',tpruvot]);
#I_wallet_mine.append(['bern','x14',alexis]);
I_wallet_mine.append(['flax','c11',alexis]);
#I_wallet_mine.append(['tzc','neoscrypt',tpruvot]);
#I_wallet_mine.append(['dnr','tribus',tpruvot]);
#I_wallet_mine.append(['crea','keccakc',tpruvot]);
I_wallet_mine.append(['btx','bitcore',tpruvot]);
I_wallet_mine.append(['rvn','x16r',msft]);
I_wallet_mine.append(['nort','xevan',krnlx]);
I_wallet_mine.append(['ifx','lyra2z',tpruvot]);

I_wallet_mine.append(['lbc','lbry',alexis]);
#I_wallet_mine.append(['vtc','lyra2v2',alexis]);
#I_wallet_mine.append(['xvg','myr-gr',alexis]);
#I_wallet_mine.append(['xvg','x17',alexis]);
#I_wallet_mine.append(['xvg','lyra2v2',alexis]);
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

eth_addr=''
dcr_addr='';
sia_addr='';
zec_addr=''

i_decred=180;
i_sia=180;

ewbf_zec='./miner/ewbf-eqhash/miner --server %s --user %s --pass x'%(zec_pool,zec_addr)
ccminer_xzc=djm34%('lyra2z','stratum+tcp://us-east.lyra2z-hub.miningpoolhub.com:20581','grrrbot.grrr3','13457')
ethminer='./miner/ethminer/ethminer --farm-recheck 200 -U -S %s -O %s'%(eth_pool,eth_addr);

pool_miners=list();
pool_miners.append({'name':'xzc-lyra2z','command':ccminer_xzc,'pairs':[['xzc','lyra2z',hashrate['lyra2z']]]});
#pool_miners.append({'name':'zec-eqhash','command':ewbf_zec,'pairs':[['zec','eqhash',hashrate['eqhash']]]});
pool_miners.append({'name':'eth-ethash','command':ethminer,'pairs':[['eth','ethash',hashrate['ethash']]]});
