from weather import Weather, Unit

class Temperature:
    
    def __init__():
        self.location = 'Fullerton,CA'
        self.threeDay = threeDayForecast(self.location)

    def threeDayForecast(loc):
        weather = Weather(unit=Unit.FAHRENHEIT)
        location = weather.lookup_by_location(loc)
        forecasts = location.forecast
        return forecasts

    def locationTemperature(loc):
        weather = Weather(unit=Unit.FAHRENHEIT)
        location = weather.lookup_by_location(loc)
        condition = location.condition
        temperature = condition.temp
        return temperature

#loca = 'Fullerton,CA'
#print("it is currently ", locationTemperature(loca), " in ", loca)
#print()
#forecast = threeDayForecast(loca)
#for i in range(1,4):
#    print(forecast[i].day)
#    print(forecast[i].high)
#    print(forecast[i].text)
#    print()
#loca = 'New York,NY'
#print("it is currently ", locationTemperature(loca), " in ", loca)
