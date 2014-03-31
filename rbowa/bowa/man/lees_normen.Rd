\name{lees.normen}
\alias{lees.normen}
\title{
Inleesroutine voor de normen voor regionaal wateroverlast
}
\description{
Functie om een tabel in te lezen die de normen voor regionaal wateroverlast bevat.
}
\usage{
lees.normen(pad, bestand)
}
\arguments{
  \item{pad}{
pad naar het bestand met de gegevens van de normen
}
  \item{bestand}{
naam van het bestand
}
}
\details{
Het bestand moet een tabel met vier kolommen bevatten. De eerste regel
(eventuele commentaarregels daargelaten, deze worden voorafgegaan met een
\code{#}) in het bestand moet een header zijn en de namen van de kolommen
bevatten. Deze namen liggen vast en zijn: 
\itemize{
  \item LG_CODE: een oplopend geheel getal (1, 2, enz.) met de grond,
  \item FUNCTIENAAM: de naam van de normfunctie,
  \item HERHALINGSTIJD: de herhalingstijd in jaren (bijv. 10, 25, enz.),
  \item MAAIVELDCTRITERIUM: percentage (getal tussen 0 en 1).
}
}
\value{
De uitvoer van deze functie is een tabel met de normen voor regionale
wateroverlast.
}

