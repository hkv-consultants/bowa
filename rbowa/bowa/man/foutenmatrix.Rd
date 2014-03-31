\name{foutenmatrix}
\alias{foutenmatrix}
\alias{.lees.foutenmatrix}
\docType{data}
\title{
Classificatiefout in LG kaart
}
\description{
Foutenmatrix voor de classificatie van cellen in de kaart met landgebruik.
}
\usage{data(foutenmatrix)}
\format{
  The format is:
 num [1:5, 1:5] 90 4 2 1 1 4 90 4 3 2 ...
}
\details{
Deze matrix wordt gebruikt om de LG (landgebruik) kaart te simuleren. Deel de
getallen op elke rij door de som van alle getallen op de rij om kansen te
krijgen.

De functie \command{.lees.foutenmatrix} is een interne routine om de gegevens in te laden. Deze is niet beschikbaar voor gebruikers.
}
\source{
Zie bijvoorbeeld de rapporten van Alterra over de nauwkeurigheid van de LGN
(Landelijk Grondgebruiksbestand Nederland).
}
\examples{
data(foutenmatrix)
}
\keyword{datasets}
