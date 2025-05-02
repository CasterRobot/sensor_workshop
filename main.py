import tkinter as tk
import numpy as np
from serial_reading import *
from data_processing import *

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
        self.plot_button1 = tk.Button(self.button_frame, text="Raw data", command=self.toggle_raw)
        self.plot_button1.pack(side=tk.LEFT, padx=5)

        self.plot_button2 = tk.Button(self.button_frame, text="Filtered data", command=self.toggle_filtered)
        self.plot_button2.pack(side=tk.LEFT, padx=5)

        self.plot_button3 = tk.Button(self.button_frame, text="Else", command=self.toggle_tangent)
        self.plot_button3.pack(side=tk.LEFT, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop/Start", command=self.stop_update)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear All Plots", command=self.clear_canvas)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_application)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # Frame for text boxes and labels
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(side=tk.RIGHT, padx=10)

        # Labels and text boxes for values
        tk.Label(self.control_frame, text="Raw:").pack(anchor=tk.W)
        self.raw_value = tk.Entry(self.control_frame, width=10)
        self.raw_value.pack(pady=5)
        self.raw_value.insert(0, "Hidden")

        tk.Label(self.control_frame, text="Filtered:").pack(anchor=tk.W)
        self.filtered_value = tk.Entry(self.control_frame, width=10)
        self.filtered_value.pack(pady=5)
        self.filtered_value.insert(0, "Hidden")

        tk.Label(self.control_frame, text="Tangent:").pack(anchor=tk.W)
        self.tangent_value = tk.Entry(self.control_frame, width=10)
        self.tangent_value.pack(pady=5)
        self.tangent_value.insert(0, "Hidden")

        # Frame for sliders
        self.slider_frame = tk.Frame(master)
        self.slider_frame.pack(side=tk.RIGHT, padx=10)

        # Cutoff frequency slider
        self.cutoff_label = tk.Label(self.slider_frame, text="Cutoff Frequency:")
        self.cutoff_label.pack(anchor=tk.W)

        self.cutoff_slider = tk.Scale(self.slider_frame, from_=1e-5, to=5, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_cutoff)
        self.cutoff_slider.pack(fill=tk.X)

        # Sampling frequency slider
        self.fs_label = tk.Label(self.slider_frame, text="Sampling Frequency (fs):")
        self.fs_label.pack(anchor=tk.W)

        self.fs_slider = tk.Scale(self.slider_frame, from_=1e-5, to=10, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_fs)
        self.fs_slider.pack(fill=tk.X)

        # Labels for current values
        self.current_cutoff = tk.Label(self.slider_frame, text="Current Cutoff: 0")
        self.current_cutoff.pack(anchor=tk.W)

        self.current_fs = tk.Label(self.slider_frame, text="Current fs: 1")
        self.current_fs.pack(anchor=tk.W)

        self.plotting_state = {
            "raw": False,
            "filtered": False,
            "tangent": False
        }

        self.is_update = True
        self.cutoff = 500.0
        self.fs = 50.0

        # self.open_serial()

    def open_serial(self):
        # Initialize serial connection
        sys.stdout.reconfigure(encoding='utf-8') 
        port = '/dev/ttyUSB0'  # or '/dev/ttyACM0'
        baud_rate = 921600
        self.ser = serial.Serial(port, baud_rate, timeout=0.5)
        if self.ser.isOpen():
            print("open success")
        else:
            print("open failed")

    def update_cutoff(self, value):
        self.current_cutoff.config(text=f"Current Cutoff: {value}")
        self.cutoff = float(value)
        self.filtered_data = lowpass_filter(self.current_data, cutoff=self.cutoff, fs=self.fs, order=6)
        self.clear_plot()

    def update_fs(self, value):
        self.current_fs.config(text=f"Current fs: {value}")
        self.fs = float(value)
        self.filtered_data = lowpass_filter(self.current_data, cutoff=self.cutoff, fs=self.fs, order=6)
        self.clear_plot()

    def toggle_raw(self):
        self.is_update = True
        self.plotting_state["raw"] = not self.plotting_state["raw"]
        self.current_data = get_serial_data()
        self.toggle_plot(self.current_data, "Raw", 'blue', self.plotting_state["raw"])
        self.update_plot()

    def toggle_filtered(self):
        self.plotting_state["filtered"] = not self.plotting_state["filtered"]
        self.filtered_data = lowpass_filter(self.current_data, cutoff=self.cutoff, fs=self.fs, order=6)
        self.toggle_plot(self.filtered_data, "Filtered", 'green', self.plotting_state["filtered"])
        self.update_plot()

    def toggle_tangent(self):
        self.plotting_state["tangent"] = not self.plotting_state["tangent"]
        self.toggle_plot(np.tan, "Tangent Wave", 'red', self.plotting_state["tangent"], limit_y=True)
        self.update_plot()

    def toggle_plot(self, func, title, color, show, limit_y=False):
        if show:
            self.plot_function(func, title, color, limit_y)
        else:
            self.clear_plot()
    
    def update_plot(self, limit_y=False):
        self.clear_canvas()
        
        if self.plotting_state["raw"]:
            self.current_data  = get_serial_data()
            self.plot_function(self.current_data, "Raw", 'blue', limit_y)
        
        if self.plotting_state["filtered"]:
            self.filtered_data = lowpass_filter(self.current_data, cutoff=self.cutoff, fs=self.fs, order=6)
            self.plot_function(self.filtered_data, "Filtered", 'green', limit_y)
        
        if self.plotting_state["tangent"]:
            self.plot_function(np.tan, "Tangent Wave", 'red', limit_y)

        if self.is_update:
            if self.plotting_state["raw"] or self.plotting_state["filtered"] or self.plotting_state["tangent"]:
                self.update_value_display()
                self.master.after(1000, self.update_plot)  # Update every 100 ms

    def draw_y_axis_labels(self, margin, height, padding, y_min, y_max):
        # Draw y-axis labels based on defined y_min and y_max
        y_ticks = 5  # Number of ticks
        for i in range(y_ticks + 1):
            y_value = y_min + i * (y_max - y_min) / y_ticks
            y_pos = height - (y_value - y_min) / (y_max - y_min) * (height - 2 * margin) - margin
            self.canvas.create_text(margin - 3, y_pos, text=f"{y_value:.2f}", anchor='e', font=("Arial", 10))

    def plot_function(self, data, title, color, limit_y=False):
        data = data[5:]
        width = 600
        height = 400
        margin = 50

        # Plotting the function
        NUM = len(data)
        x_values = list(range(NUM)) 
        y_values = data

        y_max = np.max(data)
        y_min = np.min(data)

        

        # if not hasattr(self, 'axes_drawn'):
        self.canvas.create_line(margin, height - margin, width - margin, height - margin, fill='black')  # X-axis
        self.canvas.create_line(margin, margin, margin, height - margin, fill='black')  # Y-axis
        self.draw_y_axis_labels(margin, height, margin, y_min=y_min, y_max=y_max)
        self.axes_drawn = True

        # Draw points using raw x and y values
        # point_radius = 3  # Radius for the points
        # draw points 
        # for i in range(len(x_values)):
        #     x = int((x_values[i]) * (width - 2 * margin) / NUM + margin)
        #     scaled_y = (y_values[i] - y_min) / (y_max - y_min) * (height - 2 * margin)
        #     y = int(height - scaled_y - margin)
        #     self.canvas.create_oval(x - point_radius, y - point_radius, x + point_radius, y + point_radius, fill=color)

        # draw lines
        for i in range(1, len(x_values) - 1):
            x1 = int((x_values[i]) * (width - 2 * margin) / NUM + margin)
            scaled_y = (y_values[i] - y_min) / (y_max - y_min) * (height - 2 * margin)
            y1 = int(height - scaled_y - margin)

            x2 = int((x_values[i+1]) * (width - 2 * margin) / NUM + margin)
            scaled_y = (y_values[i+1] - y_min) / (y_max - y_min) * (height - 2 * margin)
            y2 = int(height - scaled_y - margin)
            self.canvas.create_line(x1, y1, x2, y2, fill=color)

    
    def clear_plot(self):
        # Clear specific plot by redrawing the canvas and replotting the others
        self.clear_canvas()
        if self.plotting_state["raw"]:
            self.plot_function(self.current_data, "Raw", 'blue')
        if self.plotting_state["filtered"]:
            self.plot_function(self.filtered_data, "Filtered", 'green')
        if self.plotting_state["tangent"]:
            self.plot_function(np.tan, "Tangent Wave", 'red', limit_y=True)

    def clear_canvas(self):
        self.canvas.delete("all")  # Clear the canvas
        self.axes_drawn = False  # Reset axes drawn state
        self.update_value_display()  # Clear values

    def update_value_display(self):
        # Update the text boxes with current plot status
        self.raw_value.delete(0, tk.END)
        self.raw_value.insert(0, "Visible" if self.plotting_state["raw"] else "Hidden")
        
        self.filtered_value.delete(0, tk.END)
        self.filtered_value.insert(0, "Visible" if self.plotting_state["filtered"] else "Hidden")
        
        self.tangent_value.delete(0, tk.END)
        self.tangent_value.insert(0, "Visible" if self.plotting_state["tangent"] else "Hidden")

    def stop_update(self):
        self.is_update = not self.is_update  # Stop updating the plot

    def exit_application(self):
        # self.ser.close()
        # print("Serial exits")
        self.master.quit()  # Close the application

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PlottingGUI(root)
    root.mainloop()