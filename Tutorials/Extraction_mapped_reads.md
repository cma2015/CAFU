
<table>
    <tr>
        <td font-weight:bold>Functions</td>
        <td font-weight:bold>Applications</td>
        <td font-weight:bold>Input files</td>
        <td font-weight:bold>Main output files</td>
        <td font-weight:bold>Programs</td>
        <td font-weight:bold>References</td>
   </tr>
    <tr>
        <td>Quality Control</td>
        <td>Examine the quality of RNA-Seq data</td>
        <td>Quality examination reports (html)</td>
        <td>Main output files</td>
        <td>FastQC (https://www.bioinformatics.babraham.ac.uk/projects/fastqc/)</td>
        <td>Andrews *et al*., 2010</td>
   </tr>
    <tr>
        <td rowspan="2">Trim Raw Reads</td>
        <td rowspan="2">Trim poly-A/T and low-quality reads</td>
        <td rowspan="2">Raw RNA-seq data</td>
        <td rowspan="2">High-quality RNA-seq data (Fastq)</td>
        <td>Fqtrim (version 0.9.7; https://ccb.jhu.edu/software/fqtrim/)</td>
        <td>[2]</td>
   </tr>
    <tr>
        <td>Trimmomatic (version 0.36; http://www.usadellab.org/cms/?page=trimmomatic)</td>
        <td>[3]</td>
    </tr>
    <tr>
        <td rowspan="3">Extract Unmapped Reads</td>
        <td rowspan="3">Align trimmed reads and obtain unmapped reads</td>
        <td rowspan="3">High-quality RNA-seq data; Reference sequences of corresponding species</td>
        <td rowspan="3">Alignment results (BAM); Unmapped reads (Fastq)</td>
        <td>HISAT2 (version 2.1.0; https://ccb.jhu.edu/software/hisat2/index.shtml)</td>
        <td>[4]</td>
    </tr>
    <tr>
        <td>SAMTools (version 1.8; http://samtools.sourceforge.net/)</td>
        <td>[5]</td>
    </tr>
    <tr>
        <td>BEDTools (version 2.27.0; http://bedtools.readthedocs.io/en/latest/)</td>
        <td>[6]</td>
    </tr>
       <tr>
        <td>Remove contamination</td>
        <td>Remove contaminate unmapped reads</td>
        <td>Unmapped reads (Fastq)</td>
        <td>Clean unmapped reads (Fastq)</td>
        <td>Deconseq (version 0.4.3 http://deconseq.sourceforge.net/)</td>
        <td>[1]</td>
   </tr> 
 </table>
