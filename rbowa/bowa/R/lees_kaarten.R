lees.kaarten <- function(pad,werknormen) {
##########################################################################
# Functie om alle kaarten in te laden en in een data.frame op te slaan.
#
# INVOER:
#   pad           = is het pad naar de bestanden 
#                   (met file.path(...) gemaakt)
#   werknormen    = een data.frame met de tabel van de NBW werknormen
#
# UITVOER: 
#   een data frame met alle kaarten die nodig zijn volgens de NBW
#   werknormen of NULL als er een fout is bij het inlezen.
##########################################################################

# TODO: zorg ervoor dat pakketten "stilletjes" geladen worden
require(raster)

foutmelding <- FALSE

# stap 1: toetseenhedenkaart inladen en alleen cellen met waarden selecteren

#cat("Kaart te.asc inladen... ",sep="")
tryCatch(te <- raster(file.path(pad,"te.asc")),
    error=function(condition) { 
        message("\nEr is een fout opgetreden bij het inlezen van \"te.asc\":\n",conditionMessage(condition))
        foutmelding <<- TRUE
    },
    finally=if (foutmelding) return(NULL)
)
# sla de eigenschappen van de toetseenheden kaart op (later controleren we of de andere
# kaarten dezelfde extent en het zelfde aantal rijen hebben):
kaarteigenschappen <- raster(te)
# sla de celwaarden op in de vorm van een vector:
te <- getValues(te)

# om intern geheugen te sparen gaan we alleen werken met de cellen waar 
# de toetseenhedenkaart geen NA's bevat:
cells <- which(!is.na(te))
if (length(cells) == 0) {
    message("\nEr is een fout opgetreden:\nde toetseenhedenkaart bevat geen waarden")
    return(NULL)
}

# stap 2: maak een vector met namen van de overige kaarten:

# standaard kaarten:
kaarten <- c("ah","lg","pg")

# waterstandskaarten op basis van de herhalingstijden in de NBW werknormen:
for (t in unique(werknormen$HERHALINGSTIJD)) {
    kaarten <- c(kaarten,paste("ht",sprintf("%03d",t),sep=""))
}

# in de uitvoer moeten een reeks kaarten en andere gegevens staan. De lengte 
# van de list is gelijk aan: 
# 'cells' + length(cells) + 'te' + length(kaarten) + 'kaarteigenschappen'
y <- vector(mode="list", length=4+length(kaarten))

y[[1]] <- cells
y[[2]] <- length(cells)
y[[3]] <- as.integer(te[cells])

rm(te)

i <- 4
for (kaart in kaarten) {

    # stap 3: overige asciigrids inlezen als "raster" object
    #cat("Kaart ",kaart,".asc inladen...\n",sep="")

    # de volgende regel maakt voor kaart "X" de volgende expression:
    # X <- getValues(raster(file.path(pad,"X.asc")))
    cmd <- paste(kaart," <- raster(file.path(pad,\"",kaart,".asc\"))",sep="")
    
    #cat(cmd,"\n")
    tryCatch(eval(parse(text=cmd)),
        error=function(condition) { 
            message("\nEr is een fout opgetreden bij het inlezen van \"",kaart,
            ".asc\":\n",conditionMessage(condition))
            foutmelding <<- TRUE
        },
        finally=if (foutmelding) return(NULL)
    )

    # stap 4: de waarden van de "raster" objecten opslaan in een vector (als 
    # de gegevens nog niet in het geheugen stonden, dan worden ze nu ingeladen.
    # Bij grote grids kan dit wat lang duren!)
    
    # eerst vergelijken we de eigenschappen van de kaart met die van de 
    # toetseenhedenkaart. Deze moeten hetzelfde zijn!
    equal <- FALSE
    cmd <- paste("equal <- compareRaster(kaarteigenschappen,",kaart,",crs=FALSE,stopiffalse=FALSE)",sep="")
    eval(parse(text=cmd))
    if (!equal) stop(paste("De ",toupper(kaart)," kaart (raster) heeft niet dezelfde extent als de TE kaart.",sep=""))
    #cat(cmd,"\n")

    # de volgende regel maakt voor kaart "X" de volgende expression:
    # X <- getValues(X)
    cmd <- paste(kaart," <- getValues(",kaart,")",sep="")
    eval(parse(text=cmd))
    #cat(cmd,"\n")

    # cellen selecteren:
    cmd <- paste(kaart," <- ",kaart,"[cells]",sep="")
    eval(parse(text=cmd))
    #cat(cmd,"\n")

    # de volgende regel maakt voor kaart "X" de volgende expression:
    # y[[i]] <- kaart of y[[i]] <- as.integer(kaart) voor de LG en PG kaarten
    if (kaart == "lg" || kaart == "pg") {
        cmd <- paste("y[[",i,"]] <- as.integer(",kaart,")",sep="")
    } else {
        cmd <- paste("y[[",i,"]] <- ",kaart,sep="")
    }
    eval(parse(text=cmd))
    #cat(cmd,"\n")

    # geheugen vrijmaken:
    cmd <- paste("rm(",kaart,")",sep="")
    eval(parse(text=cmd))
    #cat(cmd,"\n")

    i <- i + 1
}

y[[i]] <- kaarteigenschappen

names(y) <- c("cells","length","te",kaarten,"rasterproperties")

return(y)

}

# vim: filetype=r
