# This new computations file will only be in charge of math functionality
import math
import cmath
import matplotlib.pyplot as plt
import numpy as np

#conversion constants needed for port tuning calculations
M2_TO_IN2 = 1550.003
M2_TO_CM2 = 10000.0
M3_TO_IN3 = 61023.7
M3_TO_L = 1000.0
M_TO_IN = 39.3701
M_TO_CM = 100.0

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
    # Calculates port tuning freq (fb) using averaged formula.
    # Extracts SI values from params dict and converts internally.

    # Get SI values from params
    # Sd is already in m^2, Vb is already in m^3
    port_area_m2 = params.get('port_area_m2', 0)  # Use Sd for port area in m^2
    net_volume_m3 = params.get('vb', 0)  # Use Vb for net volume in m^3
    port_length_m = params.get('port_length_m', 0)  # Get Port Length in meters
    number_of_ports = params.get('number_of_ports', 1)
    end_correction_factor = params.get('end_correction', 0.732)  # Get factor

    # --- Internal Conversions ---
    port_area_in2 = (port_area_m2 * M2_TO_IN2) * number_of_ports  # Total area in^2
    port_area_cm2 = (port_area_m2 * M2_TO_CM2)  # Single port area cm^2 for diameter calc
    net_volume_in3 = net_volume_m3 * M3_TO_IN3
    net_volume_l = net_volume_m3 * M3_TO_L
    port_length_in = port_length_m * M_TO_IN
    port_length_cm = port_length_m * M_TO_CM

    # Check for zero values to prevent division errors
    if net_volume_m3 <= 0 or port_area_m2 <= 0 or number_of_ports <= 0:
        return 0  # Or raise an error

    port_diameter_cm = calculate_port_diameter(port_area_cm2)
    if port_diameter_cm <= 0:
        return 0  # Avoid math domain error later

    # JL Audio equation
    jl_denominator = (net_volume_in3 * (port_length_in + end_correction_factor * math.sqrt(port_area_in2 / number_of_ports))) # Use single port area for sqrt part
    if jl_denominator <= 0:
        port_tuning1 = 0
    else:
        port_tuning1 = 0.159 * math.sqrt(port_area_in2 * 1.84E8 / jl_denominator)


    # DIY Audio equation
    diy_denominator = (math.sqrt(net_volume_l) * math.sqrt(port_length_cm + end_correction_factor * port_diameter_cm))
    if diy_denominator == 0:
         port_tuning2 = 0
    else:
        port_tuning2 = (153.501 * port_diameter_cm * math.sqrt(number_of_ports)) / diy_denominator


    # Return average, handle potential NaN if one formula failed
    if math.isnan(port_tuning1) or math.isnan(port_tuning2):
        # Decide how to handle: return 0, return the valid one, or raise error
        if not math.isnan(port_tuning1): return port_tuning1
        if not math.isnan(port_tuning2): return port_tuning2
        return 0 # Fallback if both fail
    else:
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

    num_ports = params.get('number_of_ports', 1)
    single_port_area_m2 = params.get('port_area_m2', 0) / num_ports if num_ports > 0 else 0
    port_vel = calculate_port_velocity(core_results, single_port_area_m2, s, lmap)
    cone_exc = calculate_cone_excursion(core_results, w)
    zin_phase_radians = cmath.phase(core_results['zin'])  # Phase in radians

    # ----
    # Return all results as dictionary of values
    # ----

    return {
        "frequency": frequency,
        "zin": core_results['zin'],
        "zin_phase_rad": zin_phase_radians,
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
        try:
            z_mech = rms + s * mms + (1 / (s * cms) if s else float('inf'))
        except ZeroDivisionError:
            z_mech = float('inf')

    # Calculate electrical impedance
    z_elec = re + s * le
    try:
        zb_inv = (s * ccab if ccab != float('inf') else 0) + \
                 (1 / ral if ral != float('inf') and ral != 0 else 0) + \
                 (1 / (s * lmap) if s and lmap != float('inf') else 0)
        zb = 1 / zb_inv if zb_inv else float('inf')
    except ZeroDivisionError:
        zb = float('inf')

    # Combine impedances
    z_mech_total = z_mech + sd ** 2 * zb if z_mech != float('inf') and zb != float('inf') else float('inf')
    zin = z_elec + (bl ** 2 / z_mech_total) if z_mech_total else z_elec # Avoid division by zero

    # ----
    # Solve for primary unknowns
    # ----

    # i represents the loop mesh current of the amplifier/driver electrical portions of the circuit model
    i = vg / zin if zin else 0

    # pd represents the voltage across loop mesh of the driver acoustical and box portion of the circuit model
    pd = i * (bl * sd * zb) / z_mech_total if z_mech_total else 0

    # u represents the loop mesh current of the driver mechanical portions of the circuit model
    u = (bl * i - sd * pd) / z_mech if z_mech else 0

    return {
        "zin": zin,
        "i": i,
        "u": u,
        "pd": pd,
        "zb": zb
    }


def calculate_port_velocity(core_results, single_port_area_m2, s, lmap):
    # Calculates port velocity from core results

    pd = core_results.get('pd', 0)

    if not s or lmap == float('inf') or single_port_area_m2 <= 0:
        return 0

    # Calculates the impedance of the port
    zlmap = s * lmap

    # Calculates RMS port velocity
    ilmap = pd / zlmap

    if not zlmap: return 0

    # Returns the peak velocity (RMS * sqrt(s))/area
    return (ilmap * math.sqrt(2)) / single_port_area_m2


def calculate_cone_excursion(core_results, w):
    # Calculates cone excursion from core results
    u = core_results.get('u', 0)
    if not w: return 0
    return (math.sqrt(2) * u) / w


def plot_selected_data(canvas, params, start_freq, stop_freq, graph_type, step):
    # Loops through a frequency range, calls the main analysis function,
    # and draws the result on the provided Tkinter canvas.

    print(f"Generating {graph_type} plot from {start_freq} Hz to {stop_freq} Hz with step {step} Hz...")

    # Create the list of frequencies to test
    num_steps = int((stop_freq - start_freq) / step) + 1
    frequencies = np.linspace(start_freq, stop_freq, num=num_steps)
    plot_data = [] # Stores the y-values for the plot
    phase_data_rad = []

    # Loop and extract the correct data based on the graph_type
    for freq in frequencies:
        if freq == 0:  # Avoid calculations exactly at 0 Hz
            results = {"zin": float('inf'), "cone_excursion_mm": 0, "port_velocity_ms": 0, "zin_phase_rad": 0}
        else:
            results = run_full_analysis_at_frequency(freq, params)
        if graph_type == "Impedance":
            plot_data.append(abs(results.get("zin", float('inf'))))
        elif graph_type == "Cone Excursion (mm)":
            plot_data.append(results.get("cone_excursion_mm", 0))
        elif graph_type == "Port Velocity (m/s)":
            plot_data.append(results.get("port_velocity_ms", 0))
        elif graph_type == "Group Delay (ms)":
            phase_data_rad.append(results.get("zin_phase_rad", 0))
        else:
            plot_data.append(abs(results.get("zin", float('inf'))))

    # Setup plot based on type after data gathering
    if graph_type == "Impedance":
        y_label = "Impedance (Ohms)"
        use_log_scale = True
        annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nImp: {y:.1f} Ω"
    elif graph_type == "Cone Excursion (mm)":
        y_label = "Cone Excursion (mm)"
        use_log_scale = False
        annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nExc: {y:.2f} mm"
    elif graph_type == "Port Velocity (m/s)":
        y_label = "Port Velocity (m/s)"
        use_log_scale = False
        annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nVel: {y:.2f} m/s"
    elif graph_type == "Group Delay (ms)":
        y_label = "Group Delay (ms)"
        use_log_scale = False
        annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nGD: {y:.2f} ms"

        # --- Calculate Group Delay ---
        # Need angular frequencies (omega = 2*pi*f)
        angular_frequencies = 2 * np.pi * frequencies

        # Unwrap phase to handle jumps (e.g., from +pi to -pi)
        unwrapped_phase = np.unwrap(phase_data_rad)

        # Numerical derivative of phase w.r.t. angular frequency
        # np.gradient calculates the gradient using central differences
        # Use edge_order=2 for potentially better accuracy at edges
        dphi_domega = np.gradient(unwrapped_phase, angular_frequencies, edge_order=2)
        # Group Delay = -dphi/domega (in seconds)
        group_delay_sec = -dphi_domega

        # Convert to milliseconds
        plot_data = group_delay_sec * 1000
        # ---------------------------

    else: # Fallback case
        graph_type = "Impedance" # Ensure title reflects fallback
        y_label = "Impedance (Ohms)"
        use_log_scale = True
        annotation_formatter = lambda x, y: f"Freq: {x:.1f} Hz\nImp: {y:.1f} Ω"

    # Plotting Section (updates based on selected type)
    fig = canvas.figure
    fig.clear()
    ax = fig.add_subplot(111)

    # Draw the new plot on the axes
    plot_data_cleaned = [d if np.isfinite(d) else np.nan for d in plot_data]
    line, = ax.plot(frequencies, plot_data_cleaned) # Plot the selected data
    ax.set_title(f"System {graph_type}") # Dynamic title
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel(y_label)  # Dynamic Y-label
    ax.grid(True, which="both", ls="--", c='0.7')
    # Apply correct Y-axis scale
    if use_log_scale:
        ax.set_yscale('log')
    else:
        ax.set_yscale('linear')
        ax.set_ylim(bottom=0 if min(plot_data_cleaned, default=0) >= 0 else None)

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