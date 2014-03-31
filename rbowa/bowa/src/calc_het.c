#include <R.h>
#include <Rinternals.h>

int code2het(double code)
/*********************************************************************** 
 * Functie om een 10e-machtscode om te zetten naar een HET waarde.
 * HET = Focal heterogeneity = aantal verschillende waarden in de 3x3
 * focal area rondom een cel.
 *
 * INVOER:
 *
 * De celwaarden in de LG-kaart kunnen een code 1 t/m 5 hebben. Voor
 * elke van de 9 cellen in een 3x3 focal area tellen we 10^x op, waarbij
 * x = de LG code. Bijvoorbeeld: 9 cellen die allemaal LG waarde 1
 * hebben, geven een code 90 (=9*10^1). Als 1 van deze cellen een LG
 * waarde van 2 heeft, dan geeft dit code 180 (8*10^1 + 1*10^2). Op basis
 * van deze code is het relatief eenvoudig om het aantal verschillende
 * LG waarden in de 3x3 focal area te bepalen.
 *
 * UITVOER:
 *
 * Een HET waarde (integer tussen 1 en 5).
 *
 ***********************************************************************/ 
{
    int n = 0;
    double x, r;

    x = floor(code/10.0);

    while ( x > 0.0 )
    {
        r = fmod(x,10.0);
        if ( r > 0.0 ) { n++; }
        x = floor(x/10.0);
    }

    return(n);
}

SEXP calc_het(SEXP C, SEXP LG, SEXP n, SEXP ncol, SEXP nrow)
/*********************************************************************** 
 * Functie om de heterogeniteit van een 3x3 focal area (neighbourhood)
 * in de LG kaart te berekenen.
 *
 * INVOER:
 *
 * C    = celnummers van geselecteerde rastercellen
 * LG   = LG kaart (geselecteerde cellen) als vector (de LG kaart mag 
 *        alleen de codes 1 t/m 5 of een NA bevatten!)
 * n    = lengte van 'C'
 * ncol = aantal kolommen in LG-kaart
 * nrow = aantal rijen in LG-kaart
 *
 * UITVOER:
 *
 * Een vector met lengte n en van type INTEGER.
 *
 ***********************************************************************/
{
    double *tmp;    // tijdelijke vector voor volle LG kaart
    double code;    // code op basis van LG waarden in focal area
    int i, k;       // iteratoren
    int index;
    double *xlg = REAL(LG);
    int *xc = INTEGER(C);
    int *xn = INTEGER(n), *xncol = INTEGER(ncol), *xnrow = INTEGER(nrow);
    int m = *xncol * *xnrow;
    int focal[9] = {-(*xncol+1), -*xncol, -(*xncol-1), -1, 0, 1, *xncol-1, *xncol, *xncol+1};

    tmp = Calloc(m,double);

    for (i = 0; i < *xn; i++) 
    {
        if (!ISNA(xlg[i]))
        {
            tmp[xc[i]] = xlg[i];
        }
    }

    SEXP HET;
    PROTECT(HET=allocVector(INTSXP,*xn));
    int *het = INTEGER(HET);

    for (i = 0; i < *xn; i++) 
    {
        if (!ISNA(xlg[i])) 
        {
            code = 0;
            for (k = 0; k < 9; k++)
            {
                index = xc[i] + focal[k];
                if (!(index < 1 || index > m))
                {
                    code += pow(10.0, tmp[index-1]);
                }
            }
            het[i] = code2het(code);
        } 
        else 
        {
            het[i] = NA_INTEGER;
        }
    }

    Free(tmp);
    UNPROTECT(1);
    return(HET);
}
