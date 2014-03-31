maak.raster <- function(kaarten,selectie) {
###########################################################################
# Functie om een RasterLayer object te maken van BOWA kaartgegevens.
# 
# INVOER:
#   kaarten             = list met minimaal een element "cells" met 
#                         celnummers
#   selectie            = naam van de gewenste kaart (bijvoorbeeld "te")
#
# UITVOER:
#   Een RasterLayer object met de gewenste kaartegegevens.
###########################################################################
    require(raster)

    if (missing(selectie)) {
        stop("argument \"selectie\" ontbreekt en heeft geen standaard waarde")
    }
    if (!is.character(selectie)) {
        stop("argument \"selectie\" moet een string zijn")
    }
    if (selectie == "cells") {
        stop("argument \"selectie\" mag niet gelijk aan \"cells\" zijn")
    }
    if (!(selectie %in% names(kaarten))) {
        stop("er is geen kaart \"",selectie,"\" beschikbaar")
    }
    if (!("cells" %in% names(kaarten))) {
        stop("argument \"kaarten\" moet een element \"cells\" hebben")
    }
    if (!("rasterproperties" %in% names(kaarten))) {
        stop("argument \"kaarten\" moet een element \"rasterproperties\" hebben")
    }

    r <- kaarten$rasterproperties
    r[kaarten$cells] <- kaarten[[selectie]]

    return(r)
}

# vim: ft=r
