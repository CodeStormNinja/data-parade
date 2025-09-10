from werkzeug.exceptions import BadRequest

def validate_coords(lat: float, lon: float):
    if not (-90.0 <= lat <= 90.0):
        raise BadRequest("lat deve estar entre -90 e 90")
    if not (-180.0 <= lon <= 180.0):
        raise BadRequest("lon deve estar entre -180 e 180")
