
import urllib, urllib2, ast, json, collections, threading, time


# +------------------------------------------------------+
# | POX tests - ALIEN project results demonstration 
# | author: Lukasz Ogrodowczyk
# | Poznan Supercomputing and Networking Center
# | lukaszog@man.poznan.pl
# +------------------------------------------------------+

url = 'http://127.0.0.1:8888/OF/'

hardware_list = {
    "00-00-00-00-00-11":"EZappliance_PUT_1",
    "00-00-00-00-00-12":"EZappliance_PUT_2",
    "00-00-00-00-00-22":"EZappliance_PSNC",
    "00-00-00-00-00-33":"Caros.io"}
hardware_list = collections.OrderedDict(sorted(hardware_list.items(), key=lambda t: t[0]))

class bcolors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    RED = '\033[91m'
    YELLOW = "\033[93m"
    ENDC = '\033[0m'
    def disable(self):
        self.OKGREEN = ''
        self.FAIL = ''
        self.ENDC = ''

print bcolors.GREEN
print "---------------------------------------------------------------------------------------------------------"
print "---     Getting flow tables from all ALIEN OpenFlow-enabled switches registered to POX Controller    --- "
print "---------------------------------------------------------------------------------------------------------"
print bcolors.ENDC
for dpid in hardware_list.keys():
	req_get_flow_stats = json.dumps({"method":"get_flow_stats","params":{"dpid":dpid}, "id":3})
	request = urllib2.Request(url, req_get_flow_stats)
	response = urllib2.urlopen(request)
	respons_json = ast.literal_eval(response.read())
	print bcolors.BLUE+"\n*** ALIEN hardware: %s  [ dpid = %s ] ***"%(hardware_list[dpid], dpid) + bcolors.ENDC
	if "result" in respons_json:
		for k in range(len(respons_json["result"]["flowstats"])):
			#print "* %s: %s"%(k+1, respons_json["result"]["flowstats"][k])
			print bcolors.YELLOW+"* %s: "%(k+1)+bcolors.ENDC + "match: %s -> outport: %s"%\
			(respons_json["result"]["flowstats"][k]["match"], respons_json["result"]["flowstats"][k]["actions"][0]["port"])
	else:
		print respons_json
