##########################################################################
# Auteur    : Maarten-Jan Kallen <m.j.kallen@hkv.nl>
# Datum     : 2011-07-06
# Project   : PR2100.10
#
# Inhoud    : 
# Hulpbestand om "foutenmatrix.txt" in te lezen. Zie ook de toelichting bij
# het R commando 'data' (roep '?data' aan in R). In feite staan er twee
# bestanden in de 'data/' map met dezelfde naam, maar met verschillende
# extensies: (1) foutenmatrix.R en (2) foutenmatrix.txt. In dit geval vindt 
# de functie 'data' eerst het bestand met extensie .R en negeert de tweede.
# Waarom deze omweg? Als we alleen het bestand met extensie .txt gebruiken
# leest het commando 'data' het bestand in met een simpel 'read.table'
# commando. Dit simpele commando is onvoldoende voor onze toepassing. 
##########################################################################

.lees.foutenmatrix <- function(pad,bestand) {

foutmelding <- FALSE

tryCatch(tmp <- read.table(
        file=file.path(pad,bestand),
        header=TRUE,
        sep=",",
        colClasses=c("integer","integer","integer")
        ),
    error=function(condition) {
        message("Er is een fout opgetreden bij het inlezen van het bestand met de foutenmatrix:\n",
            conditionMessage(condition))
        foutmelding <<- TRUE
    },
    finally=if (foutmelding) return(NULL)
)

m <- nrow(tmp)
n <- max(tmp$kaart)
if (n != max(tmp$werkelijkheid) || m != n*n) {
    stop("Er is een fout opgetreden bij het inlezen van het bestand met de foutenmatrix:\nDe LG codes in de kolom \"kaart\" en \"werkelijkheid\" kloppen niet.")
}

out <- array(0,dim=c(n,n))

for (i in seq(m)) {
    out[tmp$kaart[i],tmp$werkelijkheid[i]] <- tmp$aantal[i]
}

return(out)

}

foutenmatrix <- .lees.foutenmatrix(pad=getwd(),"foutenmatrix.txt")
