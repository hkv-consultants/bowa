\name{simuleer.ah}
\alias{simuleer.ah}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{Simuleer de AH (bodemhoogte) kaart}
\description{
Een functie om de onzekerheid in de bodemhoogtekaart te simuleren, waarbij
de onzekerheid met een Gausssiche verdeling gerepresenteerd wordt en de
ruimtelijke correlatie met een diagonal-band copula gemodelleerd wordt.
}
\usage{
simuleer.ah(kaart, sigma, rho)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{kaart}{een enkele kaart in de vorm van een vector}
  \item{sigma}{standaardafwijking voor de Gaussische verdeling (\eqn{> 0})}
  \item{rho}{(rank) correlatie als enkel getal (tussen 0 en 1)}
}
%\details{
%%  ~~ If necessary, more details than the description above ~~
%}
\value{
Een vector met dezelfde lengte als \var{kaart} of \strong{NULL} als er een fout
opgetreden is. Mochten er NA's in de kaart staan, dan staan deze ook in de
uitvoer.
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

% vim: tw=76 ft=tex
