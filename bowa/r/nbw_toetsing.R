options(warn = -1)
library(rlogging, warn.conflicts = FALSE, quietly = TRUE)

# ----- BEGIN INSTELLINGEN (wijzig hier de noodzakelijke parameters) -----

args <- commandArgs(trailingOnly = TRUE)

if (length(args) == 0) {
    # test modus
    WERKMAP <- "/home/kallen/projects/PE0051/work"
    FOUTENMATRIX <- "foutenmatrix.txt"
    NORMEN <- "normen.txt"
    args <- c(WERKMAP, FOUTENMATRIX, NORMEN)
}

WERKMAP <- args[1]             # volledige pad naar de werkmap
FOUTENMATRIX <- args[2]        # naam van het bestand met de foutenmatrix
NORMEN <- args[3]              # naam van het bestand met de normen voor regionaal wateroverlast

# ----- BEGIN SCRIPT (hieronder niets wijzigen) -----
SetLogFile(file = "berekening.log", folder = WERKMAP)

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
kaarten <- lees.kaarten(WERKMAP, normen)
message("alle benodigde kaarten zijn ingeladen.")
if (is.null(kaarten)) stop()

inundatie <- rep(0,kaarten$length)

# bepaal de focal heterogeneity van de LG-kaart:
het <- calc.het(kaarten)

toetseenheden <- unique(kaarten$te)
functiecodes  <- normen$LG_CODE

opgave <- wateropgave(normen, kaarten)

# schrijf de resultaten per peilgebied weg naar een tabel:
write.table(opgave$resultaat,
            file = file.path(WERKMAP, "resultaat.txt"),
            sep = "\t",
            quote = FALSE,
            row.names = FALSE)

# doe hetzelfde, maar dan naar een SQLite database:
library(RSQLite, warn.conflicts = FALSE, quietly = TRUE)

resultaat.db <- file.path(WERKMAP, "resultaat.db")
unlink(resultaat.db)

drv <- dbDriver("SQLite")
con <- dbConnect(drv, dbname = resultaat.db)
succes <- dbWriteTable(con, "resultaat", opgave$resultaat)
if (!succes) {
    stop("er is probleem opgetreden bij het wegschrijven van het resultaat naar een SQLite database")
} else {
    succes <- dbDisconnect(con)
    succes <- dbUnloadDriver(drv)
}

# maak een grafiek van de inundatiefractie:
kaarten$inundatie <- opgave$inundatiekaart$inundatie
r <- maak.raster(kaarten, "inundatie")

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

