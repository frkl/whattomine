
hashrate=dict();
hashrate['timetravel']=88.2												#tpruvot 
hashrate['tribus']=160                                                  #tpruvot mar
hashrate['cryptonight']=2450/pow(2.0,20)    				            #tpruvot mar
hashrate['neoscrypt']=3.8                                               #tpruvot mar
hashrate['lyra2v2']=160                                                 #alexis
hashrate['skein']=2120                                                  #alexis
hashrate['myr-gr']=280                                                  #alexis
hashrate['groestl']=150                                                 #tpruvot mar
hashrate['spread']=29.0                                                 #sp-spread
hashrate['nist5']=195                                                   #alexis
hashrate['whirl']=187                                                   #alexis
hashrate['luffa']=1240                                                  #tpruvot mar
hashrate['penta']=475                                                   #tpruvot mar
hashrate['bastion']=47                                                  #tpruvot mar
hashrate['keccak']=3025                                                 #alexis
hashrate['x15']=36                                                              #alexis
hashrate['skein2']=1810                                                 #alexis
hashrate['lbry']=1182                                                   #alexis
hashrate['yescrypt']=0
hashrate['xevan']=14
hashrate['lyra2z']=6.25                                                 #tpruvot mar
hashrate['eqhash']=1718/pow(2.0,21);                    #ewbf sol/s->h/s
hashrate['ethash']=105;                                                 #claymore
hashrate['decred-dual']=1485/pow(2.0,20)                #claymore
hashrate['sia-dual']=2300                                               #claymore
hashrate['sia']=7000                                                    #alexis
hashrate['decred']=11060/pow(2.0,20)                    #alexis
hashrate['skunk']=100                                                   #tpruvot mar
hashrate['hmq1725']=16.8                                                        #tpruvot mar
hashrate['x11evo']=61.77                                                        #alexis
hashrate['blake2s']=15000                                               #alexis
hashrate['x17']=45                                                              #alexis
hashrate['c11']=64			                                             #alexis adjusting for chaincoin coin distribution
hashrate['sib']=48                                                              #alexis
hashrate['veltor']=140                                                  #alexis
hashrate['m7']=0
hashrate['pascal']=3880
hashrate['bitcore']=58                                                  #tpruvot
hashrate['hsr']=35							#tpruvot


#Wallet miners (algo,stratum,user,pass)
alexis='../ccminer-alexis-oct2016/ccminer -a %s -o %s -u %s -p %s'
tpruvot='../ccminer-tpruvot-mar2017/ccminer -a %s -o %s -u %s -p %s'
spread='wine ../ccminer-sp-spread9/spreadminer.exe %.0s -o %s -u %s -p %s'

I_wallet_mine=list();
I_wallet_mine.append(['log','skein2',alexis]);
I_wallet_mine.append(['aur','myr-gr',alexis]);
I_wallet_mine.append(['aur','skein',alexis]);
I_wallet_mine.append(['spr','spread',spread,' -x 30']);
I_wallet_mine.append(['chc','c11',alexis]);
I_wallet_mine.append(['xlr','nist5',alexis]);
I_wallet_mine.append(['vlt','veltor',alexis]);
I_wallet_mine.append(['boat','hmq1725',tpruvot]);
I_wallet_mine.append(['j','keccak',alexis]);


#Pool miners
eth_pool='us1.ethermine.org:4444'
dcr_pool='stratum+tcp://yiimp.ccminer.org:3252'
sia_pool='stratum+tcp://sia-us-east1.nanopool.org:7777'
zec_pool='us1-zcash.flypool.org --port 13333'

eth_addr='0xd1fede8eaa0e3c4e2f1ebcd069dc6f8abe9abf2f.x'
dcr_addr='DsmJdGd8JtQNijg66JhUbC6BNwLVZnoUWnJ';
sia_addr='9ff06bc95bcf5d409514f9ae20a73b63653ce0c5f7fabef043fe749a8013905b1a91e1131830/x';
zec_addr='t1TDtxcYDrrWXsWHvr2s8LxFEsFCuCQzYeW.x'

i_decred=42;
i_sia=70;
