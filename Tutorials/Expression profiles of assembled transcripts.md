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
        <td>Analysis Condition Specificity</td>
        <td>Identify condition-specifically expressed transcripts</td>
        <td>All transcripts; High-quality RNA-seq data; Sample information</td>
        <td>Condition-specific table; Diagnostic plots(heatmap)</td>
        <td>In-house scripts</td>
        <td>Our study</td>
</tr>
<tr>
        <td>Analysis Heterogeneous</td>
        <td>Identify stablely expressed transcripts</td>
        <td>Expression matrix; Sample information</td>
        <td>Gini coefficient table; Diagnostic plot (dotplot)</td>
        <td>In-house scripts</td>
        <td>Our study</td>
</tr>
<tr>
        <td rowspan="2">Analysis Differential Expression</td>
        <td rowspan="2">Identify differentially expressed transcripts</td>
        <td rowspan="2">All transcripts; High-quality RNA-seq data; Sample information</td>
        <td rowspan="2">DE analysis table; Diagnostic plot (Volcano plot; Venn-daragram )</td>
        <td>RSEM (version 1.3.0; https://deweylab.github.io/RSEM/) ; Bowtie2 (version 2.3.4.1; http://bowtie-bio.sourceforge.net/index.shtml)</td>
        <td>Li <I>et al</I>., 2011<Br/>Langmead <I>et al</I>., 2012</td>
</tr>
<tr>
        <td>EBSeq (version 3.7; https://bioconductor.org/packages/release/bioc/html/EBSeq.html)</td>
        <td>Leng <I>et al</I>., 2013</td>
</tr>
</table>
