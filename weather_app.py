# Imports #
import tkinter as tk
from tkinter import messagebox as msgbx
from tkinter.ttk import Combobox
import requests
import json
from datetime import datetime

# WeatherApp
class WeatherApp:
    """
    class of WeatherApp
    """
    API_KEY = "d771e5e1b5ae57994e3319563f2acb60"
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
    FAVORITES_FILE = "favorites.json"

    def __init__(self, root):
        """
        inits
        """

        # Main window configuration
        self.root = root
        self.root.title("Weathuh Opp")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.window_bg_color = "#3b72ad"
        self.window_fg_color = "#9dc2b9"
        self.root.config(bg=self.window_bg_color)

        # Other Variables
        self.favorites = []
        self.current_city = ""
        self.current_unit = "C"
        self.current_mode = 0
        
        # Load favorites.json and creates widgets for app
        self.load_favorites()
        self.create_widgets()

        # Handles selecting a favorite from the dropdown
        if self.favorites:
            self.load_weather_from_favorite()

    def create_widgets(self):
        """
        Creates widgets
        """

        title_label = tk.Label(
            self.root,
            text = "Hoodini",
            font = ("Impact", 24, "bold"),
            bg = self.window_bg_color, fg = self.window_fg_color
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=20)

        favorites_label = tk.Label(
            self.root,
            text= "Favorited Locations ",
            font = ("Courier new", 12),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        favorites_label.grid(row=1,column=0,padx=10,sticky="e")


        # Combobox holds all of the favorited locations to choose from.
        self.city_dropdown = Combobox(
            self.root,
            values = self.favorites,
            width = 34,
            font = ("Courier new", 11)
        )
        self.city_dropdown.set("select city...")
        self.city_dropdown.bind("<<ComboboxSelected>>", self.load_weather_from_favorite)
        self.city_dropdown.grid(row=1,column=1,padx=5,sticky="w")
        # 3 lines above pack city_dropdown and make it search a favorited city when it's selected.

        search_label = tk.Label(
            self.root,
            text = "Search for a city --> ",
            font = ("Courier new", 12),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        search_label.grid(row=2,column=0,padx=10,pady=10,sticky="e")

        # Entry box for searching a city, can either press the search button or 'enter' to search.
        self.city_entry = tk.Entry(
            self.root,
            font = ("Courier new", 12),
            width = 18
        )
        self.city_entry.grid(row=2, column=1, padx=5,pady=10,sticky="w")
        self.city_entry.bind("<Return>", lambda e: self.search_weather())

        search_button = tk.Button(
            self.root,
            text = "Search",
            font = ("Courier new", 11),
            bg = self.window_bg_color,
            fg = self.window_fg_color,
            command = self.search_weather,
            cursor = "hand2",
            width = 10
        )
        search_button.grid(row=2, column=2,padx=5,pady=10, sticky="w")

        # Holds the info retrieved about a city
        self.weather_frame = tk.Frame(
            self.root,
            bg = self.window_bg_color,
            relief = "solid",
            borderwidth=3
        )
        self.weather_frame.grid(row=3,column=0,columnspan=5,padx=20,pady=20,sticky="nsew")

        # Displays name of city when one is searched for and found.
        self.city_label = tk.Label(
            self.weather_frame,
            text = "Search for a city",
            font = ("Courier new", 16),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.city_label.pack()

        # Displays temperature of city when found
        self.temp_label = tk.Label(
            self.weather_frame,
            text = "",
            font = ("Impact", 32),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.temp_label.pack(pady=5)

        # Displays cloud conditions of city when found
        self.condition_label = tk.Label(
            self.weather_frame,
            text = "",
            font = ("Arial", 14),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.condition_label.pack(pady=5)

        # Displays other info, like the Feels-Like temp, humidity, and wind speeds
        self.details_label = tk.Label(
            self.weather_frame,
            text = "",
            font = ("Arial", 14),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.details_label.pack()

        # Just to keep the buttons that change the forecast type away from the rest.
        top_button_frame = tk.Frame(
            self.root,
            bg = self.window_bg_color
        )
        top_button_frame.grid(row=4,column=0,columnspan=3,padx=5,pady=10)

        # Changes forecast to 1 more day than the previous, up to 5 day forecast.
        self.plus_forecast_button = tk.Button(
            top_button_frame,
            text = "Not functional",
            font = ("Arial", 11),
            bg = self.window_bg_color,
            fg = self.window_fg_color,
            #command = self.plus_forecast,
            cursor = "hand2",
            width = 18,
            )
        self.plus_forecast_button.pack(side="right",padx=10)

        # Opposite of above. one less day from previous, down to curent day forecast.
        self.minus_forecast_button = tk.Button(
            top_button_frame,
            text = "not Functional",
            font = ("Arial", 11),
            bg = self.window_bg_color,
            fg = self.window_fg_color,
            #command = self.minus_forecast,
            cursor = "hand2",
            width = 18,
            )
        self.minus_forecast_button.pack(side="left",padx=10)

        # Holds the add_Button, remove_button, unit_button, and unit_label.
        bottom_button_frame = tk.Frame(
            self.root,
            bg = self.window_bg_color
        )
        bottom_button_frame.grid(row=5,column=0,columnspan=3,padx=5,pady=10)

        # Adds the curently viewed city to the Favorited Locations dropdown, if not already.
        self.add_button = tk.Button(
            bottom_button_frame,
            text = "Add to Favorites",
            font  = ("Arial", 11),
            bg = self.window_bg_color,
            fg = self.window_fg_color,
            command = self.add_to_favorites,
            cursor = "hand2",
            width = 18,
            disabledforeground = "black"
        )
        self.add_button.pack(side="left",padx=5)

        # Removes curently viewed city from the dropdown
        self.remove_button = tk.Button(
            bottom_button_frame,
            text="Remove from Favorites",
            font=("Arial", 11),
            bg=self.window_bg_color,
            fg=self.window_fg_color,
            command = self.remove_from_favorites,
            cursor="hand2",
            width=18,
            disabledforeground="black"
        )
        self.remove_button.pack(side="left", padx=5)

        # Swaps the unit used in the forecast between Celcius and Fahrenheit
        self.unit_button = tk.Button(
            bottom_button_frame,
            text = "Swap celcius/fahrenheit",
            font=("Arial", 11),
            bg=self.window_bg_color,
            fg=self.window_fg_color,
            command = self.swap_unit,
            width = 18
            )
        self.unit_button.pack(side="left",padx=5)

        # Just makes it easier to tell what unit a user is using. (ahaha)
        self.unit_label = tk.Label(
            bottom_button_frame,
            text = f"{self.current_unit}",
            font=("Arial", 11, "bold"),
            bg=self.window_bg_color,
            fg=self.window_fg_color,
            width = 5
            )
        self.unit_label.pack(side="right",padx=5)


        # Makes all the widgets not align STUPID (no touchy)
        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.root.grid_columnconfigure(i,weight=1)


    def search_weather(self):
        """
        Searches Weather
        """
        dropdown_active = self.city_dropdown.get()
    

        city = self.city_entry.get().strip()

        if not city: # If no city is typed inside the search box

            if dropdown_active != "select city...":
                return

            msgbx.showwarning("No City!", "You did not enter a city name!\nPlease enter a city name.")
            return
       
                    
        coords = self.get_coordinates(city)
        if not coords: # If it can't find the coordinate location for a city entered
            msgbx.showerror("No City", "That City wasn't found!\nPlease enter a valid city.")
            return


        # If neither if statement is triggered, save coords into 3 vars
        self.city_dropdown.config(text="select city...")
        lat, lon, full_city_name = coords

        weather_data = self.get_weather(lat, lon)
        if weather_data:
            print(weather_data)
            self.display_weather(weather_data, full_city_name)


    def get_coordinates(self,city):
        """
        Gets the coordinates
        """

        # Attempts to retrieve coordinates of the city that is searched
        # including: City name, Latitude, Longitude, State (or equivalent),
        # and Country
        try:
            params = {
                "q": city,
                "limit": 1,
                "appid": self.API_KEY
            }
            response = requests.get(self.GEOCODING_URL, params=params, timeout=5)
            print(response)

            if response.status_code == 200:
                data = response.json()
                if data:
                    location = data[0]
                    lat = location["lat"]
                    lon = location["lon"]
                    name = location["name"]

                    state = location.get("state", "")
                    country = location.get("country", "")

                    if state:
                        full_city_name = f"{name}, {state}, {country}"
                    else:
                        full_city_name = f"{name}, {country}"

                    return lat, lon, full_city_name
                else:
                    msgbx.showerror("City Not Found", f"{city} cannot be found")


        except:
            print("err.")


    def get_weather(self, lat, lon):
        """
        Gets the weather
        """
        # Attempts to get the weather conditions on a city if it is found.
        try:
            params = {
                "lat": lat,
                "lon": lon,
                "appid": self.API_KEY,
                "units": "imperial"
            }

            response = requests.get(self.WEATHER_URL, params=params, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                msgbx.showerror("API Err.", f"Error fetching weather data: {response.status_code}")
                return None

        except:
            print(response.status_code)


    def display_weather(self, data, city):
        """
        Displays the weather
        """
    
        if not data: # If it doesn't get any weather data to use, quit immediately
            return


        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"] ################################################################ Very useful commetns
        wind_speed = data["wind"]["speed"]
        self.current_city = city

        # Temperature is always provided as Fahrenheit, so display it if the user wants Fahrenheit, convert it then display it if they want Celcius.
        if self.current_unit == "C":
            self.temp_label.config(text=f"{((temp - 32)*(5/9)):.1f} C")
        elif self.current_unit == "F":
            self.temp_label.config(text=f"{temp:.0f} F")

        # Changes all the labels in weather_frame to show the city information
        self.city_label.config(text=self.current_city)
        self.condition_label.config(text=description)
        self.details_label.config(text=f"Feels like: {feels_like:.0f} F | Humidity: {humidity}% | Wind: {wind_speed:.1f} mph")
        


    def add_to_favorites(self):
        """
        Add current city to favorites list
        """

        # if the field is empty, does nothing
        if not self.current_city:
            return

        # if the city already exists in the favorites list
        if self.current_city in self.favorites:
            msgbx.showinfo("Already Added", f"{self.current_city} is already in your favorites list!")
            return

        # Add the city to favorites list
        self.favorites.append(self.current_city)

        # Update dropdown list
        self.update_dropdown()

        # Save our favorites list to a file
        self.save_favorites()

# You are absolutely insane, there was no duplicate function here.     

    def update_dropdown(self):
        """
        updates the dropdown
        """
        self.city_dropdown["values"] = self.favorites

        if not self.favorites:
            self.city_dropdown.set("No favorites")
        else:
            self.city_dropdown.set("Select favorited city...")


    def save_favorites(self):
        """
        saves the favorites
        """

        # Usually shouldn't error, saves all the items in self.favorites into a json.
        try:
            data = {
                "favorites": self.favorites,
                "last_update": datetime.now().strftime("%T-%m-%d %H:%M:%S")
            }

            with open(self.FAVORITES_FILE, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            msgbx.showerror("Save Error", f"Could not save. {str(e)}")


    def swap_unit(self):
        """
        swaps units
        """

        # Very stupid, if A is F then A is C
        # but if A is not F and is in fact C then A is F.
        # Also updates unit_label to show the correct unit.
        if self.current_unit == "C":
            self.current_unit = "F"
        elif self.current_unit == "F":
            self.current_unit = "C"

        self.unit_label.config(text=f"{self.current_unit}")
        self.load_weather_from_favorite()
        self.search_weather()

        #print(f"Current unit is: {self.current_unit}")

    def load_favorites(self):
        """
        loads the favorites
        """

        # Loads the json file and appends the data to the combobox.
        try:
            with open(self.FAVORITES_FILE, "r") as f:
                data = json.load(f)
                self.favorites = data.get("favorites", [])
        except FileNotFounderror:
            self.favorites = []
        except Exception as e:
            msgbx.showerror("Load Error", f"Could not load favorites: {str(e)}")
            self.favorites = []


    def load_weather_from_favorite(self, event = None):
        """
        Load weather for selected favorite city
        
        Args:
            event: Combobox selection event (not used but required by bind)
        """
        
        city = self.city_dropdown.get()
        
        if city and city != "select city...":
            coords = self.get_coordinates(city)
            if not coords:
                return
            lat, lon, full_city_name = coords
            
            weather_data = self.get_weather(lat, lon)
            if weather_data:
                self.display_weather(weather_data, full_city_name)
            self.city_entry.delete(0, 'end')

    def remove_from_favorites(self):
        """
        removes city from favorite
        """
        if not self.current_city or self.current_city not in self.favorites:
            return

        response = msgbx.askyesno("Remove", "Remove city from favorites?")

        if response:
            self.favorites.remove(self.current_city)
            self.update_dropdown()
            self.save_favorites()

    def display_forecast(self):
        pass

    def minus_forecast(self):
        pass

    def multi_forecast(self):
        print("I am DEFINETLY doing something, and I do not-- I repeat-- NOT\n conflict with the swap unit.")
