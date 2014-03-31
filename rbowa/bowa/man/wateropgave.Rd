\name{wateropgave}
\alias{wateropgave}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{ Bereken de wateropgave voor alle toesteenheden en alle gebruiksfuncties }
\description{
Deze functie berekent de wateropgave voor alle aanwezige
toetseenheden in de kaarten en voor alle gebruiksfuncties in de
NBW werknormen.
}
\usage{ wateropgave(werknormen, kaarten) }
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{werknormen}{ data frame met NBW werknormen, ingeladen met \code{data(werknormen)}.  }
  \item{kaarten}{ list met kaartmateriaal, ingeladen met \code{\link{lees.kaarten}}.  }
}
%\details{
%%  ~~ If necessary, more details than the description above ~~
%}
\value{
Een \strong{list} met twee elementen. 

Het eerste element bevat de uitvoer van de berekening van de
wateropgave in de vorm van een data frame met vijf kolommen:
\item{toetseenheid}{nummer van toetseenheid (code uit 'te' kaart)}
\item{functie}{naam van gebruiksfunctie (string uit werknormen)}
\item{toetshoogte}{hoogte van maaiveldcriterium [m]}
\item{volume}{wateropgave als volume [\eqn{m^3}]}
\item{oppervlakte}{wateropgave als oppervlakte [\eqn{m^2}]}
\item{percentage}{percentage falende cellen [\%]}

Het tweede element is weer een list met een inundatiekaart. De
namen van de elementen zijn resp. \emph{cells}, \emph{length},
\emph{inundatie} en \emph{rasterproperties}. Deze inundatiekaart
kan ook geplot worden met de functie \code{\link{lees.kaarten}}.

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
\keyword{wateropgave}

% vim: tw=66 filetype=tex
