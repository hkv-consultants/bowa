teken.kaart <- function(kaarten,selectie) {
###########################################################################
# Functie om een kaart in BOWA te plotten.
# 
# INVOER:
#   kaarten             = list met minimaal een element "cells" met 
#                         celnummers
#   selectie            = naam van de gewenste kaart (bijvoorbeeld "te")
#
# UITVOER:
#   geen.
###########################################################################
    r <- maak.raster(kaarten,selectie)
    plot(r)
}

# vim: ft=r
