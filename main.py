import tkinter as tk
import numpy as np

class PlottingGUI:
    def __init__(self, master):
        self.master = master
        master.title("Multi-Plotting GUI")

        # Main frame for the plot and control area
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(side=tk.LEFT)

        # Canvas for plotting
        self.canvas = tk.Canvas(self.main_frame, width=600, height=400, bg='white')
        self.canvas.pack(pady=20)

        # Frame for control buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(side=tk.BOTTOM)

        # Buttons to plot different functions
        self.plot_button1 = tk.Button(self.button_frame, text="Show Sine Wave", command=self.toggle_sine)
        self.plot_button1.pack(side=tk.LEFT, padx=5)

        self.plot_button2 = tk.Button(self.button_frame, text="Show Cosine Wave", command=self.toggle_cosine)
        self.plot_button2.pack(side=tk.LEFT, padx=5)

        self.plot_button3 = tk.Button(self.button_frame, text="Show Tangent Wave", command=self.toggle_tangent)
        self.plot_button3.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear All Plots", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        # Frame for text boxes and labels
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, padx=10)

        # Labels and text boxes for values
        tk.Label(self.control_frame, text="Sine:").pack(anchor=tk.W)
        self.sine_value = tk.Entry(self.control_frame, width=10)
        self.sine_value.pack(pady=5)
        self.sine_value.insert(0, "Hidden")

        tk.Label(self.control_frame, text="Cosine:").pack(anchor=tk.W)
        self.cosine_value = tk.Entry(self.control_frame, width=10)
        self.cosine_value.pack(pady=5)
        self.cosine_value.insert(0, "Hidden")

        tk.Label(self.control_frame, text="Tangent:").pack(anchor=tk.W)
        self.tangent_value = tk.Entry(self.control_frame, width=10)
        self.tangent_value.pack(pady=5)
        self.tangent_value.insert(0, "Hidden")

        self.plotting_state = {
            "sine": False,
            "cosine": False,
            "tangent": False
        }

    def toggle_sine(self):
        self.plotting_state["sine"] = not self.plotting_state["sine"]
        self.toggle_plot(np.sin, "Sine Wave", 'blue', self.plotting_state["sine"])
        self.update_value_display()

    def toggle_cosine(self):
        self.plotting_state["cosine"] = not self.plotting_state["cosine"]
        self.toggle_plot(np.cos, "Cosine Wave", 'green', self.plotting_state["cosine"])
        self.update_value_display()

    def toggle_tangent(self):
        self.plotting_state["tangent"] = not self.plotting_state["tangent"]
        self.toggle_plot(np.tan, "Tangent Wave", 'red', self.plotting_state["tangent"], limit_y=True)
        self.update_value_display()

    def toggle_plot(self, func, title, color, show, limit_y=False):
        if show:
            self.plot_function(func, title, color, limit_y)
        else:
            self.clear_plot(title)

    def plot_function(self, func, title, color, limit_y=False):
        width = 600
        height = 400
        margin = 20
        
        # Draw axes (if not already drawn)
        if not hasattr(self, 'axes_drawn'):
            self.canvas.create_line(margin, height / 2, width - margin, height / 2, fill='black')  # X-axis
            self.canvas.create_line(width / 2, margin, width / 2, height - margin, fill='black')  # Y-axis
            self.axes_drawn = True

        # Plotting the function
        x_values = np.linspace(-2 * np.pi, 2 * np.pi, 100)
        y_values = func(x_values)

        if limit_y:
            y_values = np.clip(y_values, -10, 10)  # Limit y-values for tangent

        scale_x = (width - 2 * margin) / (4 * np.pi)  # Scale for x-axis
        scale_y = (height - 2 * margin) / 20  # Scale for y-axis

        # Draw the plot
        for i in range(len(x_values) - 1):
            x1 = int((x_values[i] + 2 * np.pi) * scale_x + margin)
            y1 = int(height / 2 - y_values[i] * scale_y)
            x2 = int((x_values[i + 1] + 2 * np.pi) * scale_x + margin)
            y2 = int(height / 2 - y_values[i + 1] * scale_y)
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

    def clear_plot(self, title):
        # Clear specific plot by redrawing the canvas and replotting the others
        self.clear_canvas()
        if self.plotting_state["sine"]:
            self.plot_function(np.sin, "Sine Wave", 'blue')
        if self.plotting_state["cosine"]:
            self.plot_function(np.cos, "Cosine Wave", 'green')
        if self.plotting_state["tangent"]:
            self.plot_function(np.tan, "Tangent Wave", 'red', limit_y=True)

    def clear_canvas(self):
        self.canvas.delete("all")  # Clear the canvas
        self.axes_drawn = False  # Reset axes drawn state
        self.update_value_display()  # Clear values

    def update_value_display(self):
        # Update the text boxes with current plot status
        self.sine_value.delete(0, tk.END)
        self.sine_value.insert(0, "Visible" if self.plotting_state["sine"] else "Hidden")
        
        self.cosine_value.delete(0, tk.END)
        self.cosine_value.insert(0, "Visible" if self.plotting_state["cosine"] else "Hidden")
        
        self.tangent_value.delete(0, tk.END)
        self.tangent_value.insert(0, "Visible" if self.plotting_state["tangent"] else "Hidden")

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PlottingGUI(root)
    root.mainloop()