import json
import constant

f=open('config/exchange.json','w');
json.dump(constant.exchange,f);
f.close();
