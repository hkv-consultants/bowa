\name{select.ht.ah}
\alias{select.ht.ah}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{ Wrapper voor \emph{select_ht_ah.c} }
\description{ Wrapper functie voor de C functie \emph{select_ht_ah}.  }
\usage{ select.ht.ah(toetseenheid, functie, werknormen, kaarten) }
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{toetseenheid}{ identificatienummer van toetseenheid.  }
  \item{functie}{ code landgebruik.  }
  \item{werknormen}{ data frame met NBW werknormen, ingeladen met \code{data(werknormen)}.  }
  \item{kaarten}{ data frame met kaartgegevens, ingeladen met \code{\link{lees.kaarten}} }
}
%\details{
%%  ~~ If necessary, more details than the description above ~~
%}
\value{
\strong{NULL} als er geen cellen met de betreffende gebruiksfunctie in de
toetseenheid aanwezig zijn, of een \strong{matrix} met de maaiveldhoogte
(1e kolom) en maatgevende waterstand (2e kolom) in de
geselecteerde cellen (lengte is gelijk aan het aantal
geselecteerde cellen).
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
\keyword{utilities}

% vim: tw=66 filetype=tex
