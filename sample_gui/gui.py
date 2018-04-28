##############################################
# Created on: 
# Written by: 
#
##############################################
from weather import Weather, Unit
import tkinter as tk                # python 3
from tkinter import ttk
from tkinter import font  as tkfont # python 3
from tkcalendar import Calendar, DateEntry
from datetime import date
import requests
import json
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        spaceImage = tk.PhotoImage(file = "space.gif")
        
        spaceLabel = tk.Label(self, image = spaceImage)
        spaceLabel.image = spaceImage
        spaceLabel.pack()
        
        # Fonts defined here
        self.temp_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.time_font = tkfont.Font(family='Helvetica', size=10)
        self.day_font = tkfont.Font(family='Helvetica', size=16)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(spaceLabel, background="black")
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        
        

        self.frames = {}
        for F in (StartPage, SettingsPage, CityPage, CalendarPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

################################
#                              #
#           START_PAGE         #
#                              #
################################

class StartPage(tk.Frame):

    def tempDown(self):
        if(self.requestedTemperature > 60):
            self.requestedTemperature -= 1
            self.requestedtTempString = str(self.requestedTemperature)+"° F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.upButton.config(state="normal")
        else:
            self.downButton.config(state="disable")

    def tempUp(self):
        if(self.requestedTemperature < 90):
            self.requestedTemperature += 1
            self.requestedtTempString = str(self.requestedTemperature)+"° F"
            self.requestedTempLabel.configure(text = self.requestedtTempString)
            self.downButton.config(state="normal")
        else:
            self.upButton.config(state="disable")

    def systemToggle(self):
        if(self.isOn == True):
            self.isOn = False
            self.systemOnOffButton.configure(text = "Off")
            self.onOffLabel.configure(text = "System Off")
        else:
            self.isOn = True
            self.systemOnOffButton.configure(text = "On")
            self.onOffLabel.configure(text = "System On")

    def vacayToggle(self):
        if(self.vacayIsOn == True):
            self.vacayIsOn = False
            self.systemOnOffButton.configure(text = "Off")
            self.onOffVacayLabel.configure(text = "Vacation Mode Off")
        else:
            self.vacayIsOn = True
            self.systemOnOffButton.configure(text = "On")
            self.onOffVacayLabel.configure(text = "Vacation Mode On")

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.vacayIsOn = False
        self.isOn = False
        self.currentTemperature = 80
        self.requestedTemperature = 75
        
        ################################
        #                              #
        #       TIME_WIFI_SYSTEM       #
        #           SETTINGS           #
        ################################

        twsFrame = tk.Label(self)
        twsFrame.grid(row=0,column=0,sticky='nsew',padx=10, pady=10)
        twsFrame.grid_rowconfigure(0, weight=1)
        twsFrame.grid_columnconfigure(0, weight=1)
        
       	wifiImage = tk.PhotoImage(file = "wifi.gif")
	
        wifiLabel = tk.Label(twsFrame, image = wifiImage)
        wifiLabel.image = wifiImage
        wifiLabel.pack()


        timeLabel = tk.Label(twsFrame, text="12:00pm", font=controller.time_font)
        timeLabel.pack()

        self.onOffLabel = tk.Label(twsFrame, text="System Off", font=controller.time_font)
        self.onOffLabel.pack()
        
        self.onOffVacayLabel = tk.Label(twsFrame, text="Vacation Mode Off", font=controller.time_font)
        self.onOffVacayLabel.pack()
        
        ################################
        #                              #
        #    VACATION_CITY_CALENDAR    #
        #           SETTINGS           #
        ################################

        vccFrame = tk.Label(self)
        vccFrame.grid(row=0,column=1,sticky='n',pady=10)
        vccFrame.grid_rowconfigure(0, weight=1)
        vccFrame.grid_columnconfigure(1, weight=1)

        vacayButton = tk.Button(vccFrame, text="Vaction Mode", command=self.vacayToggle)
        vacayButton.pack(side='left')


        ################################
        #                              #
        #      TWO_DIFFERENT_WAYS      #
        #       TO_DISPLAY_CITY        #
        #                              #
        ################################
        
        self.variable = tk.StringVar(self)
        self.variable.set("City")
        
        cities = ["Los Angeles,CA", "Las Vegas,NV", "New York,NY","Miami,FL","SEOUL, South Korea","São Paulo, Brazil","Bombay, India", "JAKARTA, Indonesia","Karachi, Pakistan","MOSKVA (Moscow), Russia","Istanbul, Turkey"]

        cityOptions = tk.OptionMenu(vccFrame, self.variable,*cities )
        cityOptions.pack(fill='x',side='left')
#        vacayButton = tk.Button(vccFrame, text="Choose City", command=lambda: controller.show_frame("CityPage"))
#        vacayButton.pack(side='left')

        calButton = tk.Button(vccFrame, text="Calendar", command=lambda: controller.show_frame("CalendarPage"))
        calButton.pack(side='left')

        ################################
        #                              #
        #        3 DAY FORECAST        #
        #           SETTINGS           #
        ################################

        # 3 Day forecast
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
        
        # Get current location based off of IP address
        send_url = 'http://freegeoip.net/json'
        r = requests.get(send_url)
        j = json.loads(r.text)
        city = j['city']
        reg_code = j['region_code']
        locat = city + ',' + reg_code
        self.variable.set(locat)
        days = [None] * 3
        forecast = threeDayForecast(self.variable.get())
        for i in range(0,3):
            days[i] = forecast[i].day + " " + forecast[i].date + "\n" + forecast[i].high + "° F"
        print(locat)


        day1TempString = tk.StringVar()
        day1TempString.set(days[0])

        day2TempString = tk.StringVar()
        day2TempString.set(days[1])

        day3TempString = tk.StringVar()
        day3TempString.set(days[2])

        # Create a frame to store labels of the forcast
        dfFrame = tk.Label(self)
        dfFrame.grid(row = 0, column = 2,padx=10, pady=10)
        dfFrame.grid_rowconfigure(0, weight=1)
        dfFrame.grid_columnconfigure(2, weight=1)

        # Label for the three day forecast
        day1TempLabel = tk.Label(dfFrame, text=day1TempString.get(), font=controller.day_font)
        day1TempLabel.pack()

        day2TempLabel = tk.Label(dfFrame, text=day2TempString.get(), font=controller.day_font)
        day2TempLabel.pack(pady=10)

        day3TempLabel = tk.Label(dfFrame, text=day3TempString.get(), font=controller.day_font)
        day3TempLabel.pack()


        ################################
        #                              #
        #         TEMPERATURE          #
        #           SETTINGS           #
        #                              #
        ################################


        self.currentTempString = str(self.currentTemperature)+""+"° F"

        self.requestedtTempString = str(self.requestedTemperature)+""+"° F"

        tempFrame = tk.Label(self)
        tempFrame.grid(row=1,column=0)
        tempFrame.grid_rowconfigure(1, weight=1)
        tempFrame.grid_columnconfigure(0, weight=1)

        self.currentTempLabel = tk.Label(tempFrame, text=self.currentTempString, font=controller.temp_font)
        self.currentTempLabel.pack(padx=10,pady=10)

        self.requestedTempLabel = tk.Label(tempFrame, text=self.requestedtTempString, font=controller.temp_font)
        self.requestedTempLabel.pack(padx=10,pady=10)

        ################################
        #                              #
        #           CONTROLS           #
        #           SETTINGS           #
        #                              #
        ################################

        controlFrame = tk.Label(self)
        controlFrame.grid(row=2,column=0)
        controlFrame.grid_rowconfigure(2, weight=1)
        controlFrame.grid_columnconfigure(0, weight=1)

        self.systemOnOffButton = tk.Button(controlFrame, text="Off",command= self.systemToggle)
        self.systemOnOffButton.pack(padx=10,pady=10)

        settingsButton = tk.Button(controlFrame, text="Settings", command=lambda: controller.show_frame("SettingsPage"))
        settingsButton.pack(padx=10,pady=10)

        ################################
        #                              #
        #     TEMPERTURE_BUTTONS       #
        #           SETTINGS           #
        #                              #
        ################################

        # Up and Down Arrows Images
        upArrow = tk.PhotoImage(file = "up_arrow.gif")
        downArrow = tk.PhotoImage(file = "down_arrow.gif")

        tempControlFrame = tk.Label(self)
        tempControlFrame.grid(row=2,column=1)
        controlFrame.grid_rowconfigure(2, weight=1)
        controlFrame.grid_columnconfigure(1, weight=1)

        self.upButton = tk.Button(tempControlFrame, image = upArrow, command= self.tempUp)
        self.upButton.image = upArrow
        self.upButton.pack(padx=10,pady=10,side='left')
        self.downButton = tk.Button(tempControlFrame, image = downArrow, command= self.tempDown)
        self.downButton.pack(padx=10,pady=10)
        self.downButton.image = downArrow
	



###################################
#                                 #
#           SETTINGS_PAGE         #
#                                 #
###################################
class SettingsPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="This is settings page!", font=controller.temp_font)
        label.pack(side="top", fill="x", pady=10)

        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


class CityPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        #
        # label = tk.Label(self, text="This is cities page!", font=controller.temp_font)
        # label.grid(row = 0, column = 0)

        variable = tk.StringVar(self)
        variable.set("City") # default value


        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(padx = 10)


        cityOptions = tk.OptionMenu(self, variable, "Los Angeles,CA", "Las Vegas,NV", "New York,NY","Miami,FL","SEOUL, South Korea","São Paulo, Brazil"
        "Bombay, India", "JAKARTA, Indonesia","Karachi, Pakistan","MOSKVA (Moscow), Russia","Istanbul, Turkey")
        cityOptions.pack(fill='x')

class CalendarPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        button = tk.Button(self, text="Go Back",
                           command=lambda: controller.show_frame("StartPage"))
            
        button.pack(padx = 10)
        def print_sel():
            print(cal.selection_get())
        
        cal = Calendar(self,font="Arial 14", selectmode='day',cursor="hand1", year=2018, month=2, day=5)
        cal.pack(fill="both", expand=True)
        tk.Button(self, text="ok", command=print_sel).pack()



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()
