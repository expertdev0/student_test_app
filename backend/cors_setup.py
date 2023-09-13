from truckpad.bottle.cors import CorsPlugin
from api import app

# Set CORS
app.install(CorsPlugin(
    origins=['http://localhost:4200'],
    headers=['Content-Type', 'Authorization']
))
