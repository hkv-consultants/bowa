\name{maak.raster}
\alias{maak.raster}
\title{
Maak een RasterLayer van een BOWA kaart
}
\description{
Functie om kaartgegevens in BOWA om te zetten in een RasterLayer.
}
\usage{
maak.raster(kaarten, selectie)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{kaarten}{list met kaartmateriaal, ingeladen met \code{\link{lees.kaarten}}.}
  \item{selectie}{naam van de gewenste kaart (bijvoorbeeld "te").}
}
\details{
Met deze functie kun je kaartgegevens in BOWA om zetten naar een RasterLayer, een object uit het \emph{raster} pakket.
}
\value{
%%  ~Describe the value returned
%%  If it is a LIST, use
%%  \item{comp1 }{Description of 'comp1'}
%%  \item{comp2 }{Description of 'comp2'}
%% ...
Een RasterLayer.
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

%\seealso{
%% ~~objects to See Also as \code{\link{help}}, ~~~
%}
%\examples{
%}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
%\keyword{ ~kwd1 }
%\keyword{ ~kwd2 }% __ONLY ONE__ keyword per line
