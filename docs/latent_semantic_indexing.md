# About Latent Semantic Indexing (LSI)

Latent Semantic Indexing (LSI) natural language processing technique that is used for a dual purpose:

- during the analysis phase (i.e. Latent Semantic Analysis), features 
  expressed as weighted linear combination of term co-occurences
  are extracted.
- and during the indexing phase, the extracted features are used
  as index entries for similarity-based document retrieval.
  To achieve improved performance and reduce storage requirements, less relevant
  features are removed, so that the indexing becomes approximate.
  The resulting approximation is optimal with regard to the the least-squares residual error.


```math
a_i
```

$`a^2+b^2=c^2`$


## Definitions

LSI operates on a set of documents $`D`$ (with size $`m`$), expressed as individual document vectors $`d_i`$.

