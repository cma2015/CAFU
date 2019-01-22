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
    <td rowspan="3">Expression-level Evidence</td>
    <td rowspan="3">Obtain confident transcripts according to read coverage and expression abundance</td>
    <td rowspan="3">All transcripts (combine reference transcript and assembled transcripts); High-quality RNA-seq data </td>
    <td rowspan="3">Expression matrix; Confident transcript ID</td>
    <td>RSEM (version 1.3.0; https://deweylab.github.io/RSEM/) ; Bowtie2 (version 2.3.4.1; http://bowtie-bio.sourceforge.net/index.shtml)</td>
    <td>Li <I>et al</I>., 2011<Br/>Langmead <I>et al</I>., 2012</td>
</tr>
<tr>
    <td>BEDTools (version 2.27.0; http://bedtools.readthedocs.io/en/latest/)</td>
    <td>Quinlan <I>et al</I>., 2010</td>
</tr>
<tr>
    <td>In-house scripts</td>
    <td>Our study</td>
</tr>
<tr>
    <td rowspan="2">Genome-level Evidence</td>
    <td rowspan="2">Obtain confident transcripts according to transcript-genome alignments</td>
    <td rowspan="2">Assembled transcripts; Reference sequences of corresonding and closely related speces</td>
    <td rowspan="2">Alignment results (PSL); Confident transcript ID</td>
    <td>GMAP (version 2015-09-29; https://github.com/juliangehring/GMAP-GSNAP)</td>
    <td>Wu <I>et al</I>., 2005</td>
</tr>
<tr>
    <td>In-house scripts</td>
    <td>Our study</td>
</tr>

<tr>
    <td rowspan="2">Transcript-level Evidence</td>
    <td rowspan="2">Obtain confident transcripts according to transcript-transcript alignments</td>
    <td rowspan="2">Assembled transcripts; Reference transcripts of corresonding and closely related speces</td>
    <td rowspan="2">Alignment results (PSL); Confident transcript ID</td>
    <td>GMAP (version 2015-09-29; https://github.com/juliangehring/GMAP-GSNAP)</td>
    <td>Wu <I>et al</I>., 2005</td>
</tr>
<tr>
    <td>In-house scripts</td>
    <td>Our study</td>
</tr>


<tr>
    <td rowspan="2">Protein-level Evidence</td>
    <td rowspan="2">Obtain confident transcripts according to the protein potential</td>
    <td rowspan="2">Assembled transcripts</td>
    <td rowspan="2">Confident transcripts ID; Protein potential assessment results; Domain/family results</td>
    <td>CPC2 (version 0.1; http://cpc2.cbi.pku.edu.cn/)</td>
    <td>Kang <I>et al</I>., 2017</td>
</tr>
<tr>
    <td>Pfam (version 31.0; https://pfam.xfam.org/)</td>
    <td>Finn <I>et al</I>., 2014</td>
</tr>

</table>
