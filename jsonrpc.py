import json
import base64
from future.standard_library import install_aliases
install_aliases()
from urllib import request

class ServiceProxy(object):
	def __init__(self,gateway,service=None,timeout=None):
		self.gateway=gateway
		self.timeout=timeout
		self.service=service;

	def __getattr__(self,service):
		if self.service!=None:
			service="%s.%s" % (self.service,service)
		return ServiceProxy(self.gateway,service,self.timeout)
	
	def __call__(self,*args):
		data=json.dumps({"method":self.service,'params':args,'id':'jsonrpc'})
		auth=base64.encodestring('%s:%s'%(self.gateway['username'],self.gateway['password']))[:-1]
		req=request.Request(self.gateway['url'],data=data)
		req.add_header('Authorization','Basic %s'%auth)
		handle=request.urlopen(req,timeout=self.timeout);
		respdata=handle.read()
		resp=json.loads(respdata)
		if resp['error'] != None:
			raise JSONRPCException(resp['error'])
		else:
			return resp['result']
