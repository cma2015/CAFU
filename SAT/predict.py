import numpy as np
from Bio import SeqIO
import argparse, sys, os, pickle
from sklearn.metrics import roc_curve, auc, precision_recall_curve,average_precision_score


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-candidates", dest="candidateSeq", type=str, default=None,
                        help="The mixed coding sequences")
    parser.add_argument("-out", dest = "outDir", help = "The directory of output")
    parser.add_argument("-model", dest = "modelDir", default=None, help = "The directory of model")
    args = parser.parse_args()
    return args

posHex = "/home/chenzhuod/galaxy/tools/CAFU/SAT/puccinia_striiformis_cds.txt"
posBGHex = "/home/chenzhuod/galaxy/tools/CAFU/SAT/puccinia_striiformis_dna.txt"

negHex = "/home/chenzhuod/galaxy/tools/CAFU/SAT/wheat_cds.txt"
negBGHex = "/home/chenzhuod/galaxy/tools/CAFU/SAT/wheat_dna.txt"
hexamerScore = "/home/chenzhuod/galaxy/tools/CAFU/SAT/3_RF_hexamer.R"
featureEncoding = "/home/chenzhuod/galaxy/tools/CAFU/SAT/0_featureEncoding.sh"
canfeadir = "feature.txt"
canfea1dir = "fea1.txt"
canfea2dir = "fea2.txt"
os.chdir("/home/chenzhuod/galaxy/tools/CAFU/gcForest-master")

args = parse_args()

if args.modelDir == None:
    modelDir = "/home/chenzhuod/galaxy/tools/CAFU/SAT/gcForest_2257_plus_codon_bias.pkl"
else:
    modelDir = args.modelDir
   
    
candidateSeq = args.candidateSeq
outDir = args.outDir
cmd = featureEncoding + " " + candidateSeq + " " + canfeadir
os.system(cmd)
cmdfea1 = "Rscript " + hexamerScore + " -input " + candidateSeq + " -target " + posHex + " -bg " \
          + posBGHex + " -out " + canfea1dir
cmdfea2 = "Rscript " + hexamerScore + " -input " + candidateSeq + " -target " + negHex + " -bg " \
          + negBGHex + " -out " + canfea2dir

os.system(cmdfea1)
os.system(cmdfea2)

feature = np.loadtxt(canfeadir, dtype="string")
feature1 = np.loadtxt(canfea1dir, dtype="string")
feature1 = np.reshape(feature1, (len(feature1),1))
feature2 = np.loadtxt(canfea2dir, dtype="string")
feature2 = np.reshape(feature2, (len(feature2),1))
feature = np.concatenate((feature, feature1), axis=1)
feature = np.concatenate((feature, feature2), axis=1)

sys.path.insert(0, "lib")
from gcforest.gcforest import GCForest
with open(modelDir, "rb") as f:
    gc = pickle.load(f)

score = gc.predict_proba(feature)
mixedSeq = SeqIO.parse(candidateSeq, "fasta")
SeqID = [fasta.id for fasta in mixedSeq]
SeqID = np.array(SeqID)
SeqID = np.reshape(SeqID,(len(SeqID),1))

res = np.concatenate((SeqID, score), axis = 1)
np.savetxt(outDir + "mixed_transcripts_predict.txt", res, header = "\t".join(['transcripts','prob_negative','prob_positive']), delimiter="\t", fmt="%s")
