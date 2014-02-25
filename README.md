Alien-Demo
==========
#ALIEN Demo FIA 2014 
##Software components for ALIEN project results' demonstration .

#--- POX Component ---
copy alien-demo1-pox.py to /pox/ext
run POX OF Controller: 
pox$>./pox.py alien-demo1-pox log --file=pox.log log.level --DEBUG

#--- Mininet network ---
deploy Mininet: 
mininet$> sudo python alien_topo.py
