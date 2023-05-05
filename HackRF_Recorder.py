#!/usr/bin/python3
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------------------#
# This simple script just adds an interface to the "hackrf_transfer" command so that it can be easily used with TempestSDR on Linux.
# The captured file will be overwritten each time the rec button is pressed.
# Coded by neib
#
#-------------------------------------------------------------------------------#

from tkinter import *
import tkinter as tk
from tkinter import messagebox

import os
import signal
import subprocess

#-------------------------------------------------------------------------------#
# Useless process to have something to kill.
process = subprocess.Popen(":", shell=True, stdin=subprocess.PIPE)
#-------------------------------------------------------------------------------#
# Temp file path
file = "./hackrf_tmp_record"

#-------------------------------------------------------------------------------#
#--------------------------- Rec --------------------------#
def rec():
    global process

    if process:
        os.kill(process.pid,signal.SIGINT)

    cm = "exec hackrf_transfer -s " + str(float(samp_rate.get()[:-5])*1000000) + " -f " + str(freq.get()) + " -l " + str(lna.get()) + " -g " + str(vga.get()) + " -a " + str(amp_value.get()) + " -r " + file
    process = subprocess.Popen(cm, shell=True, stdout=subprocess.PIPE)#


#-------------------------------------------------------------------------------#
#----------------------- Stop record -----------------------#
def stop():
    os.kill(process.pid,signal.SIGINT)


#-------------------------------------------------------------------------------#
#----------------------- Close window -----------------------#
def on_closing():
    if messagebox.askokcancel("Close HackRF - Recorder", "Do you really want to quit?"):
        os.kill(process.pid,signal.SIGINT)
        Window.destroy()



#-------------------------------------------------------------------------------#
#                               MAIN WINDOW
#-------------------------------------------------------------------------------#
Window = Tk()
Window.title("HackRF - Recorder")
Window.config(bg="gray95")


#-------------------------------------------------------------------------------#
#----------------------- Target area -----------------------#
tFrame = Frame(Window)
tFrame.config(width=700, height=30, borderwidth=2, relief="groove")
tFrame.pack_propagate(False)
tFrame.pack(padx=5,pady=5)

# Samp Rate
srLabel = Label(tFrame, text="Sample rate:")
srLabel.pack(side=LEFT, padx=5)

samp_rate = StringVar(tFrame)
samp_rate.set("10 MSPS") # default value
sr = OptionMenu(tFrame, samp_rate, "2 MSPS", "4 MSPS", "8 MSPS", "10 MSPS", "12.5  MSPS", "16 MSPS", "20 MSPS")
sr.pack(side=LEFT, padx=5, pady=0)

# Freq
targetLabel = Label(tFrame, text="Frequency:")
targetLabel.pack(side=LEFT, padx=5)

freq_i=tk.IntVar(value=432000000)
freq = tk.Spinbox(tFrame, from_= 5000000, to = 7000000000,width=12, increment=1000000,
    textvariable=freq_i, justify="right")
freq.pack(side=LEFT)
targetLabel = Label(tFrame, text="Hz", font="bold")
targetLabel.pack(side=LEFT, padx=1)

#-------------------------------------------------------------------------------#
#----------------------- Stop Button-----------------------#
stopButton = Button(tFrame, text=" || ", command=stop)
stopButton.config(font="bold", bg="gray90", fg="black", activeforeground="black", activebackground="gray93")
stopButton.pack(padx=5, pady=0, side=RIGHT)
#----------------------- Rec Button-----------------------#
recButton = Button(tFrame, text=" o ", command=rec)
recButton.config(font="bold", fg="black", bg="red2", activebackground="firebrick1", activeforeground="black")
recButton.pack(padx=0, pady=0, side=RIGHT)

#-------------------------------------------------------------------------------#
#----------------------- Opt area -----------------------#
# RX LNA (IF)
rxLNAFrame = Frame(Window)
rxLNAFrame.config(width=700, height=70, borderwidth=2, relief="groove")
rxLNAFrame.pack_propagate(False)
rxLNAFrame.pack(padx=5)

rx_lna = Label(rxLNAFrame, text="RX LNA (IF)   ", font="bold")
rx_lna.pack(side=LEFT)
lna = Scale(rxLNAFrame, from_=0, to=40, length=540, tickinterval=8, orient=HORIZONTAL)
lna.pack(side=LEFT)

rx_lnaDB = Label(rxLNAFrame, text="dB")
rx_lnaDB.pack(padx=5, side=LEFT)

# RX VGA (BB)
rxVGAFrame = Frame(Window)
rxVGAFrame.config(width=700, height=70, borderwidth=2, relief="groove")
rxVGAFrame.pack_propagate(False)
rxVGAFrame.pack(padx=5)

rx_vga = Label(rxVGAFrame, text="RX VGA (BB) ", font="bold")
rx_vga.pack(side=LEFT)
vga = Scale(rxVGAFrame, from_=0, to=62, length=540, tickinterval=2, orient=HORIZONTAL)
vga.pack(side=LEFT)

rx_vgaDB = Label(rxVGAFrame, text="dB")
rx_vgaDB.pack(padx=5, side=LEFT)

# AMP
ampFrame = Frame(Window)
ampFrame.config(width=700, height=30, borderwidth=2, relief="groove")
ampFrame.pack_propagate(False)
ampFrame.pack(padx=5)

amp_value = IntVar()
amp = Checkbutton(ampFrame, text="AMP", variable=amp_value, onvalue=1, offvalue=0)
amp.pack(side=LEFT)

# File location
save_as = Label(ampFrame, text="file: '"+file+"'")
save_as.pack(padx=5, side=RIGHT)


#-------------------------------------------------------------------------------#
#----------------------- START -----------------------#
Window.protocol("WM_DELETE_WINDOW", on_closing)
Window.mainloop()
