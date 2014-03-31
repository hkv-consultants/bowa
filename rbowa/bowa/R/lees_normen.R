lees.normen <- function(pad, bestand) {
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
