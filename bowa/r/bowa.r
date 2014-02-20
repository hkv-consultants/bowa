# stel het maximaal aantal characters per regel voor de uitvoer naar het scherm
# veel groter in dan de standaard waarde van 80 characters. Hierdoor komen fout-
# meldingen volledig in de ArcMap toolbox te staan:
options(width=1000)

# maak het werkgeheugen van R leeg in het geval dat het script al een eerder
# in de huidige sessie is aangeroepen:
rm(list=ls())

# laad de noodzakelijke pakketten in:
library(bowa)
if (packageVersion("bowa") < "0.2-2") stop("voor dit script is minimaal \"bowa\" versie 0.2-2 nodig")

args <- commandArgs(TRUE)

print(args[2]) 

werkmap <- file.path(args[1])
nsim <- as.integer(eval(parse(text=args[2])))
ahdev <- as.numeric(eval(parse(text=args[3])))
htdev <- as.numeric(eval(parse(text=args[4])))
rho <- as.numeric(eval(parse(text=args[5])))

# kies hieronder het bestand met de foutenmatrix voor de LG kaart:
FOUTENMATRIX <- "errLANDGEBRUIK.txt"           # wel variatie in de LG kaart
#FOUTENMATRIX <- "errLANDGEBRUIK_NOERROR.txt"    # geen variatie in de LG kaart

# ----- BEGIN SCRIPT (hieronder niets wijzigen) -----

# laad de noodzakelijke pakketten in:
library(bowa)
if (packageVersion("bowa") < "0.3-1") stop("voor dit script is minimaal \"bowa\" versie 0.3-1 nodig")

libs.loaded <- TRUE
tryCatch(library(bowa,quietly=TRUE),
    error=function (e) {
        message("\nEr is een fout opgetreden bij het inladen van de benodigde pakketten:\n",
            conditionMessage(e))
        libs.loaded <<- FALSE
    },
    finally=stopifnot(libs.loaded)
)

# laad de werknormen in vanuit het R pakket
data(werknormen)

# laad de foutenmatrix in vanuit de werkmap:
foutenmatrix <- lees.lg.foutenmatrix(werkmap,FOUTENMATRIX)

# pas de foutenmatrix aan met de focal heterogeneity:
fm <- .het.matrix(foutenmatrix)

cat("Loading maps...")
kaarten <- lees.kaarten(werkmap,werknormen)
cat("done.\n")
if (is.null(kaarten)) stop()

inundatie <- rep(0,kaarten$length)

# bepaal de focal heterogeneity van de LG-kaart:
het <- calc.het(kaarten)

toetseenheden <- unique(kaarten$te)
functiecodes  <- werknormen$lg_code

resultaat <- NULL
# FIXME: 'resultaat' wordt in de volgende loop langer gemaakt. Dit is heel
# inefficient (alhoewel verwaarloosbaar in vergelijking met de simulaties in
# de loop zelf) en moet dus verbeterd worden. Alloceer voldoende ruimte vooraf,
# bijv. nsim*nrow(werknormen)*length(toetseenheden), of gebruik een list (zie ook:
# http://menugget.blogspot.com/2011/11/another-aspect-of-speeding-up-loops-in.html)

for (sim in seq(nsim)) {
    cat("Simulation ",sim,"/",nsim,"\n",sep="")
    tic <- Sys.time()
    # maak een kopie van de set van kaarten om de trekkingen in op
    # te slaan:
    kaarten_sim <- kaarten

    # (a) simuleer waterstandskaarten (HTXXX):
    for (T in werknormen$herhalingstijd) {
        kaartnaam <- sprintf("ht%03d",T)
        kaarten_sim[[kaartnaam]] <- simuleer.ht(
            kaart=kaarten[[kaartnaam]],
            gebieden=kaarten$pg,
            sigma=htdev/qnorm(0.975),
            rho=rho
        )
    }

    # (b) simuleer maaiveldhoogtes (AH):
    kaarten_sim$ah <- simuleer.ah(
        kaart=kaarten$ah,
        sigma=ahdev/qnorm(0.975),
        rho=rho
    )

    # (c) simuleer landgebruik (LG):
    kaarten_sim$lg <- simuleer.lg(
        lg=kaarten$lg,
        het=het,
        fm=fm
    )

    res <- wateropgave(werknormen,kaarten_sim)

    opgave <- res$resultaat
    inundatie <- inundatie + res$inundatiekaart$inundatie

    resultaat <- rbind(
        resultaat,
        cbind(
            data.frame(sim=array(sim,dim=c(nrow(opgave),1))),
            opgave
        )
    )
    toc <- Sys.time()
    cat("Time in seconds: ",difftime(toc,tic,units="secs"),"\n",sep="")
}

resultaat <- transform(resultaat,
    toetshoogte=round(toetshoogte*100)/100,
    volume=round(volume*100)/100,
    percentage=round(percentage*100)/100
)

write.table(resultaat,
    file=file.path(werkmap,"resultaat.txt"),
    sep="\t",
    quote=FALSE,
    row.names=FALSE
)

# vim: filetype=r
