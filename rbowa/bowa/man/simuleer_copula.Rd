\name{simuleer.copula}
\alias{simuleer.copula}
%- Also NEED an '\alias' for EACH other topic documented here.
\title{Simuleer een diagonal-band copula}
\description{
Functie om trekkingen te doen uit een copula.
}
\usage{
simuleer.copula(n, u, rho, copula = "diagonalband")
}
%- maybe also 'usage' for other objects documented here.
\arguments{
  \item{n}{ gewenste aantal trekkingen (\eqn{1,2,3,\ldots}) }
  \item{u}{ trekking uit uniforme verdeling op (0,1) }
  \item{rho}{ een waarde voor de gewenste (rank) correlatie in (-1,1) }
  \item{copula}{ naam van het type copula die gebruikt moet worden }
}
\details{
Op dit moment is alleen de zogenaamde \emph{diagonal-band} copula
ge\"implementeerd.
}
\value{
De uitvoer is een vector met lengte \var{n} van trekkingen uit de copula
\eqn{C(U,V)} met (rank) correlatie \eqn{\rho}.
}
\references{
%% ~put references to the literature/web site here ~
\itemize{
    \item \cite{Uncertainty Analysis with High Dimensional Dependence
Modelling}, D. Kurowicka en R.M. Cooke, Wiley, 2006.
    \item \cite{Probabilistic Risk Analysis: Foundations and Methods},
T. Bedford en R.M. Cooke, Cambridge University Press, 2001.
    \item Wikipedia artikel over copula's:
\url{http://en.wikipedia.org/wiki/Copula_(probability_theory)}
    }
}
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
\examples{
v <- simuleer.copula(n=10000,u=0.9,rho=0.9)
hist(v,xlim=c(0,1),breaks=seq(0,1,0.02),col=rgb(0.8,0.8,0.8))
}
% Add one or more standard keywords, see file 'KEYWORDS' in the
% R documentation directory.
\keyword{ ~simulatie }
%\keyword{ ~kwd2 }% __ONLY ONE__ keyword per line

% vim: ft=tex tw=76
