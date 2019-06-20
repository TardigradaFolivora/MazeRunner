#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 4.22
#  in conjunction with Tcl version 8.6
#    Apr 20, 2019 11:33:00 AM +0100  platform: Windows NT

import sys
from subprocess import Popen
import os
import threading
import time

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
projectDirectory = os.path.join(scriptDirectory,"..","..")
os.environ['FOR_IGNORE_EXCEPTIONS'] = '1'

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True


class Control:
    def __init__(self):
        self.mqtt_broker_proc = 0
        self.maze_gui_proc = 0
        self.team = ""
        self.generator_action = 0
        self.running = 1
        self.mqtt_broker_state = 0
        self.maze_gui_state = 0
        self.solver_action_proc = 0
        self.solver_action_state = 0

        threading.Thread(target=self.monitor).start()

    def checkproc(self,p):
        state = 0
        if p != 0:
            poll = p.poll()

            if poll == None:
                state = 1
            else:
                state = -1
        return state


    def monitor(self):
        while self.running:
            self.mqtt_broker_state = self.checkproc(self.mqtt_broker_proc)
            self.maze_gui_state = self.checkproc(self.maze_gui_proc)
            self.solver_action_state = self.checkproc(self.solver_action_proc)

            #print("Monitor: {} {} {}".format(self.mqtt_broker_state, self.maze_gui_state, self.solver_action_state))
            
            time.sleep(1)
         

control = Control()

def handler(a,b=None):
    control.running=0
    sys.exit(0)

def install_handler():
    if sys.platform == "win32":
        import win32api
        win32api.SetConsoleCtrlHandler(handler, True)

install_handler()

def set_Tk_var():
    global combobox
    combobox = tk.StringVar()

def maze_visualize():
    print('Maze Visualizer started')
    
    sys.stdout.flush()

    executeSript=os.path.join(projectDirectory,"Framework","Visualizer","maze_visualize.py")
    control.maze_gui_proc = Popen(['python',executeSript],shell=True) # something long running


def maze_solver_loader():

    if control.team == "":
        print("Load Team please!")
    else:
        print('Solver Action')
        executeSript=os.path.join(projectDirectory,"Teams",control.team,"MazeSolverClient.py")
        control.solver_action_proc = Popen(['python',executeSript],shell=True) # something long running

def maze_solver_action():
    print('Solve Maze!')
    sys.stdout.flush()
    executeSript=os.path.join(projectDirectory,"Framework","MQTTBroker","mosquitto_pub.exe")
    control.mqtt_broker_proc = Popen([executeSript,"-t", "/maze", "-m","solve"],shell=True) # something long running

def mqtt_broker():
    print('MQTT Broker started')
    sys.stdout.flush()
    executeSript=os.path.join(projectDirectory,"Framework","MQTTBroker","mosquitto.exe")
    control.mqtt_broker_proc = Popen([executeSript],shell=True) # something long running
   

def load_team(team):
    print('Load {}'.format(team))
    control.team=team

def generator_action(width,height,complexity,density):
    print("w: {} | h: {} | c: {} | d: {}".format(width, height, complexity, density))
    
    if control.team == "":
        print("Load Team please!")
    else:
        print('Generator Action')
        executeSript=os.path.join(projectDirectory,"Teams",control.team,"MazeGeneratorClient.py")
        print(['python',executeSript,'-w', width,'-h',height,'-c',complexity,'-d',density])
        control.generator_action = Popen(['python',executeSript,"--width="+str(width),"--height="+str(height),"--complexity="+str(complexity),"--density="+str(density)],shell=True) # something long running

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None
    control.mqtt_broker_proc.terminate()    

if __name__ == '__main__':
    import maze_control
    maze_control.vp_start_gui()



