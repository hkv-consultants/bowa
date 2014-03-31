\name{simuleer.ht}
\alias{simuleer.ht}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{Simuleer een HT (waterstand) kaart}
\description{
Functie om trekkingen van een waterstandskaart te genereren, waarbij de
onzekerheid in de waarden gepresenteerd wordt door een Gaussische verdeling
en de ruimtelijke afhankelijkheid gemodelleerd wordt door een diagonal-band
copula.
}
\usage{
simuleer.ht(kaart, gebieden, sigma, rho)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{kaart}{ een enkele kaart in de vorm van een vector }
  \item{gebieden}{ een vector met gebiedscodes (bijv. uit een PG kaart) }
  \item{sigma}{ standaardafwijking voor de Gaussische verdeling (\eqn{> 0}) }
  \item{rho}{ (rank) correlatie als enkel getal (tussen 0 en 1) }
}
\details{
De waarden in rastercellen binnen een enkel gebied (gegeven door
\var{gebieden} zijn volledig gecorreleerd. Dit betekent dat binnen een enkel
gebied altijd dezelfde afwijking bij de betreffende cellen opgeteld wordt.
De afwijkingen in verschillende gebieden zijn gecorreleerd met (rank)
correlatie gelijk aan \var{rho}. Dit betekent dat de grootte van deze
afwijkingen verschillend kan zijn. De afwijking per gebied wordt bepaald
door eerst een soort \emph{master} trekking te nemen. Als deze positief is,
dan zijn alle afwijkingen ook positief en vice versa als de master trekking
negatief is.
}
\value{
Een vector met dezelfde lengte als \var{kaart} en \var{gebieden} of
\strong{NULL} als er een fout is opgetreden.
}
%\references{
%% ~put references to the literature/web site here ~
%}
\author{
Maarten-Jan Kallen, \email{m.j.kallen@hkv.nl}
}
%\note{
%%  ~~further notes~~
%}

%% ~Make other sections like Warning with \section{Warning }{....} ~

\seealso{
%% ~~objects to See Also as \code{\link{help}}, ~~~
\code{\link{simuleer.copula}}
}
%\examples{
%}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{ ~simulatie }
%\keyword{ ~kwd2 }% __ONLY ONE__ keyword per line

% vim: ft=tex tw=76
