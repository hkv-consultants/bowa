simuleer.copula <- function(n,u,rho,copula="diagonalband") {
##########################################################################
# Functie om een copula C(U,V) n keer te simuleren met gegeven u.
#
# INVOER:
#   n       = gewenst aantal trekkingen (1,2,3,...)
#   u       = getal (0,1)
#   rho     = (rank) correlatie (-1,1)
#   copula  = welke copula gebruikt moet worden (nu alleen "diagonalband")
#
# UITVOER:
#   Een vector met lengte 'n' van trekkingen uit C(U,V).
##########################################################################
beta <- 2/3 - sin(asin(abs(rho)*27/16 - 11/16)/3)*4/3

if (beta <= 0.5) {
    if (beta <= u & u <= 1-beta) {
        v <- runif(n,min=u-beta,max=u+beta)
    } else {
        p <- as.integer(runif(n,min=0,max=1.5))
        # er zitten ongeveer 2x zoveel nullen als enen in 'p'

        if (u < beta) {
            v <- ((1-p)*runif(n,min=0,max=beta-u) + 
                p*runif(n,min=beta-u,max=beta+u))
        } else {
            v <-  ((1-p)*runif(n,min=(1-u)+(1-beta),max=1) + 
                p*runif(n,min=u-beta,max=(1-u)+(1-beta)))
        }
        
    }
} else {
    p <- as.integer(runif(n,min=0,max=1.5))

    if (1-beta <= u & u <= beta) {
        q = as.integer(runif(n,min=0,max=2))
        # er zitten ongeveer evenveel nullen als enen in 'q'
        v <- (p*runif(n,min=(1-u)-(1-beta),max=(1-u)+(1-beta)) + 
            (1-p)*(q*runif(n,min=0,max=(1-u)-(1-beta)) + 
            (1-q)*runif(n,min=(1-u)+(1-beta),max=1)))
    } else {

        if (u < 1-beta) {
            v <- ((1-p)*runif(n,min=0,max=beta-u) + 
                p*runif(n,min=beta-u,max=beta+u))
        } else {
            v <- ((1-p)*runif(n,min=(1-u)+(1-beta),max=1) + 
                p*runif(n,min=u-beta,max=(1-u)+(1-beta)))
        }
    }
}

return(v)

}

# vim: set filetype=r
