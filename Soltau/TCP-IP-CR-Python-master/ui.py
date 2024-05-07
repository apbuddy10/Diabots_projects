# -*- coding: utf-8 -*-
from threading import Thread
import time
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkinter.scrolledtext import ScrolledText
from dobot_api import *
import json
from files.alarm_controller import alarm_controller_list
from files.alarm_servo import alarm_servo_list


LABEL_JOINT = [["J1-", "J2-", "J3-", "J4-", "J5-", "J6-"],
               ["J1:", "J2:", "J3:", "J4:", "J5:", "J6:"],
               ["J1+", "J2+", "J3+", "J4+", "J5+", "J6+"]]

LABEL_COORD = [["X-", "Y-", "Z-", "Rx-", "Ry-", "Rz-"],
               ["X:", "Y:", "Z:", "Rx:", "Ry:", "Rz:"],
               ["X+", "Y+", "Z+", "Rx+", "Ry+", "Rz+"]]

LABEL_ROBOT_MODE = {
    1:	"ROBOT_MODE_INIT",
    2:	"ROBOT_MODE_BRAKE_OPEN",
    3:	"",
    4:	"ROBOT_MODE_DISABLED",
    5:	"ROBOT_MODE_ENABLE",
    6:	"ROBOT_MODE_BACKDRIVE",
    7:	"ROBOT_MODE_RUNNING",
    8:	"ROBOT_MODE_RECORDING",
    9:	"ROBOT_MODE_ERROR",
    10:	"ROBOT_MODE_PAUSE",
    11:	"ROBOT_MODE_JOG"
}


class RobotUI(object):
    def __init__(self):
        self.threadStarted = False
        self.safetyThread = Thread(target=self.thread_function)
        self.safetyThread.setDaemon(True)
        0
        self.root = Tk()
        self.root.title("Diabots")
        # fixed window size
        self.root.geometry("900x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # set window icon
        # self.root.iconbitmap("images/robot.ico")

        # global state dict
        self.global_state = {}

        # all button
        self.button_list = []

        # all entry
        self.entry_dict = {}
        # Feed counter 
        self.feed_counter = 0
        # Robot Connect
        self.frame_robot = LabelFrame(self.root, text="Robot Connect",
                                      labelanchor="nw", bg="#FFFFFF", width=870, height=70, border=2)

        self.label_ip = Label(self.frame_robot, text="IP Address:")
        self.label_ip.place(rely=0.2, x=10)
        ip_port = StringVar(self.root, value="192.168.0.65")
        self.entry_ip = Entry(self.frame_robot, width=12, textvariable=ip_port)
        self.entry_ip.place(rely=0.2, x=90)

        self.label_dash = Label(self.frame_robot, text="Dashboard Port:")
        self.label_dash.place(rely=0.2, x=180)
        dash_port = IntVar(self.root, value=29999)
        self.entry_dash = Entry(
            self.frame_robot, width=7, textvariable=dash_port)
        self.entry_dash.place(rely=0.2, x=280)

        self.label_move = Label(self.frame_robot, text="Move Port:")
        self.label_move.place(rely=0.2, x=360)
        move_port = IntVar(self.root, value=30003)
        self.entry_move = Entry(
            self.frame_robot, width=7, textvariable=move_port)
        self.entry_move.place(rely=0.2, x=440)

        self.label_feed = Label(self.frame_robot, text="Feedback Port:")
        self.label_feed.place(rely=0.2, x=520)
        feed_port = IntVar(self.root, value=30004)
        self.entry_feed = Entry(
            self.frame_robot, width=7, textvariable=feed_port)
        self.entry_feed.place(rely=0.2, x=620)

        # Connect/DisConnect
        self.button_connect = self.set_button(master=self.frame_robot,
                                              text="Verbinden", rely=0.2, x=720, command=self.connect_port)
        self.button_connect["width"] = 10
        self.global_state["connect"] = False

        # Dashboard Function
        self.frame_dashboard = LabelFrame(self.root, text="Dashboard Function",
                                          labelanchor="nw", bg="#FFFFFF", pady=10, width=870, height=110, border=2)

        # Enable/Disable
        self.button_enable = self.set_button(master=self.frame_dashboard,
                                             text="Aktivieren", rely=0.05, x=10, command=self.enable)
        self.button_enable["width"] = 7
        self.global_state["enable"] = False

        # Reset Robot / Clear Error
        self.set_button(master=self.frame_dashboard,
                        text="Reset Robot", rely=0.05, x=145, command=self.reset_robot)
        self.set_button(master=self.frame_dashboard,
                        text="Clear Error", rely=0.05, x=290, command=self.clear_error)

        self.set_button(master=self.frame_dashboard,
                        text="Drag Mode", rely=0.05, x=430, command=self.set_drag_mode) # 720
        
        # Speed Ratio
        self.label_speed = Label(self.frame_dashboard, text="Speed Ratio :")
        self.label_speed.place(rely=0.05, x=580)  ## 430

        s_value = StringVar(self.root, value="100")
        self.entry_speed = Entry(self.frame_dashboard,
                                 width=6, textvariable=s_value)
        self.entry_speed.place(rely=0.05, x=670) ## 520
        self.label_cent = Label(self.frame_dashboard, text="%")
        self.label_cent.place(rely=0.05, x=715) ## 550

        self.set_button(master=self.frame_dashboard,
                        text="Confirm", rely=0.05, x=735, command=self.confirm_speed)  #600
        
        # # DO:Digital Outputs
        # self.label_digitial = Label(
        #     self.frame_dashboard, text="Digital Outputs: Index:")
        # self.label_digitial.place(rely=0.45, x=10)

        # i_value = IntVar(self.root, value="1")
        # self.entry_index = Entry(
        #     self.frame_dashboard, width=5, textvariable=i_value)
        # self.entry_index.place(rely=0.45, x=160)

        # self.label_status = Label(self.frame_dashboard, text="Status:")
        # self.label_status.place(rely=0.45, x=220)

        # self.combo_status = ttk.Combobox(self.frame_dashboard, width=5)
        # self.combo_status["value"] = ("On", "Off")
        # self.combo_status.current(0)
        # self.combo_status["state"] = "readonly"
        # self.combo_status.place(rely=0.45, x=275)

        # self.set_button(self.frame_dashboard, "Confirm",
        #                 rely=0.45, x=350, command=self.confirm_do)
        
        # self.compactMaxStatus = IntVar()
        # self.abbottStatus = IntVar()
        # self.sysmexStatus = IntVar()
        # c1 = Checkbutton(master=self.frame_dashboard, text='Compact Max',variable=self.compactMaxStatus, 
        #                  onvalue=1, offvalue=0, command=self.update_machine_status)
        # c1.pack()
        # c1.place(rely=0.05, x=450)
        # c2 = Checkbutton(master=self.frame_dashboard, text='Cobas Pure',variable=self.abbottStatus, 
        #                  onvalue=1, offvalue=0, command=self.update_machine_status)
        # c2.pack()
        # c2.place(rely=0.05, x=600)
        # c3 = Checkbutton(master=self.frame_dashboard, text='Sysmex',variable=self.sysmexStatus, 
        #                  onvalue=1, offvalue=0, command=self.update_machine_status)
        # c3.pack()
        # c3.place(rely=0.05, x=750)

        self.start_button = self.set_button(self.frame_dashboard, "Roboter Starten", rely=0.60, x=10, command=self.start_script)
        
        self.stop_button = self.set_button(self.frame_dashboard, "Roboter Stoppen", rely=0.60, x=200, command=self.stop_script)
        
        self.pause_button = self.set_button(self.frame_dashboard, "Roboter Pausieren", rely=0.60, x=400, command=self.pause_script)
        
        self.resume_button = self.set_button(self.frame_dashboard, "Roboter Fortfahren", rely=0.60, x=600, command=self.resume_script)
        
        # Move Function
        # self.frame_move = LabelFrame(self.root, text="Move Function", labelanchor="nw",
        #                              bg="#FFFFFF", width=870, pady=10, height=100, border=2)

        # self.set_move(text="X:", label_value=10,
        #               default_value="600", entry_value=40, rely=0.1, master=self.frame_move)
        # self.set_move(text="Y:", label_value=110,
        #               default_value="-260", entry_value=140, rely=0.1, master=self.frame_move)
        # self.set_move(text="Z:", label_value=210,
        #               default_value="380", entry_value=240, rely=0.1, master=self.frame_move)
        # self.set_move(text="Rx:", label_value=310,
        #               default_value="170", entry_value=340, rely=0.1, master=self.frame_move)
        # self.set_move(text="Ry:", label_value=410,
        #               default_value="12", entry_value=440, rely=0.1, master=self.frame_move)
        # self.set_move(text="Rz:", label_value=510,
        #               default_value="140", entry_value=540, rely=0.1, master=self.frame_move)

        # self.set_button(master=self.frame_move, text="MovJ",
        #                 rely=0.05, x=610, command=self.movj)
        # self.set_button(master=self.frame_move, text="MovL",
        #                 rely=0.05, x=700, command=self.movl)

        # self.set_move(text="J1:", label_value=10,
        #               default_value="0", entry_value=40, rely=0.5, master=self.frame_move)
        # self.set_move(text="J2:", label_value=110,
        #               default_value="-20", entry_value=140, rely=0.5, master=self.frame_move)
        # self.set_move(text="J3:", label_value=210,
        #               default_value="-80", entry_value=240, rely=0.5, master=self.frame_move)
        # self.set_move(text="J4:", label_value=310,
        #               default_value="30", entry_value=340, rely=0.5, master=self.frame_move)
        # self.set_move(text="J5:", label_value=410,
        #               default_value="90", entry_value=440, rely=0.5, master=self.frame_move)
        # self.set_move(text="J6:", label_value=510,
        #               default_value="120", entry_value=540, rely=0.5, master=self.frame_move)

        # self.set_button(master=self.frame_move,
        #                 text="JointMovJ", rely=0.45, x=610, command=self.joint_movj)

        self.frame_feed_log = Frame(
            self.root, bg="#FFFFFF", width=870, pady=10, height=400, border=2)
        # Feedback
        self.frame_feed = LabelFrame(self.frame_feed_log, text="Feedback", labelanchor="nw",
                                     bg="#FFFFFF", width=550, height=150)

        self.frame_feed.place(relx=0, rely=0, relheight=1)

        # Current Speed Ratio
        self.set_label(self.frame_feed,
                       text="Current Speed Ratio:", rely=0.05, x=10)
        self.label_feed_speed = self.set_label(
            self.frame_feed, "", rely=0.05, x=145)
        self.set_label(self.frame_feed, text="%", rely=0.05, x=175)

        # Robot Mode
        self.set_label(self.frame_feed, text="Robot Mode:", rely=0.1, x=10)
        self.label_robot_mode = self.set_label(
            self.frame_feed, "", rely=0.1, x=95)

        # 点动及获取坐标
        self.label_feed_dict = {}
        self.set_feed(LABEL_JOINT, 9, 52, 74, 117)
        self.set_feed(LABEL_COORD, 165, 209, 231, 272)

        # Digitial I/O
        self.set_label(self.frame_feed, "Digital Inputs:", rely=0.8, x=11)
        self.label_di_input = self.set_label(
            self.frame_feed, "", rely=0.8, x=100)
        self.set_label(self.frame_feed, "Digital Outputs:", rely=0.85, x=10)
        self.label_di_output = self.set_label(
            self.frame_feed, "", rely=0.85, x=100)

        # Error Info
        self.frame_err = LabelFrame(self.frame_feed, text="Error Info", labelanchor="nw",
                                    bg="#FFFFFF", width=180, height=50)
        self.frame_err.place(relx=0.65, rely=0, relheight=0.7)

        self.text_err = ScrolledText(
            self.frame_err, width=170, height=50, relief="flat")
        self.text_err.place(rely=0, relx=0, relheight=0.7, relwidth=1)

        self.set_button(self.frame_feed, "Clear", rely=0.71,
                        x=487, command=self.clear_error_info)

        # Log
        self.frame_log = LabelFrame(self.frame_feed_log, text="Log", labelanchor="nw",
                                    bg="#FFFFFF", width=300, height=150)
        self.frame_log.place(relx=0.65, rely=0, relheight=1)

        self.text_log = ScrolledText(
            self.frame_log, width=270, height=140, relief="flat")
        self.text_log.place(rely=0, relx=0, relheight=1, relwidth=1)

        # initial client
        self.client_dash = None
        self.client_move = None
        self.client_feed = None

        self.alarm_controller_dict = self.convert_dict(alarm_controller_list)
        self.alarm_servo_dict = self.convert_dict(alarm_servo_list)

    def update_machine_status(self):
        if self.client_dash is not None:
            if self.compactMaxStatus.get() == 1:
                self.client_dash.DO(3, 1)
            else:
                self.client_dash.DO(3, 0)
            if self.abbottStatus.get() == 1:
                self.client_dash.DO(4, 1)
            else:
                self.client_dash.DO(4, 0)
            if self.sysmexStatus.get() == 1:
                self.client_dash.DO(5, 1)
            else:
                self.client_dash.DO(5, 0)

    def thread_function(self): 
        self.sensor_1 = 1
        self.sensor_2 = 1
        self.pause = False
        self.pause_2 = False
        self.button_reset_1 = 0
        self.button_reset_2 = 0
        self.light_sensor_cam_1 = 0
        self.global_sensor=1
        while True:
            try:
                time.sleep(0.05)
                # if self.client_dash is not None:
                    # Safety
                self.button_reset_1 = self.read_sensor_avg(3,1,10)
                self.button_reset_2 = self.read_sensor_avg(5,1,10)
                self.process_indicator = self.read_sensor_avg(25,1,10)
                self.sensor_1 = self.read_sensor_avg(4,0,10)
                self.light_sensor_cam_1 = self.read_sensor_avg(1,0,10)
                self.light_sensor_cam_2 = self.read_sensor_avg(2,0,10)
                if self.light_sensor_cam_1 == 0 and  self.light_sensor_cam_2 == 0:
                    self.client_dash.DOExecute(10, 1)
                # print(self.read_sensor_avg(26,1,10))
                # Commented code for safety 
                if self.process_indicator == 1 :
                    if self.sensor_1 == 0:
                        self.global_sensor=0
                    continue
                if self.pause_2 and (self.button_reset_1 == 1 or self.button_reset_2 == 1):
                    self.client_dash.DOExecute(5, 1)
                    self.resume_script()
                    self.client_dash.DOExecute(3, 1)
                    self.client_dash.DOExecute(4, 1)
                    self.client_dash.DOExecute(5, 0)
                    self.pause_2 = False   
                    print("Resumed")             
                if self.sensor_1 == 0 or self.global_sensor == 0 and not self.pause_2:
                    self.pause_script()
                    self.pause_2 = True
                    self.global_sensor=1
                    print("Paused")
                if self.pause_2:
                    self.client_dash.DOExecute(3, 1)
                    self.client_dash.DOExecute(4, 1)
                    time.sleep(0.1)
                    self.client_dash.DOExecute(3, 0)
                    self.client_dash.DOExecute(4, 0)
                    time.sleep(0.1)
                    continue
                # End of Commented code for safety 

                # self.process_indicator_cam1 = self.read_sensor_avg(26,1,10)
                # if self.process_indicator_cam1 == 0 :
                #     continue
                
                if self.light_sensor_cam_1 == 0 and self.light_sensor_cam_2 == 0 and not self.pause:
                    self.pause_script()
                    self.pause = True
                    print("Paused")
                if self.light_sensor_cam_1 == 1 and self.light_sensor_cam_2 == 1 and self.pause:
                    self.resume_script()
                    self.pause = False
                    print("Resumed")
            except Exception as e:
                print("Exception occurred: ", e)
                if self.client_dash is not None:
                    self.client_dash.close()
                    self.client_dash = None
                try:
                    self.client_dash = DobotApiDashboard(self.entry_ip.get(), int(self.entry_dash.get()), self.text_log)
                except Exception as e:
                    print("Exception occurred in reconnecting: ", e)

    def read_sensor_avg(self,inp_DI,input_val,range_avg_val):
        sensor_read_cnt = 0
        range_avg_val = range_avg_val
        reading_val = 0
        input_val_inv = 0
        if input_val:
            input_val_inv = 0
        else:
            input_val_inv = 1
        if self.label_di_input is not None or "":
            for read_cnt in range(range_avg_val):
                reading_val = int(self.client_dash.DI(inp_DI))
                if (reading_val != input_val):
                    break
                else:
                    sensor_read_cnt +=1
            if sensor_read_cnt == range_avg_val and reading_val == input_val:
                return input_val
            else:
                return input_val_inv
        return -1

    def convert_dict(self, alarm_list):
        alarm_dict = {}
        for i in alarm_list:
            alarm_dict[i["id"]] = i
        return alarm_dict

    def read_file(self, path):
        # 读json文件耗时大，选择维护两个变量alarm_controller_list alarm_servo_list
        # self.read_file("files/alarm_controller.json")
        with open(path, "r", encoding="utf8") as fp:
            json_data = json.load(fp)
        return json_data

    def mainloop(self):
        self.root.mainloop()

    def protocol(self):
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def pack(self):
        self.frame_robot.pack()
        self.frame_dashboard.pack()
        # self.frame_move.pack()
        self.frame_feed_log.pack()

    def set_move(self, text, label_value, default_value, entry_value, rely, master):
        self.label = Label(master, text=text)
        self.label.place(rely=rely, x=label_value)
        value = StringVar(self.root, value=default_value)
        self.entry_temp = Entry(master, width=6, textvariable=value)
        self.entry_temp.place(rely=rely, x=entry_value)
        self.entry_dict[text] = self.entry_temp

    def move_jog(self, text):
        if self.global_state["connect"]:
            self.client_move.MoveJog(text)

    def move_stop(self, event):
        if self.global_state["connect"]:
            self.client_move.MoveJog("")

    def set_button(self, master, text, rely, x, **kargs):
        self.button = Button(master, text=text, padx=5,
                             command=kargs["command"])
        self.button.place(rely=rely, x=x)

        if text != "Verbinden":
            self.button["state"] = "disable"
            self.button_list.append(self.button)
        return self.button

    def set_button_bind(self, master, text, rely, x, **kargs):
        self.button = Button(master, text=text, padx=5)
        self.button.bind("<ButtonPress-1>",
                         lambda event: self.move_jog(text=text))
        self.button.bind("<ButtonRelease-1>", self.move_stop)
        self.button.place(rely=rely, x=x)

        if text != "Verbinden":
            self.button["state"] = "disable"
            self.button_list.append(self.button)
        return self.button

    def set_label(self, master, text, rely, x):
        self.label = Label(master, text=text)
        self.label.place(rely=rely, x=x)
        return self.label

    def connect_port(self):
        if self.global_state["connect"]:
            print("DisConnected from Dobot")
            self.client_dash.close()
            self.client_feed.close()
            self.client_move.close()
            self.client_dash = None
            self.client_feed = None
            self.client_move = None

            for i in self.button_list:
                i["state"] = "disable"
            self.button_connect["text"] = "Verbinden"
        else:
            try:
                self.client_dash = DobotApiDashboard(
                    self.entry_ip.get(), int(self.entry_dash.get()), self.text_log)
                self.client_move = DobotApiMove(
                    self.entry_ip.get(), int(self.entry_move.get()), self.text_log)
                self.client_feed = DobotApi(
                    self.entry_ip.get(), int(self.entry_feed.get()), self.text_log)
                print("Connected to Dobot ...")
            except Exception as e:
                messagebox.showerror("Attention!", f"Connection Error:{e}")
                return

            for i in self.button_list:
                i["state"] = "normal"
            self.button_connect["text"] = "Trennen"
        self.global_state["connect"] = not self.global_state["connect"]
        self.set_feed_back()

    def set_feed_back(self):
        if self.global_state["connect"]:
            thread = Thread(target=self.feed_back)
            thread.setDaemon(True)
            thread.start()

    def enable(self):
        if self.global_state["enable"]:
            self.client_dash.DisableRobot()
            self.button_enable["text"] = "Aktivieren"
        else:
            self.client_dash.EnableRobot()
            # if need time sleep
            # time.sleep(0.5)
            self.button_enable["text"] = "Deaktivieren"

        self.global_state["enable"] = not self.global_state["enable"]

    def reset_robot(self):
        self.client_dash.ResetRobot()

    def clear_error(self):
        self.client_dash.ClearError()

    def confirm_speed(self):
        self.client_dash.SpeedFactor(int(self.entry_speed.get()))

    def set_drag_mode(self):
        self.client_dash.SetCollideDrag()

    def start_script(self):
        self.client_dash.StopDrag()
        time.sleep(0.5)
        if not self.threadStarted:
            self.safetyThread.start()
            self.threadStarted = True
        self.client_dash.RunScript("Soltau_Crp_Onsite")
        # self.client_dash.RunScript("Test_")
        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL
        self.pause_button['state'] = tk.NORMAL
        self.resume_button['state'] = tk.DISABLED

    def stop_script(self):
        self.client_dash.StopScript()       
        # self.disable_client_dash_buttons() 
        self.stop_button['state'] = tk.DISABLED
        self.pause_button['state'] = tk.DISABLED
        self.resume_button['state'] = tk.DISABLED
        self.start_button['state'] = tk.NORMAL
        # Destroy the script
        print("Robot Stopped")
        self.root.destroy()


    def pause_script(self):
        self.client_dash.PauseScript()
        self.pause_button['state'] = tk.DISABLED
        self.resume_button['state'] = tk.NORMAL
        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL        

    def resume_script(self):
        self.client_dash.ContinueScript()
        self.resume_button['state'] = tk.DISABLED
        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL
        self.pause_button['state'] = tk.NORMAL

    def movj(self):
        self.client_move.MovJ(float(self.entry_dict["X:"].get()), float(self.entry_dict["Y:"].get()), float(self.entry_dict["Z:"].get()),
                              float(self.entry_dict["Rx:"].get()), float(self.entry_dict["Ry:"].get()), float(self.entry_dict["Rz:"].get()))

    def movl(self):
        self.client_move.MovL(float(self.entry_dict["X:"].get()), float(self.entry_dict["Y:"].get()), float(self.entry_dict["Z:"].get()),
                              float(self.entry_dict["Rx:"].get()), float(self.entry_dict["Ry:"].get()), float(self.entry_dict["Rz:"].get()))

    def joint_movj(self):
        self.client_move.JointMovJ(float(self.entry_dict["J1:"].get()), float(self.entry_dict["J2:"].get()), float(self.entry_dict["J3:"].get()),
                                   float(self.entry_dict["J4:"].get()), float(self.entry_dict["J5:"].get()), float(self.entry_dict["J6:"].get()))

    def confirm_do(self):
        if self.combo_status.get() == "On":
            print("DO On")
            self.client_dash.DO(int(self.entry_index.get()), 1)
        else:
            print("DO Off")
            self.client_dash.DO(int(self.entry_index.get()), 0)

    def set_feed(self, text_list, x1, x2, x3, x4):
        self.set_button_bind(
            self.frame_feed, text_list[0][0], rely=0.2, x=x1, command=lambda: self.move_jog(text_list[0][0]))
        self.set_button_bind(
            self.frame_feed, text_list[0][1], rely=0.3, x=x1, command=lambda: self.move_jog(text_list[0][1]))
        self.set_button_bind(
            self.frame_feed, text_list[0][2], rely=0.4, x=x1, command=lambda: self.move_jog(text_list[0][2]))
        self.set_button_bind(
            self.frame_feed, text_list[0][3], rely=0.5, x=x1, command=lambda: self.move_jog(text_list[0][3]))
        self.set_button_bind(
            self.frame_feed, text_list[0][4], rely=0.6, x=x1, command=lambda: self.move_jog(text_list[0][4]))
        self.set_button_bind(
            self.frame_feed, text_list[0][5], rely=0.7, x=x1, command=lambda: self.move_jog(text_list[0][5]))

        self.set_label(self.frame_feed, text_list[1][0], rely=0.21, x=x2)
        self.set_label(self.frame_feed, text_list[1][1], rely=0.31, x=x2)
        self.set_label(self.frame_feed, text_list[1][2], rely=0.41, x=x2)
        self.set_label(self.frame_feed, text_list[1][3], rely=0.51, x=x2)
        self.set_label(self.frame_feed, text_list[1][4], rely=0.61, x=x2)
        self.set_label(self.frame_feed, text_list[1][5], rely=0.71, x=x2)

        self.label_feed_dict[text_list[1][0]] = self.set_label(
            self.frame_feed, " ", rely=0.21, x=x3)
        self.label_feed_dict[text_list[1][1]] = self.set_label(
            self.frame_feed, " ", rely=0.31, x=x3)
        self.label_feed_dict[text_list[1][2]] = self.set_label(
            self.frame_feed, " ", rely=0.41, x=x3)
        self.label_feed_dict[text_list[1][3]] = self.set_label(
            self.frame_feed, " ", rely=0.51, x=x3)
        self.label_feed_dict[text_list[1][4]] = self.set_label(
            self.frame_feed, " ", rely=0.61, x=x3)
        self.label_feed_dict[text_list[1][5]] = self.set_label(
            self.frame_feed, " ", rely=0.71, x=x3)

        self.set_button_bind(
            self.frame_feed, text_list[2][0], rely=0.2, x=x4, command=lambda: self.move_jog(text_list[2][0]))
        self.set_button_bind(
            self.frame_feed, text_list[2][1], rely=0.3, x=x4, command=lambda: self.move_jog(text_list[2][0]))
        self.set_button_bind(
            self.frame_feed, text_list[2][2], rely=0.4, x=x4, command=lambda: self.move_jog(text_list[2][0]))
        self.set_button_bind(
            self.frame_feed, text_list[2][3], rely=0.5, x=x4, command=lambda: self.move_jog(text_list[2][0]))
        self.set_button_bind(
            self.frame_feed, text_list[2][4], rely=0.6, x=x4, command=lambda: self.move_jog(text_list[2][0]))
        self.set_button_bind(
            self.frame_feed, text_list[2][5], rely=0.7, x=x4, command=lambda: self.move_jog(text_list[2][0]))

    def feed_back(self):
        hasRead = 0
        while True:
            #print("self.global_state(connect)", self.global_state["connect"])
            try :
                if not self.global_state["connect"]:
                    break
                data = bytes()
                while hasRead < 1440:
                    temp = self.client_feed.socket_dobot.recv(1440 - hasRead)
                    if len(temp) > 0:
                        hasRead += len(temp)
                        data += temp
                hasRead = 0

                a = np.frombuffer(data, dtype=MyType)
            except Exception as e:
                print("Exception occurred: ", e)
                if self.client_feed is not None:
                    self.client_feed.close()
                    self.client_feed = None
                try:
                    self.client_feed = DobotApiDashboard(self.entry_ip.get(), int(self.entry_feed.get()), self.text_log)
                except Exception as e:
                    print("Exception occurred in reconnecting: ", e)


            #print("robot_mode:", a["robot_mode"][0])
            # print("test_value:", hex((a['test_value'][0])))
            if hex((a['test_value'][0])) == '0x123456789abcdef':
                self.feed_counter = 0
                # print('tool_vector_actual',
                #       np.around(a['tool_vector_actual'], decimals=4))
                # print('q_actual', np.around(a['q_actual'], decimals=4))

                # Refresh Properties
                self.label_feed_speed["text"] = a["speed_scaling"][0]
                self.label_robot_mode["text"] = LABEL_ROBOT_MODE[a["robot_mode"][0]]
                self.label_di_input["text"] = bin(a["digital_input_bits"][0])[
                    2:].rjust(64, '0')
                self.label_di_output["text"] = bin(a["digital_output_bits"][0])[
                    2:].rjust(64, '0')

                # Refresh coordinate points
                self.set_feed_joint(LABEL_JOINT, a["q_actual"])
                self.set_feed_joint(LABEL_COORD, a["tool_vector_actual"])

                # # check alarms
                # if a["robot_mode"] == 9:
                #     self.display_error_info()
                
            if hex((a['test_value'][0])) != '0x123456789abcdef':
                self.feed_counter = self.feed_counter + 1
                if(self.feed_counter > 10):
                    self.feed_counter = 0
                    try:
                        if self.client_feed is not None:
                            self.client_feed.close()
                            self.client_feed = None
                        # self.client_feed.close()
                        # self.client_feed = None
                        
                        self.client_feed = DobotApi(
                            self.entry_ip.get(), int(self.entry_feed.get()), self.text_log)
                        print("Connected to Client Feed Dobot ...")
                    except Exception as e:
                        print("Exception occurred in reconnecting: ", e)

            #     # Refresh coordinate points
            #     self.set_feed_joint(LABEL_JOINT, a["q_actual"])
            #     self.set_feed_joint(LABEL_COORD, a["tool_vector_actual"])
            # elif hex((a['test_value'][0])) != '0x0':
            #     # print('tool_vector_actual',
            #     #       np.around(a['tool_vector_actual'], decimals=4))
            #     # print('q_actual', np.around(a['q_actual'], decimals=4))

            #     # Refresh Properties
            #     # self.label_feed_speed["text"] = a["speed_scaling"][0]
            #     # self.label_robot_mode["text"] = LABEL_ROBOT_MODE[a["robot_mode"][0]]
            #     self.label_di_input["text"] = bin(a["digital_input_bits"][0])[
            #         2:].rjust(64, '0')
            #     self.label_di_output["text"] = bin(a["digital_output_bits"][0])[
            #         2:].rjust(64, '0')

                # Refresh coordinate points
                # self.set_feed_joint(LABEL_JOINT, a["q_actual"])
                # self.set_feed_joint(LABEL_COORD, a["tool_vector_actual"])
                # # check alarms
                # if a["robot_mode"] == 9:
                #     self.display_error_info()

            time.sleep(0.005)

    def display_error_info(self):
        error_list = self.client_dash.GetErrorID().split("{")[1].split("}")[0]

        error_list = json.loads(error_list)
        print("error_list:", error_list)
        if error_list[0]:
            for i in error_list[0]:
                self.form_error(i, self.alarm_controller_dict,
                                "Controller Error")

        for m in range(1, len(error_list)):
            if error_list[m]:
                for n in range(len(error_list[m])):
                    self.form_error(n, self.alarm_servo_dict, "Servo Error")

    def form_error(self, index, alarm_dict: dict, type_text):
        if index in alarm_dict.keys():
            date = datetime.datetime.now().strftime("%Y.%m.%d:%H:%M:%S ")
            error_info = f"Time Stamp:{date}\n"
            error_info = error_info + f"ID:{index}\n"
            error_info = error_info + \
                f"Type:{type_text}\nLevel:{alarm_dict[index]['level']}\n" + \
                f"Solution:{alarm_dict[index]['en']['solution']}\n"

            self.text_err.insert(END, error_info)

    def clear_error_info(self):
        self.text_err.delete("1.0", "end")

    def set_feed_joint(self, label, value):
        array_value = np.around(value, decimals=4)
        self.label_feed_dict[label[1][0]]["text"] = array_value[0][0]
        self.label_feed_dict[label[1][1]]["text"] = array_value[0][1]
        self.label_feed_dict[label[1][2]]["text"] = array_value[0][2]
        self.label_feed_dict[label[1][3]]["text"] = array_value[0][3]
        self.label_feed_dict[label[1][4]]["text"] = array_value[0][4]
        self.label_feed_dict[label[1][5]]["text"] = array_value[0][5]

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to Quit.?"):
            if self.client_dash is not None:            
                self.client_dash.StopScript()
                print("Stopped")
            self.root.destroy()