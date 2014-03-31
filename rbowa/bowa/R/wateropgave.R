wateropgave <- function(werknormen,kaarten) {
##########################################################################
# functie om de wateropgave te berekenen
#
# INVOER:
#   werknormen  = tabel (asl data frame) met NBW werknormen
#   kaarten     = een list met alle kaarten inclusief elke waterstandskaart 
#
# UITVOER:
#   Een data frame met vijf kolommen en een aantal rijen gelijk aan het 
#   aantal toetseenheden x het aantal gebruiksfunctie.
#   De kolommen zijn:
#   
#   toetseenheid    = nummer van toetseenheid (code uit 'te' kaart)
#   functie         = naam van gebruiksfunctie (string uit werknormen)
#   toetshoogte     = hoogte van maaiveldcriterium [m]
#   volume          = wateropgave als volume [m^3]
#   oppervlakte     = wateropgave als oppervlakte [m^2]
#   percentage      = percentage falende cellen [%]
#
#   Voor deze laatste vier kolommen geldt: 0 = geen opgave.
#
##########################################################################

# kopieer voor de leesbaarheid een aantal gegevens van de NBW werknormen:
functiecodes <- werknormen$LG_CODE
functienamen <- werknormen$FUNCTIENAAM
maaiveldcrit <- werknormen$MAAIVELDCRITERIUM

toetseenheden <- unique(kaarten$te)
nfuncties <- length(functiecodes)

# maak een data frame met nullen 
# (aantal rijen = aantal toetseenheden x aantal functies):
kolomnamen <- c("toetseenheid","functie","toetshoogte","volume","oppervlakte","percentage")
res <- as.data.frame(
    sapply(kolomnamen,
        function(x) numeric(length(toetseenheden)*length(functiecodes)))
)
 
cell.area <- xres(kaarten$rasterproperties)*yres(kaarten$rasterproperties)

nattecellen <- rep(0,kaarten$length)

row <- 1
for (eenheid in toetseenheden) {
#cat("Toetseenheid:",eenheid,"\n")
    for (i in seq(nfuncties)) {
        res$toetseenheid[row] <- eenheid
        res$functie[row] <- functienamen[i]

        selection <- select.ht.ah(eenheid,functiecodes[i],werknormen,kaarten)
        
        if (is.null(selection)) {
            # er zijn geen cellen met de betreffende functie in deze 
            # toetseenheid, dus er is ook geen wateropgave:
            row <- row + 1
            next
        }

        # aantal geselecteerde cellen:
        n <- dim(selection)[1]
        # 1e kolom in 'res' zijn de geselecteerde maaiveldhoogtes:
        ah = selection[,1]
        # 2e kolom in 'res' zijn de geselecteerde waterstanden:
        ht = selection[,2]
        # 3e kolom in 'res' zijn de indices van de geselecteerde rastercellen:
        ii = selection[,3]
        rm(selection)

        toetshoogte <- quantile(ah,probs=maaiveldcrit[i],na.rm=TRUE)

        # indices van elementen (van de vectoren 'ht' en 'ah') met
        # (a) maatgevende waterstand > toetshoogte, en 
        # (b) maaiveldhoogte < maatgevende waterstand.
        jj  <- which(ht > toetshoogte & ah < ht)
        m   <- length(jj)

        nattecellen[ii[jj]] <- 1
        res$toetshoogte[row] <- toetshoogte
        res$volume[row]      <- sum(ht[jj] - ah[jj])*cell.area
        res$oppervlakte[row] <- m*cell.area
        res$percentage[row]  <- round(10000*m/n)/100

        row <- row + 1
    }
}

inundatiekaart <- vector(mode="list",length=4)
inundatiekaart[[1]] <- kaarten$cells
inundatiekaart[[2]] <- kaarten$length
inundatiekaart[[3]] <- nattecellen
inundatiekaart[[4]] <- kaarten$rasterproperties
names(inundatiekaart) <- c("cells","length","inundatie","rasterproperties")

out <- list(resultaat=res,inundatiekaart=inundatiekaart)

return(out)

}

# vim: filetype=r
