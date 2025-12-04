import gui_setup
import gui_setup.gui_data_manager as data_manager
from gui_setup.wiring_visualizer import WiringVisualizer
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk
)
import gui_setup.computations as computations
import tkinter.messagebox as messagebox
import tkinter as tk
from tkinter import ttk, StringVar, E, W

pad = 5
txtfield_size = 8


def _update_graph_view():
    # Validates inputs, gathers data, updates tuning, and redraws the selected graph.
    print("Updating graph view...")

    # Validate ALL inputs
    if not data_manager.validate_all_inputs():
        print("Input validation failed. Graph update stopped.")
        # Optional: Clear graph or show validation error on graph
        # canvas = data_manager.get_graph_canvas()
        # if canvas:
        #     fig = canvas.figure
        #     fig.clear()
        #     ax = fig.add_subplot(111)
        #     ax.text(0.5, 0.5, 'Invalid Input Data', ha='center', va='center', color='red')
        #     canvas.draw()
        return  # Stop if validation fails

    # Gather inputs & Update Tuning
    try:
        params = data_manager.gather_all_inputs()
        # Update Port Tuning display using calculated fb
        calculated_fb = computations.port_tuning_calculation(params)
        data_manager.set_port_tuning_output(calculated_fb)
        print(f"Calculated Port Tuning (fb): {calculated_fb:.2f} Hz")

    except ValueError as e:  # Catch specific conversion errors
        print(f"Error gathering inputs or calculating tuning: {e}")
        messagebox.showerror("Input Error", f"Could not process input values: {e}")
        # Update tuning display to show error
        data_manager.set_port_tuning_output("Error")
        return  # Stop processing
    except Exception as e:  # Catch other unexpected errors
        print(f"Unexpected error during input gathering/tuning: {e}")
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")
        data_manager.set_port_tuning_output("Error")
        return

    # Get graph settings
    start_freq = data_manager.get_start_freq()
    stop_freq = data_manager.get_stop_freq()
    graph_step = data_manager.get_graph_step()
    canvas = data_manager.get_graph_canvas()
    graph_type = data_manager.get_selected_graph_type()

    # Plot
    if canvas:
        try:
            computations.plot_selected_data(canvas, params, start_freq, stop_freq, graph_type, step=graph_step)
        except Exception as e:
            print(f"Error plotting selected data: {e}")
            messagebox.showerror("Plotting Error", f"An error occurred during plotting: {e}")
            # Optionally clear the graph or show an error message on it
            fig = canvas.figure
            fig.clear()
            ax = fig.add_subplot(111)
            ax.text(0.5, 0.5, 'Error plotting graph', ha='center', va='center', color='red')
            canvas.draw()
    else:
        print("Error: Graph canvas not found.")

    print("------------------------------------------")


def _on_graph_select(event=None):
    # Called when the graph selection combobox value changes.
    _update_graph_view()


def _on_update_graph_clicked():
    # Called when the "Update Graph" button is clicked.
    _update_graph_view()


def _on_vc_type_change(*args):
    vc_type = vc_type_var.get()

    # Logic to enable/disable radio buttons on BOTH tabs
    state = tk.NORMAL if vc_type == "Dual VC" else tk.DISABLED

    # Inputs Tab Widgets
    if 'wiring_series_rb' in globals(): wiring_series_rb.config(state=state)
    if 'wiring_parallel_rb' in globals(): wiring_parallel_rb.config(state=state)

    # Wiring Tab Widgets
    if 'w_wiring_series_rb' in globals(): w_wiring_series_rb.config(state=state)
    if 'w_wiring_parallel_rb' in globals(): w_wiring_parallel_rb.config(state=state)


def _update_system_impedance(*args):
    """Calculates impedance AND updates the wiring diagram with VC details."""
    try:
        # 1. Update Impedance Text (On BOTH tabs)
        total_re = data_manager.calculate_total_system_re()

        # Update Inputs Tab
        imp_item = data_manager.get_item("system_re")
        if imp_item: imp_item.set_output_text(f"{total_re:.2f} Ohm")

        # Update Wiring Tab
        if 'w_sysImp' in globals():
            w_sysImp.txtField.configure(state='normal')
            w_sysImp.txtField.delete(0, 'end')
            w_sysImp.txtField.insert(0, f"{total_re:.2f} Ohm")
            w_sysImp.txtField.configure(state='readonly')

        # 2. Update Wiring Diagram
        # Get Topology Info
        n_drivers = data_manager.get_number_of_drivers()
        topo_item = data_manager.get_item("wiring_topology")
        wiring_mode = topo_item.cmb.cmb.get() if topo_item else "Single Driver"

        # Parse S/P counts
        s_count, p_count = 1, 1
        if wiring_mode == "All Series":
            s_count, p_count = n_drivers, 1
        elif wiring_mode == "All Parallel":
            s_count, p_count = 1, n_drivers
        elif "Series-Parallel" in wiring_mode:
            try:
                parts = wiring_mode.split('(')[1].replace(')', '').split()
                s_count = int(parts[0].replace('s', ''))
                p_count = int(parts[1].replace('p', ''))
            except:
                s_count, p_count = n_drivers, 1

        # Get VC Info
        vc_type = data_manager.get_vc_type()
        vc_wiring = data_manager.get_vc_wiring()

        # Call draw with ALL parameters
        viz = data_manager.get_item("wiring_visualizer")
        if viz:
            viz.update_diagram(s_count, p_count, vc_type, vc_wiring)

    except Exception as e:
        print(f"Viz Error: {e}")
        pass


def _sync_num_drivers(event=None):
    """Syncs Number of Drivers between tabs."""
    try:
        # Determine source of event
        widget = event.widget
        val = widget.get()

        # Sync to the other widget
        if widget == numDrivers.txtField:
            w_numDrivers.txtField.delete(0, 'end')
            w_numDrivers.txtField.insert(0, val)
        elif widget == w_numDrivers.txtField:
            numDrivers.txtField.delete(0, 'end')
            numDrivers.txtField.insert(0, val)

        # Trigger the logic
        _on_num_drivers_change()

    except:
        pass


def _sync_wiring_topo(event=None):
    """Syncs Wiring Topology selection between tabs."""
    try:
        widget = event.widget
        val = widget.get()

        # Sync
        if widget == wiringTopo.cmb.cmb:
            w_wiringTopo.cmb.cmb.set(val)
        elif widget == w_wiringTopo.cmb.cmb:
            wiringTopo.cmb.cmb.set(val)

        # Trigger update
        _update_system_impedance()
    except:
        pass


def _on_num_drivers_change(*args):
    """Updates wiring topology options when number of drivers changes."""
    try:
        # Get raw text from the PRIMARY entry widget (Inputs tab)
        nd_item = data_manager.get_item("number_of_drivers")
        if not nd_item: return

        val_str = nd_item.get_txtfield()
        n_drivers = int(val_str) if val_str else 1

        if n_drivers < 1: n_drivers = 1

        # Get valid modes
        modes = data_manager.get_valid_wiring_modes(n_drivers)

        # Update Combo on BOTH tabs
        for combo in [wiringTopo.cmb.cmb, w_wiringTopo.cmb.cmb]:
            current = combo.get()
            combo['values'] = tuple(modes)

            # Reset selection if current invalid, or default to logical first choice
            if current not in modes:
                combo.current(0)

        # Trigger impedance update
        _update_system_impedance()

    except ValueError:
        pass  # Ignore incomplete input


def _on_reset_view_clicked():
    """Resets the wiring visualizer view."""
    viz = data_manager.get_item("wiring_visualizer")
    if viz:
        viz.reset_view()


def _on_toggle_legend_clicked():
    """Toggles the visualizer legend."""
    viz = data_manager.get_item("wiring_visualizer")
    if viz:
        viz.toggle_legend()


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

# ---
# Create the "Wiring Diagram" Tab
# ---
wiring_frame = ttk.Frame(notebook)
notebook.add(wiring_frame, text='Wiring Diagram')

# Controls Frame for the "Graphs" Tab
graph_controls_frame = ttk.Frame(graph_frame)
graph_controls_frame.pack(side="top", fill="x", padx=pad, pady=(pad, 0))

# Graph Selection Controls (Left Side)
graph_select_frame = ttk.Frame(graph_controls_frame)
graph_select_frame.pack(side="left", padx=(0, pad * 2))

graph_select_label = ttk.Label(graph_select_frame, text="Select Graph:")
graph_select_label.pack(side="left", padx=(0, pad))

graph_options = ["Impedance", "Cone Excursion (mm)", "Port Velocity (m/s)", "Group Delay (ms)"]
graph_select_combo = ttk.Combobox(graph_select_frame, values=graph_options, state='readonly',
                                  width=20)  # Adjusted width
graph_select_combo.set(graph_options[0])
graph_select_combo.pack(side="left")
data_manager.register_item("graph_select_combo", graph_select_combo)
graph_select_combo.bind("<<ComboboxSelected>>", _on_graph_select)

# Graph Range/Step Controls (Middle-Right Side)
graph_range_frame = ttk.Frame(graph_controls_frame)
graph_range_frame.pack(side="left", padx=(0, pad * 2))

# Start freq for graph
start_freq = gui_setup.gui_items.Item("Start Freq", 0, 0)
# Use grid within this sub-frame for alignment
start_freq.item_setup(graph_range_frame, pad, txtfield_size, "Hz", use_btn=False, min_value=1)  # No unit button needed
start_freq.insert_default_txtfield("10")
data_manager.register_item("start_freq", start_freq)

# End freq for graph
stop_freq = gui_setup.gui_items.Item("Stop Freq", 2, 0)  # Place next to start freq
stop_freq.item_setup(graph_range_frame, pad, txtfield_size, "Hz", use_btn=False, max_value=30000)
stop_freq.insert_default_txtfield("120")
data_manager.register_item("stop_freq", stop_freq)

# Step size
graph_step = gui_setup.gui_items.Item("Step (Hz)", 4, 0)  # Place next to stop freq
graph_step.item_setup(graph_range_frame, pad, txtfield_size, "Hz", use_btn=False, min_value=.01)
graph_step.insert_default_txtfield(".5")
data_manager.register_item("graph_step", graph_step)

# Update Button (Right Side)
update_graph_button = ttk.Button(graph_controls_frame, text="Update Graph", command=_on_update_graph_clicked)
update_graph_button.pack(side="left", padx=(pad * 2, 0))

# --- Building Graph Area (Below Controls) ---
graph_area_frame = ttk.Frame(graph_frame)
graph_area_frame.pack(side="top", fill="both", expand=True, padx=pad, pady=(pad, 0))

fig = Figure(figsize=(6, 4), dpi=100)
ax = fig.add_subplot(111)
ax.grid(True, which="both", ls="--", c='0.7')
fig.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=graph_area_frame)  # Changed master
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, graph_area_frame, pack_toolbar=False)  # Changed master
toolbar.update()

toolbar.pack(side="bottom", fill="x")
canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

data_manager.register_item("graph_canvas", canvas)

# ==========================================
# WIRING TAB SETUP
# ==========================================
# Top Controls Frame
wiring_controls = ttk.Frame(wiring_frame)
wiring_controls.pack(side="top", fill="x", padx=pad, pady=pad)

# -- Column 1: VC Config --
wc_col1 = ttk.LabelFrame(wiring_controls, text="Unit Config")
wc_col1.pack(side="left", fill="y", padx=5)

# VC Type
ttk.Label(wc_col1, text="VC Type:").grid(row=0, column=0, sticky=E, padx=5)
vc_type_var = StringVar(value="Single VC")  # Shared Variable!
vc_type_var.trace_add("write", _on_vc_type_change)
vc_type_var.trace_add("write", _update_system_impedance)

w_vc_single = ttk.Radiobutton(wc_col1, text="Single", variable=vc_type_var, value="Single VC")
w_vc_single.grid(row=0, column=1, sticky=W)
w_vc_dual = ttk.Radiobutton(wc_col1, text="Dual", variable=vc_type_var, value="Dual VC")
w_vc_dual.grid(row=0, column=2, sticky=W)

# VC Wiring
ttk.Label(wc_col1, text="Wiring:").grid(row=1, column=0, sticky=E, padx=5)
vc_wiring_var = StringVar(value="Series")  # Shared Variable!
vc_wiring_var.trace_add("write", _update_system_impedance)

w_wiring_series_rb = ttk.Radiobutton(wc_col1, text="Series", variable=vc_wiring_var, value="Series", state=tk.DISABLED)
w_wiring_series_rb.grid(row=1, column=1, sticky=W)
w_wiring_parallel_rb = ttk.Radiobutton(wc_col1, text="Parallel", variable=vc_wiring_var, value="Parallel",
                                       state=tk.DISABLED)
w_wiring_parallel_rb.grid(row=1, column=2, sticky=W)

# -- Column 2: System Config --
wc_col2 = ttk.LabelFrame(wiring_controls, text="System Config")
wc_col2.pack(side="left", fill="y", padx=5)

# Num Drivers
w_numDrivers = gui_setup.gui_items.Item("Num Drivers", 0, 0)
w_numDrivers.item_setup(wc_col2, pad, 5, "no unit", use_btn=False, min_value=1)
w_numDrivers.insert_default_txtfield("1")
w_numDrivers.txtField.bind("<KeyRelease>", _sync_num_drivers)  # Sync handler

# System Wiring
w_wiringTopo = gui_setup.gui_items.Item("Wiring", 2, 0)
w_wiringTopo.item_setup(wc_col2, pad, 18, "Single Driver", use_btn=False, use_cmb=True)
w_wiringTopo.cmb.cmb.bind("<<ComboboxSelected>>", _sync_wiring_topo)  # Sync handler

# -- Column 3: Output & Tools --
wc_col3 = ttk.Frame(wiring_controls)
wc_col3.pack(side="left", fill="y", padx=10)

# Total Re
w_sysImp = gui_setup.gui_items.Item("Total Re", 0, 0)
w_sysImp.item_setup(wc_col3, pad, 8, "Ohm", use_btn=False)
w_sysImp.txtField.configure(state='readonly')

# Button Frame
btn_row_frame = ttk.Frame(wc_col3)
btn_row_frame.grid(row=1, column=0, columnspan=2, pady=5)

# Reset View Button
reset_viz_btn = ttk.Button(btn_row_frame, text="Reset View", command=_on_reset_view_clicked)
reset_viz_btn.pack(side="left", padx=2)

# Legend Button (NEW)
legend_btn = ttk.Button(btn_row_frame, text="Toggle Legend", command=_on_toggle_legend_clicked)
legend_btn.pack(side="left", padx=2)

# --- Canvas ---
wiring_viz = WiringVisualizer(wiring_frame, width=1200, height=600, bg="#2b2b2b")
wiring_viz.pack(side="top", fill="both", expand=True, padx=5, pady=5)
data_manager.register_item("wiring_visualizer", wiring_viz)

# ==========================================
# INPUTS TAB SETUP
# ==========================================
# Organize the "Inputs" Tab with Labelframes
# We'll create two groups
driver_frame = ttk.Labelframe(input_frame, text="Driver Parameters")
driver_frame.grid(column=0, row=0, padx=pad, pady=pad, sticky="nw", ipadx=pad, ipady=pad)

box_frame = ttk.Labelframe(input_frame, text="Box & Port Parameters")
box_frame.grid(column=1, row=0, padx=pad, pady=pad, sticky="nw", ipadx=pad, ipady=pad)

# Add All Widgets to their new 'Labelframe' parents
# Note: The 'col' and 'rw' are now relative to their new frame.

# Driver Frame Widgets
cms = gui_setup.gui_items.Item("Cms", 0, 0)
cms.item_setup(driver_frame, pad, txtfield_size, "m/N", "mm/N", "um/N")
data_manager.register_item("cms", cms)

mms = gui_setup.gui_items.Item("Mms", 0, 1)
mms.item_setup(driver_frame, pad, txtfield_size, "Kg", "g")
data_manager.register_item("mms", mms)

le = gui_setup.gui_items.Item("Le", 0, 2)
le.item_setup(driver_frame, pad, txtfield_size, "H", "mH")
data_manager.register_item("le", le)

re = gui_setup.gui_items.Item("Re", 0, 3)
re.item_setup(driver_frame, pad, txtfield_size, "ohm", use_btn=False)
data_manager.register_item("re", re)

rms = gui_setup.gui_items.Item("Rms", 0, 4)
rms.item_setup(driver_frame, pad, txtfield_size, "Kg/s", "Ns/s")
data_manager.register_item("rms", rms)

bl = gui_setup.gui_items.Item("Bl", 0, 5)
bl.item_setup(driver_frame, pad, txtfield_size, "Tm", "N/A")
data_manager.register_item("bl", bl)

sd = gui_setup.gui_items.Item("Sd", 0, 6)
sd.item_setup(driver_frame, pad, txtfield_size, "m^2", "cm^2", "mm^2", "in^2", "ft^2")
data_manager.register_item("sd", sd)

vg = gui_setup.gui_items.Item("Vg", 0, 7)
vg.item_setup(driver_frame, pad, txtfield_size, "W")
data_manager.register_item("vg", vg)

# Start determining rows after Vg (which is at row 7)
current_row = 8

# --- STEP 1: Define the "Unit" (The Individual Driver) ---

# 1. VC Type Selection
vc_type_label = ttk.Label(driver_frame, text="VC Type:")
vc_type_label.grid(column=0, row=current_row, padx=pad, pady=pad, sticky=E)

# Create a sub-frame to group buttons closer together
vc_type_frame = ttk.Frame(driver_frame)
vc_type_frame.grid(column=1, row=current_row, padx=pad, pady=pad, sticky=W, columnspan=2)

# Use same variable as Wiring Tab
vc_single_rb = ttk.Radiobutton(vc_type_frame, text="Single", variable=vc_type_var, value="Single VC")
vc_single_rb.pack(side="left", padx=(0, 10))  # 10px gap between buttons
vc_dual_rb = ttk.Radiobutton(vc_type_frame, text="Dual", variable=vc_type_var, value="Dual VC")
vc_dual_rb.pack(side="left")

data_manager.register_item("vc_type", vc_type_var)

current_row += 1

# 2. Dual VC Wiring Selection
vc_wiring_label = ttk.Label(driver_frame, text="Dual VC Wiring:")
vc_wiring_label.grid(column=0, row=current_row, padx=pad, pady=pad, sticky=E)

# Create a sub-frame for wiring buttons
vc_wiring_frame = ttk.Frame(driver_frame)
vc_wiring_frame.grid(column=1, row=current_row, padx=pad, pady=pad, sticky=W, columnspan=2)

# Use same variable as Wiring Tab
wiring_series_rb = ttk.Radiobutton(vc_wiring_frame, text="Series", variable=vc_wiring_var, value="Series",
                                   state=tk.DISABLED)
wiring_series_rb.pack(side="left", padx=(0, 10))
wiring_parallel_rb = ttk.Radiobutton(vc_wiring_frame, text="Parallel", variable=vc_wiring_var, value="Parallel",
                                     state=tk.DISABLED)
wiring_parallel_rb.pack(side="left")

data_manager.register_item("vc_wiring", vc_wiring_var)

current_row += 1

# --- STEP 2: Define the "System" (The Group of Drivers) ---

# 3. Number of Drivers
numDrivers = gui_setup.gui_items.Item("Num Drivers", 0, current_row)
numDrivers.item_setup(driver_frame, pad, txtfield_size, "no unit", use_btn=False, min_value=1)
numDrivers.insert_default_txtfield("1")
# Stop the field from stretching to fill the column width
numDrivers.txtField.grid_configure(sticky='w')
numDrivers.txtField.bind("<KeyRelease>", _sync_num_drivers)  # Sync handler
data_manager.register_item("number_of_drivers", numDrivers)

current_row += 1

# 4. System Wiring Topology
wiringTopo = gui_setup.gui_items.Item("System Wiring", 0, current_row)
# Note: This wide dropdown forces the column to be wide, but now the other fields won't stretch to match it
wiringTopo.item_setup(driver_frame, pad, 18, "Single Driver", use_btn=False, use_cmb=True)
data_manager.register_item("wiring_topology", wiringTopo)
wiringTopo.cmb.cmb.bind("<<ComboboxSelected>>", _sync_wiring_topo)  # Sync handler

current_row += 1

# --- STEP 3: The Result ---

# 5. Final Impedance (Read Only)
sysImp = gui_setup.gui_items.Item("Total System Re", 0, current_row)
sysImp.item_setup(driver_frame, pad, txtfield_size, "Ohm", use_btn=False)
sysImp.txtField.configure(state='readonly')
# Stop the field from stretching
sysImp.txtField.grid_configure(sticky='w')
data_manager.register_item("system_re", sysImp)

# Box & Port Frame Widgets
portArea = gui_setup.gui_items.Item("Port Cross Sectional Area", 0, 0)
portArea.item_setup(box_frame, pad, txtfield_size, "in^2", "cm^2", "ft^2", "mm^2", 'm^2')
data_manager.register_item("port_area", portArea)

netVolume = gui_setup.gui_items.Item("Net Volume (Box)", 0, 1)
netVolume.item_setup(box_frame, pad, txtfield_size, "in^3", "L", "cm^3", "ft^3", "mm^3", "m^3")
data_manager.register_item("net_volume", netVolume)

portLength = gui_setup.gui_items.Item("Length of Port", 0, 2)
portLength.item_setup(box_frame, pad, txtfield_size, "in", "cm", "ft", "m", "mm")
data_manager.register_item("port_length", portLength)

endCorrection = gui_setup.gui_items.Item("End Correction", 0, 3)
endCorrection.item_setup(box_frame, pad, txtfield_size, "One Flanged End",
                         "Both Flanged Ends",
                         "Both Free Ends",
                         "3 Common Walls",
                         "2 Common Walls",
                         "1 Common Wall",
                         use_btn=False, use_cmb=True)
data_manager.register_item("end_correction", endCorrection)

numPorts = gui_setup.gui_items.Item("Number of Ports", 0, 4)
numPorts.item_setup(box_frame, pad, txtfield_size, 'no name', use_btn=False)
numPorts.insert_default_txtfield("1")
data_manager.register_item("number_of_ports", numPorts)

portTuning = gui_setup.gui_items.Item("Port Tuning (fb)", 0, 5)
portTuning.item_setup(box_frame, pad, txtfield_size, 'no name', use_btn=False)
portTuning.txtField.configure(state='readonly')  # Make it read-only
data_manager.register_item("port_tuning", portTuning)

# --- Buttons (Bottom - Spanning 2 columns to center under both frames) ---
button_frame = ttk.Frame(input_frame)
button_frame.grid(column=0, row=1, columnspan=2, padx=pad, pady=pad, sticky="")  # Center align

submit = gui_setup.buttons.Btn(0, 0, "Submit")
submit.btn_setup(button_frame, pad)

loadTest = gui_setup.buttons.Btn(1, 0, "Load Test")
loadTest.btn_setup(button_frame, pad)

# Centering Logic
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