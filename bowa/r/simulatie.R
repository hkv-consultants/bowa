options(warn = -1)
library(rlogging, warn.conflicts = FALSE, quietly = TRUE)

# ----- BEGIN INSTELLINGEN (wijzig hier de noodzakelijke parameters) -----

args <- commandArgs(trailingOnly=TRUE)

if (length(args) == 0 ) {
    # test modus
    WERKMAP <- "/home/kallen/projects/PE0051/work"
    FOUTENMATRIX <- "foutenmatrix.txt"
    NORMEN <- "normen.txt"
    args <- c(WERKMAP, FOUTENMATRIX, NORMEN, "5", "0.10", "0.10", "0.8")
}

WERKMAP <- args[1]             # volledige pad naar de werkmap voor deze simulatie
FOUTENMATRIX <- args[2]        # naam van het bestand met de foutenmatrix
NORMEN <- args[3]              # naam van het bestand met de normen voor regionaal wateroverlast
nsim  <- as.integer(args[4])   # aantal simulaties
ahdev <- as.numeric(args[5])   # afwijking [m] in de maaiveldhoogtekaart
htdev <- as.numeric(args[6])   # afwijking [m] in de waterstandskaarten
rho   <- as.numeric(args[7])   # (rank) correlatie [-] tussen gebieden

# ----- BEGIN SCRIPT (hieronder niets wijzigen) -----
SetLogFile(base.file = "berekening.log", folder = WERKMAP)

# laad de noodzakelijke pakketten in:
library(bowa)
if (packageVersion("bowa") < "0.4-1") stop("voor dit script is minimaal \"bowa\" versie 0.4-1 nodig")

libs.loaded <- TRUE
tryCatch(library(bowa,quietly=TRUE),
    error=function (e) {
        message("\nEr is een fout opgetreden bij het inladen van de benodigde pakketten:\n",
            conditionMessage(e))
        libs.loaded <<- FALSE
    },
    finally=stopifnot(libs.loaded)
)

# laad de foutenmatrix in vanuit de werkmap:
foutenmatrix <- lees.foutenmatrix(WERKMAP, FOUTENMATRIX)

# laad de normen voor regionaal wateroverlast in vanuit de werkmap:
normen <- lees.normen(WERKMAP, NORMEN)

# pas de foutenmatrix aan met de focal heterogeneity:
fm <- .het.matrix(foutenmatrix)

message("begin met inladen van de benodigde kaarten...")
kaarten <- lees.kaarten(WERKMAP,normen)
message("alle benodigde kaarten zijn ingeladen.")
if (is.null(kaarten)) stop()

inundatie <- rep(0,kaarten$length)

# bepaal de focal heterogeneity van de LG-kaart:
het <- calc.het(kaarten)

toetseenheden <- unique(kaarten$te)
functiecodes  <- normen$LG_CODE

resultaat <- NULL
# FIXME: 'resultaat' wordt in de volgende loop langer gemaakt. Dit is heel
# inefficient (alhoewel verwaarloosbaar in vergelijking met de simulaties in
# de loop zelf) en moet dus verbeterd worden. Alloceer voldoende ruimte vooraf,
# bijv. nsim*nrow(normen)*length(toetseenheden), of gebruik een list (zie ook:
# http://menugget.blogspot.com/2011/11/another-aspect-of-speeding-up-loops-in.html)

for (sim in seq(nsim)) {
    sim.nr <- paste(sim, nsim, sep = "/")
    message("start simulatie ", sim.nr)
    tic <- Sys.time()
    # maak een kopie van de set van kaarten om de trekkingen in op
    # te slaan:
    kaarten_sim <- kaarten

    # (a) simuleer waterstandskaarten (HTXXX):
    for (T in normen$HERHALINGSTIJD) {
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

    res <- wateropgave(normen, kaarten_sim)

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
    message("einde simulatie ", sim.nr, ", rekentijd in seconden: ", difftime(toc,tic,units="secs"))
}

# resultaten afronden:
resultaat <- transform(resultaat,
    toetshoogte=round(toetshoogte*100)/100,
    volume=round(volume*100)/100,
    percentage=round(percentage*100)/100
)

# schrijf de resultaten weg naar een tabel in een tekstbestand:
write.table(resultaat,
    file=file.path(WERKMAP,"resultaat.txt"),
    sep="\t",
    quote=FALSE,
    row.names=FALSE
)

# maak een grafiek van de inundatiefractie:
message("Maak grafiek van de inundatiefractie")
kaarten$inundatie <- inundatie
r <- maak.raster(kaarten, "inundatie")
writeRaster(r, file.path(WERKMAP, "inundatiekaart.asc"), NAflag=-9999)

succes <- TRUE
tryCatch(png(file = file.path(WERKMAP, "inundatiekaart.png"),
             width = 480*3,
             height = 480*3,
             bg = "transparent",
             type = "cairo"),
         error = function(e) succes <<- FALSE,
         warn = function(w) succes <<- FALSE,
         finally = {
             if (!succes) warning("kon geen PNG figuur maken van de inundatiefractie")
         }
         )

message("einde simulatie")

