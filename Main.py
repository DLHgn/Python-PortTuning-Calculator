import gui_setup
import gui_setup.gui_data_manager as data_manager
from tkinter import ttk  # Import the Themed Tkinter widgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)

pad = 5
txtfield_size = 8

# setup main window
# We make it larger to accommodate the new layout
mainWindow = gui_setup.window_setup.Window()
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

# --- Building Impedance Graph ---
# Create a figure
fig = Figure(figsize=(6, 4), dpi=100)

# Add a default plot area (we'll draw on this later)
ax = fig.add_subplot(111)
ax.grid(True, which="both", ls="--", c='0.7') # Add a grid
fig.tight_layout()

# Create the Tkinter canvas object
canvas = FigureCanvasTkAgg(fig, master=graph_frame)
canvas.draw()

# Create the navigation toolbar
toolbar = NavigationToolbar2Tk(canvas, graph_frame, pack_toolbar=False)
toolbar.update()

# Pack the toolbar and canvas into the Graphs tab
toolbar.pack(side="bottom", fill="x")
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

# Tell the data manager where the canvas is
data_manager.set_graph_canvas(canvas)

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
endCorrection.item_setup(box_frame, pad, txtfield_size, "One Flanged End",
                         "Both Flanged Ends",
                         "Both Free Ends",
                         "3 Common Walls",
                         "2 Common Walls",
                         "1 Common Wall",
                         use_btn=False, use_cmb=True)
data_manager.set_end_correction(endCorrection)

numPorts = gui_setup.gui_items.Item("Number of Ports", 0, 4)
numPorts.item_setup(box_frame, pad, txtfield_size, 'no name', use_btn=False)
numPorts.insert_default_txtfield("1")
data_manager.set_number_of_ports(numPorts)

portTuning = gui_setup.gui_items.Item("Port Tuning", 0, 5)
portTuning.item_setup(box_frame, pad, txtfield_size, 'no name', use_btn=False)
portTuning.txtField.configure(state='readonly') # Make it read-only
data_manager.set_port_tuning(portTuning)


# ---
# Controls Frame Widgets
# ---
submit = gui_setup.buttons.Btn(0, 0, "Submit")
submit.btn_setup(controls_frame, pad)

loadTest = gui_setup.buttons.Btn(1, 0, "Load Test")
loadTest.btn_setup(controls_frame, pad)

# Start freq for graph
start_freq = gui_setup.gui_items.Item("Graph Start Freq", 0, 1)
start_freq.item_setup(controls_frame, pad, txtfield_size, "Hz")
start_freq.insert_default_txtfield("20") # Add default text
data_manager.set_start_freq(start_freq)

# End freq for graph
stop_freq = gui_setup.gui_items.Item("Graph Stop Freq", 2, 1)
stop_freq.item_setup(controls_frame, pad, txtfield_size, "Hz", use_btn=False)
stop_freq.insert_default_txtfield("100") # Add default text
data_manager.set_stop_freq(stop_freq)

# Step size (how fine the graph is)
graph_step = gui_setup.gui_items.Item("Graph Step (Hz)", 4, 1)
graph_step.item_setup(controls_frame, pad, txtfield_size, "Hz")
graph_step.insert_default_txtfield("1") # Default to 1 Hz step
data_manager.set_graph_step(graph_step)

# ----
# Centering Logic
# ----

# Force tkinter to update and calculate the window's required size
mainWindow.window.update_idletasks()

# Get the calculated width and height
window_width = mainWindow.window.winfo_width()
window_height = mainWindow.window.winfo_height()

# Get the screen dimensions
screen_width = mainWindow.window.winfo_screenwidth()
screen_height = mainWindow.window.winfo_screenheight()

# Calculate the centered coordinates
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))

# Set the final geometry (size AND position)
mainWindow.window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

# Run the main application
mainWindow.window.mainloop()