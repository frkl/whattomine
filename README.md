# whattomine
Simple switch mining script.

Mainly supports aur, spr, log, xlr, chc, vlt, boat and j.

Intended for hobby mining only.


## Install dependencies

For a fresh Ubuntu install, The following packages need to be installed.

```
sudo apt-get update
sudo apt-get install -y build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils python3 libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev qt4-qmake libqt4-dev libminiupnpc-dev libdb++-dev libdb-dev libcrypto++-dev libqrencode-dev libboost-all-dev build-essential libboost-system-dev libboost-filesystem-dev libboost-program-options-dev libboost-thread-dev libboost-filesystem-dev libboost-program-options-dev libboost-thread-dev libssl-dev libdb++-dev libssl-dev ufw libminiupnpc-dev libzmq3-dev python-pip git libcurl4-openssl-dev libpth-dev libgmp-dev
pip install future
```

## Install wallets

I have mostly streamlined wallet installation in install_wallet.py.

```
cd wallet/
python install_wallet.py
cd ..
```
The code will generate run_wallet.sh which is a script that runs all wallets. Run it on boot every time.

```
./wallet/run_wallet.sh
```

Quite a few coins use new bitcoin code and have dropped support for getwork which ccminer uses for solo-mining. I have developed patches that add getwork back to the code for some of the coins. I have successfully mined blocks for GRS and SIB. But some others like VTC, MONA, LBC and DGB are still being tested. 

## Install miners

Install Nvidia driver and CUDA. CUDA 7.5 or 8.0 are preferred because of miner support. 

For miners I personally use open source ccminer forks by [tpruvot](https://github.com/tpruvot/ccminer) and [alexis78](https://github.com/alexis78). Please donate to the authors to keep open source mining going.

```
mkdir miner
cd miner
git clone https://github.com/tpruvot/ccminer ccminer-tpruvot
cd ccminer-tpruvot;./build.sh;cd ..
git clone https://github.com/alexis78/ccminer ccminer-alexis
cd ccminer-alexis;./build.sh;cd ..
cd ..
```

You may also use other ccminer forks, as well as closed source miners if config.py is configured properly.

## Configure the profit switch script

Update exchange addresses with your addresses in config.py. You may also modify which coins you are mining, what username and password you are using for the wallets (need to be consistent with wallet/run_wallet.sh).

Make sure the wallets are running, and then run
```
python update_exchange.py
python update_wallet.py
python update_miner.py
```
Those commands will automatically scan which wallets are currently running through json-rpc APIs and generate config/exchange.json, config/wallet.json and config/miner.json.

## Run

Make sure all wallets are running and synced. Then use 

```
python main.py | tee log.txt
```

to run the program.

Use 

```
python calculate_reward.py
```
to check wallet balances.

Use 

```
python send_to_exchange.py
```
to send wallet coins to exchange addresses.

Use

```
python test_miners.py
```

to check if miners are able to mine into those wallets are not.

Hopefully this gives you a reason to buy cards for deep learning.
