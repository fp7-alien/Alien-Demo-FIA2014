# Copyright 2013 <Your Name Here>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# +------------------------------------------------------+
# | POX component for ALIEN project results demonstration 
# | author: Lukasz Ogrodowczyk
# | Poznan Supercomputing and Networking Center
# | lukaszog@man.poznan.pl
# +------------------------------------------------------+


# Import some POX stuff
from pox.core import core                     # Main POX object
import pox.openflow.libopenflow_01 as of      # OpenFlow 1.0 library
import pox.lib.packet as pkt                  # Packet parsing/construction
from pox.lib.addresses import EthAddr, IPAddr # Address types
import pox.lib.util as poxutil                # Various util functions
import pox.lib.revent as revent               # Event library
import pox.lib.recoco as recoco               # Multitasking library
from pox.lib.util import dpid_to_str
from pox.lib.packet.arp import arp



# Create a logger for this component
log = core.getLogger()

CLIENT_A_IP_MN = "192.168.0.3"
SERVER_A_IP_MN = "192.168.0.4" 

CLIENT_A_IP = "10.0.0.3"
SERVER_A_IP = "10.0.0.4" 

IP_TO_ENABLE_RTSP_TRANS = "10.0.0.200"
IP_TO_DISABLE_RTSP_RTP_TRANS = "10.0.0.201"
IP_TO_ENABLE_RTSP_TRANS_MN = "192.168.0.200"
IP_TO_DISABLE_RTSP_RTP_TRANS_MN = "192.168.0.201"

#mininet configuration
EZ1_EZ2_PORT_MN = 1
EZ1_EZ3_PORT_MN = 2
EZ1_CLIENT_A_PORT_MN = 4
EZ2_EZ1_PORT_MN = 1
EZ2_EZ3_PORT_MN = 2
EZ2_SERVER_A_PORT_MN = 3
EZ3_EZ2_PORT_MN = 2
EZ3_EZ1_PORT_MN = 1

#alien hardware testbed configuration
EZPUT1_CAROS_PORT=1
EZPUT1_EZPSNC_PORT=2
EZPUT1_SRV_PORT=3
EZPSNC_EZPUT1_PORT=1
EZPSNC_EZPUT2_PORT=2
CAROS_EZPUT2_PORT=1
CAROS_EZPUT1_PORT=2
EZPUT2_EZPSNC_PORT=1
EZPUT2_CAROS_PORT=2
EZPUT2_CLIENT_PORT=3


'''
# dataModel structure:
dataModel 
  * dpid
    * match : action
    * proactive 
      * arp : action
      * icmp : action
      * web : action
'''

dataModel = {
  #mininet:
  "00-00-00-00-00-01":{
    "match":{
      "rtsp": [
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "dstport":8554, "outport":EZ1_EZ2_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "srcport":8554, "outport":EZ1_CLIENT_A_PORT_MN}
      ],
      "rtp" : [
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "dstport":[], "outport":EZ1_CLIENT_A_PORT_MN}
      ]
    }, 
    "proactive":{
      "arp": [      
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "ethtype":0x806, "outport":EZ1_EZ3_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "ethtype":0x806, "outport":EZ1_CLIENT_A_PORT_MN} 
      ],
      "icmp": [
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "ethtype":0x800, "outport":EZ1_EZ3_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "ethtype":0x800, "outport":EZ1_CLIENT_A_PORT_MN}
      ],
      "web" :[
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "dstport":80, "outport":EZ1_EZ3_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "srcport":80, "outport":EZ1_CLIENT_A_PORT_MN}
      ]
    }
  },
  "00-00-00-00-00-02":{
    "match":{
      "rtsp": [
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "dstport":8554, "outport":EZ2_SERVER_A_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "srcport":8554, "outport":EZ2_EZ1_PORT_MN}
      ],
      "rtp" : [
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "dstport":[], "outport":EZ2_EZ1_PORT_MN}
      ]
    }, 
    "proactive":{
      "arp": [      
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "ethtype":0x806, "outport":EZ2_SERVER_A_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "ethtype":0x806, "outport":EZ2_EZ3_PORT_MN} 
      ],
      "icmp": [
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "ethtype":0x800, "outport":EZ2_SERVER_A_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "ethtype":0x800, "outport":EZ2_EZ3_PORT_MN}
      ],
      "web" :[
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "dstport":80, "outport":EZ2_SERVER_A_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "srcport":80, "outport":EZ2_EZ3_PORT_MN}
      ]
    }
  },
  "00-00-00-00-00-03":{
    "match":{
      "rtsp": [],
      "rtp" : []
    }, 
    "proactive":{
      "arp": [      
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "ethtype":0x806, "outport":EZ3_EZ2_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "ethtype":0x806, "outport":EZ3_EZ1_PORT_MN} 
      ],
      "icmp": [
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "ethtype":0x800, "outport":EZ3_EZ2_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "ethtype":0x800, "outport":EZ3_EZ1_PORT_MN}
      ],
      "web" :[
        {"ipsrc":CLIENT_A_IP_MN, "ipdst":SERVER_A_IP_MN, "dstport":80, "outport":EZ3_EZ2_PORT_MN},
        {"ipsrc":SERVER_A_IP_MN, "ipdst":CLIENT_A_IP_MN, "srcport":80, "outport":EZ3_EZ1_PORT_MN}
      ]
    }
  },
  # --- ALIEN HW ---
  "00-00-00-00-00-11":{
    "match":{
      "rtsp": [
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "dstport":8554, "outport":EZPUT1_SRV_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "srcport":8554, "outport":EZPUT1_EZPSNC_PORT}
      ],
      "rtp" : [
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "dstport":[], "outport":EZPUT1_EZPSNC_PORT}
      ]
    }, 
    "proactive":{
      "arp": [      
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x806, "outport":EZPUT1_SRV_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x806, "outport":EZPUT1_CAROS_PORT} 
      ],
      "icmp": [
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x800, "outport":EZPUT1_SRV_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x800, "outport":EZPUT1_CAROS_PORT}
      ],
      "web" :[
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "dstport":80, "outport":EZPUT1_SRV_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "srcport":80, "outport":EZPUT1_CAROS_PORT}
      ]
    }
  },
  "00-00-00-00-00-12":{
    "match":{
      "rtsp": [
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "dstport":8554, "outport":EZPUT2_EZPSNC_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "srcport":8554, "outport":EZPUT2_CLIENT_PORT}
      ],
      "rtp" : [
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "dstport":[], "outport":EZPUT2_CLIENT_PORT}
      ]
    }, 
    "proactive":{
      "arp": [      
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x806, "outport":EZPUT2_CAROS_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x806, "outport":EZPUT2_CLIENT_PORT} 
      ],
      "icmp": [
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x800, "outport":EZPUT2_CAROS_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x800, "outport":EZPUT2_CLIENT_PORT}
      ],
      "web" :[
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "dstport":80, "outport":EZPUT2_CAROS_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "srcport":80, "outport":EZPUT2_CLIENT_PORT}
      ]
    }
  },
  "00-00-00-00-00-22":{
    "match":{
      "rtsp": [
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "dstport":8554, "outport":EZPSNC_EZPUT1_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "srcport":8554, "outport":EZPSNC_EZPUT2_PORT}
      ],
      "rtp" : [
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "dstport":[], "outport":EZPSNC_EZPUT2_PORT}
      ]
    }, 
    "proactive":{
      "arp": [      
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x806, "outport":EZPSNC_EZPUT1_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x806, "outport":EZPSNC_EZPUT2_PORT} 
      ],
      "icmp": [
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x800, "outport":EZPSNC_EZPUT1_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x800, "outport":EZPSNC_EZPUT2_PORT}
      ],
      "web" :[
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "dstport":80, "outport":EZPSNC_EZPUT1_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "srcport":80, "outport":EZPSNC_EZPUT2_PORT}
      ]
    }
  },
  "00-00-00-00-00-33":{
    "match":{
      "rtsp": [],
      "rtp" : []
    }, 
    "proactive":{
      "arp": [      
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x806, "outport":CAROS_EZPUT1_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x806, "outport":CAROS_EZPUT2_PORT} 
      ],
      "icmp": [
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "ethtype":0x800, "outport":CAROS_EZPUT1_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "ethtype":0x800, "outport":CAROS_EZPUT2_PORT}
      ],
      "web" :[
        {"ipsrc":CLIENT_A_IP, "ipdst":SERVER_A_IP, "dstport":80, "outport":CAROS_EZPUT1_PORT},
        {"ipsrc":SERVER_A_IP, "ipdst":CLIENT_A_IP, "srcport":80, "outport":CAROS_EZPUT2_PORT}
      ]
    }
  }        
}


def _go_up (event):
  # Event handler called when POX goes into up state
  # (we actually listen to the event in launch() below)
  log.info("ALIEN demo1 POX started!")

class AlienComponent (object):
  def __init__ (self, an_arg):
    self.arg = an_arg
    self.connection = {}
    self.RTSP_ENABLED = False #init

    core.openflow.addListeners(self)
    log.info("Alien Component instance registered with arg: %s", self.arg)
  
  def _handle_ConnectionUp (self, event):
    log.info("Switch %s has come up.", dpid_to_str(event.dpid))
    
    if not dpid_to_str(event.dpid) in dataModel:
      log.warning("dpid not in dataModel")  
    #log.debug("dataModel: %s"%dataModel)

    self.connection[dpid_to_str(event.dpid)] = event.connection

    # create ofp_flow_mod message to delete all flows
    msg = of.ofp_flow_mod(command=of.OFPFC_DELETE)
    #log.debug("delete Massage:%s ", msg.show())
    self.connection[dpid_to_str(event.dpid)].send(msg)
    log.debug("Clearing all flows from %s.",dpid_to_str(event.dpid))

    self.installFlowModProactive(dpid_to_str(event.dpid))   

  def _handle_ConnectionDown (self, event):
    self.connection = {}
    log.debug("bye ALIENs!")

  def _handle_PacketIn (self, event):
    packet = event.parsed
    dpid = event.dpid
    port = event.port
    log.debug("PacketIn received: %s | dpid: %s | port: %s | "%(packet, dpid, port))

    protocol_arp = packet.find('arp')
    if protocol_arp: 
        # not handled in proactive mode (e.g. other ipdst in arp payload)
        self.handleARP(event, protocol_arp)
    
    protocol_udp = packet.find('udp')
    if protocol_udp: 
        self.handleUDP(event, protocol_udp)


  def handleARP (self, event, protocol_arp):
   
    a = protocol_arp
    log.debug("Received: %s ARP %s %s => %s", dpid_to_str(event.dpid), {arp.REQUEST:"request",arp.REPLY:"reply"}.get(a.opcode,'op:%i' % (a.opcode,)), str(a.protosrc), str(a.protodst))

    #set path for RTSP:
    if (not self.RTSP_ENABLED)and((str(a.protodst) == IP_TO_ENABLE_RTSP_TRANS)or(str(a.protodst) == IP_TO_ENABLE_RTSP_TRANS_MN)):
      
      for dpid in dataModel.keys():
        log.debug("RTSP enabling. Installing Flow Modes for RTSP into switch %s"%dpid)

        if not dpid in self.connection:
          log.warning("Switch %s not connected to POX"%dpid)
          continue

        for i in dataModel[dpid]["match"]["rtsp"]:
          if "dstport" in i:
            self.connection[dpid].send( of.ofp_flow_mod( action=of.ofp_action_output( port=i["outport"] ),
                                                priority=1,
                                                match=of.ofp_match(nw_proto = pkt.ipv4.TCP_PROTOCOL,
                                                                  dl_type = pkt.ethernet.IP_TYPE,
                                                                  tp_dst=i["dstport"],
                                                                  nw_src=i["ipsrc"],
                                                                  nw_dst=i["ipdst"]
                                                                  )))   

          if "srcport" in i:
            self.connection[dpid].send( of.ofp_flow_mod( action=of.ofp_action_output( port=i["outport"] ),
                                                  priority=1,
                                                  match=of.ofp_match(nw_proto = pkt.ipv4.TCP_PROTOCOL,
                                                                    dl_type = pkt.ethernet.IP_TYPE,
                                                                    tp_src=i["srcport"],
                                                                    nw_src=i["ipsrc"],
                                                                    nw_dst=i["ipdst"]
                                                                    )))               
              
        self.RTSP_ENABLED = True      

    # disable path for RTSP and RTP:
    if (self.RTSP_ENABLED)and((str(a.protodst) == IP_TO_DISABLE_RTSP_RTP_TRANS)or(str(a.protodst) == IP_TO_DISABLE_RTSP_RTP_TRANS_MN)):                                                                 
      
      for dpid in dataModel.keys():
        log.debug("Deconfigure RTSP and RTP paths | dpid: %s"%dpid)
        
        if not dpid in self.connection:
          log.warning("Switch %s not connected to POX"%dpid)
          continue

        #disable path for RTSP:        
        for i in dataModel[dpid]["match"]["rtsp"]:
          if "dstport" in i:
            match = of.ofp_match(nw_proto = pkt.ipv4.TCP_PROTOCOL,  dl_type = pkt.ethernet.IP_TYPE,
                                                                    tp_dst=i["dstport"],
                                                                    nw_src=i["ipsrc"],
                                                                    nw_dst=i["ipdst"]
                                                                    )
            log.debug("Removing flow | dpid: %s match RTP: %s",dpid, match)
            self.connection[dpid].send( of.ofp_flow_mod(command=of.OFPFC_DELETE,
                                                  action=of.ofp_action_output( port=i["outport"] ),
                                                  priority=1,
                                                  match=match ))   

          if "srcport" in i:
            match = of.ofp_match(nw_proto = pkt.ipv4.TCP_PROTOCOL,  dl_type = pkt.ethernet.IP_TYPE,
                                                                    tp_src=i["srcport"],
                                                                    nw_src=i["ipsrc"],
                                                                    nw_dst=i["ipdst"]
                                                                    )
            log.debug("Removing flow | dpid: %s match RTSP: %s",dpid, match)             
            self.connection[dpid].send( of.ofp_flow_mod(command=of.OFPFC_DELETE,
                                                  action=of.ofp_action_output( port=i["outport"] ),
                                                  priority=1,
                                                  match=match))   
        
        #discable path for RTP:
        for i in dataModel[dpid]["match"]["rtp"]:
          for port in i["dstport"]:
            match = of.ofp_match(nw_proto = pkt.ipv4.UDP_PROTOCOL,  dl_type = pkt.ethernet.IP_TYPE,
                                                                    tp_dst=port,
                                                                    nw_src=i["ipsrc"],
                                                                    nw_dst=i["ipdst"]
                                                                    )
            log.debug("Removing flow | dpid: %s match RTP: %s",dpid, match)   
            self.connection[dpid].send( of.ofp_flow_mod(command=of.OFPFC_DELETE,
                                                  action=of.ofp_action_output( port=i["outport"] ),
                                                  priority=1,
                                                  match=match))           
 
        self.RTSP_ENABLED = False         

  def handleUDP (self, event, protocol_udp):
      
      #set path for RTP:
      if self.RTSP_ENABLED:
        log.debug("Handling UDP | protocol_udp: %s"%protocol_udp)
        dpid = event.dpid
        portUDP = protocol_udp.dstport

        for i in dataModel[dpid_to_str(dpid)]["match"]["rtp"]:
          if (i["ipsrc"]==event.parsed.payload.srcip)and(i["ipdst"]==event.parsed.payload.dstip):
            if portUDP not in i["dstport"]:
              i["dstport"].append(portUDP)
              self.connection[dpid_to_str(dpid)].send( of.ofp_flow_mod( action=of.ofp_action_output( port=i["outport"] ),
                                                    priority=1,
                                                    match=of.ofp_match(nw_proto = pkt.ipv4.UDP_PROTOCOL,
                                                                      dl_type = pkt.ethernet.IP_TYPE,
                                                                      tp_dst=portUDP,
                                                                      nw_src=i["ipsrc"],
                                                                      nw_dst=i["ipdst"]
                                                                      )))   
          else:
            log.warning("UDP packet not defined in dataModel!")  
            
      else:
        log.warning("RTSP is not enabled! UDP/RTP packets can't be exchanged")      

      #print "dataModel: %s"%dataModel

  def installFlowModProactive (self, dpid):
    log.debug("FlowMode installing - proactive mode | switch dpid: %s",dpid)
    
    #arp:
    for i in dataModel[dpid]["proactive"]["arp"]:
      self.connection[dpid].send( of.ofp_flow_mod( action=of.ofp_action_output( port=i["outport"] ),
                                            priority=1,
                                            match=of.ofp_match(dl_type=i["ethtype"], nw_src=i["ipsrc"], nw_dst=i["ipdst"])))
    
    #icmp:
    for i in dataModel[dpid]["proactive"]["icmp"]:
      self.connection[dpid].send( of.ofp_flow_mod( action=of.ofp_action_output( port=i["outport"] ),
                                            priority=1,
                                            match=of.ofp_match(nw_proto = pkt.ipv4.ICMP_PROTOCOL,
                                                              dl_type=i["ethtype"],
                                                              nw_src=i["ipsrc"],
                                                              nw_dst=i["ipdst"])))
      
                                                        
    #web:
    for i in dataModel[dpid]["proactive"]["web"]:
      if "dstport" in i:
        self.connection[dpid].send( of.ofp_flow_mod( action=of.ofp_action_output( port=i["outport"] ),
                                              priority=1,
                                              match=of.ofp_match(nw_proto = pkt.ipv4.TCP_PROTOCOL,
                                                                dl_type = pkt.ethernet.IP_TYPE,
                                                                tp_dst=i["dstport"]
                                                                #nw_src=i["ipsrc"],
                                                                #nw_dst=i["ipdst"]
                                                                )))      
      if "srcport" in i:
        self.connection[dpid].send( of.ofp_flow_mod( action=of.ofp_action_output( port=i["outport"] ),
                                              priority=1,
                                              match=of.ofp_match(nw_proto = pkt.ipv4.TCP_PROTOCOL,
                                                                dl_type = pkt.ethernet.IP_TYPE,
                                                                tp_src=i["srcport"]
                                                                #nw_src=i["ipsrc"],
                                                                #nw_dst=i["ipdst"]
                                                                )))      


@poxutil.eval_args
def launch (foo = False, bar = False):
  
  component = AlienComponent("demo1")
  core.register("alien", component)

  core.addListenerByName("UpEvent", _go_up)
  