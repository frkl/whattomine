# whattomine
Simple switch mining script.

Mainly supports aur, spr, log, xlr, chc, vlt, boat and j.

Intended for hobby mining only.

## Install

Uses python2.7. Requires 
```
pip install future
```
Requires various ccminers for best results.

Requires wallets installed and running. Program will scan ports for wallets.

## Configure

Change wallet, exchange and miner settings in config.py. Then run
```
python update_exchange.py
python update_wallet.py
python update_miner.py
```
Those commands will generate config/exchange.json, config/wallet.json and config/miner.json.

## Run

Use 

```
python main.py
```

to run the program.

Hopefully this gives you a reason to buy cards for deep learning.
