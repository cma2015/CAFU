library(seqinr)
library(argparse)

parser <- ArgumentParser()

# specify our desired options 
# by default ArgumentParser will add a help option 
parser$add_argument("-input" , default = NULL, dest = "inputSeq",
                    help="The input sequence")
parser$add_argument("-out" , default = NULL, dest = "out",
                    help="The output file")

args <- parser$parse_args()
inputSeq <- read.fasta(file = args$inputSeq)
posLen <- unlist(lapply(inputSeq, length))
inputSeq <- inputSeq[which(posLen > 6)]
idx <- which(!unlist(lapply(inputSeq, function(x) is.element("n", x))))
inputSeq <- inputSeq[names(idx)]
res <- lapply(inputSeq, translate)
write.fasta(lapply(res, toupper), names = names(res), file.out = args$out)
