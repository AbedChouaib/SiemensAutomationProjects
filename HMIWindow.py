from tkinter import *
from tkinter import ttk
import plcM as PLC
import snap7
import time

Window = Tk()
Window.title("HMI Siemens S7-1200 Interface")
Window.minsize(400, 300)
# Window.configure(background="#afffff")

# ===========================================================
PLCS7 = snap7.client.Client()
global MLamp
MLamp = 0
global ELamp
ELamp = 0
global Live
Live = False
MidButtColor = ""
MidButtText = ""
EdgeButtColor = ""
EdgeButtText = ""
# ===========================================================

TabControl = ttk.Notebook(Window)
TabControl.pack(expan=1, fill="both")

Root = ttk.Frame(TabControl)
TabControl.add(Root, text="Root")
Master = ttk.Frame(TabControl)
TabControl.add(Master, text="Master")

# ==================== Root Tab =================================================================
Frame2 = Frame(Root)
Frame2.grid(row=2, column=1, sticky=W)
MasterButt = Button(Frame2, text="Master Room", width=12,
                    height=2, bg="gray", command=lambda: ChangeTab(Master))
MasterButt.grid(row=1, column=0, padx=5, pady=5, sticky=W)
Label5 = Label(Frame2, fg="red")
Label5.grid(row=1, column=3, sticky=W)
Lable3 = Label(Frame2, font=40)
Lable3.grid(row=2, column=1, sticky=E)
IPlabel = Label(Frame2, text="IP address:")
IPlabel.grid(row=2, column=2, sticky=E)
RackLable = Label(Frame2, text="Rack:")
RackLable.grid(row=3, column=2, sticky=E)
SlotLable = Label(Frame2, text="Slot:")
SlotLable.grid(row=3, column=3, padx=50, sticky=W)

IPe = Entry(Frame2)
IPe.grid(row=2, column=3, sticky=W)
IPe.insert(1, "192.168.31.222")
PLCRack = Entry(Frame2, width=4)
PLCRack.grid(row=3, column=3, sticky=W)
PLCRack.insert(1, 0)
PLCSlot = Entry(Frame2, width=4)
PLCSlot.grid(row=3, column=3, padx=80, sticky=W)
PLCSlot.insert(1, 1)


ConnectButt = Button(Frame2, text="Connect", width=12,
                     height=2, bg="gray", command=lambda: ConnectToPLC())
ConnectButt.grid(row=4, column=3, padx=15, pady=6, sticky=W)
ExitButt = Button(Frame2, text="Quit", width=12,
                  height=2, bg="Red", command=lambda: exit())
ExitButt.grid(row=5, column=0, padx=5, pady=40, sticky=W)
# ==================== Root Tab =================================================================
# ==================== Master Room Tab ==========================================================
Frame1 = Frame(Master)
Frame1.grid(row=2, column=1, sticky=W)
# Frame1.configure(background="#afffff")
Lable1 = Label(Frame1, text="   Middle Lamp", font=30)
Lable1.grid(row=1, column=1, padx=10, pady=10, sticky=W)
Lable2 = Label(Frame1, text="   Edge Lamp", font=30)  # bg = "#afffff"
Lable2.grid(row=4, column=1, padx=10, pady=10, sticky=W)
TestMod = Label(Frame1)
TestMod.grid(row=1, column=2, padx=20, sticky=E)
# --------------------------------------
RootButt = Button(Frame1, text="To Root", width=12,
                  height=2, bg="gray", command=lambda: ChangeTab(Root))
RootButt.grid(row=1, column=0, padx=5, pady=5, sticky=E)
# --------------------Lamp if conditions------------------
if Live == False:
    if MLamp == 0:
        MidButtColor = "gray"
        MidButtText = "Turn ON"
    elif MLamp == 1:
        MidButtColor = "7CFC00"
        MidButtText = "Turn OFF"
    if ELamp == 0:
        EdgeButtColor = "gray"
        EdgeButtText = "Turn ON"
    elif ELamp == 1:
        EdgeButtColor = "7CFC00"
        EdgeButtText = "Turn OFF"
else:
    if PLC.ReadOutput(PLCS7, 0, 0) == False:
        MidButtColor = "gray"
        MidButtText = "Turn ON"
    else:
        MidButtColor = "7CFC00"
        MidButtText = "Turn OFF"
    if PLC.ReadOutput(PLCS7, 0, 1) == False:
        EdgeButtColor = "gray"
        EdgeButtText = "Turn ON"
    else:
        EdgeButtColor = "7CFC00"
        EdgeButtText = "Turn OFF"
# --------------------if conditions------------------
MiddleButt = Button(Frame1, text=MidButtText, width=12,
                    height=4, bg=MidButtColor, command=lambda: TurnOnOffMid(MiddleButt))
MiddleButt.grid(row=3, column=1, sticky=E)
EdgeButt = Button(Frame1, text=EdgeButtText, width=12,
                  height=4, bg=EdgeButtColor, command=lambda: TurnOnOffEdge(EdgeButt))
EdgeButt.grid(row=5, column=1, sticky=E)
if Live == False:
    TestMod.configure(
        text="Not connected \n your in test mod!", fg="red")
else:
    TestMod.configure(
        text="Live!", fg="#7CFC00", font=10)
# ==================== Master Room Tab ==========================================================

# ==================== Buttons function =========================================================


def TurnOnOffMid(Butt):
    global MLamp
    if Live == False:
        if MLamp == 0:
            Butt.configure(background="#7CFC00", text="Turn OFF")
            MLamp = 1
            print("Mid Lamps is on")
            return MLamp
        elif MLamp == 1:
            Butt.configure(background="gray", text="Turn ON")
            MLamp = 0
            print("Mid Lamp is off")
            return MLamp
    else:
        if PLC.ReadOutput(PLCS7, 0, 0) == False:
            Butt.configure(background="#7CFC00", text="Turn OFF")
            PLC.WriteMemory(PLCS7, 0, 1, 1, 1)
            time.sleep(0.05)
            PLC.WriteMemory(PLCS7, 0, 1, 1, 0)
            print("Mid Lamps is on")
        else:
            Butt.configure(background="gray", text="Turn ON")
            PLC.WriteMemory(PLCS7, 0, 1, 1, 1)
            time.sleep(0.05)
            PLC.WriteMemory(PLCS7, 0, 1, 1, 0)
            print("Mid Lamp is off")


def TurnOnOffEdge(Butt):
    global ELamp
    if Live == False:
        if ELamp == 0:
            Butt.configure(background="#7CFC00", text="Turn OFF")
            ELamp = 1
            print("Edge Lamps is on")
            return ELamp
        elif ELamp == 1:
            Butt.configure(background="gray", text="Turn ON")
            ELamp = 0
            print("Edge Lamp is off")
            return ELamp
    else:
        # PLC.ReadMemory(PLCS7, 0, 2, 1) == 0:
        if PLC.ReadOutput(PLCS7, 0, 1) == False:
            Butt.configure(background="#7CFC00", text="Turn OFF")
            PLC.WriteMemory(PLCS7, 0, 2, 1, 1)
            time.sleep(0.05)
            PLC.WriteMemory(PLCS7, 0, 2, 1, 0)
        else:
            Butt.configure(background="gray", text="Turn ON")
            PLC.WriteMemory(PLCS7, 0, 2, 1, 1)
            time.sleep(0.05)
            PLC.WriteMemory(PLCS7, 0, 2, 1, 0)


def ChangeTab(tab_id):
    TabControl.select(tab_id)
    pass


def ConnectToPLC():
    global Live
    if Live == False:
        IPaddress = IPe.get()
        Rack = int(PLCRack.get())
        Slot = int(PLCSlot.get())
        if len(PLCRack.get()) == 0:
            PLCRack.insert(1, 0)
        if len(PLCSlot.get()) == 0:
            PLCSlot.insert(1, 1)
        if len(IPe.get()) == 0:
            Label5.configure(text="Please enter an IP address!", fg="red")
            pass
        elif len(IPe.get()) < 8:
            Label5.configure(text="Please enter a vaild IP address!", fg="red")
            pass
        else:
            Label5.configure(text="")
            PLCS7.connect(IPaddress, Rack, Slot)
            Live = True
            if PLCS7.get_connected():
                ConnectButt.configure(text="Connected!", bg="#7CFC00")
                TestMod.configure(text="Live!", fg="#7CFC00", font=10)
                pass
            else:
                Label5.configure(
                    text="Please enter a correct IP address!", fg="red")
                pass
    else:
        pass


# ==================== Buttons function =========================================================
# ==============================
Window.mainloop()
# ==============================
