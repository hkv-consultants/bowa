simuleer.ht <- function(kaart,gebieden,sigma,rho) {
###########################################################################
# Functie om een waterstandskaart ("ht") te simuleren met een Gaussisch
# verdeelde afwijking. Per gebied trekt deze functie 1 getal en deze 
# trekkingen zijn (mogelijk) gecorreleerd met (rank) correlatie 'rho'.
#
# INVOER:
#   kaart       = een enkele kaart in de vorm van een vector
#   gebieden    = een vector met gebiedscodes (bijv. een PG kaart)
#   sigma       = standaardafwijking voor de Gaussische verdeling (>0)
#   rho         = (rank) correlatie als enkel getal (tussen 0 en 1)
#
# UITVOER: 
#   een vector met dezelfde lengte als 'kaart' en 'gebieden' of NULL als
#   er een fout opgetreden is.
###########################################################################

n <- length(kaart)

if (length(gebieden) != n) {
    message("Er is een fout opgetreden:\n\"kaart\" en \"gebieden\" hebben 
        niet dezelfde lengte.")
    return(NULL)
}

gebiedscodes <- unique(gebieden)
if (length(gebiedscodes) == n) {
    # kennelijk moet een waarde voor elke individuele cel gesimuleerd worden
}
# de functie 'unique' geeft ook een NA als een waarde indien deze voorkomt in
# de vector 'gebieden'. Deze willen we echter niet beschouwen, dus zorgen we 
# met de volgende statement ervoor dat er geen NA aanwezig is in 'gebiedscodes'.
gebiedscodes <- gebiedscodes[which(!is.na(gebiedscodes))]
m <- length(gebiedscodes)
# NOTE: zijn hier nog controles op 'm' nodig?

# 'u' is een master trekking:
u <- runif(1)
# 'v' trekken gecorreleerd met 'u' (met rank correlatie 'rho'):
v <- simuleer.copula(m,u,rho)

out <- .Call("simuleer_ht",
    as.double(kaart),
    as.integer(gebieden),
    as.integer(n),
    as.integer(gebiedscodes),
    as.double(v),
    as.integer(m),
    NAOK=TRUE,
    PACKAGE="bowa"
)

return(out)

}

# vim: filetype=r
