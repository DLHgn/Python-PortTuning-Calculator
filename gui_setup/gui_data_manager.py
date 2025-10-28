# Creating this file to handle the storing/retrieving of GUI objects.
import math
import tkinter.messagebox as messagebox
#this import is used for setting test data and can be removed/commented out when not needed
from . import test_data
from . import computations as computations

_gui_items = {}

# Target base units: m, m^2, m^3, H, Kg, N/A (for factors like Bl, Rms, Re)
_conversion_factors = {
    # Length (target: m)
    "m": 1.0,
    "cm": 0.01,
    "mm": 0.001,
    "in": 0.0254,
    "ft": 0.3048,
    # Area (target: m^2)
    "m^2": 1.0,
    "cm^2": 0.0001,
    "mm^2": 0.000001,
    "in^2": 0.00064516, # 1 / 1550.003
    "ft^2": 0.092903,   # 1 / 10.7639
    # Volume (target: m^3)
    "m^3": 1.0,
    "L": 0.001,
    "cm^3": 0.000001,
    "mm^3": 1e-9,
    "in^3": 1.63871e-5, # 1 / 61023.7
    "ft^3": 0.0283168,  # 1 / 35.3147
    # Inductance (target: H)
    "H": 1.0,
    "mH": 0.001,
    # Mass (target: Kg)
    "Kg": 1.0,
    "g": 0.001,
    # Compliance (target: m/N)
    "m/N": 1.0,
    "mm/N": 0.001,
    "um/N": 0.000001,
    # Resistance/Force/Impedance (target: N/A - factor is 1.0)
    "Kg/s": 1.0,
    "Ns/s": 1.0, # Assuming Ns/m or Rayls? Standard is Kg/s. Let's keep 1.0
    "Tm": 1.0,
    "N/A": 1.0,
    "ohm": 1.0,
    "V": 1.0, # Keeping Vg as voltage for now
    "W": 1.0, # If Vg is treated as power, factor is still 1
}

def convert_to_si(item_name, target_si_unit):
    #Converts the value of a registered GUI item to the specified SI base unit.

    # Args:
    #    item_name (str): The registered name of the GUI item (e.g., "port_length").
    #    target_si_unit (str): The target SI unit ('m', 'm^2', 'm^3', 'H', 'Kg', 'm/N').

    # Returns:
    #    float: The value converted to the target SI unit.

    #Raises:
    #    ValueError: If item not found, unit unknown, or value invalid.

    global _gui_items
    global _conversion_factors

    item_obj = _gui_items.get(item_name)
    if not item_obj:
        raise ValueError(f"GUI item '{item_name}' not registered.")

    widget_type = getattr(item_obj, '_unit_widget_type', None)
    current_unit = None

    if widget_type == 'button':
        current_unit = item_obj.get_btn()
    elif widget_type == 'cmb':
        current_unit = item_obj.get_cmb()
    elif item_name in ["re", "rms", "bl", "vg"]:  # Infer for known unitless items
        current_unit = target_si_unit

    # Proceed only if current_unit was determined
    if not current_unit:  # Handles None or ""
        # If still no unit, raise the specific error
        raise ValueError(f"Unit for item '{item_name}' is missing or empty. Check item setup/widget type.")

    value_str = item_obj.get_txtfield()
    try:
        value = float(value_str)
    except ValueError:
        messagebox.showerror("Input Error", f"Invalid numeric value for {item_obj.text}.")
        raise ValueError(f"Invalid numeric value for {item_name}")

    # If no unit widget returned a unit (None or ""),
    # AND the item name corresponds to parameters that often don't have explicit units,
    # assume the current unit IS the target SI unit (implies factor=1.0)
    if not current_unit:  # Checks for None or empty string
        if item_name in ["re", "rms", "bl", "vg"]:  # Add other unitless items if needed
            current_unit = target_si_unit  # e.g., target_si_unit is 'ohm' for 're'

    # Special case: Combo box units need mapping if display differs from factor key
    unit_map = {
        # e.g., if combo displayed "Inches" but factor key is "in"
    }
    current_unit = unit_map.get(current_unit, current_unit) # Use mapped key or original

    if not current_unit:
        raise ValueError(f"Unit for item '{item_name}' is missing or empty. Check get_current_unit() or widget setup.")

    factor = _conversion_factors.get(current_unit)

    if factor is None:
        raise ValueError(f"Unknown unit '{current_unit}' for item '{item_name}'. Check _conversion_factors dict.")

    target_factor = _conversion_factors.get(target_si_unit, 1.0)
    converted_value = (value * factor) / target_factor

    return converted_value

def register_item(name, item_object):
    # Registers a GUI Item object in the central dictionary
    global _gui_items
    if name in _gui_items:
        print(f"Warning: Overwriting GUI item registration for '{name}'")
    _gui_items[name] = item_object
    # Special case: Store graph canvas reference separately if needed elsewhere quickly
    if name == 'graph_canvas':
        global __graph_canvas # Keep this one if direct access is preferred
        __graph_canvas = item_object

def validate_all_inputs():
    # Checks the 'is_valid' status of all required numeric Item objects
    global _gui_items
    invalid_fields = []
    all_valid = True

    # Define which items need numeric validation by their registered name
    required_numeric_items = [
        "re", "le", "bl", "sd", "cms", "mms", "rms", "vg",
        "net_volume", "port_area", "port_length", "number_of_ports",
        "start_freq", "stop_freq", "graph_step"
    ]

    for item_name in required_numeric_items:
        item_obj = _gui_items.get(item_name) # Use .get() for safer access
        if item_obj and hasattr(item_obj, 'txtField'): # Check if it's an Item with an Entry
            # Re-run validation in case it wasn't triggered by an event
            if not item_obj.validate_numeric_input():
                all_valid = False
                invalid_fields.append(item_obj.text) # Use item's label text for message
        elif item_name not in _gui_items:
             print(f"Warning: GUI Item object for '{item_name}' not registered.")
             all_valid = False # Treat missing required items as invalid state
             invalid_fields.append(f"{item_name} (Missing)")


    if not all_valid:
        error_message = "Invalid or missing input in the following fields:\n\n"
        error_message += "\n".join(f"- {name}" for name in invalid_fields)
        messagebox.showerror("Input Error", error_message)

    return all_valid

# Below is our getters
def get_re():
    return convert_to_si("re", "ohm") # Target unit doesn't really matter (factor=1)

def get_rms():
    return convert_to_si("rms", "Kg/s") # Target unit doesn't really matter

def get_bl():
    return convert_to_si("bl", "Tm") # Target unit doesn't really matter

def get_vg():
    # Keep using 'V' internally based on previous decision, although labeled 'W'
    return convert_to_si("vg", "V")  # Target unit doesn't really matter

def get_graph_step():
    item_obj = _gui_items.get("graph_step")
    if item_obj:
        try:
            step = float(item_obj.get_txtfield())
            return step if step > 0 else 1.0
        except ValueError:
            return 1.0  # Default if invalid
    return 1.0  # Default if object doesn't exist

def get_port_tuning_hz():
    # This is a placeholder.
    # The port_tuning_calculation itself should be
    # moved here, but for now, we just read the value.
    item_obj = _gui_items.get("port_tuning")
    if item_obj:
        try:
            return float(item_obj.get_txtfield())
        except ValueError:
            return 25.1082 # Default test value
    return 25.1082 # Default test value

def get_end_correction():
    item_obj = _gui_items.get("end_correction")
    if not item_obj: raise ValueError("End Correction item not registered.")
    value = item_obj.get_cmb()
    # (Rest of the end correction logic remains the same)
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
    else:
        return 0.823  # Default or handle error

def get_number_of_ports():
    item_obj = _gui_items.get("number_of_ports")
    if item_obj:
        val_str = item_obj.get_txtfield()
        if not val_str: return 1  # Default if empty
        try:
            num = int(val_str)
            return num if num > 0 else 1  # Ensure positive integer
        except ValueError:
            return 1  # Default if invalid
    return 1  # Default if object doesn't exist

def get_graph_canvas():
    # Returns the main Matplotlib canvas object
    return _gui_items.get("graph_canvas")

def get_start_freq():
    item_obj = _gui_items.get("start_freq")
    if item_obj:
        try:
            freq = int(float(item_obj.get_txtfield()))
            return freq if freq >= 1 else 1  # Enforce minimum >= 1
        except ValueError:
            return 10  # Default
    return 10  # Default

def get_stop_freq():
    item_obj = _gui_items.get("stop_freq")
    if item_obj:
        try:
            freq = int(float(item_obj.get_txtfield()))
            # Add check against start freq if desired
            return freq if freq > get_start_freq() else get_start_freq() + 1
        except ValueError:
            return 120  # Default
    return 120  # Default

def get_selected_graph_type():
    item_obj = _gui_items.get("graph_select_combo")
    if item_obj:
        # Assuming the combobox object itself was registered
        return item_obj.get()  # ttk.Combobox has a get() method
    return "Impedance"  # Default

# Master function which creates a dictionary of GUI values
def gather_all_inputs():
    # Gathers all values, converts to SI using the general function, returns dict.
    try:
        params = {
            # Core driver params (converted to SI)
            're': convert_to_si('re', 'ohm'),             # N/A -> ohm (factor 1)
            'le': convert_to_si('le', 'H'),               # H or mH -> H
            'bl': convert_to_si('bl', 'Tm'),              # N/A -> Tm (factor 1)
            'sd': convert_to_si('sd', 'm^2'),             # Area units -> m^2
            'cms': convert_to_si('cms', 'm/N'),           # Compl units -> m/N
            'mms': convert_to_si('mms', 'Kg'),            # Mass units -> Kg
            'rms': convert_to_si('rms', 'Kg/s'),          # N/A -> Kg/s (factor 1)
            'vg': convert_to_si('vg', 'V'),               # N/A -> V (factor 1) for calculation

            # Physics constants (remain the same)
            'ql': 10,
            'p0': 1.18, # Corrected density
            'c': 343.68,

            # Box/port params (converted to SI where needed by computations.py)
            'vb': convert_to_si('net_volume', 'm^3'),     # Volume units -> m^3
            'number_of_ports': get_number_of_ports(),     # Integer (no conversion)
            'end_correction': get_end_correction(),       # Factor (no conversion)
            'port_area_m2': convert_to_si('port_area', 'm^2'),
            'port_length_m': convert_to_si('port_length', 'm')
        }
        return params
    except ValueError as e:
        # Error already shown by convert_to_si, just re-raise
        raise
    except Exception as e:
        messagebox.showerror("Error", f"Failed to gather inputs: {e}")
        raise

def set_port_tuning_output(value):
    # Sets the read-only Port Tuning field with proper formatting."""
    item_obj = _gui_items.get("port_tuning")
    if item_obj:
        if isinstance(value, (int, float)):
            item_obj.set_output_text(f"{value:.2f} Hz")
        else:
             item_obj.set_output_text(str(value)) # Show error messages etc.

# This function is used for setting test data. Can be removed when no longer needed
def load_test_values():
    # Loads all test values from the test_data module
    # and populates the GUI fields.
    global _gui_items, computations
    data = test_data.test_values
    print("Loading test values...")

    for key, value in data.items():
        if key.endswith('_unit'):
            # --- Handling units (includes setting combobox text) ---
            base_key = key[:-5]
            item_key_map_unit = {'vb': 'net_volume'}
            item_name_unit = item_key_map_unit.get(base_key, base_key)
            item_obj = _gui_items.get(item_name_unit)
            if item_obj:
                if hasattr(item_obj, 'set_btn_text') and getattr(item_obj, '_unit_widget_type', None) == 'button':
                    item_obj.set_btn_text(value)
                # Check specifically for the end_correction combobox based on the base key
                elif base_key == 'end_correction' and hasattr(item_obj, 'set_cmb_text'):
                     item_obj.set_cmb_text(value)
                # Add elif for other potential future comboboxes if needed

        else:
            # --- Handling values (only set text field if it exists) ---
            item_key_map = {
                'vb': 'net_volume',
                'port_tuning': 'port_tuning',
            }
            item_name = item_key_map.get(key, key)
            item_obj = _gui_items.get(item_name)
            if item_obj:
                if item_name == 'port_tuning':
                    pass # Skip read-only field
                # --- ADD THIS CHECK ---
                elif hasattr(item_obj, 'txtField') and item_obj.txtField is not None and hasattr(item_obj, 'set_input_text'):
                # ----------------------
                    item_obj.set_input_text(value) # Only call if txtField exists
                # No need to handle combobox text here, it's done via the _unit key

    # ... (setting defaults, validation, tuning calculation remains the same) ...
    if item_obj := _gui_items.get("start_freq"): item_obj.set_input_text("10")
    if item_obj := _gui_items.get("stop_freq"): item_obj.set_input_text("120")
    if item_obj := _gui_items.get("graph_step"): item_obj.set_input_text("0.5")
    validate_all_inputs()
    try:
        params = gather_all_inputs()
        calculated_fb = computations.port_tuning_calculation(params)
        set_port_tuning_output(calculated_fb)
        print(f"Calculated Port Tuning for Test Data: {calculated_fb:.2f} Hz")
    except Exception as e:
        set_port_tuning_output("Error")
    print("Test values processing complete.")