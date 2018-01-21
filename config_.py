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
exchange_addr['xlr']='SREDC5vHJDJMx92JEFxS3yiFDNosp8tRAE'
exchange_addr['xre']='1H8aa35uamKw8WSe1L4p1Dbv26NGLwJsHV'
exchange_addr['bern']='BBfdUrekwFehS6EFUBnAijBeg59qJQ84wo'
exchange_addr['flax']='JJwBdcudRoh3hvjXhuN5Wo9Q9DvBdQZ4Cb'
exchange_addr['tzc']='ToDwu4gWZ9REwnsWgWAKgxvj6a6ASWasid'
exchange_addr['dnr']='DBeyQu5J4Go4AEGBnv1JxaY5RV7zVfPAy7'
exchange_addr['crea']='CJP7Y1xcBNpjT83HkdcKhKpchk8oWBAhkd'
exchange_addr['altcom']='ATWBzMqUUNwWTHJMWVo9Bf2zi4LCiRnYFa'
exchange_addr['max']='mWK1Q1eo4X1BBMhYwtW3GZTnFqttUE8eSJ'
exchange_addr['btx']='1NGhmGAVc2tSNtSKqCqAn8tEDw3b1a9kQJ'



#----------------MINERS-----------------
gpuinfo='export CUDA_VISIBLE_DEVICES=0,1,2,3;'
miner_efficiency=1;
#TODO: Benchmark all algorithms using corresponding miners and fill in your hashrates. 
#Enter hashrate in Mh/s
#Hashrates below are for 4x 1070.

hashrate=dict();
hashrate['timetravel']=90												#tpruvot 
hashrate['tribus']=210                                                  #tpruvot 
hashrate['cryptonight']=2450/pow(2.0,20)    				            #tpruvot 
hashrate['neoscrypt']=3.6                                               #tpruvot 
hashrate['lyra2v2']=160                                                 #alexis
hashrate['skein']=2000                                                  #alexis
hashrate['myr-gr']=245                                                  #alexis
hashrate['groestl']=133                                                 #tpruvot 
hashrate['spread']=29.0                                                 #sp-spread
hashrate['nist5']=195                                                   #alexis
hashrate['whirl']=187                                                   #alexis
hashrate['luffa']=1240                                                  #tpruvot 
hashrate['penta']=475                                                   #tpruvot 
hashrate['bastion']=47                                                  #tpruvot 
hashrate['keccak']=3025                                                 #alexis
hashrate['keccakc']=2710                                                #tpruvot
hashrate['x15']=36                                                      #alexis
hashrate['x14']=46                                                      #alexis
hashrate['skein2']=1700                                                 #alexis
hashrate['lbry']=1182                                                   #alexis
hashrate['xevan']=12.5													#krnlx
hashrate['lyra2z']=5.2                                                  #djm34
hashrate['eqhash']=1718/pow(2.0,21);                                    #ewbf sol/s->h/s
hashrate['ethash']=105;                                                 #claymore
hashrate['sia']=7000                                                    #alexis
hashrate['decred']=11060/pow(2.0,20)                                    #alexis
hashrate['skunk']=108                                                   #tpruvot 
hashrate['hmq1725']=17                                                  #tpruvot 
hashrate['x11evo']=61.77                                                #alexis
hashrate['blake2s']=15000                                               #alexis
hashrate['x17']=45                                                      #alexis
hashrate['c11']=63			                                            #alexis 
hashrate['sib']=47                                                      #alexis
hashrate['veltor']=128.7                                                #alexis
hashrate['pascal']=3880													#
hashrate['bitcore']=62                                                  #tpruvot
hashrate['hsr']=35							                            #tpruvot

#Wallet miners (algo,stratum,user,pass)
alexis='./miner/ccminer-alexis/ccminer -a %s -o %s -u %s -p %s  --scantime=5'
tpruvot='./miner/ccminer-tpruvot/ccminer -a %s -o %s -u %s -p %s  --scantime=5'
djm34='./miner/ccminer-djm34/ccminer -a %s -o %s -u %s -p %s'
spread='wine ./miner/ccminer-sp-spread9/spreadminer.exe %.0s -o %s -u %s -p %s'
penta='wine ./miner/ccminer-sp-penta/ccminer.exe -a %s -o %s -u %s -p %s'
krnlx='./miner/ccminer-krnlx/ccminer -a %s -o %s -u %s -p %s  --scantime=5'

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
I_wallet_mine.append(['j','myr-gr',alexis]);
I_wallet_mine.append(['xlr','xevan',krnlx]);
I_wallet_mine.append(['vlt','veltor',alexis]);
I_wallet_mine.append(['orb','neoscrypt',tpruvot]);
I_wallet_mine.append(['xre','x11evo',alexis]);
I_wallet_mine.append(['mac','timetravel',tpruvot]);
I_wallet_mine.append(['boat','hmq1725',tpruvot]);
I_wallet_mine.append(['bsd','xevan',krnlx]);
I_wallet_mine.append(['altcom','skunk',tpruvot]);
I_wallet_mine.append(['bern','x14',alexis]);
I_wallet_mine.append(['flax','c11',alexis]);
I_wallet_mine.append(['tzc','neoscrypt',tpruvot]);
#I_wallet_mine.append(['dnr','tribus',tpruvot]);
I_wallet_mine.append(['crea','keccakc',tpruvot]);
I_wallet_mine.append(['btx','bitcore',tpruvot]);

#I_wallet_mine.append(['lbc','lbry',alexis]);
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

eth_addr='0xd1fede8eaa0e3c4e2f1ebcd069dc6f8abe9abf2f.x'
dcr_addr='DsmJdGd8JtQNijg66JhUbC6BNwLVZnoUWnJ';
sia_addr='9ff06bc95bcf5d409514f9ae20a73b63653ce0c5f7fabef043fe749a8013905b1a91e1131830/x';
zec_addr='t1TDtxcYDrrWXsWHvr2s8LxFEsFCuCQzYeW.x'

i_decred=180;
i_sia=180;

ewbf_zec='./miner/ewbf-eqhash/miner --server %s --user %s --pass x'%(zec_pool,zec_addr)
ccminer_xzc=djm34%('lyra2z','stratum+tcp://us-east.lyra2z-hub.miningpoolhub.com:20581','grrrbot.grrr1','13457')

pool_miners=list();
pool_miners.append({'name':'xzc-lyra2z','command':ccminer_xzc,'pairs':[['xzc','lyra2z',hashrate['lyra2z']]]});
#pool_miners.append({'name':'zec-eqhash','command':ewbf_zec,'pairs':[['zec','eqhash',hashrate['eqhash']]]});
