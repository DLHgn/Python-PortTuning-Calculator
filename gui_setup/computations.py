# This new computations file will only be in charge of math functionality
import math
import cmath
import matplotlib.pyplot as plt
import numpy as np


class CursorAnnotation(object):
    # Creates an interactive data cursor that "snaps" to the plot line
    # and displays the (x, y) coordinates.

    def __init__(self, ax, line, formatter):
        self.ax = ax
        self.line = line
        self.formatter = formatter
        self.data_x, self.data_y = line.get_xdata(), line.get_ydata()
        self.canvas = ax.figure.canvas

        # Create the annotation object, but keep it hidden
        self.annotation = ax.annotate(
            text="",
            xy=(0, 0),
            xytext=(15, 15),  # 15-pixel offset from the point
            textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.4", fc="white", alpha=0.7),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0.1"),
            visible=False
        )

        # Connect the mouse-move event to our update function
        self.cid = self.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    def on_mouse_move(self, event):
        # Callback for the mouse-move event
        if not event.inaxes:
            # Mouse is outside the plot area
            if self.annotation.get_visible():
                self.annotation.set_visible(False)
                self.canvas.draw_idle()
            return

        x, y = event.xdata, event.ydata

        # Find the index of the closest data point on the line
        index = np.searchsorted(self.data_x, x)

        # Handle edge cases (cursor left of first point or right of last point)
        if index == 0:
            index = 1
        if index == len(self.data_x):
            index = len(self.data_x) - 1

        # Get the x-coordinates before and after the cursor
        x_left, x_right = self.data_x[index - 1], self.data_x[index]

        # Find which of the two points is closer to the cursor
        if abs(x - x_left) < abs(x - x_right):
            index = index - 1

        # Get the actual (x, y) of the data point
        point_x = self.data_x[index]
        point_y = self.data_y[index]

        # Update the annotation text and position
        self.annotation.set_text(self.formatter(point_x, point_y))
        self.annotation.xy = (point_x, point_y)

        # Make the annotation visible and redraw
        if not self.annotation.get_visible():
            self.annotation.set_visible(True)

        self.canvas.draw_idle()

def calculate_port_diameter(value):
    # Converts port area in cm^2 to diameter in cm for DIY audio equation
    return 2 * math.sqrt(value / math.pi)


def port_tuning_calculation(params):
    # Calculates port tuning freq (fb) using the averaged formula.
    # Uses raw values from the params dictionary.

    # Get all the raw values from the params dict
    number_of_ports = params['number_of_ports']
    port_area_in = params['port_area_in'] * number_of_ports
    port_area_cm = params['port_area_cm']
    net_volume_in = params['net_volume_in']
    net_volume_l = params['net_volume_l']
    port_length_in = params['port_length_in']
    port_length_cm = params['port_length_cm']
    end_correction = params['end_correction']

    port_diameter = calculate_port_diameter(port_area_cm)

    # JL Audio equation
    port_tuning1 = 0.159 * math.sqrt(
        port_area_in * 1.84E8 / (net_volume_in * (port_length_in + end_correction * math.sqrt(port_area_in))))

    # DIY Audio equation
    port_tuning2 = (153.501 * port_diameter * math.sqrt(number_of_ports)) / (
                (math.sqrt(net_volume_l)) * (math.sqrt(port_length_cm + end_correction * port_diameter)))

    return (port_tuning1 + port_tuning2) / 2

def run_full_analysis_at_frequency(frequency, params):
   # This is the main controller function for this file.
   # As the name suggests, it will run all computations for a given frequency
   # Args:
    # frequency (float): The frequency to analyze (given in Hz)
    # params (dict): A dictionary of all driver/enclosure parameters
   # Returns:  Dictionary of all final calculations

    # ----
    # Calculate intermediate values
    # ----

    # w represents angular tuning frequency. Note that this is distinctly different than wb.
    # This value is used during analysis and will vary based on the frequency being calculated.
    w = 2.0 * math.pi * frequency

    # s represents the common abbreviation for j*w where j in an imaginary number.
    s = 1j * w

    # First, calculate fb using your averaged formula
    fb = port_tuning_calculation(params)

    # Now, use fb to calculate the rest of the physics components

    # wb represents angular box tuning frequency as 2*PI*port_tuning
    wb = 2.0 * math.pi * fb

    # ccab represents the acoustic compliance of the enclosure volume
    ccab = calculate_ccab(params['vb'], params['p0'], params['c'])

    # ral represents the acoustic resistance modeling air leak
    ral = calculate_ral(params['ql'], wb, ccab)

    # lmap represents angular frequency as 2*PI*frequency
    lmap = calculate_lmap(wb, ccab)

    # ----
    # Run the core physics simulation
    # ----

    core_results = calculate_pd_i_u(s, params, ccab, ral, lmap, z_mech=None)

    # ----
    # Use core results to find final values
    # ----

    port_vel = calculate_port_velocity(core_results, params['port_area_cm'] / 10000, s, lmap)
    cone_exc = calculate_cone_excursion(core_results, w)

    # ----
    # Return all results as dictionary of values
    # ----

    return {
        "frequency": frequency,
        "zin": core_results['zin'],
        "i": core_results['i'],
        "u": core_results['u'],
        "pd": core_results['pd'],
        "fb": fb,
        "port_velocity_ms": abs(port_vel),
        "cone_excursion_mm": abs(cone_exc) * 1000,
        # Add other results as needed
    }

# ----
# Pure Math Functions
# ---

def calculate_ccab(vb, p0, c):
    # Calculates acoustic compliance of the enclosure
    return vb / (p0 * c ** 2)


def calculate_ral(ql, wb, ccab):
    # Calculates acoustic resistance (losses)
    return ql / (wb * ccab)


def calculate_lmap(wb, ccab):
    # Calculates acoustic mass (inductance) of the port
    return 1 / (wb ** 2 * ccab)


def calculate_pd_i_u(s, params, ccab, ral, lmap, z_mech=None):
    # Core physics simulation
    # Accepts all parameters as arguments.

    # Get values from the params dict
    re = params['re']
    le = params['le']
    rms = params['rms']
    mms = params['mms']
    cms = params['cms']
    bl = params['bl']
    sd = params['sd']
    vg = params['vg']

    # Calculate mechanical impedance
    if z_mech is None:
        z_mech = rms + s * mms + 1 / (s * cms)

    # Calculate electrical impedance
    z_elec = re + s * le
    zb = 1 / (s * ccab + (1 / ral) + (1 / (s * lmap)))

    # Combine impedances
    z_mech_total = z_mech + sd ** 2 * zb
    zin = z_elec + (bl ** 2 / z_mech_total)

    # ----
    # Solve for primary unknowns
    # ----

    # i represents the loop mesh current of the amplifier/driver electrical portions of the circuit model
    i = vg / zin

    # pd represents the voltage across loop mesh of the driver acoustical and box portion of the circuit model
    pd = i * (bl * sd * zb) / z_mech_total

    # u represents the loop mesh current of the driver mechanical portions of the circuit model
    u = (bl * i - sd * pd) / z_mech

    return {
        "zin": zin,
        "i": i,
        "u": u,
        "pd": pd,
        "zb": zb
    }


def calculate_port_velocity(core_results, port_area, s, lmap):
    # Calculates port velocity from core results

    pd = core_results['pd']

    # Calculates the impedance of the port
    zlmap = s * lmap

    # Calculates RMS port velocity
    ilmap = pd / zlmap

    # Returns the peak velocity (RMS * sqrt(s))/area
    return (ilmap * math.sqrt(2)) / port_area


def calculate_cone_excursion(core_results, w):
    # Calculates cone excursion from core results
    u = core_results['u']
    return (math.sqrt(2) * u) / w


def plot_selected_data(canvas, params, start_freq, stop_freq, graph_type, step):
    # Loops through a frequency range, calls the main analysis function,
    # and draws the result on the provided Tkinter canvas.

    print(f"Generating Impedance plot from {start_freq} Hz to {stop_freq} Hz with step {step} Hz...")

    # Create the list of frequencies to test
    num_steps = int((stop_freq - start_freq) / step) + 1
    frequencies = np.linspace(start_freq, stop_freq, num=num_steps)
    plot_data = [] # Stores the y-values for the plot

    # Loop and extract the correct data based on the graph_type
    for freq in frequencies:
        results = run_full_analysis_at_frequency(freq, params)
        if graph_type == "Impedance":
            plot_data.append(abs(results["zin"]))
            y_label = "Impedance (Ohms)"
            use_log_scale = True
            annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nImp: {y:.1f} Ω"
        elif graph_type == "Cone Excursion (mm)":
            plot_data.append(results["cone_excursion_mm"])
            y_label = "Cone Excursion (mm)"
            use_log_scale = False  # Linear scale for excursion
            annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nExc: {y:.2f} mm"
        elif graph_type == "Port Velocity (m/s)":
            plot_data.append(results["port_velocity_ms"])
            y_label = "Port Velocity (m/s)"
            use_log_scale = False  # Linear scale for velocity
            annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nVel: {y:.2f} m/s"
        else:
            # Fallback to Impedance if type is unknown
            plot_data.append(abs(results["zin"]))
            y_label = "Impedance (Ohms)"
            use_log_scale = True
            annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nImp: {y:.1f} Ω"

    # Plotting Section (updates based on selected type)
    fig = canvas.figure
    fig.clear()
    ax = fig.add_subplot(111)

    # Draw the new plot on the axes
    line, = ax.plot(frequencies, plot_data) # Plot the selected data
    ax.set_title(f"System {graph_type}") # Dynamic title
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(y_label)  # Dynamic Y-label
    ax.grid(True, which="both", ls="--", c='0.7')
    # Apply correct Y-axis scale
    if use_log_scale:
        ax.set_yscale('log')
    else:
        ax.set_yscale('linear')
        ax.set_ylim(bottom=0)  # Ensure linear plots start at 0

    # Auto-set x-ticks based on range, or set manually
    ax.set_xticks(np.linspace(start_freq, stop_freq, num=10, dtype=int))
    ax.set_xlim(start_freq, stop_freq)  # Set x-axis limits
    fig.tight_layout()

    # Create the interactive cursor object
    cursor = CursorAnnotation(ax, line, annotation_formatter)
    # Store it on the canvas to prevent it from being garbage-collected
    canvas.cursor_annotation = cursor

    # Redraw the canvas
    canvas.draw()
    print("Plot updated.")