##########################################################################
# Datum     : 2014-03-12
# Inhoud    : Functie om een tabel met gegevens over de klassificatiefout 
#             in de LG kaart in te lezen.
##########################################################################
lees.foutenmatrix <- function(pad, bestand) {

    foutmelding <- FALSE

    tryCatch(tmp <- read.table(
            file=file.path(pad,bestand),
            header=TRUE,
            sep=";",
            colClasses=c("integer","integer","integer")
            ),
        error=function(condition) {
            message("Er is een fout opgetreden bij het inlezen van het bestand met de foutenmatrix:\n",
                conditionMessage(condition))
            foutmelding <<- TRUE
        },
        finally=if (foutmelding) return(NULL)
    )

    cols <- c("GRIDWAARDE", "WERKWAARDE", "AANTAL")
    if (length(ontbrekende.cols <- setdiff(cols, names(tmp))) > 0) {
        stop("het bestand met de foutenmatrix bevat niet de verplichte kolom(men): ",
             paste(ontbrekende.cols, sep = "", collapse = ", "))
    }

    m <- nrow(tmp)
    n <- max(tmp$GRIDWAARDE)
    if (n != max(tmp$WERKWAARDE) || m != n*n) {
        stop("Er is een fout opgetreden bij het inlezen van het bestand met de foutenmatrix: ",
             "De LG codes in de kolom \"GRIDWAARDE\" en \"WERKWAARDE\" kloppen niet.")
    }

    out <- array(0,dim=c(n,n))

    for (i in seq(m)) {
        out[tmp$GRIDWAARDE[i],tmp$WERKWAARDE[i]] <- tmp$AANTAL[i]
    }

    return(out)
}
