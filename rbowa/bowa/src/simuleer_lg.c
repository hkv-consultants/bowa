#include <R.h>
#include <Rinternals.h>

SEXP simuleer_lg(SEXP LG, SEXP HET, SEXP fm, SEXP fmdim, SEXP n)
{
    double *xlg = REAL(LG);
    int *xhet = INTEGER(HET);
    double *xfm = REAL(fm);
    int *xfmdim = INTEGER(fmdim);
    int nrow = xfmdim[0];
    int ncol = xfmdim[1];
    int *xn = INTEGER(n);
    int i, j, k;
    int lg, het;
    double u;
    double row[ncol];
    SEXP out;
    PROTECT(out=allocVector(INTSXP,*xn));
    int *xout = INTEGER(out);

    // read .Random.Seed from R:
    GetRNGstate();

    for (i = 0; i < *xn; i++)
    {
        if (ISNA(xlg[i])) {
            xout[i] = NA_INTEGER;
            continue;
        } 

        lg = (int)xlg[i] - 1;
        if (lg < 0 || lg > 4) {
            // we only sample LG codes 1 to 5!
            xout[i] = lg + 1;
            continue;
        }

        het = xhet[i] - 1;

        // extract the relevant row from the error matrix 'fm' and store
        // the cumulative probability:
        k = 0;
        for (j = het*nrow*ncol + lg; j < (het+1)*nrow*ncol + lg; j += nrow) 
        {
            if (k > 0)
            {
                row[k] = xfm[j] + row[k-1];
            }
            else
            {
                row[k] = xfm[j];
            }
            k++;
        }

        // sample a number between 0 and 1:
        u = unif_rand();
        
        k = 0;
        while (u > row[k])
        {
            k++;
        }

        xout[i] = k + 1;
        
    }

    // write .Random.Seed to R
    PutRNGstate();

    UNPROTECT(1);
    return(out);
}
