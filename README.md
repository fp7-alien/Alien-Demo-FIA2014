Alien-Demo FIA 2014 
==========
###Software components for ALIEN project results' demonstration.

#### POX Component 
- copy alien-demo1-pox.py to /pox/ext
- run POX OF Controller: 
```bash
pox$>./pox.py alien-demo1-pox log --file=pox.log log.level --DEBUG
```

#### Mininet network 
- deploy Mininet: 
```bash
mininet$> sudo python alien_mininet_topo_demo1.py
```

#### Demo1 web GUI
- deploy: copy the whole "demo_website" to HTTP server host directory
