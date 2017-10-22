# whattomine
Simple switch mining script.

Mainly supports aur, boat, bsd, chc, dgb, ftc, grs, hsr, j, log, mac, sib, vlt, xlr, xvg.

Intended for hobby mining only.


## Install dependencies

For a fresh Ubuntu install, the following packages need to be installed.

```
sudo apt-get update
sudo apt-get install -y build-essential libtool autotools-dev automake pkg-config libssl-dev libevent-dev bsdmainutils python3 libboost-system-dev libboost-filesystem-dev libboost-chrono-dev libboost-program-options-dev libboost-test-dev libboost-thread-dev qt4-qmake libqt4-dev libminiupnpc-dev libdb++-dev libdb-dev libcrypto++-dev libqrencode-dev libboost-all-dev build-essential libboost-system-dev libboost-filesystem-dev libboost-program-options-dev libboost-thread-dev libboost-filesystem-dev libboost-program-options-dev libboost-thread-dev libssl-dev libdb++-dev libssl-dev ufw libminiupnpc-dev libzmq3-dev python-pip git libcurl4-openssl-dev libpth-dev libgmp-dev
pip install future
```

Install Nvidia driver and CUDA. CUDA 7.5 or 8.0 are preferred because of miner support. 

I find adding the following lines into ~/.bashrc help

```
export CUDA_HOME=/usr/local/cuda/
export CPATH=/usr/local/cuda/include:$CPATH
export LIBRARY_PATH=/usr/local/cuda/lib64:/usr/local/ssl/lib:$LIBRARY_PATH
export PATH=/usr/local/cuda/bin:/usr/lib/i386-linux-gnu/:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64/:/usr/local/cuda/lib/:/usr/local/ssl/lib:$LD_LIBRARY_PATH
export DYLD_LIBRARY_PATH=/usr/local/cuda/lib64/:/usr/local/cuda/lib/:/usr/local/ssl/lib:$DYLD_LIBRARY_PATH
```


## Install wallets

I have mostly streamlined wallet installation in install_wallet.py.

```
cd wallet/
python install_wallet.py
cd ..
```
The code will download and compile all wallets and in the end generate run_wallet.sh which is a script that runs all wallets. Run it on boot every time.

```
./wallet/run_wallet.sh
```

Quite a few coins use new bitcoin code and have dropped support for getwork which ccminer uses for solo-mining. I have developed patches that add getwork back to some of those coins. I have successfully mined blocks for MAC, GRS, SIB, BSD and DGB. But some others like VTC, MONA, LBC and are still being tested. 

## Install miners

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

Important: update exchange addresses with your addresses in config.py. 

You may also update my hashrates with your actual hashrates (config_1080Ti, config_1080 and config_1070 has examples of 4 cards hashrates), modify which coins you are mining, what username and password you are using for the wallets (need to be consistent with wallet/run_wallet.sh).

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

to check if miners are able to mine into those wallets or not.

Hopefully this gives you a reason to buy cards for deep learning.
