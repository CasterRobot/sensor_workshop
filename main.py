import tkinter as tk
import numpy as np

class PlottingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Multi-Plotting GUI")

        self.canvas = tk.Canvas(master, width=600, height=400, bg='white')
        self.canvas.pack(pady=10)

        # Buttons to plot different functions
        self.plot_button1 = tk.Button(master, text="Show Sine Wave", command=self.plot_sine)
        self.plot_button1.pack(side=tk.LEFT, padx=5)

        self.plot_button2 = tk.Button(master, text="Show Cosine Wave", command=self.plot_cosine)
        self.plot_button2.pack(side=tk.LEFT, padx=5)

        self.plot_button3 = tk.Button(master, text="Show Tangent Wave", command=self.plot_tangent)
        self.plot_button3.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(master, text="Clear Plots", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.show_all_button = tk.Button(master, text="Show All Plots", command=self.show_all)
        self.show_all_button.pack(side=tk.LEFT, padx=5)

    def plot_sine(self):
        self.plot_function(np.sin, "Sine Wave", 'blue')

    def plot_cosine(self):
        self.plot_function(np.cos, "Cosine Wave", 'green')

    def plot_tangent(self):
        self.plot_function(np.tan, "Tangent Wave", 'red', limit_y=True)

    def show_all(self):
        self.clear_canvas()
        self.plot_sine()
        self.plot_cosine()
        self.plot_tangent()

    def plot_function(self, func, title, color, limit_y=False):
        width = 600
        height = 400
        margin = 20
        
        # Draw axes
        self.canvas.create_line(margin, height / 2, width - margin, height / 2, fill='black')  # X-axis
        self.canvas.create_line(width / 2, margin, width / 2, height - margin, fill='black')  # Y-axis

        # Plotting the function
        x_values = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y_values = func(x_values)

        if limit_y:
            y_values = np.clip(y_values, -10, 10)  # Limit y-values for tangent

        scale_x = (width - 2 * margin) / (4 * np.pi)  # Scale for x-axis
        scale_y = (height - 2 * margin) / 20  # Scale for y-axis

        for i in range(len(x_values) - 1):
            x1 = int((x_values[i] + 2 * np.pi) * scale_x + margin)
            y1 = int(height / 2 - y_values[i] * scale_y)
            x2 = int((x_values[i + 1] + 2 * np.pi) * scale_x + margin)
            y2 = int(height / 2 - y_values[i + 1] * scale_y)
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

    def clear_canvas(self):
        self.canvas.delete("all")  # Clear the canvas

if __name__ == "__main__":
    root = tk.Tk()
    gui = PlottingGUI(root)
    root.mainloop()