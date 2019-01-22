tt=`pwd`
cd /home/chenzhuod/galaxy/tools/CAFU/BioSeq-Analysis
Rscript /home/chenzhuod/galaxy/tools/CAFU/SAT/translate.R -input $1 -out tmp_protein.fa
sed -i 's/*//g' tmp_protein.fa
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  Kmer -k 1 -out Kmer_1.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  Kmer -k 2 -out Kmer_2.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  DR  -out DR.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  AC  -out AC.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  CC  -out CC.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  ACC  -out ACC.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  PDT  -out PDT.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  PC-PseAAC  -out PC-PseAAC.txt
/usr/bin/python feature.pyc tmp_protein.fa Protein -method  SC-PseAAC  -out SC-PseAAC.txt
paste AC.txt CC.txt ACC.txt Kmer_1.txt PC-PseAAC.txt SC-PseAAC.txt Kmer_2.txt PDT.txt DR.txt > $2
mv $2 $tt"/"
cd $tt
