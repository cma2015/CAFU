import matplotlib
matplotlib.use('Agg')
import numpy as np
from Bio import SeqIO
from sklearn.model_selection import StratifiedKFold
import os, math, sys, argparse, pickle
from sklearn.metrics import roc_curve, auc, precision_recall_curve,average_precision_score
import matplotlib.pyplot as plt
from scipy import interp


# Supposing that the following scripts are located in your directory
readHexamer = "/your/directory/RSeQC-2.6.5/scripts/read_hexamer.py"
generateBG = "/your/directory/SAT/generateBGSeq.py"
hexamerScore = "/your/directory/SAT/RF_hexamer.R"
featureEncoding = "/your/directory/SAT/featureEncoding.sh"

#saving pos1fea.txt, pos2fea.txt, neg1fea.txt, neg2fea.txt positive_feature.txt negative_feature.txt
#  in current working directory
posfea1dir = "pos1fea.txt"
posfea2dir = "pos2fea.txt"
negfea1dir = "neg1fea.txt"
negfea2dir = "neg2fea.txt"
#canfea1dir = "fea1.txt"
#canfea2dir = "fea2.txt"
#canfeadir = "feature.txt"
posOut = "positive_feature.txt"
negOut = "negative_feature.txt"


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-positive", dest = "posSeq", type = str, default = None,
                        help = "The positive CDS sequences in fasta format")
    parser.add_argument("-negative", dest ="negSeq", type = str, default = None,
                        help = "The negative CDS sequences in fasta format")
#    parser.add_argument("-candidates", dest="candidateSeq", type=str, default=None,
#                        help="The mixed coding sequences")
    parser.add_argument("-posBG", dest = "posBGSeq", type = str, default = None,
                        help = "The positive background sequences in fasta format")
    parser.add_argument("-negBG", dest="negBGSeq", type=str, default=None,
                        help="The negative background sequences in fasta format")
    parser.add_argument("-out", dest = "outDir", help = "The directory of output")
    parser.add_argument("-t", dest = "cpu", type = int, default = 1,
                        help="The number of threads")
    parser.add_argument("-k", dest="k", type=int, default = 5,
                        help = "The k-fold cross validation")
    parser.add_argument("-threshold", dest="threshold", type=float, default = None,
                        help = "The threshold used for classifying transcripts")
    args = parser.parse_args()
    return args


def get_toy_config(cpu):
    config = {}
    ca_config = {}
    ca_config["random_state"] = 0
    ca_config["max_layers"] = 10
    ca_config["early_stopping_rounds"] = 3
    ca_config["n_classes"] = 2
    ca_config["estimators"] = []
    ca_config["estimators"].append(
            {"n_folds": 5, "type": "XGBClassifier", "n_estimators": 10, "max_depth": 5,
             "objective": "binary:logistic", "silent": True, "nthread": cpu, "learning_rate": 0.1} )
    ca_config["estimators"].append({"n_folds": 5, "type": "RandomForestClassifier",
                                    "n_estimators": 10, "max_depth": None, "n_jobs": cpu})
    ca_config["estimators"].append({"n_folds": 5, "type": "ExtraTreesClassifier",
                                    "n_estimators": 10, "max_depth": None, "n_jobs": cpu})
    config["cascade"] = ca_config
    return config

def traingcForest(X_train, y_train, cpu = 1):
    config = get_toy_config(cpu = cpu)
    gc = GCForest(config)
    X_train_enc = gc.fit_transform(X_train, y_train)
    return gc

def evalModel(posScore, negScore, threshold = 0.5, beta = 2):
    TP = float(sum(posScore > threshold))
    TN = float(sum(negScore <= threshold))
    FN = float(len(posScore)-TP)
    FP = float(len(negScore)-TN)
    res = {}
    res['Sn'] = TP/(TP + FN)
    res['Sp'] = TN/(TN + FP)
    res['Pr'] = TP/(TP + FP)
    res['Acc'] = (TP+TN)/(TP+TN+FP+FN)
    res['Fscore'] = ((1+beta*beta)*res['Pr']*res['Sn'])/(beta*beta*res['Pr']+res['Sn'])
    res['MCC']=(TP*TN-FP*FN)/math.sqrt(((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN)))
    return res


def cross_validation(X, y, k, cpu):
    config = get_toy_config(cpu = cpu)
    classifier = GCForest(config)
    cv = StratifiedKFold(n_splits = k)
    res = {}
    i=1
    for train, test in cv.split(X, y):
        tt = classifier.fit_transform(X[train], y[train])
        yscore = classifier.predict_proba(X[test])
        tmpID = "fold_" + str(i)
        curDic = {}
        curDic["yscore"] = yscore
        curDic["ytest"] = y[test]
        res[tmpID] = curDic
        i = i + 1    
    return res


def plotROC(cvRes, out):
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)
    i = 1
    f = plt.figure()
    for fold in cvRes.keys():
        curFold = cvRes[fold]
        yscore = curFold["yscore"][:,1]
        ytest = curFold["ytest"]
        fpr, tpr, thresholds = roc_curve(ytest, yscore)
        tprs.append(interp(mean_fpr, fpr, tpr))
        tprs[-1][0] = 0.0
        roc_auc = auc(fpr, tpr)
        aucs.append(roc_auc)
        plt.plot(fpr, tpr, lw=1, alpha=0.3,
                 label='ROC fold %d (AUC = %0.2f)' % (i, roc_auc))
        i += 1
    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)
    plt.plot(mean_fpr, mean_tpr, color='b',
             label=r'Mean ROC (AUC = %0.2f $\pm$ %0.2f)' % (mean_auc, std_auc),
             lw=2, alpha=.8)
    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    plt.fill_between(mean_fpr, tprs_lower, tprs_upper, color='grey', alpha=.2,
                     label=r'$\pm$ 1 std. dev.')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    f.savefig(out + "ROC.pdf", bbox_inches='tight')
    return f

def plotPR(cvRes, out):
    yscores = []
    ytests = []
    i = 1
    f = plt.figure()
    for fold in cvRes.keys():
        curFold = cvRes[fold]
        yscore = curFold["yscore"][:, 1]
        ytest = curFold["ytest"]
        precision, recall, _ = precision_recall_curve(ytest, yscore)
        yscores.append(yscore)
        ytests.append(ytest)
        curAUC = average_precision_score(ytest, yscore)
        plt.plot(recall, precision, lw=1, alpha=0.3, label='PR fold %d (AUPR = %0.2f)' % (i, curAUC))
        i += 1

    yscores = np.concatenate(yscores)
    ytests = np.concatenate(ytests)
    precision, recall, _ = precision_recall_curve(ytests, yscores)
    plt.plot(recall, precision, color='b', lw=2, alpha=.8)
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.title('precision-recall curve')
    plt.legend(loc="lower right")
    f.savefig(out + "precision_recall.pdf", bbox_inches='tight')

def plotFscore(cvRes, out, beta = 1):
    i = 0
    f = plt.figure()
    thresVec = [float(i+1)/float(1000) for i in range(1000)]
    thresVec = thresVec[199:(len(thresVec)-100)]
    posScores = []
    negScores = []
    for fold in cvRes.keys():
        curFold = cvRes[fold]
        yscore = curFold["yscore"][:, 1]
        ytest = curFold["ytest"]
        pos_score = list(yscore[np.where(ytest == 1)])
        neg_score = list(yscore[np.where(ytest == 0)])
        posScores.extend(pos_score)
        negScores.extend(neg_score)
    posScores = np.array(posScores)
    negScores = np.array(negScores)
    FscoreVec = []
    for j in thresVec:
        curFscore = evalModel(posScore=posScores, negScore=negScores, threshold=j, beta=beta)["Fscore"]
        FscoreVec.append(curFscore)
    f = plt.figure()
    plt.plot(thresVec, FscoreVec, lw = 1, alpha = 0.3)
    plt.xlabel('Threshold')
    plt.ylabel('F1-score')
    #f.savefig(out + "Fscore.pdf", bbox_inches='tight')
    maxF = max(FscoreVec)
    res = thresVec[FscoreVec.index(maxF)]
    return res


def plotMeasures(cvRes, out, beta = 1, threshold = 0.5):
    i = 0
    thresVec = [float(i + 1) / float(1000) for i in range(1000)]
    thresVec = thresVec[199:(len(thresVec) - 100)]
    posScores = []
    negScores = []
    for fold in cvRes.keys():
        curFold = cvRes[fold]
        yscore = curFold["yscore"][:, 1]
        ytest = curFold["ytest"]
        pos_score = list(yscore[np.where(ytest == 1)])
        neg_score = list(yscore[np.where(ytest == 0)])
        posScores.extend(pos_score)
        negScores.extend(neg_score)
    posScores = np.array(posScores)
    negScores = np.array(negScores)
    Sn = evalModel(posScore = posScores, negScore = negScores, threshold = threshold)["Sn"]
    Sp = evalModel(posScore = posScores, negScore = negScores, threshold = threshold)["Sp"]
    Pr = evalModel(posScore = posScores, negScore = negScores, threshold = threshold)["Pr"]
    Acc = evalModel(posScore = posScores, negScore = negScores, threshold = threshold)["Acc"]
    MCC = evalModel(posScore = posScores, negScore = negScores, threshold = threshold)["MCC"]
    Fscore = evalModel(posScore = posScores, negScore = negScores, threshold = threshold)["Fscore"]
    predictScore = np.concatenate((posScores, negScores), axis = 0)
    Label = [1]*len(posScores) + [0]*len(negScores)
    AUPR = average_precision_score(Label,predictScore)
    fpr, tpr, thresholds = roc_curve(Label, predictScore)
    AUC = auc(fpr, tpr)
    x = ['Sn', 'Sp', 'Pr', 'Acc', 'MCC', 'Fscore', 'AUC', 'AUPR']
    y = [Sn, Sp, Pr, Acc, MCC, Fscore, AUC, AUPR]
    fig, ax = plt.subplots()
    width = 0.75  # the width of the bars
    ind = np.arange(len(y))  # the x locations for the groups
    ax.barh(ind, y, width, color = ['#FF0000FF', '#FFBF00FF', '#80FF00FF', '#00FF40FF', '#00FFFFFF', '#0040FFFF', '#8000FFFF', '#FF00BFFF'])
    for i, v in enumerate(y):
        ax.text(v + 3, i + .25, str(v), color='black', fontweight='bold')
    ax.set_yticks(ind + width / 2)
    ax.set_yticklabels(x, minor=False)
    plt.title('title')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(out + "measures.pdf", format='pdf',bbox_inches='tight')

args = parse_args()
posSeq = args.posSeq
posHex = posSeq + "_hexamer.txt"

#Generating positive background sequences
if args.posBGSeq == None:
    tmpcmd1 = "/usr/bin/python " + generateBG + " " + posSeq + " " + posSeq + "_BG.fa"
    os.system(tmpcmd1)
    posBGSeq = posSeq + "_BG.fa"
else:
    posBGSeq = args.posBGSeq
posBGHex = posBGSeq + "_hexamer.txt"

#Generating negative background sequences
negSeq = args.negSeq
negHex = negSeq + "_hexamer.txt"
if args.negBGSeq == None:
    tmpcmd2 = "/usr/bin/python " + generateBG + " " + negSeq + " " + negSeq + "_BG.fa"
    os.system(tmpcmd2)
    negBGSeq = negSeq + "_BG.fa"
else:
    negBGSeq = args.negBGSeq
negBGHex = negBGSeq + "_hexamer.txt"

#run command
posFreqcmd = "/usr/bin/python " + readHexamer + " -i " + posSeq + " > " + posHex
posBGFreqcmd = "/usr/bin/python " + readHexamer + " -i " + posBGSeq + " > " + posBGHex
negFreqcmd = "/usr/bin/python " + readHexamer + " -i " + negSeq + " > " + negHex
negBGFreqcmd = "/usr/bin/python " + readHexamer + " -i " + negBGSeq + " > " + negBGHex
os.system(posFreqcmd)
os.system(posBGFreqcmd)
os.system(negFreqcmd)
os.system(negBGFreqcmd)


pos1feacmd = "Rscript " + hexamerScore + " -input " + posSeq + " -target " + posHex + " -bg " \
             + posBGHex + " -out " + posfea1dir
pos2feacmd = "Rscript " + hexamerScore + " -input " + posSeq + " -target " + negHex + " -bg " \
             + negBGHex + " -out " + posfea2dir


neg1feacmd = "Rscript " + hexamerScore + " -input " + negSeq + " -target " + posHex + " -bg " \
             + posBGHex + " -out " + negfea1dir
neg2feacmd = "Rscript " + hexamerScore + " -input " + negSeq + " -target " + negHex + " -bg " \
             + negBGHex + " -out " + negfea2dir

os.system(pos1feacmd)
os.system(pos2feacmd)
os.system(neg1feacmd)
os.system(neg2feacmd)

poscmd = featureEncoding + " " + posSeq + " " + posOut
negcmd = featureEncoding + " " + negSeq + " " + negOut

os.system(poscmd)
os.system(negcmd)

posFeature = np.loadtxt(posOut, dtype = "string")
negFeature = np.loadtxt(negOut, dtype = "string")

X = np.concatenate((posFeature, negFeature), axis=0)
pos1fea = np.loadtxt(posfea1dir, dtype = "string")
neg1fea = np.loadtxt(negfea1dir, dtype = "string")
pos2fea = np.loadtxt(posfea2dir, dtype =  "string")
neg2fea = np.loadtxt(negfea2dir, dtype = "string")

fea_1 = np.concatenate((pos1fea, neg1fea), axis=0)
fea_2 = np.concatenate((pos2fea, neg2fea), axis=0)
fea_1 = np.reshape(fea_1,(len(fea_1),1))
fea_2 = np.reshape(fea_2, (len(fea_2),1))

X = np.concatenate((X, fea_1), axis=1)
X = np.concatenate((X, fea_2), axis=1)
#print(X.shape)
X = X[:, np.newaxis, :]
y = np.array([1] * posFeature.shape[0] + [0] * negFeature.shape[0])
os.chdir("/your/directory//gcForest-master")
sys.path.insert(0, "lib")
from gcforest.gcforest import GCForest
cpu = args.cpu




#Perform k-fold cross validation
outDir = args.outDir
k = args.k
cvRes = cross_validation(X = X, y = y, cpu = cpu, k = k)

#plot receiver operating curves
plotROC(cvRes = cvRes, out = outDir)

#plot precision-recall curves
plotPR(cvRes = cvRes, out = outDir)

#plot F-score under different threshold
tmp = plotFscore(cvRes = cvRes, out = outDir, beta = 1)

#plot Sn, Sp, Pr, Acc, MCC, F-score
if args.threshold == None:
    threshold = tmp
else:
    threshold = args.threshold

plotMeasures(cvRes = cvRes, out = outDir, threshold = threshold)

#candidateSeq = args.candidateSeq
#cmd = featureEncoding + " " + candidateSeq + " " + canfeadir
#os.system(cmd)
#cmdfea1 = "Rscript " + hexamerScore + " -input " + candidateSeq + " -target " + posHex + " -bg " \
#          + posBGHex + " -out " + canfea1dir
#cmdfea2 = "Rscript " + hexamerScore + " -input " + candidateSeq + " -target " + negHex + " -bg " \
#          + negBGHex + " -out " + canfea2dir

#os.system(cmdfea1)
#os.system(cmdfea2)

#feature = np.loadtxt(canfeadir, dtype="string")
#feature1 = np.loadtxt(canfea1dir, dtype="string")
#feature1 = np.reshape(feature1, (len(feature1),1))
#feature2 = np.loadtxt(canfea2dir, dtype="string")
#feature2 = np.reshape(feature2, (len(feature2),1))
#feature = np.concatenate((feature, feature1), axis=1)
#feature = np.concatenate((feature, feature2), axis=1)
res = traingcForest(X_train = X, y_train = y, cpu = cpu)
#score = res.predict_proba(feature)
#mixedSeq = SeqIO.parse(candidateSeq, "fasta")
#SeqID = [fasta.id for fasta in mixedSeq]
#SeqID = np.array(SeqID)
#SeqID = np.reshape(SeqID,(len(SeqID),1))
#res = np.concatenate((SeqID, score), axis = 1)
#np.savetxt(outDir + "mixed_transcripts_predict.txt", res, header = "\t".join(['transcripts','prob_negative','prob_positive']), delimiter="\t", fmt="%s")
with open(outDir + "gcForest.pkl", "wb") as f:
        pickle.dump(res, f, pickle.HIGHEST_PROTOCOL)


