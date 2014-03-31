\name{lees.kaarten}
\alias{lees.kaarten}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{Lees kaarten in voor toetsing aan de NBW werknormen}
\description{Deze functie leest alle benodigde kaarten in voor het toetsen van een beheergebied aan de NBW werknormen.}
\usage{lees.kaarten(pad, werknormen)}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{pad}{ Pad naar de map waarin alle kaarten staan.  }
  \item{werknormen}{ data frame met gegevens van de NBW werknormen, ingelezen met \code{data(werknormen)}.  }
}
\details{
Het doel van deze functie is om een hele serie aan kaarten
(rasters) op een effici\"ente manier in te laden. Het nadeel van
het inladen als \pkg{raster} objecten is het feit dat de meeste
grids veel lege (NODATA) cellen bevatten en dus onnodig veel
intern geheugen in beslag nemen. Deze functie laadt daarom alle
rasters in, selecteert de cellen waar de toetseenhedenkaart
waarden bevat en stopt deze cellen in een vector.
}

\value{
Een list met tenminste de elementen \emph{cells}, \emph{length},
\emph{te}, \emph{ah}, \emph{lg}, \emph{pg} en
\emph{rasterproperties}. De overige elementen zijn
waterstandsgegevens en hebben de naam \emph{htXXX}, waarbij
\emph{XXX} de herhalingstijd weergeeft. Bijvoorbeeld: \emph{ht010}
voor de waterstanden met een herhalingstijd van 10 jaar.

Het element \emph{cells} is een vector met indices van de
geselecteerde cellen uit de originele rasters. \emph{length} geeft
de lengte van deze vector. Het element \emph{rasterproperties} is
een `Raster' object.
}

%\references{
%% ~put references to the literature/web site here ~
%}
\author{
Maarten-Jan Kallen \email{m.j.kallen@hkv.nl}
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
\keyword{ ~utilities }

% vim: tw=66 filetype=tex
