select.ht.ah <- function(toetseenheid,functie,werknormen,kaarten) {
###########################################################################
# Wrapper functie voor de C functie "select_ht_ah".
# INVOER:
#   toetseenheid    = identificatienummer van toetseenheid
#   functie         = code landgebruik
#   werknormen      = data frame met NBW werknormen
#   kaarten         = data frame met alle kaarten
#
# UITVOER: zie de beschrijving in select_ht_ah.c.
###########################################################################

# de te gebruiken waterstandskaart hangt af van de functie/herhalingstijd:
i <- which(werknormen$LG_CODE == functie)
T <- werknormen$HERHALINGSTIJD[i]

res <- .Call("select_ht_ah",
    as.integer(toetseenheid),
    as.integer(functie),
    as.integer(kaarten$te),
    as.integer(kaarten$lg),
    as.double(kaarten$ah),
    as.double(kaarten[[sprintf("ht%03d",T)]]),
    NAOK=TRUE,
    PACKAGE="bowa"
)

return(res)

}

# vim: filetype=r
