
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

#Wallet miners (algo,stratum,user,pass)
alexis='./miner/ccminer-alexis/ccminer -a %s -o %s -u %s -p %s'
tpruvot='./miner/ccminer-tpruvot/ccminer -a %s -o %s -u %s -p %s'
spread='wine ./miner/ccminer-sp-spread9/spreadminer.exe %.0s -o %s -u %s -p %s'
krnlx='./miner/ccminer-krnlx-xevan/ccminer -a %s -o %s -u %s -p %s'

#Specify which (coin,algorithm,miner) you use for wallet mining
#Make sure you 
#  -- Have that wallet
#  -- The wallet is synced
#Or you'll encounter errors
I_wallet_mine=list();
I_wallet_mine.append(['log','skein2',alexis,'-i 27.13']);
#I_wallet_mine.append(['aur','myr-gr',alexis.'-i 23.13']);
#I_wallet_mine.append(['aur','skein',alexis,'-i 23.13']);
I_wallet_mine.append(['spr','spread',spread,' -x 15']);
I_wallet_mine.append(['chc','c11',alexis,'-i 22']);
I_wallet_mine.append(['xlr','nist5',alexis,'-i 21.13']);
I_wallet_mine.append(['vlt','veltor',alexis,'-i 25.13']);
I_wallet_mine.append(['boat','hmq1725',tpruvot,'-i 19.13']);
I_wallet_mine.append(['j','myr-gr',alexis,'-i 23.13']);
I_wallet_mine.append(['sib','sib',alexis,'-i 22.13']);
I_wallet_mine.append(['lbc','lbry',alexis,'-i 28.13']);
I_wallet_mine.append(['grs','groestl',tpruvot,'-i 19.13']);
I_wallet_mine.append(['mac','timetravel',tpruvot,'-i 20.13']);
I_wallet_mine.append(['ftc','neoscrypt',tpruvot,'-i 21.13']);
I_wallet_mine.append(['vtc','lyra2v2',alexis,'-i 22.13']);
I_wallet_mine.append(['mona','lyra2v2',alexis,'-i 22.13']);
I_wallet_mine.append(['dgb','myr-gr',alexis,'-i 23.13']);
I_wallet_mine.append(['dgb','skein',alexis,'-i 27.13']);
#I_wallet_mine.append(['xvg','myr-gr',alexis,'-i 23.13']);
#I_wallet_mine.append(['xvg','x17',alexis]);
#I_wallet_mine.append(['xvg','lyra2v2',alexis,'-i 22.13']);
I_wallet_mine.append(['bsd','xevan',krnlx,'-i 20.13']);
I_wallet_mine.append(['xlrx','xevan',krnlx,'-i 20.13']);


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
