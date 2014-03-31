##########################################################################
# Auteur    : Maarten-Jan Kallen <m.j.kallen@hkv.nl>
# Datum     : 2011-06-22
# Project   : PR2100.10
# Inhoud    : Functie voor het inladen van 'select_ht_ah.dll' 
#             (of 'select_ht_ah.so' op Linux) bij het inladen van het
#             pakket. Zie '?.First.lib' en '?library.dynam'.
##########################################################################
.First.lib <- function(libname,pkgname) {
    library.dynam("bowa",package=pkgname,lib.loc=libname)
}
# vim: filetype=r
