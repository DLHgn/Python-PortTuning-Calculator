import gui_setup
import gui_setup.gui_data_manager as data_manager
from tkinter import ttk  # Import the Themed Tkinter widgets

pad = 5
txtfield_size = 8

# setup main window
# We make it larger to accommodate the new layout
mainWindow = gui_setup.window_setup.Window(800, 500)
mainWindow.window_setup("Port Tuning Calculator")

# ---
# Create the Tabbed Notebook
# ---
notebook = ttk.Notebook(mainWindow.window)
notebook.pack(expand=True, fill='both', padx=pad, pady=pad)

# ---
# Create the "Inputs" Tab
# ---
input_frame = ttk.Frame(notebook)
notebook.add(input_frame, text='Inputs')

# ---
# Create the "Graphs" Tab
# ---
graph_frame = ttk.Frame(notebook)
notebook.add(graph_frame, text='Graphs')

# ---
# Organize the "Inputs" Tab with Labelframes
# ---
# We'll create three groups
driver_frame = ttk.Labelframe(input_frame, text="Driver Parameters")
driver_frame.grid(column=0, row=0, padx=pad, pady=pad, sticky="nw", ipadx=pad, ipady=pad)

box_frame = ttk.Labelframe(input_frame, text="Box & Port Parameters")
box_frame.grid(column=1, row=0, padx=pad, pady=pad, sticky="nw", ipadx=pad, ipady=pad)

controls_frame = ttk.Labelframe(input_frame, text="Controls & Analysis")
controls_frame.grid(column=0, row=1, columnspan=2, padx=pad, pady=pad, sticky="ew", ipadx=pad, ipady=pad)


# ---
# Add All Widgets to their new 'Labelframe' parents
# ---
# Note: The 'col' and 'rw' are now relative to their new frame.

# ---
# Driver Frame Widgets
# ---
cms = gui_setup.gui_items.Item("Cms", 0, 0)
cms.item_setup(driver_frame, pad, txtfield_size, "m/N", "mm/N", "um/N")
data_manager.set_cms(cms)

mms = gui_setup.gui_items.Item("Mms", 0, 1)
mms.item_setup(driver_frame, pad, txtfield_size, "Kg", "g")
data_manager.set_mms(mms)

le = gui_setup.gui_items.Item("Le", 0, 2)
le.item_setup(driver_frame, pad, txtfield_size, "H", "mH")
data_manager.set_le(le)

re = gui_setup.gui_items.Item("Re", 0, 3)
re.item_setup(driver_frame, pad, txtfield_size, "ohm")
data_manager.set_re(re)

rms = gui_setup.gui_items.Item("Rms", 0, 4)
rms.item_setup(driver_frame, pad, txtfield_size, "Kg/s", "Ns/s")
data_manager.set_rms(rms)

bl = gui_setup.gui_items.Item("Bl", 0, 5)
bl.item_setup(driver_frame, pad, txtfield_size, "Tm", "Na")
data_manager.set_bl(bl)

sd = gui_setup.gui_items.Item("Sd", 0, 6)
sd.item_setup(driver_frame, pad, txtfield_size, "m^2", "cm^2", "mm^2", "in^2", "ft^2")
data_manager.set_sd(sd)

vg = gui_setup.gui_items.Item("Vg", 0, 7)
vg.item_setup(driver_frame, pad, txtfield_size, "V")
data_manager.set_vg(vg)


# ---
# Box & Port Frame Widgets
# ---
portArea = gui_setup.gui_items.Item("Port Cross Sectional Area", 0, 0)
portArea.item_setup(box_frame, pad, txtfield_size, "in^2", "cm^2", "ft^2", "mm^2", 'm^2')
data_manager.set_port_area(portArea)

netVolume = gui_setup.gui_items.Item("Net Volume (Box)", 0, 1)
netVolume.item_setup(box_frame, pad, txtfield_size, "in^3", "L", "cm^3", "ft^3", "mm^3", "m^3")
data_manager.set_net_volume(netVolume)

portLength = gui_setup.gui_items.Item("Length of Port", 0, 2)
portLength.item_setup(box_frame, pad, txtfield_size, "in", "cm", "ft", "m", "mm")
data_manager.set_port_length(portLength)

endCorrection = gui_setup.gui_items.Item("End Correction", 0, 3)
endCorrection.item_setup(box_frame, pad, txtfield_size, True, "One Flanged End", "Both Flanged Ends",
                         "Both Free Ends", "3 Common Walls", "2 Common Walls", "1 Common Wall")
data_manager.set_end_correction(endCorrection)

numPorts = gui_setup.gui_items.Item("Number of Ports", 0, 4)
numPorts.item_setup(box_frame, pad, txtfield_size,1)
data_manager.set_number_of_ports(numPorts)

portTuning = gui_setup.gui_items.Item("Port Tuning", 0, 5)
portTuning.item_setup(box_frame, pad, txtfield_size, "Hz")
data_manager.set_port_tuning(portTuning)


# ---
# Controls Frame Widgets
# ---
frequency = gui_setup.gui_items.Item("Test Frequency", 0, 0)
frequency.item_setup(controls_frame, pad, txtfield_size, "Hz")
data_manager.set_frequency(frequency)

submit = gui_setup.buttons.Btn(2, 0, "Submit")
submit.btn_setup(controls_frame, pad)

loadTest = gui_setup.buttons.Btn(3, 0, "Load Test")
loadTest.btn_setup(controls_frame, pad)


# --- 6. Run the main application ---
mainWindow.window.mainloop()