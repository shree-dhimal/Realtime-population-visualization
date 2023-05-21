import tkinter as tk
import random
from itertools import count
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

x_vals = []
y_vals = []
index = count()
def plot_chart():
    x_vals.append(next(index))
    y_vals.append(random.randint(0,5))
    axes.cla()
    axes.plot(x_vals, y_vals)

    canvas.draw()
    ani = FuncAnimation(plot_chart, interval = 1000)

# Create a Tkinter window
window = tk.Tk()
window.title("Matplotlib Chart in Tkinter")



# Create a Matplotlib figure and axes
figure = Figure(figsize=(10, 60), dpi=100)
axes = figure.add_subplot(111)


canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

# Create a frame for the textboxes and controls
frame = tk.Frame(window)
frame.pack(side=tk.RIGHT, padx=2, pady=5)

# Create a textbox for y values
label_y = tk.Label(frame, text="Country Name")
label_y.pack()
textbox_y = tk.Text(frame, height=2, width=20, pady=0)
textbox_y.pack()

# Create a button
button = tk.Button(frame, text="Plot Chart", command=plot_chart)
button.pack()



window.mainloop()