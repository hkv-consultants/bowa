\name{werknormen}
\alias{werknormen}
\alias{.lees.werknormen}
\docType{data}
\title{
NBW werknormen
}
\description{
Tabel met normen voor regionale wateroverlast gebaseerd op de werknormen uit
het Nationaal Bestuursakkoord Water (NBW) van 2005.
}
\usage{data(werknormen)}
\format{
    Een data frame met waarden voor vier normfuncties:
  \describe{
    \item{\code{lg_code}}{een code voor het landgebruik (zie 'details'
hieronder)}
    \item{\code{functienaam}}{naam van de normfunctie}
    \item{\code{herhalingstijd}}{herhalingstijd in jaren}
    \item{\code{maaiveldcriterium}}{precentage als fractie (tussen 0 en 1)}
  }
}
\details{
In deze tabel staan vier codes: 1 = grasland, 2 = akkerbouw, 3 = glastuinbouw +
hoogwaardige land- en tuinbouw, 4 = stedelijk gebied. Gebruik in de LG code 5 voor open water.

De functie \command{.lees.werknormen} is een interne routine om de gegevens in te laden. Deze is niet beschikbaar voor gebruikers.
}
\source{
Bijlage 4 in het Nationaal Bestuursakkoord Water (NBW) 2003.
}
\examples{
data(werknormen)
print(werknormen)
}
\keyword{datasets}
