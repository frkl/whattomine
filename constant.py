#Whattomine.com API for a few coins
whattomine_lookup=dict();
whattomine_lookup['zec']={'name':'zec','url':'https://www.whattomine.com/coins/166.json','algorithm':'eqhash'}
whattomine_lookup['eth']={'name':'eth','url':'https://www.whattomine.com/coins/151.json','algorithm':'ethash'}
whattomine_lookup['dcr']={'name':'dcr','url':'https://www.whattomine.com/coins/152.json','algorithm':'decred'}
whattomine_lookup['sc']={'name':'sc','url':'https://www.whattomine.com/coins/161.json','algorithm':'sia'}
whattomine_lookup['xzc']={'name':'xzc','url':'https://www.whattomine.com/coins/175.json','algorithm':'lyra2z'}
whattomine_lookup['etc']={'name':'etc','url':'https://www.whattomine.com/coins/162.json','algorithm':'ethash'}
whattomine_lookup['grs']={'name':'grs','url':'https://www.whattomine.com/coins/48.json','algorithm':'groestl'};
whattomine_lookup['zcl']={'name':'zcl','url':'https://www.whattomine.com/coins/167.json','algorithm':'eqhash'};
whattomine_lookup['kmd']={'name':'kmd','url':'https://www.whattomine.com/coins/174.json','algorithm':'eqhash'};
whattomine_lookup['pasc']={'name':'pasc','url':'https://www.whattomine.com/coins/172.json','algorithm':'pascal'};
whattomine_lookup['btx']={'name':'btx','url':'https://www.whattomine.com/coins/202.json','algorithm':'bitcore'};
whattomine_lookup['btg']={'name':'btg','url':'https://www.whattomine.com/coins/214.json','algorithm':'eqhash'};

#What algos a coin use.
algo_lookup=dict();
algo_lookup['aur']=['skein','myr-gr'];
algo_lookup['log']='skein2';
algo_lookup['spr']='spread';
algo_lookup['xvg']=['x17','lyra2v2','myr-gr'];
algo_lookup['chc']='c11';
algo_lookup['xlr']='xevan';
algo_lookup['sigt']='skunk';
algo_lookup['boat']='hmq1725';
algo_lookup['mona']='lyra2v2';
algo_lookup['vtc']='lyra2v2';
algo_lookup['lbc']='lbry';
algo_lookup['btx']='bitcore';
algo_lookup['j']=['bastion','myr-gr','whirl','luffa','keccak','nist5','penta'];
algo_lookup['dgb']=['skein','myr-gr'];
algo_lookup['orb']='neoscrypt';
algo_lookup['ftc']='neoscrypt';
algo_lookup['bsd']='xevan';
algo_lookup['xre']='x11evo';
algo_lookup['bntly']='x17';
algo_lookup['mac']='timetravel';
algo_lookup['sib']='sib';
algo_lookup['grs']='groestl';
algo_lookup['myr']=['groestl','skein'];
algo_lookup['xzc']='lyra2z';
algo_lookup['altcom']='skunk';
algo_lookup['hsr']='hsr';
algo_lookup['lux']='phi';
algo_lookup['bern']='x14';
algo_lookup['max']='keccak';
algo_lookup['flax']='c11';
algo_lookup['dnr']='tribus';
algo_lookup['tzc']='neoscrypt';
algo_lookup['crea']='keccakc';
algo_lookup['btg']='eqhash';
algo_lookup['rvn']='x16r';
algo_lookup['nort']='xevan';
algo_lookup['ifx']='lyra2z';
algo_lookup['bwk']='nist5';
algo_lookup['proton']='x16r';



#These coins have multiple algos, getinfo()['pow_algo'] is used to check algo.
multi_algo_coins=['aur','dgb','myr','j','xvg'];


#keys to tell what wallet a port corresponds to
wallets_key=dict();
wallets_key['aur']='auroracoin';
wallets_key['log']='woodcoin';
wallets_key['spr']='spreadcoin';
wallets_key['chc']='chaincoin';
wallets_key['xlr']='solaris';
wallets_key['sigt']='signatum';
wallets_key['boat']='doubloon';
wallets_key['mona']='monacoin';
wallets_key['vtc']='vertcoin';
wallets_key['lbc']='lbrycrd';
wallets_key['btx']='bitcore';
wallets_key['j']='joincoin';
wallets_key['dgb']='digibyte';
wallets_key['ftc']='feathercoin';
wallets_key['bsd']='bitsend';
wallets_key['xre']='revolvercoin';
wallets_key['orb']='orbitcoin';
wallets_key['bntly']='bentleycoin';
wallets_key['grs']='groestlcoin';
wallets_key['mac']='machinecoin';
wallets_key['sib']='sibcoin';
wallets_key['myr']='myriad';
wallets_key['xvg']='VERGE';
wallets_key['xzc']='zcoin';
wallets_key['altcom']='altcommunity';
wallets_key['hsr']='hshare';
wallets_key['lux']='Lux';
wallets_key['bern']='BERN';
wallets_key['max']='maxcoin';
wallets_key['flax']='flaxscript';
wallets_key['tzc']='trezarcoin';
wallets_key['dnr']='denarius';
wallets_key['crea']='creativecoin';
wallets_key['rvn']='Raven';
wallets_key['nort']='northern';
wallets_key['ifx']='Infinex';
wallets_key['bwk']='Bulwark';
wallets_key['proton']='proton';

#executable names
executable=dict();
executable['log']='woodcoind';
executable['aur']='auroracoind';
executable['spr']='spreadcoind';
executable['orb']='orbitcoind';
executable['vlt']='veltord';
executable['chc']='chaincoind';
executable['j']='joincoind';
executable['altcom']='altcommunitycoind';
executable['boat']='doubloond';
executable['grs']='groestlcoind';
executable['ftc']='feathercoind';
executable['mac']='machinecoind';
executable['mona']='monacoind';
executable['flax']='flaxscriptd';
executable['lbc']='lbrycrdd';
executable['sib']='sibcoind';
executable['dgb']='digibyted';
executable['bsd']='bitsendd';
executable['hsr']='hshared';
executable['xlr']='solarisd';
executable['bern']='BERNd';
executable['max']='maxcoind';
executable['xre']='revolvercoind';
executable['btx']='bitcored';
executable['dnr']='denariusd';
executable['tzc']='trezarcoind';
executable['crea']='creativecoind';
executable['rvn']='ravend';
executable['nort']='northernd';
executable['ifx']='infinexd';
executable['bwk']='bulwarkd';
executable['proton']='protond';


#Exchange
exchange=dict();
exchange['zec']=['poloniex','BTC_ZEC']
exchange['etc']=['poloniex','BTC_ETC']
exchange['eth']=['poloniex','BTC_ETH']
exchange['dcr']=['poloniex','BTC_DCR']
exchange['sc']=['poloniex','BTC_SC']
exchange['pasc']=['poloniex','BTC_PASC']
exchange['aur']=['bittrex','BTC-AUR']
exchange['dgb']=['bittrex','BTC-DGB']
exchange['spr']=['bittrex','BTC-SPR']
exchange['xzc']=['bittrex','BTC-XZC']
exchange['ftc']=['bittrex','BTC-FTC']
exchange['lbc']=['bittrex','BTC-LBC']
exchange['vtc']=['bittrex','BTC-VTC']
exchange['xvg']=['bittrex','BTC-XVG']
exchange['mona']=['bittrex','BTC-MONA']
exchange['myr']=['bittrex','BTC-XMY']
exchange['zcl']=['bittrex','BTC-ZCL']
exchange['kmd']=['bittrex','BTC-KMD']
exchange['dmd']=['bittrex','BTC-DMD']
exchange['grs']=['bittrex','BTC-GRS']
exchange['bsd']=['bittrex','BTC-BSD']
exchange['sib']=['bittrex','BTC-SIB']
exchange['myr']=['bittrex','BTC-MYR']
exchange['xlr']=['coinmarketcap','solaris']
exchange['chc']=['cryptopia','CHC/BTC']
exchange['orb']=['cryptopia','ORB/BTC']
exchange['btx']=['cryptopia','BTX/BTC']
exchange['xre']=['cryptopia','XRE/BTC']
exchange['mac']=['cryptopia','MAC/BTC']
exchange['hsr']=['cryptopia','HSR/BTC']
exchange['lux']=['cryptopia','LUX/BTC']
exchange['bwk']=['cryptopia','BWK/BTC']
exchange['log']=['ccex','log-btc']
exchange['boat']=['tradesatoshi','BOAT_BTC']
exchange['sigt']=['coinmarketcap','signatum']
exchange['j']=['tradesatoshi','J_BTC']
exchange['bntly']=['','']; #no exchange available
exchange['altcom']=['yobit','altcom_btc'];
exchange['bern']=['cryptopia','BERN/BTC'];
exchange['max']=['yobit','max_btc'];
exchange['flax']=['cryptopia','FLAX/BTC'];
exchange['tzc']=['cryptopia','TZC/BTC'];
exchange['dnr']=['cryptopia','DNR/BTC'];
exchange['crea']=['cryptopia','CREA/BTC'];
exchange['btg']=['yobit','btg_btc'];
exchange['rvn']=['cryptobridge','RVN_BTC'];
exchange['nort']=['cryptobridge','NORT_BTC'];
exchange['ifx']=['cryptobridge','IFX_BTC'];
exchange['proton']=['cryptobridge','PROTON_BTC'];

def alias(orig,see,replace,name='',cond=''):
	if orig==see and name==cond:
		return replace;
	else:
		return orig;

def aliases(algo,coin):
	algo=alias(algo,'groestle','myr-gr','j',coin);
	algo=alias(algo,'groestle','groestl');
	algo=alias(algo,'groestl','myr-gr');
	algo=alias(algo,'myriad-groestl','myr-gr');
	algo=alias(algo,'pentablake','penta');
	algo=alias(algo,'whirlpool','whirl');
	algo=alias(algo,'whirlpoolx','whirl');
	algo=alias(algo,'lyra2re','lyra2v2');
	algo=alias(algo,'lyra2rev2','lyra2v2');
	algo=alias(algo,'blake2s','blake');
	return algo;

