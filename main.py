import tkinter as tk
import requests
import os

HEIGHT = 700
WIDTH = 800

# Format the weather response to display
def format_response(weather):
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        temp = round(temp, 2)
        final_str = f'City: {name}\nDescription: {desc}\nTemperature: {temp}°C\n'
    except Exception as e:
        final_str = f'Exception: {e}\nThere was a problem retrieving the data!'
    return final_str

# Fetch the weather data using latitude and longitude
def get_weather(lat, lon):
    weather_key = os.environ.get('WEATHER_KEY')
    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {'appid': weather_key, 'lat': lat, 'lon': lon, 'units': 'metric'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        weather = response.json()
        label['text'] = format_response(weather)
        print(weather)
    else:
        label['text'] = f'Error: Unable to fetch weather data. Status code: {response.status_code}'
        print(f'Error: {response.status_code} - {response.text}')

# Fetch the coordinates using city name
def get_cords(city):
    weather_key = os.environ.get('WEATHER_KEY')
    url = 'http://api.openweathermap.org/geo/1.0/direct'
    params = {'appid': weather_key, 'q': city, 'limit': 1}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        cords = response.json()
        print(cords)  # Debugging output to see the response
        try:
            if cords:
                lat = cords[0]['lat']
                lon = cords[0]['lon']
                get_weather(lat, lon)
            else:
                label['text'] = 'Invalid Selection! No coordinates found.'
        except Exception as e:
            label['text'] = f'Invalid Selection!\nException: {e}!'
    else:
        label['text'] = f'Error: Unable to fetch coordinates. Status code: {response.status_code}'
        print(f'Error: {response.status_code} - {response.text}')

root = tk.Tk()
root.title("Sky Tracker")  # Set the title of the window

# Create a canvas for the GUI
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# Set background image
bg_img = tk.PhotoImage(file='background.png')
bg_label = tk.Label(root, image=bg_img)
bg_label.place(relwidth=1, relheight=1)

# Create a frame for the input and button
frame = tk.Frame(root, bg='purple', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# Input field for city name
entry = tk.Entry(frame, font=('Bell MT', 20))
entry.place(relwidth=0.65, relheight=1)

# Button to trigger the get_cords function
button = tk.Button(frame, text='Get Info', fg='dark blue', bg='light gray', font=('Bell MT', 20),
                   command=lambda: get_cords(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.25)

# Create a lower frame to display weather information
lower_frame = tk.Frame(root, bg='purple', bd=5)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.5, anchor='n')

# Label to show the weather data
label = tk.Label(lower_frame, bg='pink', font=('Bell MT', 16))
label.place(relwidth=1, relheight=1)

# Run the Tkinter event loop
root.mainloop()
