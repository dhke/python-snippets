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


## Definitions

| Symbol | Description |
| ------ | ------------| 
| $`D`$ | an indexes family of size $`n`$ of documents. |
| $`T`$ | an indexed family of size $`m`$ of terms. |
| $`d_i`$ | a document vector, expressed a vector of size $`m`$ of term frequencies.  Each element of the vector indicates the (relative) frequency of the numbered term within the document at index $`i`$. |
| $`t_j`$ | a term vector, expressed as a vector of size $`n`$ of document frequencies.  Each element of the vector indicates the (relative) frequency that the term at index $`j`$ appears within the indexed document. |
| $`X`$ | An $`m \times n`$ matrix containing the cross-tabulation of all $`d_i`$s and $`t_j`$. |


$`X`$ is thus of the form

```math
X = \left(\begin{matrix}
 x_{1,1} & \ldots & x_{i, n} \\
 \vdots & & \vdots \\
 x_{m,1} & \ldots & x_{m, n} \\
\end{matrix}\right) 

\bordermatrix{
	&& \begin{array}{c} d_i \cr \downarrow \end{array} \cr
	 & x_{1,1} & \ldots & x_{i, n} \\
	 t_j \rightarrow & \vdots & & \vdots \\
	 & x_{m,1} & \ldots & x_{m, n} \\
}

```


LSI operates on a set of documents $`D`$ (with size $`m`$), expressed as individual document vectors $`d_i`$.

