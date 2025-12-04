import tkinter as tk
from tkinter import messagebox as msgbx
from tkinter.ttk import Combobox
import requests
import json
from datetime import datetime

class WeatherApp:
    """
    Weather my app till I forecast the precipitation chances
    """
    API_KEY = "d771e5e1b5ae57994e3319563f2acb60"
    WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
    GEOCODING_URL = "http://api.openweathermap.org/geo/1.0/direct"
    FAVORITES_FILE = "favorites.json"

    def __init__(self, root):
        """
        does more junk
        """

        # Tkinter stuff
        self.root = root
        self.root.title("Weathuh Opp")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.window_bg_color = "#3b72ad"
        self.window_fg_color = "#9dc2b9"
        self.root.config(bg=self.window_bg_color)

        self.favorites = []
        self.current_city = ""
        self.current_unit = "F"
        # make widgets

        self.load_favorites()

        self.create_widgets()

        if self.favorites:
            self.load_weather_from_favorite()

    def create_widgets(self):
        """
        gwgwgrewgwgewewgewgewggwg2wgewgewgewgewgewgegewgewgewwgewwggrewwgwgrwbrgrewewggwggewggwgewgewgewgewegewgewgogegewewggewgewewggwgewgew
        """


        # title label
        title_label = tk.Label(
            self.root,
            text = "Hoodini",
            font = ("Impact", 24, "bold"),
            bg = self.window_bg_color, fg = self.window_fg_color
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="ew", pady=20)


        # Favorites Section
        favorites_label = tk.Label(
            self.root,
            text= "Favorited Locations ",
            font = ("Courier new", 12),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        favorites_label.grid(row=1,column=0,padx=10,sticky="e")


        self.city_dropdown = Combobox(
            self.root,
            values = self.favorites,
            width = 34,
            font = ("Courier new", 11)
        )
        self.city_dropdown.set("select city...")
        self.city_dropdown.bind("<<ComboboxSelected>>", self.load_weather_from_favorite)
        self.city_dropdown.grid(row=1,column=1,padx=5,sticky="w")
        # Fav. Sec.


        # Search Label
        search_label = tk.Label(
            self.root,
            text = "Search for a city --> ",
            font = ("Courier new", 12),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        search_label.grid(row=2,column=0,padx=10,pady=10,sticky="e")


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


        #weathuh displayuh framuh
        self.weather_frame = tk.Frame(
            self.root,
            bg = self.window_bg_color,
            relief = "solid",
            borderwidth=3
        )
        self.weather_frame.grid(row=3,column=0,columnspan=3,padx=20,pady=20,sticky="nsew")


        self.city_label = tk.Label(
            self.weather_frame,
            text = "Search for a city",
            font = ("Courier new", 16),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.city_label.pack()


        self.temp_label = tk.Label(
            self.weather_frame,
            text = "",
            font = ("Impact", 32),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.temp_label.pack(pady=5)


        self.condition_label = tk.Label(
            self.weather_frame,
            text = "",
            font = ("Arial", 14),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.condition_label.pack(pady=5)


        self.details_label = tk.Label(
            self.weather_frame,
            text = "",
            font = ("Arial", 14),
            bg = self.window_bg_color,
            fg = self.window_fg_color
        )
        self.details_label.pack()


        button_frame = tk.Frame(
            self.root,
            bg = self.window_bg_color
        )
        button_frame.grid(row=4,column=0,columnspan=3,padx=5,pady=10)


        self.add_button = tk.Button(
            button_frame,
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


        self.remove_button = tk.Button(
            button_frame,
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


        self.unit_button = tk.Button(
            button_frame,
            text = "Swap celcius/fahrenheit",
            font=("Arial", 11),
            bg=self.window_bg_color,
            fg=self.window_fg_color,
            command = self.swap_unit,
            width = 18
            )
        self.unit_button.pack(side="right",padx=5)

        self.unit_label = tk.Label(
            button_frame,
            text = f"{self.current_unit}",
            font=("Arial", 11, "bold"),
            bg=self.window_bg_color,
            fg=self.window_fg_color,
            width = 5
            )
        self.unit_label.pack(side="left",padx=5)

        for i in range(4):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(3):
            self.root.grid_columnconfigure(i,weight=1)


    def search_weather(self):
        city = self.city_entry.get().strip()

        if not city:
            msgbx.showwarning("No City!", "You did not enter a city name!\nPlease enter a city name.")
            return

        coords = self.get_coordinates(city)
        if not coords:
            msgbx.showerror("No City", "That City wasn't found!\nPlease enter a valid city.")
            return

        lat, lon, full_city_name = coords

        weather_data = self.get_weather(lat, lon)
        if weather_data:
            print(weather_data)
            self.display_weather(weather_data, full_city_name)


    def get_coordinates(self,city):

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

        if not data:
            return

        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"] ################################################################
        wind_speed = data["wind"]["speed"]
        self.current_city = city

        if self.current_unit == "C":
            self.temp_label.config(text=f"{((temp - 32)*(5/9)):.0f} C")
        elif self.current_unit == "F":
            self.temp_label.config(text=f"{temp} F")

        self.city_label.config(text=self.current_city)
        self.condition_label.config(text=description)
        self.details_label.config(text=f"Feels like: {feels_like:.0f} F | Humidity: {humidity}% | Wind: {wind_speed:.1f} mph")
        self.city_entry.delete(0, 'end')


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


    def update_dropdown(self):
        """
        Update the favorites dropdown with our current favorites list
        """

        self.city_dropdown["values"] = self.favorites

        if not self.favorites:
            self.city_dropdown.set("No favorites found")
        else:
            self.city_dropdown.set("Select favorite city...")
      

    def update_dropdown(self):

        self.city_dropdown["values"] = self.favorites

        if not self.favorites:
            self.city_dropdown.set("No favorites")
        else:
            self.city_dropdown.set("Select favorited city...")


    def save_favorites(self):

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
        if self.current_unit == "F":
            self.current_unit == "C"
        elif self.current_unit == "C":
            self.current_unit == "F"

        self.unit_label.config(text=f"{self.current_unit}")
        print(f"Current unit is: {self.current_unit}")

    def load_favorites(self):
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


    def remove_from_favorites(self):

        if not self.current_city or self.current_city not in self.favorites:
            return

        response = msgbx.askyesno("Remove", "Remove city from favorites?")

        if response:
            self.favorites.remove(self.current_city)
            self.update_dropdown()
            self.save_favorites()