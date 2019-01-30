[![Docker Repository on Quay](https://quay.io/repository/bgruening/galaxy-rna-workbench/status "Docker Repository on Quay")](https://hub.docker.com/r/malab/cafu/)


## CAFU
- CAFU is a Galaxy-based bioinformatics framework for comprehensive assembly and functional annotation of unmapped RNA-seq data from single- and mixed-species samples which integrates plenty of existing NGS analytical tools and our developed programs, and features an easy-to-use interface to manage, manipulate and most importantly, explore large-scale unmapped reads. 
- Besides the common process of reads cleansing, reads mapping, unmapped reads generation and novel transcription assembly, CAFU optionally offers the multiple-level evidence analysis of assembled transcripts, the sequence and expression characteristics of assembled transcripts, and the functional exploration of assembled transcripts through gene co-expression analysis and genome-wide association analysis. 
- Taking advantages of machine learning (ML) technologies, CAFU also effectively addresses the challenge of classifying species-specific transcripts assembled using unmapped reads from mixed-species samples. 
- The CAFU project is hosted on GitHub(https://github.com/cma2015/CAFU) and can be accessed from http://bioinfo.nwafu.edu.cn:4001. The CAFU Docker image is available at https://hub.docker.com/r/malab/cafu.

    ![CAFU](https://github.com/cma2015/CAFU/blob/master/Tutorials/CAFU_images/Overview_of_CAFU.png)

## Overview of functional modules in CAFU
- [**Extraction of unmapped reads**](https://github.com/cma2015/CAFU/blob/master/Tutorials/Extraction_mapped_reads.md)
- [***De novo* transcript assembly of unmapped reads**](https://github.com/cma2015/CAFU/blob/master/Tutorials/De_novo_transcript_assembly_of_unmapped_reads.md)
- [**Evidence support of assembled transcripts**](https://github.com/cma2015/CAFU/blob/master/Tutorials/Evidence_support_of_assembled_transcripts.md)
- [**Species assignment of assembled transcripts**](https://github.com/cma2015/CAFU/blob/master/Tutorials/SAT.md)
- [**Sequence characterization of assembled transcripts**](https://github.com/cma2015/CAFU/blob/master/Tutorials/Sequence%20characterization%20of%20assembled%20transcripts.md)
- [**Expression profiles of assembled transcripts**](https://github.com/cma2015/CAFU/blob/master/Tutorials/Expression%20profiles%20of%20assembled%20transcripts.md)
- [**Function annotation of assembled transcripts**](https://github.com/cma2015/CAFU/blob/master/Tutorials/Function%20annotation%20of%20assembled%20transcripts.md)


## How to use CAFU

- Tutorials for CAFU: https://github.com/cma2015/CAFU/blob/master/Tutorials/User_manual.md
- Test datasets referred in the tutorials for CAFU: https://github.com/cma2015/CAFU/tree/master/Test_data

## News and updates

### CAFU updated on Jan 1, 2019

- In the function **Assemble Unmapped Reads**, a parameter "Memory" was added for setting the maximum memory to be used by Triniry (1G in default). 
- To run the function **Species Assignment of Transcripts**, users can now use pre-trained or self-trained models. Currently, a pre-trained model was provided by training 20,502 and 137,052 mRNAs annotated in the reference genome of stripe rust pathogen *Puccinia striiformis f. sp. tritici* (PST-78 v1) and Chinese Spring wheat (IWGSC RefSeq v1.0), respectively.
- The user tutorial was updated to highlight the importance of CPUs, Memory and Swap settings for running CAFU docker.

### CAFU updated on Nov 30, 2018

- A function **Remove Contamination** was added to remove potential contamination sequences using Deconseq (Schmieder *et al*., 2011).
- A function **Remove Batch Effect** was added to remove batch effects using an R package sva (Leek *et al*., 2012).

### CAFU released on Oct 13, 2018

- CAFU source codes, web server and Docker image were released for the first time.


## How to access help
* For any bugs/issues, please feel free to leave a message at Github [issues](<https://github.com/cma2015/CAFU/issues>). We will try our best to deal with all issues as soon as possible.
* For any suggestions/comments, please send emails to: __Siyuan Chen__ <chenzhuod@gmail.com> or __Jingjing Zhai__ <zhaijingjing603@gmail.com> 

## How to cite this work
Siyuan Chen#, Chengzhi Ren#, Jingjing Zhai#, Jiantao Yu#, Xuyang Zhao, Zelong Li, Ting Zhang, Wenlong Ma, Zhaoxue Han, Chuang Ma*, CAFU: A Galaxy framework for exploring unmapped RNA-Seq data. Briefings in Bioinformatics, doi:10.1093/bib/bbz018.
