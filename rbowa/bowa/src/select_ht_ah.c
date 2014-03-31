#include <R.h>
#include <Rinternals.h>

SEXP select_ht_ah(SEXP e, SEXP f, SEXP TE, SEXP LG, SEXP AH, SEXP HT)
/*********************************************************************** 
 * Functie om de celwaarden te selecteren binnen een enkele toetseenheid 
 * en voor een enkele functie.
 *
 * INVOER:
 *
 * e    = nummer van de toetseenheid
 * f    = nummer van de gebruiksfunctie
 * TE   = raster van toetseenheden als vector
 * LG   = raster van gebruiksfuncties als vector
 * AH   = raster van maaiveldhoogtes als vector
 * HT   = raster van maatgevende waterstanden als vector
 *
 * UITVOER:
 *
 * NULL als er geen cellen met de betreffende gebruiksfunctie in de 
 * toetseenheid aanwezig zijn, of een matrix met de maaiveldhoogte 
 * (1e kolom), maatgevende waterstand (2e kolom) in de geselecteerde 
 * cellen (lengte is gelijk aan het aantal geselecteerde cellen) en
 * celnummer (3e kolom). Deze laatste kan gebruikt worden om later
 * te achterhalen welke rastercellen geinundeerd zijn.
 *
 ***********************************************************************/
{
    int i, j, n, count;
    int *toetseenheid = INTEGER(e), *gebruiksfunctie = INTEGER(f);
    int *te = INTEGER(TE), *lg = INTEGER(LG);
    double *ah = REAL(AH), *ht = REAL(HT);

    n = length(TE);

    count = 0;
    for (i = 0; i < n; i++) {
        if (te[i] == *toetseenheid && lg[i] == *gebruiksfunctie && !ISNA(ah[i])) {
            count++;
        }
    }

    //Rprintf("Aantal cellen = %d\n",count);

    if (count > 0) {
        // create a new vector of length equal to the number of counted cells:
        SEXP Rsel;
        PROTECT(Rsel=allocMatrix(REALSXP,count,3));
        double *selection = REAL(Rsel);

        // loop over the raster data again and save selected AH and HT 
        // values to the new vector:
        j = 0;
        for (i = 0;i < n; i++) {
            if (te[i] == *toetseenheid && lg[i] == *gebruiksfunctie && !ISNA(ah[i])) {
                selection[j] = ah[i];
                selection[j+count] = ht[i];
                selection[j+count*2] = i + 1.0;
                j++;
            }
        }

        UNPROTECT(1);
        return(Rsel);

    } else {
        return R_NilValue;
    }
        
}
