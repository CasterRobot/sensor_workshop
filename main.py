import tkinter as tk
import numpy as np
from serial_reading import *
from data_processing import *
from motor_control import *

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
        self.plot_button1 = tk.Button(self.button_frame, text="Measure", command=self.toggle_measure)
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
        tk.Label(self.control_frame, text="Measure:").pack(anchor=tk.W)
        self.measure_value = tk.Entry(self.control_frame, width=10)
        self.measure_value.pack(pady=5)
        self.measure_value.insert(0, "Hidden")

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
            "measure": False,
            "filtered": False,
            "tangent": False
        }

        self.is_update = False
        self.cutoff = 500.0
        self.fs = 50.0

        self.angle_dis_dict = {}
        for i in range(10):
            self.angle_dis_dict[i] = []
        self.data_id = -1

        self.colors = {
                        0:"red", 
                        1:"blue", 
                        2:"green", 
                        3:"yellow", 
                        4:"orange",
                        5:"purple", 
                        6:"cyan", 
                        7:"magenta", 
                        8:"lime", 
                        9:"pink"
        }

        # self.open_serial()

    def open_serial(self):
        # Initialize serial connection
        # sys.stdout.reconfigure(encoding='utf-8') 
        # port = '/dev/ttyUSB0'  # or '/dev/ttyACM0'
        # baud_rate = 921600
        # self.ser = serial.Serial(port, baud_rate, timeout=0.5)
        # if self.ser.isOpen():
        #     print("open success")
        # else:
        #     print("open failed")

        self.motor_ins = motor(port = '/dev/ttyUSB0', baud_rate = 115200)
        self.laser_ins = laser(port = '/dev/ttyUSB1', baud_rate = 9600)

    def close_serial(self):
        self.motor_ins.disconnect()
        self.laser_ins.disconnect()

    def outlier_remove(self, ind, data):
        # Calculate Q1 (25th percentile) and Q3 (75th percentile)
        Q1 = np.percentile(data, 25)
        Q3 = np.percentile(data, 75)
        IQR = Q3 - Q1

        # Define bounds for outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filter the data
        filtered_data = data[(data >= lower_bound) & (data <= upper_bound)]
        filtered_ind = ind[(data >= lower_bound) & (data <= upper_bound)]

        return filtered_ind, filtered_data


    def measure_once(self):
        angle_list = []
        dis_list = []
        inds = []
        for i in range(0, 359, 60):
            self.motor_ins.move_to(i)
            inds.append(i)
            dis = self.laser_ins.get_distance()
            if dis is None:
                continue

            angle_list.append(i)
            dis_list.append(dis)
            

        for i in reversed(inds):
            self.motor_ins.move_to(i)
            inds.append(i)
            dis = self.laser_ins.get_distance()
            if dis is None:
                continue

            angle_list.append(i)
            dis_list.append(dis)
        angle_list, dis_list = self.outlier_remove(np.array(angle_list), np.array(dis_list))

        angle_dis = []
        for a, d in zip(angle_list, dis_list):
            rad = np.deg2rad(a)
            x = d * np.cos(rad)
            y = d * np.sin(rad)
            angle_dis.append([a, d, x, y])
        self.angle_dis_dict[self.data_id] = angle_dis

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

    def toggle_measure(self):
        self.data_id += 1
        self.is_update = True
        self.plotting_state["measure"] = True #not self.plotting_state["measure"]
        self.measure_once()
        
        self.toggle_plot(self.angle_dis_dict[self.data_id], "measure", self.colors[self.data_id], self.plotting_state["measure"])
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
        # self.clear_canvas()
        
        if self.plotting_state["measure"]:
            self.plot_function(self.angle_dis_dict[self.data_id], "Measure", self.colors[self.data_id], limit_y)
        
        if self.plotting_state["filtered"]:
            self.filtered_data = lowpass_filter(self.current_data, cutoff=self.cutoff, fs=self.fs, order=6)
            self.plot_function(self.filtered_data, "Filtered", 'green', limit_y)
        
        if self.plotting_state["tangent"]:
            self.plot_function(np.tan, "Tangent Wave", 'red', limit_y)

        if self.is_update:
            if self.plotting_state["measure"] or self.plotting_state["filtered"] or self.plotting_state["tangent"]:
                self.update_value_display()
                self.master.after(1000, self.update_plot)  # Update every 100 ms

    def draw_y_axis_labels(self, margin, height, padding, y_min, y_max):
        # Draw y-axis labels based on defined y_min and y_max
        y_ticks = 5  # Number of ticks
        for i in range(y_ticks + 1):
            y_value = y_min + i * (y_max - y_min) / y_ticks
            y_pos = height - (y_value - y_min) / (y_max - y_min) * (height - 2 * margin) - margin
            self.canvas.create_text(margin - 3, y_pos, text=f"{y_value:.2f}", anchor='e', font=("Arial", 10))

    def draw_x_axis_labels(self, margin, width, padding, x_min, x_max):
        # Draw y-axis labels based on defined y_min and y_max
        x_ticks = 5  # Number of ticks
        for i in range(x_ticks + 1):
            x_value = x_min + i * (x_max - x_min) / x_ticks
            x_pos = width - (x_value - x_min) / (x_max - x_min) * (width - 2 * margin) - margin
            self.canvas.create_text(margin - 3, x_pos, text=f"{x_value:.2f}", anchor='e', font=("Arial", 10))

    def plot_function(self, data, title, color, limit_y=False):
        data = np.array(data)

        width = 400
        height = 400
        center_x = width // 2
        center_y = height // 2

        margin = 0

        # Draw axes
        self.canvas.create_line(0, center_y, width, center_y, fill='black', width=2)  # x-axis
        self.canvas.create_line(center_x, 0, center_x, height, fill='black', width=2)  # y-axis

        # Draw lines in negative x and y
        self.canvas.create_line(center_x, center_y, 0, center_y, fill='black', dash=(4, 2))  # Negative x
        self.canvas.create_line(center_x, center_y, center_x, 0, fill='black', dash=(4, 2))  # Negative y

        # # Draw diagonal lines
        # self.canvas.create_line(center_x, center_y, width, height, fill='green')  # Positive diagonal
        # self.canvas.create_line(center_x, center_y, 0, 0, fill='purple')  # Negative diagonal

        # Plotting the function
        print("the data are: ", data)
        NUM = data.shape[0]
        x_values = data[:, 2]
        y_values = data[:, 3]

        print(x_values, y_values)

        x_max = np.max(x_values)*1.2
        x_min = np.min(x_values)*1.2

        y_max = np.max(y_values)*1.2
        y_min = np.min(y_values)*1.2

        print(y_min,y_max )

        

        # if not hasattr(self, 'axes_drawn'):
        # self.canvas.create_line(-1 * width + margin, -1 * height + margin, width - margin, height - margin, fill='black')  # X-axis
        # # self.canvas.create_line(margin, margin, margin, height - margin, fill='black')  # Y-axis
        # self.draw_y_axis_labels(margin, height, margin, y_min=y_min, y_max=y_max)
        # #self.draw_x_axis_labels(margin, width, margin, x_min=y_min, x_max=x_max)
        self.axes_drawn = True

        # Draw points using raw x and y values
        point_radius = 3  # Radius for the points
        # draw points 
        for i in range(len(x_values)):
            # x = int((x_values[i]) * (width - 2 * margin) / NUM + margin)
            scaled_x = (x_values[i] - x_min) / (x_max - x_min) * (width - 2 * margin)
            scaled_y = (y_values[i] - y_min) / (y_max - y_min) * (height - 2 * margin)
            # y = int(height - scaled_y - margin)
            # self.canvas.create_oval(x - point_radius, y - point_radius, x + point_radius, y + point_radius, fill=color)
            canvas_x = scaled_x
            canvas_y = scaled_y  # Invert y-axis for canvas
            self.canvas.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill=color)

        # draw lines
        # for i in range(1, len(x_values) - 1):
        #     x1 = int((x_values[i]) * (width - 2 * margin) / NUM + margin)
        #     scaled_y = (y_values[i] - y_min) / (y_max - y_min) * (height - 2 * margin)
        #     y1 = int(height - scaled_y - margin)

        #     x2 = int((x_values[i+1]) * (width - 2 * margin) / NUM + margin)
        #     scaled_y = (y_values[i+1] - y_min) / (y_max - y_min) * (height - 2 * margin)
        #     y2 = int(height - scaled_y - margin)
        #     self.canvas.create(x1, y1, x2, y2, fill=color)




        

        # # Draw points
        # points = [
        #     (50, 50),    # Positive x, Positive y
        #     (-50, 50),   # Negative x, Positive y
        #     (50, -50),   # Positive x, Negative y
        #     (-50, -50),  # Negative x, Negative y
        #     (100, 0),    # Positive x-axis
        #     (0, 100),    # Positive y-axis
        #     (-100, 0),   # Negative x-axis
        #     (0, -100)    # Negative y-axis
        # ]

        # for x, y in points:
        #     # Translate coordinates to canvas
        #     canvas_x = center_x + x
        #     canvas_y = center_y - y  # Invert y-axis for canvas
        #     self.canvas.create_oval(canvas_x - 3, canvas_y - 3, canvas_x + 3, canvas_y + 3, fill='black')

    
    def clear_plot(self):
        # Clear specific plot by redrawing the canvas and replotting the others
        self.clear_canvas()
        if self.plotting_state["measure"]:
            self.plot_function(self.current_data, "Measure", self.colors[self.data_id])
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
        self.measure_value.delete(0, tk.END)
        self.measure_value.insert(0, "Visible" if self.plotting_state["measure"] else "Hidden")
        
        self.filtered_value.delete(0, tk.END)
        self.filtered_value.insert(0, "Visible" if self.plotting_state["filtered"] else "Hidden")
        
        self.tangent_value.delete(0, tk.END)
        self.tangent_value.insert(0, "Visible" if self.plotting_state["tangent"] else "Hidden")

    def stop_update(self):
        self.is_update = not self.is_update  # Stop updating the plot
        
        if self.is_update is True:
            self.open_serial()
        else:
            self.close_serial()
            print("Serials closed.")

    def exit_application(self):
        # self.ser.close()
        # print("Serial exits")
        self.master.quit()  # Close the application

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PlottingGUI(root)
    root.mainloop()