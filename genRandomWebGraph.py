import sys
import random


if len(sys.argv) != 4:
    print "usage: python <node count> <vertices count> <random seed>"
    exit()

node = int(sys.argv[1])
vertice = int(sys.argv[2])
randomSeed = int(sys.argv[3])

if vertice >= node * (node-1) // 3:
    print "please decrease your vertice or increase your node"
    exit()

connected = set()
f = open("../sampleWork/sampleWebGraph_" + str(node) + "_" + str(vertice) + "_" + str(randomSeed) + ".txt", "w")

random.seed(randomSeed)
while len(connected) < vertice:
    a = random.randint(0, node-1)
    b = random.randint(0, node-1)
    if a == b or (a, b) in connected:
        continue
    connected.add((a, b))
    f.write(str(a))
    f.write(" ")
    f.write(str(b))
    f.write("\n")
f.close()
    
