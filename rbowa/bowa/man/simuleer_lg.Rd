\name{simuleer.lg}
\alias{simuleer.lg}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{Simuleer de LG (landgebruik) kaart}
\description{
Wrapper functie voor de C code in \emph{simuleer_lg.c}.
}
\usage{
simuleer.lg(lg, het, fm)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{lg}{ een enkele kaart met LG codes in de vorm van een vector }
  \item{het}{ een vector met de focal heterogeneity (HET) per rastercel in
\var{lg} (uitvoer van \code{\link{calc.het}}) }
  \item{fm}{ foutenmatrix (uitvoer van \code{.het.matrix}) }
}
%\details{
%%  ~~ If necessary, more details than the description above ~~
%}
\value{
Een vector van dezelfde lengte als \var{lg}.
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
