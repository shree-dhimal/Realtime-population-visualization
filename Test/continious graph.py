import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

plt.style.use('fivethirtyeight')

x_vals =[]
y_vals = []

df = pd.read_csv('data.csv')
plt.plot(x_vals,y_vals)

index = count()

def animate(i):
    new_data = df.iloc[i]
    x = new_data['X']  # Assuming 'x' column in the CSV file
    y = new_data['Y']

    x_vals.append(x)
    y_vals.append(y)
    plt.cla()
    plt.plot(x_vals,y_vals)

ani = FuncAnimation(plt.gcf(),animate, interval = 10)
# plt.tight_layout()
plt.show()