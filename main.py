import tkinter as tk
import numpy as np
from serial_reading import *
from data_processing import *
from motor_control import *
import customtkinter as ctk
from tkinter import ttk, messagebox


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

        self.stop_button = tk.Button(self.button_frame, text="Connect", command=self.stop_update)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        self.plot_button1 = tk.Button(self.button_frame, text="Measure", command=self.toggle_measure)
        self.plot_button1.pack(side=tk.LEFT, padx=5)

        # self.plot_button2 = tk.Button(self.button_frame, text="Filtered data", command=self.toggle_filtered)
        # self.plot_button2.pack(side=tk.LEFT, padx=5)

        # self.plot_button3 = tk.Button(self.button_frame, text="Else", command=self.toggle_tangent)
        # self.plot_button3.pack(side=tk.LEFT, padx=5)

        # self.clear_button = tk.Button(self.button_frame, text="Clear All Plots", command=self.clear_canvas)
        # self.clear_button.pack(side=tk.LEFT, padx=5)

        # self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.exit_application)
        # self.exit_button.pack(side=tk.LEFT, padx=5)

        # Frame for text boxes and labels
        

        # # Labels and text boxes for values
        # tk.Label(self.control_frame, text="Diameter:").pack(anchor=tk.W)
        # self.measure_value = tk.Entry(self.control_frame, width=10)
        # self.measure_value.pack(pady=5)
        # self.measure_value.insert(0, "Diameter")

        # tk.Label(self.control_frame, text="Filtered:").pack(anchor=tk.W)
        # self.filtered_value = tk.Entry(self.control_frame, width=10)
        # self.filtered_value.pack(pady=5)
        # self.filtered_value.insert(0, "Hidden")

        # tk.Label(self.control_frame, text="Tangent:").pack(anchor=tk.W)
        # self.tangent_value = tk.Entry(self.control_frame, width=10)
        # self.tangent_value.pack(pady=5)
        # self.tangent_value.insert(0, "Hidden")


        self.control_frame_title = tk.Frame(master)
        self.control_frame_title.pack(side=tk.TOP, padx=5)

        # Labels and text boxes for values
        self.num_points_label = tk.Label(self.control_frame_title, text="  Num of points    |")
        self.num_points_label.pack(side=tk.LEFT, pady=5)
        self.diameter_ave_label = tk.Label(self.control_frame_title, text="|    Diameter Ave (mm) |")
        self.diameter_ave_label.pack(side=tk.LEFT, pady=5)
        self.diameter_max_label = tk.Label(self.control_frame_title, text="| Diameter Max (mm) |")
        self.diameter_max_label.pack(side=tk.LEFT, pady=5)
        self.diameter_min_label = tk.Label(self.control_frame_title, text="|   Diameter Min (mm) |")
        self.diameter_min_label.pack(side=tk.LEFT, pady=5)
        self.display_not_label = tk.Label(self.control_frame_title, text="|    Display/Not")
        self.display_not_label.pack(side=tk.LEFT, pady=5)



        NUM_sampling = ["4", "6", "10", "30", "90", "180", "360"]

        self.selection_var0 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var1 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var2 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var3 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var4 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var5 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var6 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var7 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var8 = tk.StringVar(value=NUM_sampling[0])
        self.selection_var9 = tk.StringVar(value=NUM_sampling[0])

        ## for measurement 0
        self.control_frame_0 = tk.Frame(master)
        self.control_frame_0.pack(side=tk.TOP, padx=5)
        self.selection_menu_0 = ttk.Combobox(
            self.control_frame_0, 
            textvariable=self.selection_var0,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_0.pack(side=tk.LEFT, pady=5)
        self.selection_menu_0.bind("<<ComboboxSelected>>", self.on_selection_change_0)
        # Labels and text boxes for values
        self.measure_value_label_0 = tk.Label(self.control_frame_0, text="      ")
        self.measure_value_label_0.pack(side=tk.LEFT, pady=5)
        self.measure_value_0 = tk.Entry(self.control_frame_0, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_0.pack(side=tk.LEFT, pady=1)
        self.measure_value_0.insert(0, "Diameter Ave")
        self.measure_value_max_0 = tk.Entry(self.control_frame_0, width=20)
        self.measure_value_max_0.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_0.insert(0, "Diameter Max")
        self.measure_value_min_0 = tk.Entry(self.control_frame_0, width=20)
        self.measure_value_min_0.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_0.insert(0, "Diameter Min")
        self.data_0_switch = ctk.CTkSwitch(self.control_frame_0, text="Display 0", command=self.data_0_on_off)
        self.data_0_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 1
        self.control_frame_1 = tk.Frame(master)
        self.control_frame_1.pack(side=tk.TOP, padx=5)
        self.selection_menu_1 = ttk.Combobox(
            self.control_frame_1, 
            textvariable=self.selection_var1,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_1.pack(side=tk.LEFT, pady=5)
        self.selection_menu_1.bind("<<ComboboxSelected>>", self.on_selection_change_1)
        self.measure_value_label_1 = tk.Label(self.control_frame_1, text="      ")
        self.measure_value_label_1.pack(side=tk.LEFT, pady=5)
        self.measure_value_1 = tk.Entry(self.control_frame_1, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_1.pack(side=tk.LEFT, pady=5)
        self.measure_value_1.insert(0, "Diameter Ave")
        self.measure_value_max_1 = tk.Entry(self.control_frame_1, width=20)
        self.measure_value_max_1.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_1.insert(0, "Diameter Max")
        self.measure_value_min_1 = tk.Entry(self.control_frame_1, width=20)
        self.measure_value_min_1.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_1.insert(0, "Diameter Min")
        self.data_1_switch = ctk.CTkSwitch(self.control_frame_1, text="Display 1", command=self.data_1_on_off)
        self.data_1_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 2
        self.control_frame_2 = tk.Frame(master)
        self.control_frame_2.pack(side=tk.TOP, padx=5)
        self.selection_menu_2 = ttk.Combobox(
            self.control_frame_2, 
            textvariable=self.selection_var2,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_2.pack(side=tk.LEFT, pady=5)
        self.selection_menu_2.bind("<<ComboboxSelected>>", self.on_selection_change_2)
        self.measure_value_label_2 = tk.Label(self.control_frame_2, text="      ")
        self.measure_value_label_2.pack(side=tk.LEFT, pady=5)
        self.measure_value_2 = tk.Entry(self.control_frame_2, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_2.pack(side=tk.LEFT, pady=5)
        self.measure_value_2.insert(0, "Diameter Ave")
        self.measure_value_max_2 = tk.Entry(self.control_frame_2, width=20)
        self.measure_value_max_2.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_2.insert(0, "Diameter Max")
        self.measure_value_min_2 = tk.Entry(self.control_frame_2, width=20)
        self.measure_value_min_2.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_2.insert(0, "Diameter Min")
        self.data_2_switch = ctk.CTkSwitch(self.control_frame_2, text="Display 2", command=self.data_2_on_off)
        self.data_2_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 3
        self.control_frame_3 = tk.Frame(master)
        self.control_frame_3.pack(side=tk.TOP, padx=5)
        self.selection_menu_3 = ttk.Combobox(
            self.control_frame_3, 
            textvariable=self.selection_var3,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_3.pack(side=tk.LEFT, pady=5)
        self.selection_menu_3.bind("<<ComboboxSelected>>", self.on_selection_change_3)
        self.measure_value_label_3 = tk.Label(self.control_frame_3, text="      ")
        self.measure_value_label_3.pack(side=tk.LEFT, pady=5)
        self.measure_value_3 = tk.Entry(self.control_frame_3, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_3.pack(side=tk.LEFT, pady=5)
        self.measure_value_3.insert(0, "Diameter Ave")
        self.measure_value_max_3 = tk.Entry(self.control_frame_3, width=20)
        self.measure_value_max_3.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_3.insert(0, "Diameter Max")
        self.measure_value_min_3 = tk.Entry(self.control_frame_3, width=20)
        self.measure_value_min_3.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_3.insert(0, "Diameter Min")
        self.data_3_switch = ctk.CTkSwitch(self.control_frame_3, text="Display 3", command=self.data_3_on_off)
        self.data_3_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 4
        self.control_frame_4 = tk.Frame(master)
        self.control_frame_4.pack(side=tk.TOP, padx=5)
        self.selection_menu_4 = ttk.Combobox(
            self.control_frame_4, 
            textvariable=self.selection_var4,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_4.pack(side=tk.LEFT, pady=5)
        self.selection_menu_4.bind("<<ComboboxSelected>>", self.on_selection_change_4)
        self.measure_value_label_4 = tk.Label(self.control_frame_4, text="      ")
        self.measure_value_label_4.pack(side=tk.LEFT, pady=5)
        self.measure_value_4 = tk.Entry(self.control_frame_4, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_4.pack(side=tk.LEFT, pady=5)
        self.measure_value_4.insert(0, "Diameter Ave")
        self.measure_value_max_4 = tk.Entry(self.control_frame_4, width=20)
        self.measure_value_max_4.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_4.insert(0, "Diameter Max")
        self.measure_value_min_4 = tk.Entry(self.control_frame_4, width=20)
        self.measure_value_min_4.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_4.insert(0, "Diameter Min")
        self.data_4_switch = ctk.CTkSwitch(self.control_frame_4, text="Display 4", command=self.data_4_on_off)
        self.data_4_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 5
        self.control_frame_5 = tk.Frame(master)
        self.control_frame_5.pack(side=tk.TOP, padx=5)
        self.selection_menu_5 = ttk.Combobox(
            self.control_frame_5, 
            textvariable=self.selection_var5,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_5.pack(side=tk.LEFT, pady=5)
        self.selection_menu_5.bind("<<ComboboxSelected>>", self.on_selection_change_5)
        self.measure_value_label_5 = tk.Label(self.control_frame_5, text="      ")
        self.measure_value_label_5.pack(side=tk.LEFT, pady=5)
        self.measure_value_5 = tk.Entry(self.control_frame_5, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_5.pack(side=tk.LEFT, pady=5)
        self.measure_value_5.insert(0, "Diameter Ave")
        self.measure_value_max_5 = tk.Entry(self.control_frame_5, width=20)
        self.measure_value_max_5.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_5.insert(0, "Diameter Max")
        self.measure_value_min_5 = tk.Entry(self.control_frame_5, width=20)
        self.measure_value_min_5.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_5.insert(0, "Diameter Min")
        self.data_5_switch = ctk.CTkSwitch(self.control_frame_5, text="Display 5", command=self.data_5_on_off)
        self.data_5_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 6
        self.control_frame_6 = tk.Frame(master)
        self.control_frame_6.pack(side=tk.TOP, padx=5)
        self.selection_menu_6 = ttk.Combobox(
            self.control_frame_6, 
            textvariable=self.selection_var6,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_6.pack(side=tk.LEFT, pady=5)
        self.selection_menu_6.bind("<<ComboboxSelected>>", self.on_selection_change_6)
        self.measure_value_label_6 = tk.Label(self.control_frame_6, text="      ")
        self.measure_value_label_6.pack(side=tk.LEFT, pady=5)
        self.measure_value_6 = tk.Entry(self.control_frame_6, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_6.pack(side=tk.LEFT, pady=5)
        self.measure_value_6.insert(0, "Diameter Ave")
        self.measure_value_max_6 = tk.Entry(self.control_frame_6, width=20)
        self.measure_value_max_6.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_6.insert(0, "Diameter Max")
        self.measure_value_min_6 = tk.Entry(self.control_frame_6, width=20)
        self.measure_value_min_6.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_6.insert(0, "Diameter Min")
        self.data_6_switch = ctk.CTkSwitch(self.control_frame_6, text="Display 6", command=self.data_6_on_off)
        self.data_6_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 7
        self.control_frame_7 = tk.Frame(master)
        self.control_frame_7.pack(side=tk.TOP, padx=5)
        self.selection_menu_7 = ttk.Combobox(
            self.control_frame_7, 
            textvariable=self.selection_var7,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_7.pack(side=tk.LEFT, pady=5)
        self.selection_menu_7.bind("<<ComboboxSelected>>", self.on_selection_change_7)
        self.measure_value_label_7 = tk.Label(self.control_frame_7, text="      ")
        self.measure_value_label_7.pack(side=tk.LEFT, pady=5)
        self.measure_value_7 = tk.Entry(self.control_frame_7, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_7.pack(side=tk.LEFT, pady=5)
        self.measure_value_7.insert(0, "Diameter Ave")
        self.measure_value_max_7 = tk.Entry(self.control_frame_7, width=20)
        self.measure_value_max_7.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_7.insert(0, "Diameter Max")
        self.measure_value_min_7 = tk.Entry(self.control_frame_7, width=20)
        self.measure_value_min_7.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_7.insert(0, "Diameter Min")
        self.data_7_switch = ctk.CTkSwitch(self.control_frame_7, text="Display 7", command=self.data_7_on_off)
        self.data_7_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 8
        self.control_frame_8 = tk.Frame(master)
        self.control_frame_8.pack(side=tk.TOP, padx=5)
        self.selection_menu_8 = ttk.Combobox(
            self.control_frame_8, 
            textvariable=self.selection_var8,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_8.pack(side=tk.LEFT, pady=5)
        self.selection_menu_8.bind("<<ComboboxSelected>>", self.on_selection_change_8)
        self.measure_value_label_8 = tk.Label(self.control_frame_8, text="      ")
        self.measure_value_label_8.pack(side=tk.LEFT, pady=5)
        self.measure_value_8 = tk.Entry(self.control_frame_8, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_8.pack(side=tk.LEFT, pady=5)
        self.measure_value_8.insert(0, "Diameter Ave")
        self.measure_value_max_8 = tk.Entry(self.control_frame_8, width=20)
        self.measure_value_max_8.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_8.insert(0, "Diameter Max")
        self.measure_value_min_8 = tk.Entry(self.control_frame_8, width=20)
        self.measure_value_min_8.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_8.insert(0, "Diameter Min")
        self.data_8_switch = ctk.CTkSwitch(self.control_frame_8, text="Display 8", command=self.data_8_on_off)
        self.data_8_switch.pack(side=tk.LEFT, pady=5)

        ## for measurement 9
        self.control_frame_9 = tk.Frame(master)
        self.control_frame_9.pack(side=tk.TOP, padx=5)
        self.selection_menu_9 = ttk.Combobox(
            self.control_frame_9, 
            textvariable=self.selection_var9,
            values=NUM_sampling,
            state="readonly",  # Prevent typing
            width=12
        )
        self.selection_menu_9.pack(side=tk.LEFT, pady=5)
        self.selection_menu_9.bind("<<ComboboxSelected>>", self.on_selection_change_9)
        self.measure_value_label_9 = tk.Label(self.control_frame_9, text="      ")
        self.measure_value_label_9.pack(side=tk.LEFT, pady=5)
        self.measure_value_9 = tk.Entry(self.control_frame_9, width=20)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_9.pack(side=tk.LEFT, pady=5)
        self.measure_value_9.insert(0, "Diameter Ave")
        self.measure_value_max_9 = tk.Entry(self.control_frame_9, width=20)
        self.measure_value_max_9.pack(side=tk.LEFT, pady=1)
        self.measure_value_max_9.insert(0, "Diameter Max")
        self.measure_value_min_9 = tk.Entry(self.control_frame_9, width=20)
        self.measure_value_min_9.pack(side=tk.LEFT, pady=1)
        self.measure_value_min_9.insert(0, "Diameter Min")
        self.data_9_switch = ctk.CTkSwitch(self.control_frame_9, text="Display 9", command=self.data_9_on_off)
        self.data_9_switch.pack(side=tk.LEFT, pady=5)


        self.control_frame_ave = tk.Frame(master)
        self.control_frame_ave.pack(side=tk.TOP, padx=5)
        self.measure_value_label_ave = tk.Label(self.control_frame_ave, text="Average:  ")
        self.measure_value_label_ave.pack(side=tk.LEFT, pady=5)
        self.measure_value_ave = tk.Entry(self.control_frame_ave, width=10)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_ave.pack(side=tk.LEFT, pady=5)
        self.measure_value_ave.insert(0, "Diameter")

        self.measure_value_label_max = tk.Label(self.control_frame_ave, text="  Max:  ")
        self.measure_value_label_max.pack(side=tk.LEFT, pady=5)
        self.measure_value_max = tk.Entry(self.control_frame_ave, width=10)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_max.pack(side=tk.LEFT, pady=5)
        self.measure_value_max.insert(0, "Diameter")

        self.measure_value_label_min = tk.Label(self.control_frame_ave, text="  Min:  ")
        self.measure_value_label_min.pack(side=tk.LEFT, pady=5)
        self.measure_value_min = tk.Entry(self.control_frame_ave, width=10)
        # self.measure_value.place(relx=0.95, rely=0.95)
        self.measure_value_min.pack(side=tk.LEFT, pady=5)
        self.measure_value_min.insert(0, "Diameter")


        # # Frame for sliders
        # self.slider_frame = tk.Frame(master)
        # self.slider_frame.pack(side=tk.RIGHT, padx=10)

        # # Cutoff frequency slider
        # self.cutoff_label = tk.Label(self.slider_frame, text="Cutoff Frequency:")
        # self.cutoff_label.pack(anchor=tk.W)

        # self.cutoff_slider = tk.Scale(self.slider_frame, from_=1e-5, to=5, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_cutoff)
        # self.cutoff_slider.pack(fill=tk.X)

        # # Sampling frequency slider
        # self.fs_label = tk.Label(self.slider_frame, text="Sampling Frequency (fs):")
        # self.fs_label.pack(anchor=tk.W)

        # self.fs_slider = tk.Scale(self.slider_frame, from_=1e-5, to=10, orient=tk.HORIZONTAL, resolution=0.01, command=self.update_fs)
        # self.fs_slider.pack(fill=tk.X)

        # # Labels for current values
        # self.current_cutoff = tk.Label(self.slider_frame, text="Current Cutoff: 0")
        # self.current_cutoff.pack(anchor=tk.W)

        # self.current_fs = tk.Label(self.slider_frame, text="Current fs: 1")
        # self.current_fs.pack(anchor=tk.W)

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

        self.data_plot = {
                        0:False, 
                        1:False, 
                        2:False, 
                        3:False, 
                        4:False,
                        5:False, 
                        6:False, 
                        7:False, 
                        8:False, 
                        9:False
        }

        self.measure_points = {
                        0: 4, 
                        1: 4, 
                        2: 4, 
                        3: 4, 
                        4: 4,
                        5: 4, 
                        6: 4, 
                        7: 4, 
                        8: 4, 
                        9: 4
        }

        self.diameters_ave = {
                        0: 0, 
                        1: 0, 
                        2: 0, 
                        3: 0, 
                        4: 0,
                        5: 0, 
                        6: 0, 
                        7: 0, 
                        8: 0, 
                        9: 0
        }

        self.diameters_max = {
                        0: 0, 
                        1: 0, 
                        2: 0, 
                        3: 0, 
                        4: 0,
                        5: 0, 
                        6: 0, 
                        7: 0, 
                        8: 0, 
                        9: 0
        }

        self.diameters_min = {
                        0: 0, 
                        1: 0, 
                        2: 0, 
                        3: 0, 
                        4: 0,
                        5: 0, 
                        6: 0, 
                        7: 0, 
                        8: 0, 
                        9: 0
        }

        # self.open_serial()

        self.axes_drawn = False

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

        self.motor_ins = motor(port = '/dev/ttyUSB1', baud_rate = 115200)
        self.laser_ins = laser(port = '/dev/ttyUSB0', baud_rate = 38400)

        # self.show_status_window("Serial Connected")

        messagebox.showinfo(title="", message="Serial Connected.")

    def show_status_window(self, task_name):
        """Create and display the system status window"""
        # Create top-level window
        self.status_window = tk.Toplevel(self.master)
        self.status_window.title("System Status")
        self.status_window.geometry("400x200")
        self.status_window.resizable(False, False)
        self.status_window.configure(bg="#f5f5f5")
        
        # Make it modal (prevent interaction with main window)
        # self.status_window.grab_set()
        
        # Header
        # header = tk.Label(
        #     self.status_window,
        #     text="SYSTEM IS RUNNING",
        #     font=("Arial", 14, "bold"),
        #     bg="#2c3e50",
        #     fg="white",
        #     pady=10
        # )
        # header.pack(fill="x")
        
        # Animated icon
        icon_frame = tk.Frame(self.status_window, bg="#f5f5f5", pady=10)
        icon_frame.pack()
        
        # self.icon_label = tk.Label(
        #     icon_frame,
        #     text="▶",  # Play symbol
        #     font=("Arial", 24),
        #     fg="#27ae60",
        #     bg="#f5f5f5"
        # )
        # self.icon_label.pack()
        # self.animate_icon()
        
        # Status message
        self.status_label = tk.Label(
            self.status_window,
            text=f"{task_name}",
            font=("Arial", 11),
            bg="#f5f5f5"
        )
        self.status_label.pack(pady=(50, 10))
        
        
        # Center the status window relative to main window
        # self.center_window(self.status_window)


    # def animate_icon(self):
    #     """Animate the status icon"""
    #     if self.status_window and self.status_window.winfo_exists():
    #         current_text = self.icon_label.cget("text")
    #         if current_text == "▶":
    #             self.icon_label.config(text="▷")
    #         else:
    #             self.icon_label.config(text="▶")
            
    #         # Schedule next animation
    #         self.master.after(500, self.animate_icon)
    
    # def center_window(self, window):
    #     """Center a window relative to the main window"""
    #     self.master.update_idletasks()
    #     main_x = self.master.winfo_x()
    #     main_y = self.master.winfo_y()
    #     main_width = self.master.winfo_width()
    #     main_height = self.master.winfo_height()
        
    #     window.update_idletasks()
    #     width = window.winfo_width()
    #     height = window.winfo_height()
        
    #     x = main_x + (main_width // 2) - (width // 2)
    #     y = main_y + (main_height // 2) - (height // 2)
        
    #     window.geometry(f"+{x}+{y}")


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


    def measure_once(self, num_points):
        angle_list = []
        dis_list = []
        inds = []
        internal = 360 // num_points
        full_diameters = []
        for i in range(0, 361, internal):
            print("move to: ", i)
            self.motor_ins.move_to(i)
            inds.append(360-i)
            dis = self.laser_ins.get_distance()
            if dis is None:
                continue

            angle_list.append(360-i)
            dis_list.append(dis)
            

        for ind, a in enumerate(angle_list):
            print("move to: ", a)
            self.motor_ins.move_to(a)
            dis = self.laser_ins.get_distance()
            if dis is None:
                continue

            # angle_list.append(a)
            # dis_list.append(dis)

            full_diameters.append(dis_list[ind]+dis)

        #angle_list, dis_list = self.outlier_remove(np.array(angle_list), np.array(dis_list))

        self.diameters_ave[self.data_id] = np.average(full_diameters)
        self.diameters_max[self.data_id] = np.max(full_diameters)
        self.diameters_min[self.data_id] = np.min(full_diameters)

        angle_dis = []
        for a, d in zip(angle_list, dis_list):
            rad = np.deg2rad(a)
            x = d * np.cos(rad)
            y = d * np.sin(rad)
            angle_dis.append([a, d, x, y])
        self.angle_dis_dict[self.data_id] = angle_dis

    # def update_cutoff(self, value):
    #     self.current_cutoff.config(text=f"Current Cutoff: {value}")
    #     self.cutoff = float(value)
    #     self.filtered_data = lowpass_filter(self.current_data, cutoff=self.cutoff, fs=self.fs, order=6)
    #     self.clear_plot()

    # def update_fs(self, value):
    #     self.current_fs.config(text=f"Current fs: {value}")
    #     self.fs = float(value)
    #     self.filtered_data = lowpass_filter(self.current_data, cutoff=self.cutoff, fs=self.fs, order=6)
    #     self.clear_plot()

    def toggle_measure(self):
        messagebox.showinfo(title="", message="Cclik 'OK' to start measurement, \n and WAIT ......")
        self.data_id += 1
        self.is_update = True
        self.plotting_state["measure"] = True #not self.plotting_state["measure"]
        self.data_plot[self.data_id] = True
        
        self.measure_once(self.measure_points[self.data_id])
        
        self.toggle_plot(self.angle_dis_dict[self.data_id], "measure", self.colors[self.data_id], self.plotting_state["measure"])
        self.update_plot()
        self.update_value_display()
        messagebox.showinfo(title="", message="Finished.")

    def toggle_plot(self, func, title, color, show, limit_y=False):
        if show:
            self.plot_function(func, title, color, limit_y)
            self.update_value_display()
        else:
            self.clear_plot()
    
    def update_plot(self, limit_y=False):
        self.clear_canvas()
        
        if self.plotting_state["measure"]:
            for d_i in range(10):
                if self.data_plot[d_i]:
                    self.plot_function(self.angle_dis_dict[d_i], "Measure", self.colors[d_i], limit_y)

        if self.is_update:
            if self.plotting_state["measure"] or self.plotting_state["filtered"] or self.plotting_state["tangent"]:
                self.update_value_display()
                self.master.after(1000, self.update_plot)  # Update every 100 ms

    def draw_y_axis_labels(self, center_x, center_y, margin, height, y_min, y_max):
        # Draw y-axis labels based on defined y_min and y_max
        y_ticks = 5  # Number of ticks
        for i in range(y_ticks + 1):
            y_value = y_min + i * (y_max - y_min) / y_ticks
            y_pos = margin + (y_value - y_min) / (y_max - y_min) * (height - 2 * margin) - margin
            self.canvas.create_text(center_x, y_pos, text=f"{y_value:.2f}", anchor='e', font=("Arial", 10))

    def draw_x_axis_labels(self, center_x, center_y, margin, width, x_min, x_max):
        # Draw y-axis labels based on defined y_min and y_max
        x_ticks = 5  # Number of ticks
        for i in range(x_ticks + 1):
            x_value = x_min + i * (x_max - x_min) / x_ticks
            x_pos = margin + (x_value - x_min) / (x_max - x_min) * (width - 2 * margin) - margin
            self.canvas.create_text(x_pos, center_y, text=f"{x_value:.2f}", anchor='e', font=("Arial", 10))

    def plot_function(self, data, title, color, axis=False):
        data = np.array(data)
        width = 400
        height = 400
        center_x = width // 2
        center_y = height // 2

        margin = 20


        # Plotting the function
        print("the data are: ", data)
        NUM = data.shape[0]
        x_values = data[:, 2]
        y_values = data[:, 3]

        print(x_values, y_values)

        x_max = np.max(x_values)*2
        x_min = np.min(x_values)*2

        y_max = np.max(y_values)*2
        y_min = np.min(y_values)*2

        print(y_min,y_max )

        
        if not hasattr(self, 'axes_drawn'):
            
            # Draw axes
            self.canvas.create_line(0, center_y, width, center_y, fill='black', width=2)  # x-axis
            self.canvas.create_line(center_x, 0, center_x, height, fill='black', width=2)  # y-axis

            # Draw lines in negative x and y
            self.canvas.create_line(center_x, center_y, 0, center_y, fill='black', dash=(4, 2))  # Negative x
            self.canvas.create_line(center_x, center_y, center_x, 0, fill='black', dash=(4, 2))  # Negative y

            # # Draw diagonal lines
            # self.canvas.create_line(center_x, center_y, width, height, fill='green')  # Positive diagonal
            # self.canvas.create_line(center_x, center_y, 0, 0, fill='purple')  # Negative diagonal
            # self.canvas.create_line(-1 * width + margin, -1 * height + margin, width - margin, height - margin, fill='black')  # X-axis
            # # self.canvas.create_line(margin, margin, margin, height - margin, fill='black')  # Y-axis
            self.draw_y_axis_labels(center_x, center_y, margin=margin, height=height, y_min=y_min, y_max=y_max)
            self.draw_x_axis_labels(center_x, center_y, margin=margin, width=width, x_min=x_min, x_max=x_max)
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

    def data_0_on_off(self):
        if self.data_0_switch.get():
            self.data_plot[0] =True
        else:
            self.data_plot[0] =False
        self.update_plot()
        self.update_value_display()

    def data_1_on_off(self):
        if self.data_1_switch.get():
            self.data_plot[1] =True
        else:
            self.data_plot[1] =False
        self.update_plot()
        self.update_value_display()

    def data_2_on_off(self):
        if self.data_2_switch.get():
            self.data_plot[2] =True
        else:
            self.data_plot[2] =False
        self.update_plot()
        self.update_value_display()

    def data_3_on_off(self):
        if self.data_3_switch.get():
            self.data_plot[3] =True
        else:
            self.data_plot[3] =False
        self.update_plot()
        self.update_value_display()

    def data_4_on_off(self):
        if self.data_4_switch.get():
            self.data_plot[4] =True
        else:
            self.data_plot[4] =False
        self.update_plot()
        self.update_value_display()

    def data_5_on_off(self):
        if self.data_5_switch.get():
            self.data_plot[5] =True
        else:
            self.data_plot[5] =False
        self.update_plot()
        self.update_value_display()

    def data_6_on_off(self):
        if self.data_6_switch.get():
            self.data_plot[6] =True
        else:
            self.data_plot[6] =False
        self.update_plot()
        self.update_value_display()

    def data_7_on_off(self):
        if self.data_7_switch.get():
            self.data_plot[7] =True
        else:
            self.data_plot[7] =False
        self.update_plot()
        self.update_value_display()

    def data_8_on_off(self):
        if self.data_8_switch.get():
            self.data_plot[8] =True
        else:
            self.data_plot[8] =False
        self.update_plot()
        self.update_value_display()

    def data_9_on_off(self):
        if self.data_9_switch.get():
            self.data_plot[9] =True
        else:
            self.data_plot[9] =False
        self.update_plot()
        self.update_value_display()

    def clear_plot(self):
        # Clear specific plot by redrawing the canvas and replotting the others
        self.clear_canvas()
        if self.plotting_state["measure"]:
            self.plot_function(self.current_data, "Measure", self.colors[self.data_id])
        # if self.plotting_state["filtered"]:
        #     self.plot_function(self.filtered_data, "Filtered", 'green')
        # if self.plotting_state["tangent"]:
        #     self.plot_function(np.tan, "Tangent Wave", 'red', limit_y=True)

    def clear_canvas(self):
        self.canvas.delete("all")  # Clear the canvas
        self.axes_drawn = False  # Reset axes drawn state
        self.update_value_display()  # Clear values

    def update_value_display(self):
        # Update the text boxes with current plot status
        self.measure_value_0.delete(0, tk.END)
        # self.measure_value.insert(0, "Visible" if self.plotting_state["measure"] else "Hidden")

        self.measure_value_0.insert(0, self.diameters_ave[0])
        self.measure_value_max_0.delete(0, tk.END)
        self.measure_value_max_0.insert(0, self.diameters_max[0])
        self.measure_value_min_0.delete(0, tk.END)
        self.measure_value_min_0.insert(0, self.diameters_min[0])

        self.measure_value_1.delete(0, tk.END)
        self.measure_value_1.insert(0, self.diameters_ave[1])
        self.measure_value_max_1.delete(0, tk.END)
        self.measure_value_max_1.insert(0, self.diameters_max[1])
        self.measure_value_min_1.delete(0, tk.END)
        self.measure_value_min_1.insert(0, self.diameters_min[1])

        self.measure_value_2.delete(0, tk.END)
        self.measure_value_2.insert(0, self.diameters_ave[2])
        self.measure_value_max_2.delete(0, tk.END)
        self.measure_value_max_2.insert(0, self.diameters_max[2])
        self.measure_value_min_2.delete(0, tk.END)
        self.measure_value_min_2.insert(0, self.diameters_min[2])

        self.measure_value_3.delete(0, tk.END)
        self.measure_value_3.insert(0, self.diameters_ave[3])
        self.measure_value_max_3.delete(0, tk.END)
        self.measure_value_max_3.insert(0, self.diameters_max[3])
        self.measure_value_min_3.delete(0, tk.END)
        self.measure_value_min_3.insert(0, self.diameters_min[3])

        self.measure_value_4.delete(0, tk.END)
        self.measure_value_4.insert(0, self.diameters_ave[4])
        self.measure_value_max_4.delete(0, tk.END)
        self.measure_value_max_4.insert(0, self.diameters_max[4])
        self.measure_value_min_4.delete(0, tk.END)
        self.measure_value_min_4.insert(0, self.diameters_min[4])

        self.measure_value_5.delete(0, tk.END)
        self.measure_value_5.insert(0, self.diameters_ave[5])
        self.measure_value_max_5.delete(0, tk.END)
        self.measure_value_max_5.insert(0, self.diameters_max[5])
        self.measure_value_min_5.delete(0, tk.END)
        self.measure_value_min_5.insert(0, self.diameters_min[5])

        self.measure_value_6.delete(0, tk.END)
        self.measure_value_6.insert(0, self.diameters_ave[6])
        self.measure_value_max_6.delete(0, tk.END)
        self.measure_value_max_6.insert(0, self.diameters_max[6])
        self.measure_value_min_6.delete(0, tk.END)
        self.measure_value_min_6.insert(0, self.diameters_min[6])

        self.measure_value_7.delete(0, tk.END)
        self.measure_value_7.insert(0, self.diameters_ave[7])
        self.measure_value_max_7.delete(0, tk.END)
        self.measure_value_max_7.insert(0, self.diameters_max[7])
        self.measure_value_min_7.delete(0, tk.END)
        self.measure_value_min_7.insert(0, self.diameters_min[7])

        self.measure_value_8.delete(0, tk.END)
        self.measure_value_8.insert(0, self.diameters_ave[8])
        self.measure_value_max_8.delete(0, tk.END)
        self.measure_value_max_8.insert(0, self.diameters_max[8])
        self.measure_value_min_8.delete(0, tk.END)
        self.measure_value_min_8.insert(0, self.diameters_min[8])

        self.measure_value_9.delete(0, tk.END)
        self.measure_value_9.insert(0, self.diameters_ave[9])
        self.measure_value_max_9.delete(0, tk.END)
        self.measure_value_max_9.insert(0, self.diameters_max[9])
        self.measure_value_min_9.delete(0, tk.END)
        self.measure_value_min_9.insert(0, self.diameters_min[9])

        self.update_ave()

    def update_ave(self):
        ave = 0
        max_v = 0
        min_v = 0
        num = 0
        for k in self.data_plot .keys():
            if self.data_plot[k]:
                ave += self.diameters_ave[k]
                max_v += self.diameters_max[k]
                min_v += self.diameters_min[k]
                num +=1
        if num == 0:
            final_ave = 0
            final_max = 0
            final_min = 0
        else:
            final_ave = ave / num
            final_max = max_v / num
            final_min = min_v / num

        self.measure_value_ave.insert(0, final_ave)
        self.measure_value_max.insert(0, final_max)
        self.measure_value_min.insert(0, final_min)



    def stop_update(self):
        self.is_update = not self.is_update  # Stop updating the plot
        
        if self.is_update is True:
            self.open_serial()
        else:
            self.close_serial()
            print("Serials closed.")

    def exit_application(self):
        self.close_serial()
        print("Serials closed.")
        # self.ser.close()
        # print("Serial exits")
        self.master.quit()  # Close the application


    def on_selection_change_0(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var0.get()

        self.measure_points[0] = int(selected)
        #result_label.config(text=f"Selected: {selected}")
        
        # # Update the label colors based on selection
        # if selected == "Red":
        #     result_label.config(background="#ffcccc")
        #     color_display.config(background="#ff0000", text="")
        # elif selected == "Green":
        #     result_label.config(background="#ccffcc")
        #     color_display.config(background="#00ff00", text="")
        # elif selected == "Blue":
        #     result_label.config(background="#ccccff")
        #     color_display.config(background="#0000ff", text="")
        # else:
        #     result_label.config(background="#ffffff")
        #     color_display.config(background="#f0f0f0", text="Pick a color")

    def on_selection_change_1(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var1.get()

        self.measure_points[1] = int(selected)

    def on_selection_change_2(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var2.get()

        self.measure_points[2] = int(selected)

    def on_selection_change_3(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var3.get()

        self.measure_points[3] = int(selected)

    def on_selection_change_4(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var4.get()

        self.measure_points[4] = int(selected)

    def on_selection_change_5(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var5.get()

        self.measure_points[5] = int(selected)

    def on_selection_change_6(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var6.get()

        self.measure_points[6] = int(selected)

    def on_selection_change_7(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var7.get()

        self.measure_points[7] = int(selected)

    def on_selection_change_8(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var8.get()

        self.measure_points[8] = int(selected)

    def on_selection_change_9(self, event):
        """Update the display when a new option is selected"""
        selected = self.selection_var9.get()

        self.measure_points[9] = int(selected)


# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = PlottingGUI(root)
    root.mainloop()