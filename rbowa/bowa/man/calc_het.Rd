\name{calc.het}
\alias{calc.het}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{Wrapper functie voor \emph{calc_het.c}}
\description{
Wrapper functie voor de C functie "calc_het".
}
\usage{
calc.het(kaarten)
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{kaarten}{ list met kaartmateriaal, ingeladen met \code{\link{lees.kaarten}} }
}
%\details{
%%  ~~ If necessary, more details than the description above ~~
%}
\value{
Een vector met lengte gelijk aan \code{kaarten$length}.
}
\references{
%% ~put references to the literature/web site here ~
Spatial variability in classification accuracy of agricultural crops in
the Dutch national land-cover database, 
P.A.J. van Oort, A.K. Bregt, S. de Bruin,
A.J.W. de Wit en A. Stein in \cite{Int. J. Geographical Information
Science}, 18(\strong{6}):611--626, 2004.
}
\author{
Maarten-Jan Kallen, \email{m.j.kallen@hkv.nl}
}
%\note{
%%  ~~further notes~~
%}

%% ~Make other sections like Warning with \section{Warning }{....} ~

\seealso{
%% ~~objects to See Also as \code{\link{help}}, ~~~
\code{\link{simuleer.lg}}
}
%\examples{
%}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
%\keyword{ ~kwd1 }
%\keyword{ ~kwd2 }% __ONLY ONE__ keyword per line

% vim: ft=tex tw=76
