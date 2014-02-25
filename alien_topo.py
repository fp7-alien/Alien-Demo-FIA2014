#!/usr/bin/python

''' ALIEN mininet tests '''

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.link import Intf
from mininet.node import RemoteController

n_Vswitch = 2

class MyTopo( Topo ):

    def __init__( self, n):

        # Initialize topology
        Topo.__init__( self )

        if n==3:
            # Add hosts 
            leftHost = self.addHost( 'h1' )

            #add swiches:
            ez1 = self.addSwitch( 's1-ez' )
            ez2 = self.addSwitch( 's2-ez' )
            ez3 = self.addSwitch( 's3-ez' )

            # Add links
            self.addLink( ez1, ez2, 1, 1)
            self.addLink( ez1, ez3, 2, 2)
            self.addLink( ez2, ez3, 2, 1)

            self.addLink( leftHost, ez1, 1, 3 )

        if n==2:
           # Add hosts 
            host = self.addHost( 'h1' )

            #add swiches:
            ez1 = self.addSwitch( 's1-ez' )
            ez3 = self.addSwitch( 's3-ez' )

            # Add links
            self.addLink( ez1, ez3, 1, 1)

            self.addLink( host, ez1, 1, 2 )        



if __name__ == '__main__':
    setLogLevel('info')
    topo = MyTopo(n_Vswitch)
    
    #set remote controller:
    from functools import partial
    net = Mininet( topo=topo, controller=partial( RemoteController, ip='10.134.0.20', port=6633 ) )
    
    if n_Vswitch==3:
        #add eth1 to s1-ez:
        switch = net.switches[ 0 ]
        _intf = Intf( "eth1", node=switch )

        #add sth2 to s2-ez:
        switch = net.switches[ 1 ]
        _intf = Intf( "eth2", node=switch )

    if n_Vswitch==2:
        #add eth3 and eth1 to s1-ez:
        switch = net.switches[ 0 ]
        _intf = Intf( "eth3", node=switch )
        _intf = Intf( "eth1", node=switch )

        #add eth2 to s3-ez:
        switch = net.switches[ 1 ]
        _intf = Intf( "eth2", node=switch )

    
    net.start()
    CLI(net)
    net.stop()
