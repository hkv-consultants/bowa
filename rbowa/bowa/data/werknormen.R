##########################################################################
# Auteur    : Maarten-Jan Kallen <m.j.kallen@hkv.nl>
# Datum     : 2011-06-22
# Project   : PR2100.10
#
# Inhoud    : 
# Hulpbestand om "werknormen.txt" in te lezen. Zie ook de toelichting bij
# het R commando 'data' (roep '?data' aan in R). In feite staan er twee
# bestanden in de 'data/' map met dezelfde naam, maar met verschillende
# extensies: (1) werknormen.R en (2) werknormen.txt. In dit geval vindt de 
# functie 'data' eerst het bestand met extensie .R en negeert de tweede.
# Waarom deze omweg? Als we alleen het bestand met extensie .txt gebruiken
# leest het commando 'data' het bestand in met een simpel 'read.table'
# commando. Dit simpele commando is onvoldoende voor onze toepassing. 
##########################################################################

.lees.werknormen <- function(pad,bestand) {
##########################################################################
# Functie om de tabel met NBW werknormen in te lezen. 
#
# INVOER:
#   pad     = pad naar het bestand met werknormen
#   bestand = naam van het bestand
#
# UITVOER:
#   Een data frame met vier kolommen. Deze kolommen zijn:
#
#   lg_code             = code van gebruiksfunctie (integer waarde)
#   functienaam         = naam van gebruiksfunctie (character string)
#   herhalingstijd      = herhalingstijd in jaren (integer waarde)
#   maaiveldcriterium   = maaiveldcriterium als percentage 
#                         (numeric tussen 0 en 1)
##########################################################################
foutmelding <- FALSE

tryCatch(out <- read.table(
        file=file.path(pad,bestand),
        header=TRUE,
        sep=";",
        colClasses=c("integer","character","integer","numeric")
        ),
    error=function(condition) {
        message("Er is een fout opgetreden bij het inlezen van het bestand met de NBW werknormen:\n",conditionMessage(condition))
        foutmelding <<- TRUE
    },
    finally=if (foutmelding) return(NULL)
)

return(out)

}

werknormen <- .lees.werknormen(pad=getwd(),"werknormen.txt")

# vim: filetype=r
