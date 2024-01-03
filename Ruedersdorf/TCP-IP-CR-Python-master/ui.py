# -*- coding: utf-8 -*-
import json
import time
import tkinter as tk
from threading import Thread
from tkinter import *
from tkinter import messagebox, ttk
from tkinter.scrolledtext import ScrolledText

from dobot_api import *
from files.alarm_controller import alarm_controller_list
from files.alarm_servo import alarm_servo_list
from settings import Settings
import os

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
        # self.doThread = Thread(target=self.do_thread_function)
        # self.doThread.setDaemon(True)
        self.isDoorOpened = False
        self.pause_do = False

        self.root = Tk()
        self.root.title("") 
        
        # Get the absolute path to the image
        image_filename = "diabots.png"
        image_path = self.get_image_path(image_filename)
        self.logo_image = PhotoImage(file=image_path)
        # Create a custom title bar
        title_frame = Frame(self.root, bg="#262261", height=20)
        # Load and display the logo image
        # logo_image = PhotoImage(file="images/diabots.png")
        logo_label = Label(title_frame, image=self.logo_image,fg="#FFFFFF", bg="#262261")
        logo_label.pack(side=LEFT, padx=10)

        # Display the title text
        title_label = Label(title_frame, text="Diabots", font=("Arial", 24), fg="#FFFFFF", bg="#262261")
        title_label.pack(side=LEFT)
        title_frame.pack(fill=X)
        # fixed window size
        self.root.geometry("900x700")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        # set window icon
        image_filename = "diabots.ico"
        image_path = self.get_image_path(image_filename)
        self.root.iconbitmap(image_path)

        # global state dict
        self.global_state = {}

        # all button
        self.button_list = []

        # all entry
        self.entry_dict = {}

        # Robot Connect
        self.frame_robot = LabelFrame(self.root, text="Robot Connect",  font=("Arial", 12), fg="#FFFFFF", bg="#ACAEAB",
                                      labelanchor="nw", width=870, height=70, border=3)

        # Current Speed Ratio
        self.set_label(self.frame_robot,
                       text="Current Speed Ratio:", rely=0.2, x=10)
        self.label_feed_speed = self.set_label(
            self.frame_robot, "", rely=0.2, x=145)
        self.set_label(self.frame_robot, text="%", rely=0.2, x=175)

        # Robot Mode
        self.set_label(self.frame_robot, text="Robot Mode:", rely=0.2, x=290)
        self.label_robot_mode = self.set_label(
        self.frame_robot, "", rely=0.2, x=390)

        self.label_ip = Label(self.frame_robot, text="IP Address:" , bg="#ACAEAB" )
        # self.label_ip.place(rely=0.2, x=10)
        ip_port = StringVar(self.root, value=Settings.IP_CR)
        self.entry_ip = Entry(self.frame_robot, width=12, textvariable=ip_port)
        # self.entry_ip.place(rely=0.2, x=90)

        self.label_dash = Label(self.frame_robot, text="Dashboard Port:" , bg="#ACAEAB")
        # self.label_dash.place(rely=0.2, x=180)
        dash_port = IntVar(self.root, value=29999)
        self.entry_dash = Entry(
            self.frame_robot, width=7, textvariable=dash_port)
        # self.entry_dash.place(rely=0.2, x=280)

        self.label_move = Label(self.frame_robot, text="Move Port:" , bg="#ACAEAB")
        # self.label_move.place(rely=0.2, x=360)
        move_port = IntVar(self.root, value=30003)
        self.entry_move = Entry(
            self.frame_robot, width=7, textvariable=move_port)
        # self.entry_move.place(rely=0.2, x=440)

        self.label_feed = Label(self.frame_robot, text="Feedback Port:" , bg="#ACAEAB")
        # self.label_feed.place(rely=0.2, x=520)
        feed_port = IntVar(self.root, value=30004)
        self.entry_feed = Entry(
            self.frame_robot, width=7, textvariable=feed_port)
        # self.entry_feed.place(rely=0.2, x=620)

        # Connect/DisConnect
        self.button_connect = self.set_button(master=self.frame_robot,
                                              text="Verbinden", rely=0, x=670, command=self.connect_port)
        self.button_connect["width"] = 18
        self.button_connect["height"] = 2
        self.global_state["connect"] = False

        # Dashboard Function
        self.frame_dashboard = LabelFrame(self.root, text="Dashboard Function", font=("Arial", 12), fg="#FFFFFF",  bg="#ACAEAB", 
                                          labelanchor="nw",pady=10, width=870, height=250, border=2)

        # Enable/Disable
        self.button_enable = self.set_button(master=self.frame_dashboard,
                                             text="Aktivieren", rely=0.05, x=10, command=self.enable)
        self.global_state["enable"] = False

        # Reset Robot / Clear Error
        # self.set_button(master=self.frame_dashboard, 
        #                 text="Reset Robot", rely=0.05, x=190, command=self.reset_robot)
        self.set_button(master=self.frame_dashboard, 
                        text="Home Pos", rely=0.05, x=190, command=self.home_pos)
        self.set_button(master=self.frame_dashboard, 
                        text="Clear Error", rely=0.05, x=380, command=self.clear_error)

        self.set_button(master=self.frame_dashboard,
                        text="Drag Mode", rely=0.05, x=580, command=self.set_drag_mode) # 720
        
        self.start_button = self.set_button(self.frame_dashboard, "Roboter Starten", rely=0.3, x=10, command=self.start_script)
        self.stop_button = self.set_button(self.frame_dashboard, "Roboter Stoppen", rely=0.3, x=190, command=self.stop_script)
        self.pause_button = self.set_button(self.frame_dashboard, "Roboter Pausieren", rely=0.3, x=380, command=self.pause_script)
        self.resume_button = self.set_button(self.frame_dashboard, "Roboter Fortfahren", rely=0.3, x=580, command=self.resume_script)
        
        self.archiveCheckB = self.set_button(self.frame_dashboard, "Reset Archiv", rely=0.55, x=10, command=self.reset_archive)
        # self.versandCheckB = self.set_button(self.frame_dashboard, "Reset Versand", rely=0.55, x=180, command=self.reset_versand)
        self.fehlerCheckB = self.set_button(self.frame_dashboard, "Reset Fehler", rely=0.55, x=190, command=self.reset_fehler)
        # self.openDoor = self.set_button(self.frame_dashboard, "Open Door", rely=0.55, x=580, command=self.open_fridge_door)
        # self.closeDoor = self.set_button(self.frame_dashboard, "Close Door", rely=0.55, x=720, command=self.close_fridge_door)
        # self.InitPosCheckB = self.set_button(self.frame_dashboard, "Home Pos", rely=0.55, x=350, command=self.home_pos)

        self.CsStatus = IntVar(value=1)
        self.CsCheckB = Checkbutton(master=self.frame_dashboard, text='BCS XP',variable=self.CsStatus, 
                         onvalue=1, offvalue=0, command=self.update_machine_status)
        self.CsCheckB.pack()
        self.CsCheckB.place(rely=0.8, x=10,width=145,height=35)
        self.CsCheckB.config(state=DISABLED)

        self.CobasStatus = IntVar(value=1)
        self.CobasCheckB = Checkbutton(master=self.frame_dashboard, text='Cobas Pure',variable=self.CobasStatus, 
                         onvalue=1, offvalue=0, command=self.update_machine_status)
        self.CobasCheckB.pack()
        self.CobasCheckB.place(rely=0.8, x=190,width=145,height=35)
        self.CobasCheckB.config(state=DISABLED)

        self.XnStatus = IntVar(value=1)
        self.XnCheckB = Checkbutton(master=self.frame_dashboard, text='Beckman',variable=self.XnStatus, 
                         onvalue=1, offvalue=0, command=self.update_machine_status)
        self.XnCheckB.pack()
        self.XnCheckB.place(rely=0.8, x=380,width=145,height=35)
        self.XnCheckB.config(state=DISABLED)
        # Speed Ratio
        self.label_speed = Label(self.frame_dashboard, text="Speed Ratio:", bg="#ACAEAB")
        self.label_speed.place(rely=0.8, x=580)

        s_value = StringVar(self.root, value="100")
        self.entry_speed = Entry(self.frame_dashboard,
                                 width=6, textvariable=s_value)
        self.entry_speed.place(rely=0.8, x=670)
        self.label_cent = Label(self.frame_dashboard, text="%" , bg="#ACAEAB")
        self.label_cent.place(rely=0.8, x=715)
        self.set_button(master=self.frame_dashboard, text="Confirm", rely=0.75, x=735,width=7,height=2, command=self.confirm_speed)  #600

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
        #  text="Feedback" removed
        self.frame_feed = LabelFrame(self.frame_feed_log, text="", labelanchor="nw", font=("Arial", 12), fg="#FFFFFF",  bg="#ACAEAB", 
                                    width=550, height=150)

        self.frame_feed.place(relx=0, rely=0, relheight=1)

        # Current Speed Ratio
        # self.set_label(self.frame_feed,
        #                text="Current Speed Ratio:", rely=0.05, x=10)
        # self.label_feed_speed = self.set_label(
        #     self.frame_feed, "", rely=0.05, x=145)
        # self.set_label(self.frame_feed, text="%", rely=0.05, x=175)

        # Robot Mode
        # self.set_label(self.frame_feed, text="Robot Mode:", rely=0.1, x=10)
        # self.label_robot_mode = self.set_label(
        #     self.frame_feed, "", rely=0.1, x=95)

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
        self.frame_err = LabelFrame(self.frame_feed, text="Error Info", labelanchor="nw", font=("Arial", 12), fg="#FFFFFF",  bg="#ACAEAB", 
                                    width=180, height=50)
        self.frame_err.place(relx=0.65, rely=0, relheight=0.7)

        self.text_err = ScrolledText(
            self.frame_err, width=170, height=100, relief="flat")
        self.text_err.place(rely=0, relx=0, relheight=1, relwidth=1)

        self.set_button(self.frame_feed, "Clear", rely=0.71, width= 4 , height=2,
                        x=487, command=self.clear_error_info)

        # Log
        self.frame_log = LabelFrame(self.frame_feed_log, text="Log", labelanchor="nw", font=("Arial", 12), fg="#FFFFFF",  bg="#ACAEAB", 
                                    width=300, height=150)
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

    def get_image_path(self,image_filename):
        # Get the directory of the executable
        executable_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(executable_dir, "images", image_filename)
        return image_path

    def update_machine_status(self):
        if self.client_dash is not None:
            if self.CsStatus.get() == 1:
                self.client_dash.DOExecute(11, 1)
            else:
                self.client_dash.DOExecute(11, 0)
            if self.CobasStatus.get() == 1:
                self.client_dash.DOExecute(12, 1)
            else:
                self.client_dash.DOExecute(12, 0)
            if self.XnStatus.get() == 1:
                self.client_dash.DOExecute(13, 1)
            else:
                self.client_dash.DOExecute(13, 0)

    def reset_archive(self):
        msgBox = messagebox.askquestion('Reset Archive', 'Are you sure, you want to RESET ARCHIVE.?', icon='warning')
        if msgBox == 'yes':
            if self.client_dash is not None:
                self.client_dash.DOExecute(8, 1)
                if self.pause_do:
                    if self.safetySensor:
                        self.resume_script()
                    self.pause_do = False
                         
    def reset_versand(self):
        msgBox = messagebox.askquestion('Reset Versand', 'Are you sure, you want to RESET VERSAND.?', icon='warning')
        if msgBox == 'yes':
            if self.client_dash is not None:
                self.client_dash.DOExecute(9, 1)
                if self.pause_do:
                    if self.safetySensor:
                        self.resume_script()
                    self.pause_do = False

    def reset_fehler(self):
        msgBox = messagebox.askquestion('Reset Fehler', 'Are you sure, you want to RESET FEHLER.?', icon='warning')
        if msgBox == 'yes':
            if self.client_dash is not None:
                self.client_dash.DOExecute(10, 1)
                if self.pause_do:
                    if self.safetySensor:
                        self.resume_script()
                    self.pause_do = False

    def home_pos(self):
        self.client_dash.ClearError()
        time.sleep(0.5)
        self.client_dash.StopDrag()
        time.sleep(0.5)
        self.client_move.JointMovJ(Settings.drive_pos_mj[0],Settings.drive_pos_mj[1],Settings.drive_pos_mj[2],Settings.drive_pos_mj[3],Settings.drive_pos_mj[4],Settings.drive_pos_mj[5])
    
    def do_thread_function(self): 
        # 8   24        Reset Archiv
        # 9   25        Reset Versand
        # 10  26        Reset Fehler
        # 11  27        CS Status
        # 12  28        Cobas Status
        # 13  29        XN Status
        # 14  30        Filled Archiv
        # 15  31        Filled Versand
        # 16  32        Filled Fehler
        # self.pause_do = False
        while True:
            time.sleep(0.05)
            if self.client_dash is not None:
                self.di30 = self.read_sensor_avg(30,1,2) # DO14
                self.di31 = self.read_sensor_avg(31,1,2) # DO15
                self.di32 = self.read_sensor_avg(32,1,2) # DO16
                if self.di30 == 1:
                    self.pause_do = True
                    messagebox.showwarning('Reset Archive', 'Please empty Archive and click RESET button.', icon='warning')
                    self.client_dash.DOExecute(14, 0)
                    # self.pause = False
                if self.di31 == 1:
                    self.pause_do = True
                    messagebox.showwarning('Reset Versand', 'Please empty Versand and click RESET button.', icon='warning')
                    self.client_dash.DOExecute(15, 0)
                    # self.pause = False
                if self.di32 == 1:
                    self.pause_do = True
                    messagebox.showwarning('Reset Fehler', 'Please empty Fehler and click RESET button.', icon='warning')
                    self.client_dash.DOExecute(16, 0)
                    # self.pause = False
                self.di19 = self.read_sensor_avg(19,0,2) # DO3
                if self.di19 == 0:
                    self.archiveCheckB["state"] = "normal"
                    # self.versandCheckB["state"] = "normal"
                    self.fehlerCheckB["state"] = "normal"                    
                    # self.openDoor["state"] = "normal"
                    # self.closeDoor["state"] = "normal"
                else:
                    self.archiveCheckB["state"] = "disabled"
                    # self.versandCheckB["state"] = "disabled"
                    self.fehlerCheckB["state"] = "disabled" 
                    # if not self.isDoorOpened:
                    #     self.closeDoor["state"] = "disabled"
                    # self.openDoor["state"] = "disabled"
                    

    def thread_function(self): 
        # 8   24        Reset Archiv
        # 9   25        Reset Versand
        # 10  26        Reset Fehler
        # 11  27        CS Status
        # 12  28        Cobas Status
        # 13  29        XN Status
        # 14  30        Filled Archiv
        # 15  31        Filled Versand
        # 16  32        Filled Fehler
        self.pause_do = False
        self.safetySensor = 1
        self.cam1Sensor = 1
        self.pause = False
        while True:
            time.sleep(0.05)
            if self.client_dash is not None:
                self.safetySensor = self.read_sensor_avg(3,0,10) # safety  sensor
                self.cam1Sensor = self.read_sensor_avg(1,0,10) # camera sensor
                self.di21 = self.read_sensor_avg(21,1,10) # DO5
                self.isRobotAtCamera1 = self.read_sensor_avg(22,1,10)   # DO6    
                self.isRobotAtMachine = self.read_sensor_avg(23,1,10)   # DO7         
                if self.safetySensor == 1 and self.cam1Sensor == 1 and self.pause and not self.pause_do:
                    self.resume_script()
                    self.pause = False  
                    print("Resumed")
                if not self.pause and (self.safetySensor == 0 or (self.cam1Sensor == 0 and self.isRobotAtCamera1 == 1)) :
                    self.client_dash.DOExecute(5, 1)
                    if self.isRobotAtMachine == 0:
                        self.pause_script()
                        self.pause = True
                        print("Paused")
                if self.cam1Sensor == 0 and self.di21 != 1: 
                    self.client_dash.DOExecute(5, 1)
                    print("ping at camera1")

                self.di30 = self.read_sensor_avg(30,1,5) # DO14
                # self.di31 = self.read_sensor_avg(31,1,5) # DO15
                self.di32 = self.read_sensor_avg(32,1,5) # DO16
                if self.di30 == 1:
                    self.pause_do = True
                    messagebox.showwarning('Reset Archive', 'Please empty Archive and click RESET button.', icon='warning')
                    self.client_dash.DOExecute(14, 0)
                    # self.pause = False
                # if self.di31 == 1:
                #     self.pause_do = True
                #     messagebox.showwarning('Reset Versand', 'Please empty Versand and click RESET button.', icon='warning')
                #     self.client_dash.DOExecute(15, 0)
                    # self.pause = False
                if self.di32 == 1:
                    self.pause_do = True
                    messagebox.showwarning('Reset Fehler', 'Please empty Fehler and click RESET button.', icon='warning')
                    self.client_dash.DOExecute(16, 0)
                    # self.pause = False
                self.di19 = self.read_sensor_avg(19,0,2) # DO3
                if self.di19 == 0:
                    self.archiveCheckB["state"] = "normal"
                    # self.versandCheckB["state"] = "normal"
                    self.fehlerCheckB["state"] = "normal"                    
                    # self.openDoor["state"] = "normal"
                    # self.closeDoor["state"] = "normal"
                else:
                    self.archiveCheckB["state"] = "disabled"
                    # self.versandCheckB["state"] = "disabled"
                    self.fehlerCheckB["state"] = "disabled" 
                    # if not self.isDoorOpened:
                    #     self.closeDoor["state"] = "disabled"
                    # self.openDoor["state"] = "disabled"

    def read_sensor_avg(self,inp_DI,input_val,range_avg_val):
        try:
            sensor_read_cnt = 0
            range_avg_val = range_avg_val
            reading_val = 0
            input_val_inv = 0
            if input_val:
                input_val_inv = 0
            else:
                input_val_inv = 1
            for read_cnt in range(range_avg_val):
                # print(self.client_dash.DI(inp_DI))
                reading_val = int(self.client_dash.DI(inp_DI))
                if (reading_val != input_val):
                    break
                else:
                    sensor_read_cnt +=1
            if sensor_read_cnt == range_avg_val and reading_val == input_val:
                return input_val
            else:
                return input_val_inv
        except Exception as e:
            print(e)

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
        self.frame_robot.pack(pady=10)
        self.frame_dashboard.pack()
        # self.frame_move.pack()
        self.frame_feed_log.pack()

    def set_move(self, text, label_value, default_value, entry_value, rely, master):
        self.label = Label(master, text=text, bg="#ACAEAB")
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

    def set_button(self, master, text, rely, x, width=18, height=2, **kargs):
        self.button = Button(master, text=text, padx=5, fg="#FFFFFF", bg="#262261", width=width, height=height,
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
        self.label = Label(master, text=text, bg="#ACAEAB")
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
            self.disable_client_dash_buttons()
        self.global_state["connect"] = not self.global_state["connect"]
        self.set_feed_back()

    def disable_client_dash_buttons(self):
        self.archiveCheckB["state"] = "disabled"
        # self.versandCheckB["state"] = "disabled"
        self.fehlerCheckB["state"] = "disabled" 
        # self.openDoor["state"] = "disabled"
        # self.closeDoor["state"] = "disabled"
        self.start_button["state"] = "disabled"
        self.stop_button["state"] = "disabled"
        self.pause_button["state"] = "disabled"
        self.resume_button["state"] = "disabled"

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
            self.start_button["state"] = "normal"
            self.stop_button["state"] = "normal"
            self.pause_button["state"] = "normal"
            self.resume_button["state"] = "normal"
            self.archiveCheckB["state"] = "normal"
            # self.versandCheckB["state"] = "normal"
            self.fehlerCheckB["state"] = "normal" 
            # self.openDoor["state"] = "normal"
            # self.closeDoor["state"] = "normal"
            self.CsCheckB.config(state=NORMAL)
            self.client_dash.DOExecute(11, 1)
            self.CobasCheckB.config(state=NORMAL)
            self.client_dash.DOExecute(12, 1)
            self.XnCheckB.config(state=NORMAL)
            self.client_dash.DOExecute(13, 1)
        self.global_state["enable"] = not self.global_state["enable"]        

    def reset_robot(self):
        self.client_dash.ResetRobot()

    def clear_error(self):
        self.client_dash.ClearError()

    def confirm_speed(self):
        self.client_dash.SpeedFactor(int(self.entry_speed.get()))

    def set_drag_mode(self):
        self.client_dash.ClearError()
        time.sleep(0.5)
        self.client_dash.SetCollideDrag()
        time.sleep(0.5)
        self.client_dash.StartDrag()
    
    def open_fridge_door(self):
        if self.client_dash is not None:
            self.client_dash.DOExecute(3, 1)
            self.isDoorOpened = True
    
    def close_fridge_door(self):
        if self.client_dash is not None:
            self.client_dash.DOExecute(3, 0)
            self.isDoorOpened = False
            
    def start_script(self):
        if not self.label_robot_mode["text"] == "ROBOT_MODE_ENABLE":
            self.client_dash.ClearError()
            time.sleep(1)
            self.client_dash.StopDrag()
            time.sleep(1)
        if not self.threadStarted:
            self.safetyThread.start()
            self.threadStarted = True

        self.CsCheckB.config(state=DISABLED)
        self.CobasCheckB.config(state=DISABLED)
        self.XnCheckB.config(state=DISABLED)
        self.client_dash.RunScript(Settings.prjName_CR)
        time.sleep(1.5)
        self.client_dash.SpeedFactor(int(self.entry_speed.get()))
        self.start_button['state'] = tk.DISABLED
        self.stop_button['state'] = tk.NORMAL
        self.pause_button['state'] = tk.NORMAL
        self.resume_button['state'] = tk.DISABLED
        if not self.threadStarted:
            self.safetyThread.start()
            self.threadStarted = True 

    def stop_script(self):         
        self.client_dash.StopScript()       
        self.disable_client_dash_buttons()
        self.start_button['state'] = tk.NORMAL
        self.CsCheckB.config(state=NORMAL)
        self.CobasCheckB.config(state=NORMAL)
        self.XnCheckB.config(state=NORMAL)

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
            #print("robot_mode:", a["robot_mode"][0])
            #print("test_value:", hex((a['test_value'][0])))
            if hex((a['test_value'][0])) == '0x123456789abcdef':
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

                # check alarms
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