#include <R.h>
#include <Rinternals.h>

SEXP simuleer_ht(SEXP HT, SEXP PG, SEXP n, SEXP gc, SEXP v, SEXP m)
{
    double *xht = REAL(HT);     // vector met waterstanden
    int *xpg = INTEGER(PG);     // vector met codes van peilgebieden
    int *xn = INTEGER(n);       // lengte van vectoren HT en PG
    int *xgc = INTEGER(gc);     // vector met unieke gebiedscodes uit PG
    double *xv = REAL(v);       // vector met gesimuleerde afwijkingen per peilgebied
    int *xm = INTEGER(m);       // lengte van vectoren gc en v

    int i, j;
    // geheugen reserveren voor de uitvoer:
    SEXP out;
    PROTECT(out=allocVector(REALSXP,*xn));
    double *xout = REAL(out);

    for (i = 0; i < *xn; i++) {
        if (ISNA(xpg[i])) {
            // als er geen code van het peilgebied beschikbaar is, zetten we
            // ook een NA in de uitvoer. Dit zou uiterst zelfdzaam moeten zijn.
            xout[i] = NA_REAL;
        } else {
            j = 0;
            while (xpg[i] != xgc[j] && j < *xm) {
                j++;
            }
            xout[i] = xht[i] + xv[j];
        }
    }

    UNPROTECT(1);
    return(out);
}
