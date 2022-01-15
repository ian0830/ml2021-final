def fixLocation(header, content):
    indexCity = header.index('City')
    indexZipCode = header.index('Zip Code')
    indexLatLong = header.index('Lat Long')
    indexLatitude = header.index('Latitude')
    indexLongitude = header.index('Longitude')
    
    return header, content