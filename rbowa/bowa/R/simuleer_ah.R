simuleer.ah <- function(kaart,sigma,rho) {
###########################################################################
# Functie om een kaart met maaiveldhoogtes ("ah") te simuleren met een 
# Gaussisch verdeelde afwijking. Per gebied trekt deze functie 1 getal en 
# deze trekkingen zijn (mogelijk) gecorreleerd met (rank) correlatie 'rho'.
#
# INVOER:
#   kaart       = een enkele kaart in de vorm van een vector
#   sigma       = standaardafwijking voor de Gaussische verdeling (>0)
#   rho         = (rank) correlatie als enkel getal (tussen 0 en 1)
#
# UITVOER: 
#   een vector met dezelfde lengte als 'kaart' of NULL als
#   er een fout opgetreden is. Mochten er NA's in de kaart staan, dan staan
#   deze ook in de uitvoer.
###########################################################################

n <- length(kaart)

# 'u' is een master trekking:
u <- runif(1)
# 'v' trekken gecorreleerd met 'u' (met rank correlatie 'rho'):
v <- simuleer.copula(n,u,rho)

out <- vector(mode="numeric",length=n)

out <- kaart + qnorm(v,mean=0,sd=sigma)

return(out)

}

# vim: filetype=r
