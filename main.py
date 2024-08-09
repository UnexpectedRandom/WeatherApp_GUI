import customtkinter as ctk
import requests

# Weather App
API_KEY = ""

class App:
    def __init__(self, API="", Location_Name="London"):
        self.API = API
        self.Location_Name = Location_Name

    def get_response(self):
        response = requests.get(
            f'http://api.weatherapi.com/v1/current.json?key={self.API}&q={self.Location_Name}&aqi=no')
        if response.status_code == 200:
            return response.json()
        else:
            return "Not A Location Or Invalid API Key"

    def filter_json(self):
        response = self.get_response()
        if isinstance(response, dict) and "current" in response:
            temp_c = response["current"].get("temp_c", "Temperature data not found")
            day_q = response["current"].get("is_day", "Is_day data not found")
            wind_speed = response["current"].get("wind_mph", "Wind speed data not found")
            humidity = response["current"].get("humidity", "Humidity data not found")
            feels_like = response["current"].get("feelslike_c", "Feels like data not found")

            day_q = "Day" if day_q == 1 else "Night"

            return temp_c, day_q, wind_speed, humidity, feels_like
        else:
            return "Error: Unable to fetch data"

class GUI(ctk.CTk):
    def __init__(self, geometry_x=450, geometry_y=450, title="Weather App"):
        super().__init__()

        self.geometry_x = geometry_x
        self.geometry_y = geometry_y
        self.title = title

        self.geometry(f"{self.geometry_x}x{self.geometry_y}")

        # Center the widgets
        self.columnconfigure([0, 1], weight=1)
        self.rowconfigure([0, 1, 2, 3, 4], weight=1)

        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Pick a City or Country", font=("Arial", 16, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="n")

        # Entry for city name
        self.text_box = ctk.CTkEntry(self, placeholder_text="Enter City: ")
        self.text_box.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="ew")

        # Create frames to act as backgrounds for labels
        self.frame_temp_c = ctk.CTkFrame(self, corner_radius=10)
        self.frame_temp_c.grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        self.label_temp_c = ctk.CTkLabel(self.frame_temp_c, text="")
        self.label_temp_c.pack(padx=10, pady=10)

        self.frame_day_q = ctk.CTkFrame(self, corner_radius=10)
        self.frame_day_q.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        self.label_day_q = ctk.CTkLabel(self.frame_day_q, text="")
        self.label_day_q.pack(padx=10, pady=10)

        self.frame_wind_speed = ctk.CTkFrame(self, corner_radius=10)
        self.frame_wind_speed.grid(row=3, column=0, padx=10, pady=5, sticky="ew")
        self.label_wind_speed = ctk.CTkLabel(self.frame_wind_speed, text="")
        self.label_wind_speed.pack(padx=10, pady=10)

        self.frame_humidity = ctk.CTkFrame(self, corner_radius=10)
        self.frame_humidity.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.label_humidity = ctk.CTkLabel(self.frame_humidity, text="")
        self.label_humidity.pack(padx=10, pady=10)

        self.frame_feels_like = ctk.CTkFrame(self, corner_radius=10)
        self.frame_feels_like.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.label_feels_like = ctk.CTkLabel(self.frame_feels_like, text="")
        self.label_feels_like.pack(padx=10, pady=10)

        # Button to check weather
        self.check_button = ctk.CTkButton(self, text="Check", command=self.update_labels)
        self.check_button.grid(row=5, column=0, columnspan=2, padx=20, pady=10)

    def update_labels(self):
        city = self.text_box.get()
        weather_app = App(API=API_KEY, Location_Name=city)
        output = weather_app.filter_json()

        if isinstance(output, tuple):
            self.label_temp_c.configure(text=f"Temperature: {output[0]} °C")
            self.label_day_q.configure(text=f"Day/Night: {output[1]}")
            self.label_wind_speed.configure(text=f"Wind Speed: {output[2]} mph")
            self.label_humidity.configure(text=f"Humidity: {output[3]}%")
            self.label_feels_like.configure(text=f"Feels Like: {output[4]} °C")
        else:
            self.label_temp_c.configure(text=output)

# Create and run the application
app = GUI()
app.mainloop()
