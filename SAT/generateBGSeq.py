#! /usr/bin/env/ python
# _*_ coding:utf-8 _*_


import numpy as np
from Bio import SeqIO
import sys
import random

inputSeq = list(SeqIO.parse(sys.argv[1], "fasta"))
outputSeq = open(sys.argv[2], "w")
for fasta in inputSeq:
    name, sequence = fasta.id, str(fasta.seq)
    ranIdx = random.sample(range(0, len(sequence)), len(sequence))
    curNegSeq = np.array(list(sequence))[ranIdx]
    curNegSeq = ''.join(curNegSeq)
    outputSeq.write(">" + name  + "\n" + curNegSeq + "\n")

outputSeq.close()



