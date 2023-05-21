import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to handle button click event
def plot_chart():
    # Clear previous chart
    axes.cla()

    # Get data from the textboxes
    x_data = textbox_x.get("1.0", tk.END).strip().split('\n')
    y_data = textbox_y.get("1.0", tk.END).strip().split('\n')

    # Convert data to float
    x = [float(value) for value in x_data if value.strip()]
    y = [float(value) for value in y_data if value.strip()]

    # Plot the selected chart
    if chart_type.get() == "Bar Chart":
        axes.bar(x, y)
    elif chart_type.get() == "Line Chart":
        axes.plot(x, y)
    elif chart_type.get() == "Scatter Plot":
        axes.scatter(x, y)

    canvas.draw()

# Create a Tkinter window
window = tk.Tk()
window.title("Matplotlib Chart in Tkinter")

# Create a Matplotlib figure and axes
figure = Figure(figsize=(6, 4), dpi=100)
axes = figure.add_subplot(111)

# Create a FigureCanvasTkAgg object to display the chart in the Tkinter window
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.LEFT, padx=10, pady=10)

# Create a frame for the textboxes and controls
frame = tk.Frame(window)
frame.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a textbox for x values
label_x = tk.Label(frame, text="X Values:")
label_x.pack()
textbox_x = tk.Text(frame, height=10, width=10)
textbox_x.pack()

# Create a textbox for y values
label_y = tk.Label(frame, text="Y Values:")
label_y.pack()
textbox_y = tk.Text(frame, height=10, width=10)
textbox_y.pack()

# Create a drop-down menu for chart selection
chart_type_label = tk.Label(frame, text="Chart Type:")
chart_type_label.pack()
chart_type = tk.StringVar()
chart_type.set("Bar Chart")
chart_type_dropdown = tk.OptionMenu(frame, chart_type, "Bar Chart", "Line Chart", "Scatter Plot")
chart_type_dropdown.pack()

# Create a button
button = tk.Button(frame, text="Plot Chart", command=plot_chart)
button.pack()

# Run the Tkinter event loop
window.mainloop()
