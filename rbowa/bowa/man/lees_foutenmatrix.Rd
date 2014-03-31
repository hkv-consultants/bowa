\name{lees.foutenmatrix}
\alias{lees.foutenmatrix}
\title{
Inleesroutine voor de foutenmatrix van de landgebruikkaart.
}
\description{
Functie om een tabel in te lezen die de foutenmatrix bevat van de LG
(landgebruik) kaart.
}
\usage{
lees.foutenmatrix(pad, bestand)
}
\arguments{
  \item{pad}{
pad naar het bestand met de gegevens van classificatiefouten
}
  \item{bestand}{
naam van het bestand
}
}
\details{
Het bestand moet een tabel met drie kolommen bevatten. De eerste regel in het
bestand moet een header zijn en de namen van de kolommen bevatten. Deze namen
liggen vast en zijn: GRIDWAARDE, WERKWAARDE en AANTAL. Alle waarden moeten
integers zijn.
}
\value{
De uitvoer van deze functie is een matrix met het aantal kolommen rijen gelijk
aan het aantal landgebruiksklassen in het bestand.
}
\seealso{
\code{\link{simuleer.lg}}
}
