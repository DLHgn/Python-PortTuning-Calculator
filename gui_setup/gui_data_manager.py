import math
import tkinter.messagebox as messagebox
import tkinter as tk
# this import is used for setting test data
from . import test_data
# We import computations only for port tuning calc if needed here,
# but usually Main calls computations directly.
# Keeping it if you use it for the test loader.
from . import computations

_gui_items = {}

# Target base units: m, m^2, m^3, H, Kg, N/A
_conversion_factors = {
    "m": 1.0, "cm": 0.01, "mm": 0.001, "in": 0.0254, "ft": 0.3048,
    "m^2": 1.0, "cm^2": 0.0001, "mm^2": 0.000001, "in^2": 0.00064516, "ft^2": 0.092903,
    "m^3": 1.0, "L": 0.001, "cm^3": 0.000001, "mm^3": 1e-9, "in^3": 1.63871e-5, "ft^3": 0.0283168,
    "H": 1.0, "mH": 0.001,
    "Kg": 1.0, "g": 0.001,
    "m/N": 1.0, "mm/N": 0.001, "um/N": 0.000001,
    "Kg/s": 1.0, "Ns/s": 1.0,
    "Tm": 1.0, "N/A": 1.0, "ohm": 1.0, "V": 1.0, "W": 1.0,
}


def register_item(name, item_object):
    global _gui_items
    if name in _gui_items:
        print(f"Warning: Overwriting GUI item registration for '{name}'")
    _gui_items[name] = item_object


def get_item(name):
    return _gui_items.get(name)


def convert_to_si(item_name, target_si_unit):
    global _gui_items, _conversion_factors
    item_obj = _gui_items.get(item_name)
    if not item_obj:
        raise ValueError(f"GUI item '{item_name}' not registered.")

    widget_type = getattr(item_obj, '_unit_widget_type', None)
    current_unit = None

    if widget_type == 'button':
        current_unit = item_obj.get_btn()
    elif widget_type == 'cmb':
        current_unit = item_obj.get_cmb()
    elif item_name in ["re", "rms", "bl", "vg", "sd"]:
        # Infer for known unitless items or fixed unit items if widget missing
        current_unit = target_si_unit

    if not current_unit:
        # Fallback if unit is implicit
        current_unit = target_si_unit

    value_str = item_obj.get_txtfield()
    try:
        value = float(value_str)
    except ValueError:
        raise ValueError(f"Invalid numeric value for {item_name}")

    factor = _conversion_factors.get(current_unit)
    if factor is None:
        # Try mapped units if specific names differ
        raise ValueError(f"Unknown unit '{current_unit}' for item '{item_name}'.")

    target_factor = _conversion_factors.get(target_si_unit, 1.0)
    converted_value = (value * factor) / target_factor
    return converted_value


# --- Getters for Specific Fields ---

def get_vc_type():
    var_obj = _gui_items.get("vc_type")
    if var_obj and isinstance(var_obj, tk.StringVar):
        return var_obj.get()
    return "Single VC"


def get_vc_wiring():
    var_obj = _gui_items.get("vc_wiring")
    if var_obj and isinstance(var_obj, tk.StringVar):
        return var_obj.get()
    return "Series"


def get_number_of_drivers():
    item_obj = _gui_items.get("number_of_drivers")
    if item_obj:
        val_str = item_obj.get_txtfield()
        if not val_str: return 1
        try:
            num = int(val_str)
            return num if num > 0 else 1
        except ValueError:
            return 1
    return 1


def get_driver_wiring_mode():
    item_obj = _gui_items.get("wiring_topology")
    if item_obj:
        return item_obj.get_cmb()
    return "Single Driver"


def get_start_freq():
    item_obj = _gui_items.get("start_freq")
    return int(float(item_obj.get_txtfield())) if item_obj else 10


def get_stop_freq():
    item_obj = _gui_items.get("stop_freq")
    return int(float(item_obj.get_txtfield())) if item_obj else 120


def get_graph_step():
    item_obj = _gui_items.get("graph_step")
    return float(item_obj.get_txtfield()) if item_obj else 1.0


def get_selected_graph_type():
    item_obj = _gui_items.get("graph_select_combo")
    return item_obj.get() if item_obj else "Impedance"


def get_graph_canvas():
    return _gui_items.get("graph_canvas")


def get_number_of_ports():
    item_obj = _gui_items.get("number_of_ports")
    if item_obj:
        try:
            return int(item_obj.get_txtfield())
        except:
            return 1
    return 1


def get_end_correction():
    item_obj = _gui_items.get("end_correction")
    if not item_obj: return 0.732
    value = item_obj.get_cmb()
    if value == '3 Common Walls':
        return 2.227
    elif value == '2 Common Walls':
        return 1.728
    elif value == '1 Common Wall':
        return 1.23
    elif value == 'One Flanged End':
        return 0.732
    elif value == 'Both Flanged Ends':
        return 0.85
    elif value == 'Both Free Ends':
        return 0.614
    return 0.732


# --- Base Unit Getters ---
def get_re_base(): return convert_to_si("re", "ohm")


def get_le_base(): return convert_to_si("le", "H")


def get_bl_base(): return convert_to_si("bl", "Tm")


# --- Multi-Driver Logic ---

def get_valid_wiring_modes(n_drivers):
    """Generates valid wiring topology strings based on driver count."""
    if n_drivers <= 1:
        return ["Single Driver"]

    modes = ["All Series", "All Parallel"]

    # Calculate Series-Parallel combinations for composite numbers
    # i = number of Series Groups, j = drivers per Parallel Group
    for i in range(2, int(n_drivers ** 0.5) + 1):
        if n_drivers % i == 0:
            j = n_drivers // i
            modes.append(f"Series-Parallel ({i}s {j}p)")
            if i != j:
                modes.append(f"Series-Parallel ({j}s {i}p)")
    return modes


def _parse_wiring_mode(mode_string, n_drivers):
    """Parses wiring string to return (series_groups, parallel_per_group)."""
    if mode_string == "All Series":
        return (n_drivers, 1)  # N groups of 1
    elif mode_string == "All Parallel":
        return (1, n_drivers)  # 1 group of N
    elif "Series-Parallel" in mode_string:
        try:
            # Extract numbers from string like "Series-Parallel (2s 3p)"
            parts = mode_string.split('(')[1].replace(')', '').split()
            s = int(parts[0].replace('s', ''))
            p = int(parts[1].replace('p', ''))
            return (s, p)
        except:
            return (n_drivers, 1)  # Fallback
    return (1, 1)  # Default/Single


def calculate_total_system_re(params=None):
    """Calculates final system DC resistance for display."""
    try:
        if params:
            # If we already have processed params, 're' is already total
            return params.get('re', 0)

        # Otherwise calculate from raw GUI inputs
        re_base = get_re_base()
        vc_type = get_vc_type()
        vc_wiring = get_vc_wiring()
        n_drivers = get_number_of_drivers()
        wiring_mode = get_driver_wiring_mode()

        # 1. Unit Re
        re_unit = re_base
        if vc_type == "Dual VC":
            if vc_wiring == "Series":
                re_unit *= 2
            elif vc_wiring == "Parallel":
                re_unit /= 2

        # 2. Array Re
        s_groups, p_groups = _parse_wiring_mode(wiring_mode, n_drivers)
        re_total = (re_unit / p_groups) * s_groups
        return re_total
    except:
        return 0


def gather_all_inputs():
    """Gathers values, scales for VC and Multi-Driver Array, returns dict."""
    try:
        n_drivers = get_number_of_drivers()
        wiring_mode = get_driver_wiring_mode()

        # --- 1. Unit Parameters (Single Driver) ---
        re_base = get_re_base()
        le_base = get_le_base()
        bl_base = get_bl_base()

        vc_type = get_vc_type()
        vc_wiring = get_vc_wiring()

        re_unit, le_unit, bl_unit = re_base, le_base, bl_base

        if vc_type == "Dual VC":
            if vc_wiring == "Series":
                re_unit = re_base * 2
                le_unit = le_base * 2
                bl_unit = bl_base * 2
            elif vc_wiring == "Parallel":
                re_unit = re_base / 2
                le_unit = le_base / 2
                bl_unit = bl_base

                # --- 2. Array Scaling ---
        s_groups, p_groups = _parse_wiring_mode(wiring_mode, n_drivers)

        # Electrical: Z_total = (Z_unit / P) * S
        re_total = (re_unit / p_groups) * s_groups
        le_total = (le_unit / p_groups) * s_groups

        # Bl: Scales with Series groups only (Bl_total = Bl_unit * S)
        bl_total = bl_unit * s_groups

        # Mechanical: Scales by N
        sd_total = convert_to_si('sd', 'm^2') * n_drivers
        mms_total = convert_to_si('mms', 'Kg') * n_drivers
        rms_total = convert_to_si('rms', 'Kg/s') * n_drivers
        cms_total = convert_to_si('cms', 'm/N') / n_drivers

        params = {
            're': re_total,
            'le': le_total,
            'bl': bl_total,
            'sd': sd_total,
            'cms': cms_total,
            'mms': mms_total,
            'rms': rms_total,
            'vg': convert_to_si('vg', 'V'),
            'ql': 10, 'p0': 1.18, 'c': 343.68,
            'vb': convert_to_si('net_volume', 'm^3'),
            'number_of_ports': get_number_of_ports(),
            'end_correction': get_end_correction(),
            'port_length_m': convert_to_si('port_length', 'm'),
            'port_area_m2': convert_to_si('port_area', 'm^2')
        }
        return params
    except ValueError as e:
        raise
    except Exception as e:
        messagebox.showerror("Error", f"Failed to gather inputs: {e}")
        raise


def set_port_tuning_output(value):
    item_obj = _gui_items.get("port_tuning")
    if item_obj:
        if isinstance(value, (int, float)):
            item_obj.set_output_text(f"{value:.2f} Hz")
        else:
            item_obj.set_output_text(str(value))


def validate_all_inputs():
    valid = True
    required = ["re", "le", "bl", "sd", "cms", "mms", "rms", "vg", "net_volume", "port_area", "port_length"]
    for name in required:
        item = _gui_items.get(name)
        if item and hasattr(item, 'validate_numeric_input'):
            if not item.validate_numeric_input(): valid = False
    return valid


def load_test_values():
    """
    Loads test values into GUI items, handling different widget types safely.
    """
    global _gui_items
    data = test_data.test_values
    print("Loading test values...")

    # 1. Handle Variables (Radio Buttons)
    # Check if keys exist in test data, otherwise use defaults
    vc_type_var = _gui_items.get("vc_type")
    if vc_type_var:
        vc_type_var.set(data.get("vc_type", "Single VC"))

    vc_wiring_var = _gui_items.get("vc_wiring")
    if vc_wiring_var:
        vc_wiring_var.set(data.get("vc_wiring", "Series"))

    # 2. Handle GUI Items (Entry and Comboboxes)
    for key, val in data.items():
        # Remap legacy keys from test_data if necessary
        if key == 'vb':
            item_name = 'net_volume'
        else:
            item_name = key

        # Skip keys we already handled or calculated fields
        if item_name in ['port_tuning', 'vc_type', 'vc_wiring', 'vb_unit',
                         'le_unit', 'bl_unit', 'sd_unit', 'cms_unit',
                         'mms_unit', 'rms_unit', 'port_area_unit', 'port_length_unit']:
            continue

        item = _gui_items.get(item_name)
        if not item:
            continue

        # --- SAFETY CHECK ---
        # If it is a Text Entry Item
        if hasattr(item, 'txtField') and item.txtField is not None:
            # Only write if it's not Read-Only (prevents errors on output fields)
            try:
                if str(item.txtField.cget('state')) == 'normal':
                    item.set_input_text(val)
            except Exception:
                pass

                # If it is a Combobox Item (e.g., End Correction)
        elif hasattr(item, 'set_cmb_text') and hasattr(item, 'cmb') and item.cmb:
            item.set_cmb_text(val)

    # 3. Set Defaults for New Features (if not in test data)
    # Ensure Num Drivers is at least 1
    nd_item = _gui_items.get("number_of_drivers")
    if nd_item and (not nd_item.get_txtfield() or nd_item.get_txtfield() == "0"):
        nd_item.set_input_text("1")

    # 4. Trigger Calculation & Updates
    try:
        # Force validation to clear red borders
        validate_all_inputs()

        # Calculate
        params = gather_all_inputs()
        calculated_fb = computations.port_tuning_calculation(params)
        set_port_tuning_output(calculated_fb)

        # Update System Impedance Display
        total_re = calculate_total_system_re(params)
        sys_imp_item = _gui_items.get("system_re")
        if sys_imp_item:
            sys_imp_item.set_output_text(f"{total_re:.2f} Ohm")

        print(f"Test Data Loaded. Tuning: {calculated_fb:.2f} Hz")
    except Exception as e:
        print(f"Error post-processing test data: {e}")