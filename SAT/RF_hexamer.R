library(seqinr)
library(argparse)
parser <- ArgumentParser()

# specify our desired options 
# by default ArgumentParser will add an help option 
parser$add_argument("-input" , default = NULL, dest = "inputSeq",
                    help="The input sequence")
parser$add_argument("-target" , default = NULL, dest = "target",
                    help="The hexamer frequencies of target")
parser$add_argument("-bg" , default = NULL, dest = "bg",
                    help="The hexamer frequencies of target")
parser$add_argument("-out" , default = NULL, dest = "out",
                    help="The output filename")

extractSeq <- function(rangeVec, inputSeq){
  res <- inputSeq[rangeVec[1]:rangeVec[2]]
  res
}

generateKmer <- function(inputSeq){
  seqLen <- length(inputSeq)
  Start <- 1:(seqLen-5)
  End <- Start + 5 
  idxMat <- cbind(Start, End)
  resSeq <- apply(idxMat, 1, extractSeq, inputSeq = inputSeq)
  resSeq <- apply(resSeq, 2, c2s)
  resSeq
}


calHexScore <- function(inputSeq, targetGenome, bgGenome){
  kmer <- generateKmer(inputSeq = inputSeq)
  targetFreq <- as.numeric(targetGenome[kmer, 2])
  bgGenomeFreq <- as.numeric(bgGenome[kmer, 2])
  resScore <- sum(log(targetFreq/bgGenomeFreq))/length(kmer)
  resScore
}

args <- parser$parse_args()
inputSeq <- read.fasta(file = args$inputSeq)
posLen <- unlist(lapply(inputSeq, length))
inputSeq <- inputSeq[which(posLen > 6)]
idx <- which(!unlist(lapply(inputSeq, function(x) is.element("n", x))))
inputSeq <- inputSeq[names(idx)]
#inputSeq <- inputSeq[1:100]

target <- read.table(file = args$target, sep = "\t", header = F, quote = "",
                     stringsAsFactors = F)
target <- target[-1,]
rownames(target) <- tolower(target$V1)

bg <- read.table(file = args$bg, sep = "\t", header = F, quote = "",
                     stringsAsFactors = F)
bg <- bg[-1,]
rownames(bg) <- tolower(bg$V1)

resScore <-  lapply(inputSeq, calHexScore, targetGenome = target,
                    bgGenome = bg)
write.table(matrix(resScore, ncol = 1), file = args$out, sep = "\t", quote = F, row.names = F, col.names = F)
