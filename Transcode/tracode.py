#!/usr/bin/python
#-*- coding:iso-8859-1 -*-
import sys
#filename=raw_input("please input the file name:")
if(len(sys.argv)!=2):
    print "There is no filename!"
else:
    filename=sys.argv[1]
    fin=open(filename)
    lines=fin.readlines()
    fin.close()
    for line in lines:
        line2=line.decode("iso-8859-1").encode("utf-8")
        fout=open(filename,"a")
        fout.write(line2)
    fin.close()
