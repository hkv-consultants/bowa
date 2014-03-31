calc.het <- function(kaarten) {
###########################################################################
# Wrapper functie voor de C functie "calc_het".
# INVOER:
#   kaarten         = list met alle kaarten en bijbehorende gegevens
#
# UITVOER: zie de beschrijving in bowa/src/calc_het.c.
###########################################################################
require(raster)

# aantal geselecteerde gridcellen:
n <- kaarten$length
# totaal aantal cellen in originele kaart:
cols <- ncol(kaarten$rasterproperties)
rows <- nrow(kaarten$rasterproperties)

# de LG codes zijn eigenlijk integers, maar we kunnen ISNA() in de C code
# alleen gebruiken met doubles:
res <- .Call("calc_het",
    as.integer(kaarten$cells),
    as.double(kaarten$lg),
    as.integer(n),
    as.integer(cols),
    as.integer(rows),
    NAOK=TRUE,
    PACKAGE="bowa"
)

return(res)
    
}

# vim: filetype=r
