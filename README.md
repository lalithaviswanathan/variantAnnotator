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
1. Allele (or ALT): In case of multiple ALT fields, this helps to identify which ALT we are referring to. E.g.:
#CHROM  POS     ID  REF  ALT    QUAL  FILTER  INFO     
chr1    123456  .   C    A      .     .       ANN=A|...
chr1    234567  .   A    G,T    .     .       ANN=G|... , T|...

2. Annotation (a.k.a. effect): Annotated using Sequence Ontology terms. Multiple effects can be concatenated using ‘&’.
#CHROM  POS     ID  REF  ALT  QUAL  FILTER  INFO     
chr1    123456  .   C    A    .     .      ANN=A|intron_variant&nc_transcript_variant|...

3. Gene Name: Common gene name (HGNC). Optional: use closest gene when the variant is “intergenic”.

4. Gene ID: Gene ID

5. Feature type: Which type of feature is in the next field (e.g. transcript, motif, miRNA, etc.). 

6. Feature ID: Depending on the annotation, this may be: Transcript ID (preferably using version number)

7. Transcript biotype: The bare minimum is at least a description on whether the transcript is {“Coding”, “Noncoding”}. Whenever possible, use ENSEMBL biotypes.

8. HGVS.c: Variant using HGVS notation (DNA level)

9. HGVS.p: If variant is coding, this field describes the variant using HGVS notation (Protein level). 

10. cDNA_position / cDNA_len: Position in cDNA and trancript’s cDNA length (one based).

11. CDS_position / CDS_len: Position and number of coding bases (one based includes START and STOP codons).

12. Protein_position / Protein_len: Position and number of AA (one based, including START, but not STOP).


## Prerequisites
Python 2.x

### Installing

## Built With

## Versioning
V 0.1 

## Author
Lalitha Viswanathan

## License
Open Source License

## Acknowledgments
http://snpeff.sourceforge.net/SnpEff_manual.html#input
