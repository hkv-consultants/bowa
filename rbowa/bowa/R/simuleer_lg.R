.het.matrix <- function(fm) {
##########################################################################
# Functie om een enkele foutenmatrix 'fm' aan te passen met de focal
# heterogeneity (HET). 
#
# INVOER:
# een enkele matrix 'fm' (length(dim(fm)) = 2), bijvoorbeeld ingeladen met
# het commando 'data(foutenmatrix)'. 
#
# UITVOER:
# Een driedimensionale array waarbij de 3e dimensie overeenkomt met de 
# waarde van HET (1 t/m 5). out[,,1] bevat dus de foutenmatrix voor HET=1.
##########################################################################

    n <- dim(fm)[1]
    rowsum <- fm %*% array(1,dim=c(n,1))
    out <- array(0,dim=c(n,n,5))
    for (het in seq(5)) {
        for (i in seq(n)) {
            off.diag.total <- rowsum[i] - fm[i,i]
            frac <- off.diag.total/rowsum[i]
            for (j in seq(n)) {
                if (i == j) {
                    out[i,j,het] <- 1 - frac*(het-1)/2
                } else {
                    if (off.diag.total > 0) {
                        out[i,j,het] <- (fm[i,j]/(rowsum[i] - fm[i,i]))*frac*(het-1)/2
                    }
                }
            }
        }
    }
    return(out)
}

simuleer.lg <- function(lg,het,fm) {
##########################################################################
# Wrapper functie voor de C code in 'simuleer_lg.c'.
##########################################################################

    if (length(dim(fm)) != 3) {
        stop("De functie \"simuleer.lg()\" heeft een driedimensionale foutenmatrix nodig.")
    }

    n <- length(lg)
    if (length(het) != n) {
        stop("De vector \"het\" moet evenveel elementen hebben als \"lg\".")
    }

    out <- .Call("simuleer_lg",
        as.double(lg),
        as.integer(het),
        as.double(fm),
        as.integer(dim(fm)),
        as.integer(n),
        NAOK=TRUE,
        PACKAGE="bowa"
    )

    return(out)
}

# vim: filetype=r
