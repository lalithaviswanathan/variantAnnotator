## variantAnnotator
Variant Annotator
## Description
variantAnnotator takes as input 2 arguments, a valid VCF File and an output file to write the annotated VCF to
## Getting Started
The below annotations are added to the VCF File.

Functional annotations information is added to the INFO field using an ANN tag. The annotation 'ANN' field looks like this 
ANN=T|missense_variant|MODERATE|CCT8L2|ENSG00000198445|transcript|ENST00000359963|protein_coding|1/1|c.1406G>A|p.Gly469Glu|1666/2034|1406/1674|469/557||,T|downstream_gene_variant|MODIFIER|FABP5P11|ENSG00000240122|transcript|ENST00000430910|processed_pseudogene||n.*397G>A|||||3944|
A variant can have (and ususally has) more than one annotaion. Multiple annotations are separated by commas. In the previous example there were two annotations corresponding to different genes (CCT8L2 and FABP5P11). 

Each annotation consists of multiple sub-fields separated by the pipe character "|" (fields 15 and 16 are empty in this example):
Annotation      : T|missense_variant|MODERATE|CCT8L2|ENSG00000198445|transcript|ENST00000359963|protein_coding|1/1|c.1406G>A|p.Gly469Glu|1666/2034|1406/1674|469/557|  |
SubField number : 1|       2        |    3   |  4   |       5       |    6     |      7        |      8       | 9 |    10   |    11     |   12    |   13    |   14  |15| 16

Here is a description of the meaning of each sub-field
Allele (or ALT): In case of multiple ALT fields, this helps to identify which ALT we are referring to. E.g.:
#CHROM  POS     ID  REF  ALT    QUAL  FILTER  INFO     
chr1    123456  .   C    A      .     .       ANN=A|...
chr1    234567  .   A    G,T    .     .       ANN=G|... , T|...

Annotation (a.k.a. effect): Annotated using Sequence Ontology terms. Multiple effects can be concatenated using ‘&’.
#CHROM  POS     ID  REF  ALT  QUAL  FILTER  INFO     
chr1    123456  .   C    A    .     .      ANN=A|intron_variant&nc_transcript_variant|...

Putative_impact: A simple estimation of putative impact / deleteriousness : {HIGH, MODERATE, LOW, MODIFIER}

Gene Name: Common gene name (HGNC). Optional: use closest gene when the variant is “intergenic”.

Gene ID: Gene ID

Feature type: Which type of feature is in the next field (e.g. transcript, motif, miRNA, etc.). It is preferred to use Sequence Ontology (SO) terms, but ‘custom’ (user defined) are allowed. ANN=A|stop_gained|HIGH|||transcript|... Tissue specific features may include cell type / tissue information separated by semicolon e.g.: ANN=A|histone_binding_site|LOW|||H3K4me3:HeLa-S3|...

Feature ID: Depending on the annotation, this may be: Transcript ID (preferably using version number), Motif ID, miRNA, ChipSeq peak, Histone mark, etc. Note: Some features may not have ID (e.g. histone marks from custom Chip-Seq experiments may not have a unique ID).

Transcript biotype: The bare minimum is at least a description on whether the transcript is {“Coding”, “Noncoding”}. Whenever possible, use ENSEMBL biotypes.

Rank / total: Exon or Intron rank / total number of exons or introns.

HGVS.c: Variant using HGVS notation (DNA level)

HGVS.p: If variant is coding, this field describes the variant using HGVS notation (Protein level). Since transcript ID is already mentioned in ‘feature ID’, it may be omitted here.

cDNA_position / cDNA_len: Position in cDNA and trancript’s cDNA length (one based).

CDS_position / CDS_len: Position and number of coding bases (one based includes START and STOP codons).

Protein_position / Protein_len: Position and number of AA (one based, including START, but not STOP).


## Prerequisites
Python 2.x

## Give examples
### Installing

## Running the tests

## Built With

## Versioning
V 0.1 

## Author
Lalitha Viswanathan

## License
Open Source License

## Acknowledgments
http://snpeff.sourceforge.net/SnpEff_manual.html#input
