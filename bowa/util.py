import gdal

from lizard_map.coordinates import rd_to_wgs84

def extent_geotransform(shape, geotransform):
    width, height = shape

    minx = geotransform[0]
    miny = geotransform[3] + width * geotransform[4] + height * geotransform[5]
    maxx = geotransform[0] + width * geotransform[1] + height * geotransform[2]
    maxy = geotransform[3]
    return (minx, miny, maxx, maxy)


def google_extent_from_geotransform(shape, rd_geotransform):
    minx, miny, maxx, maxy = extent_geotransform(shape, rd_geotransform)

    wgs84_nw = rd_to_wgs84(minx, maxy)
    wgs84_se = rd_to_wgs84(maxx, miny)

    return {
        'north': wgs84_nw[1],
        'west': wgs84_nw[0],
        'south': wgs84_se[1],
        'east': wgs84_se[0]
        }


def gdal_open(path):
    if path.lower().endswith('.zip'):
        path = str('/vsizip/' + path)
    else:
        path = str(path)

    return gdal.Open(path)

