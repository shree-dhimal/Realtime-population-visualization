from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ctypes
import requests
import datetime
import os
import csv

# Get the screen resolution
user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

# Create a Tkinter window
root = tk.Tk()
root.title("Real-Time Population Visualization")
root.geometry(f"{screen_width}x{screen_height}")
root.configure(bg="white")
root.resizable(False, False)

# Create a Matplotlib figure and subplot
fig = Figure(figsize=(0.8 * screen_width / 100, 0.6 * screen_height / 100), dpi=100)
ax = fig.add_subplot(1, 1, 1)

plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

df = pd.read_csv('data_stream.csv')

index = count()
current_index = 0  # Track the current index for animation

animation_running = False  # Flag variable to control animation loop

def add_data(x, y):
    x_vals.append(x)
    y_vals.append(y)
    ax.clear()
    ax.plot(x_vals, y_vals)

    # Set the x-axis and y-axis labels
    ax.set_xlabel('Year')
    ax.set_ylabel('Population')

    # Update the plot on the canvas
    canvas.draw()

    # Keep the last data point visible on the graph
    ax.relim()
    ax.autoscale_view()

def animate():
    global current_index

    if not animation_running:
        return

    if current_index >= len(df):
        current_index = 0  # Restart from the beginning

    new_data = df.iloc[current_index]
    x = new_data['Year']  # Assuming 'Year' column in the CSV file
    y = new_data['Population']

    add_data(x, y)

    current_index += 1  # Increment the current index

    # Schedule the next animation
    root.after(5000, animate)

def update_chart():
    if textbox_country.index("end") == 0:
        tk.messagebox.showinfo("Empty Text Box", "Please Enter The Country Code to Continue!")
    else:
        write_csv()
        # Clear the existing data
        x_vals.clear()
        y_vals.clear()

        # Reset the current index to start from the same spot
        global current_index
        current_index = 0

        # Set the animation flag to True
        global animation_running
        animation_running = True

        country_name = textbox_country.get()
        label_static_country.config(text=f"Country Name: {country_name.upper()}")

        # Start the animation
        animate()
        textbox_country.delete(0, tk.END)

def stop_animation():
    global animation_running
    animation_running = False

    # Update the country name
    country_name = textbox_country.get()
    label_static_country.config(text=f"Country Name: {country_name.upper()}")

    # Clear the textbox
    textbox_country.delete(0, tk.END)

def get_country_population(country_code, year):
    # Your World Bank Open Data API key
    api_key = "YOUR_API_KEY"

    # Prepare the URL
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/SP.POP.TOTL?format=json"

    # Send a GET request to the API with the API key and desired year
    response = requests.get(url, params={"api_key": api_key, "date": year})

    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        try:
            # Extract the population value
            population = data[1][0]['value']
            return year, population
        except:
            tk.messagebox.showinfo("ERROR", "The Country Code you provided doesn't have the data or you have entered the wrong Country code, please try again")
            return None

    else:
        tk.messagebox.showinfo("ERROR", "The Country Code you provided doesn't have the data or you have entered the wrong Country code, please try again")
        return None

def write_csv():
    x = datetime.datetime.now()
    this_year = x.year - 1

    country_name = textbox_country.get().upper()
    init_year = 1980
    data_list = []

    if get_country_population(country_name, init_year) is None:
        tk.messagebox.showinfo("ERROR", "The Country Code you provided doesn't have the data or you have entered the wrong Country code, please try again")
    else:
        while init_year < this_year:
            year, population = get_country_population(country_name, init_year)
            data_list.append([year, population])
            init_year += 1

    file_path = 'data_stream.csv'
    file_exists = os.path.isfile(file_path)

    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Year', 'Population'])
        writer.writerows(data_list)
        return True

# Create a label for the static country name
label_static_country = tk.Label(root, text="Country Name:", font=("Arial", 12), bg="white")
label_static_country.pack(pady=10)

# Create a canvas to display the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=(10, 0))

# Create a label for the country name
label_country = tk.Label(button_frame, text="Enter Country Name:", font=("Arial", 12), bg="white")
label_country.grid(row=0, column=0, padx=10, pady=5)

# Create a textbox for the country name
textbox_country = tk.Entry(button_frame, font=("Arial", 12), width=20)
textbox_country.grid(row=0, column=1, padx=10, pady=5)

# Create buttons
start_button = tk.Button(button_frame, text="Start", font=("Arial", 12), command=update_chart)
start_button.grid(row=0, column=2, padx=10, pady=5)

stop_button = tk.Button(button_frame, text="Stop", font=("Arial", 12), command=stop_animation)
stop_button.grid(row=0, column=3, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
