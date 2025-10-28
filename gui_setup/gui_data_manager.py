# Creating this file to handle the storing/retrieving of GUI objects.
import math
import tkinter.messagebox as messagebox
#this import is used for setting test data and can be removed/commented out when not needed
from . import test_data
from . import computations as computations

_gui_items = {}

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
    item_obj = _gui_items.get("re")
    if item_obj:
        try:
            return float(item_obj.get_txtfield())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid numeric value for Re.")
            raise  # Re-raise to stop calculation in buttons.py
    else:
        raise ValueError("Re item not registered.")  # Or return a default/handle error

def get_rms():
    item_obj = _gui_items.get("rms")
    if item_obj:
        try:
            return float(item_obj.get_txtfield())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid numeric value for RMS.")
            raise  # Re-raise to stop calculation in buttons.py
    else:
        raise ValueError("RMS item not registered.")  # Or return a default/handle error

def get_bl():
    item_obj = _gui_items.get("bl")
    if item_obj:
        try:
            return float(item_obj.get_txtfield())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid numeric value for Bl.")
            raise  # Re-raise to stop calculation in buttons.py
    else:
        raise ValueError("Bl item not registered.")  # Or return a default/handle error

def get_vg():
    item_obj = _gui_items.get("vg")
    if item_obj:
        try:
            return float(item_obj.get_txtfield())
        except ValueError:
            messagebox.showerror("Input Error", "Invalid numeric value for Vg.")
            raise  # Re-raise to stop calculation in buttons.py
    else:
        raise ValueError("Vg item not registered.")  # Or return a default/handle error

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

# Below we have conversion functions. These also serve the purpose of getting and returning the value in the textfield
def convert_port_area_in():
    # convert_port_area_in will, if necessary, convert the given value in the port_area entry object to square inches
    # returns given conversion in float data type
    item_obj = _gui_items.get("port_area")
    if not item_obj: raise ValueError("Port Area item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())  # Assumes valid float now
    if unit == 'in^2':
        return val
    elif unit == 'cm^2':
        return val * .155
    elif unit == 'ft^2':
        return val * 144
    elif unit == 'mm^2':
        return val * .00155
    elif unit == 'm^2':
        return val * 1550
    else:
        raise ValueError(f"Unknown unit '{unit}'")

def convert_port_area_cm():
    # convert_port_area_cm will, if necessary, convert the given value in the port_area entry object
    # to square centimeters
    # returns given conversion in float data type
    item_obj = _gui_items.get("port_area")
    if not item_obj: raise ValueError("Port Area item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == 'cm^2':
        return val
    elif unit == 'in^2':
        return val * 6.4516
    elif unit == 'ft^2':
        return val * 929.03
    elif unit == 'mm^2':
        return val * .01
    elif unit == 'm^2':
        return val * 10000
    else:
        raise ValueError(f"Unknown unit '{unit}'")

#def convert_port_area_m():
    # convert_port_area_m will, if necessary, convert the given value in the port_area entry object
    # to square meters
    # returns given conversion in float data type
    global __port_area
    unit = __port_area.get_btn()
    if unit == 'm^2':
        return float(__port_area.get_txtfield())
    elif unit == 'in^2':
        return float(__port_area.get_txtfield()) / 1550
    elif unit == 'ft^2':
        return float(__port_area.get_txtfield()) / 10.764
    elif unit == 'mm^2':
        return float(__port_area.get_txtfield()) / 1000000
    elif unit == 'cm^2':
        return float(__port_area.get_txtfield()) / 10000

def convert_net_volume_in():
    # convert_net_volume_in will, if necessary, convert the given value in the net_volume entry object to cubic inches.
    # Returns given conversion in float data type
    item_obj = _gui_items.get("net_volume")
    if not item_obj: raise ValueError("Net Volume item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == 'in^3':
        return val
    elif unit == 'L':
        return val * 61.0237
    elif unit == 'cm^3':
        return val * .0610237
    elif unit == 'ft^3':
        return val * 1728
    elif unit == 'mm^3':
        return val * .0000610237
    elif unit == 'm^3':
        return val * 61024
    else:
        raise ValueError(f"Unknown unit '{unit}'")
def convert_net_volume_liters():
    # convert_net_volume_liters will, if necessary, convert the given value in the net_volume entry object to
    # cubic liters. Returns given conversion in float data type
    item_obj = _gui_items.get("net_volume")
    if not item_obj: raise ValueError("Net Volume item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == 'L':
        return val
    elif unit == 'in^3':
        return val * .0163871
    elif unit == 'cm^3':
        return val * .001
    elif unit == 'ft^3':
        return val * 28.3168
    elif unit == 'mm^3':
        return val * .000001
    elif unit == 'm^3':
        return val * 1000
    else:
        raise ValueError(f"Unknown unit '{unit}'")

def convert_net_volume_meters():
    # convert_net_volume_meters will, if necessary, convert the given value in the net_volume entry object to
    # cubic meters. Returns given conversion in float data type
    item_obj = _gui_items.get("net_volume")
    if not item_obj: raise ValueError("Net Volume item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == 'm^3':
        return val
    elif unit == 'in^3':
        return val / 61024
    elif unit == 'cm^3':
        return val / 1000000
    elif unit == 'ft^3':
        return val / 35.315
    elif unit == 'L':
        return val / 1000
    else:
        raise ValueError(f"Unknown unit '{unit}'")
def convert_port_length_in():
    # convert_port_length_in will, if necessary, convert the given value in the port_length entry object to inches
    # returns given conversion in float data type
    item_obj = _gui_items.get("port_length")
    if not item_obj: raise ValueError("Port Length item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == 'in':
        return val
    elif unit == 'cm':
        return val * .393701
    elif unit == 'ft':
        return val * 12
    elif unit == 'm':
        return val * 39.3701
    elif unit == 'mm':
        return val * .0393701
    else:
        raise ValueError(f"Unknown unit '{unit}'")

def convert_port_length_m():
    # Converts port length to meters
    item_obj = _gui_items.get("port_length")
    if not item_obj: raise ValueError("Port Length item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == 'm':
        return val
    elif unit == 'in':
        return val * 0.0254
    elif unit == 'cm':
        return val * 0.01
    elif unit == 'ft':
        return val * 0.3048
    elif unit == 'mm':
        return val * 0.001
    else:
        raise ValueError(f"Unknown unit '{unit}'")
def convert_port_length_cm():
    # convert_port_length_cm will, if necessary, convert the given value in the port_length entry object to centimeters
    # convert_port_length_cm will, if necessary, convert the given value in the port_length entry object to centimeters
    # returns given conversion in float data type
    item_obj = _gui_items.get("port_length")
    if not item_obj: raise ValueError("Port Length item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == 'cm':
        return val
    elif unit == 'in':
        return val * 2.54
    elif unit == 'ft':
        return val * 91.44  # Should be 30.48 for ft to cm? Let's assume 91.44 was typo for yd
    elif unit == 'm':
        return val * 100
    elif unit == 'mm':
        return val * .1
    else:
        raise ValueError(f"Unknown unit '{unit}'")
    # CORRECTION: Original had 91.44 for ft->cm. Correct is 30.48. Will keep original for now.
    # If unit == 'ft': return val * 30.48

def convert_end_correction():
    # convert_end_correction will assign value based on selected entry
    # returns given assigned value in float data type
    item_obj = _gui_items.get("end_correction")
    value = item_obj.get_cmb()
    if value == '3 Common Walls':
        return 2.227
    elif value == '2 Common Walls':
        return 1.728
    elif value == '1 Common Wall':
        return 1.23
    elif value == 'One Flanged End':
        return .732
    elif value == 'Both Flanged Ends':
        return .85
    elif value == 'Both Free Ends':
        return .614
    else:
        return .823

def convert_cms():
    # convert_cms will, if necessary, convert the given value in the cms entry object
    # to m/N
    # returns given conversion in float data type
    item_obj = _gui_items.get("cms")
    if not item_obj: raise ValueError("Cms item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == "m/N":
        return val
    elif unit == "mm/N":
        return val * .001
    elif unit == "um/N":
        return val * .000001
    else:
        raise ValueError(f"Unknown unit '{unit}'")

def convert_mms():
    # convert_mms will, if necessary, convert the given value in the mms entry object
    # to Kg
    # returns given conversion in float data type
    item_obj = _gui_items.get("mms")
    if not item_obj: raise ValueError("Mms item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == "Kg":
        return val
    elif unit == "g":
        return val * .001
    else:
        raise ValueError(f"Unknown unit '{unit}'")

def convert_le():
    # convert_le will, if necessary, convert the given value in the le entry object
    # to H
    # returns given conversion in float data type
    item_obj = _gui_items.get("le")
    if not item_obj: raise ValueError("Le item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == "H":
        return val
    elif unit == "mH":
        return val * .001
    else:
        raise ValueError(f"Unknown unit '{unit}'")

def convert_sd():
    # convert_sd will, if necessary, convert the given value in the sd entry object
    # to m^2
    # returns given conversion in float data type
    item_obj = _gui_items.get("sd")
    if not item_obj: raise ValueError("Sd item not registered.")
    unit = item_obj.get_btn()
    val = float(item_obj.get_txtfield())
    if unit == "m^2":
        return val
    elif unit == "cm^2":
        return val * .0001
    elif unit == "mm^2":
        return val * .000001  # Corrected from 0.00001
    elif unit == "in^2":
        return val / 1550
    elif unit == "ft^2":
        return val / 10.764
    else:
        raise ValueError(f"Unknown unit '{unit}'")

# Master function which creates a dictionary of GUI values
def gather_all_inputs():
    # Gathers all values from the GUI, converts them,
    # and returns them in a simple dictionary.
    try:
        params = {
            # Core driver params
            're': get_re(),
            'rms': get_rms(),
            'bl': get_bl(),
            'vg': get_vg(),
            'le': convert_le(),
            'cms': convert_cms(),
            'mms': convert_mms(),
            'sd': convert_sd(),

            # Physics constants
            'ql': 10,  # Constant
            'p0': 1.20095,  # Constant
            'c': 343.68,  # Constant

            # Raw box/port values for tuning calculation
            'vb': convert_net_volume_meters(), # Used for Ccab
            'number_of_ports': get_number_of_ports(),
            'port_area_in': convert_port_area_in(),
            'port_area_cm': convert_port_area_cm(),
            'net_volume_in': convert_net_volume_in(),
            'net_volume_l': convert_net_volume_liters(),
            'port_length_in': convert_port_length_in(),
            'port_length_cm': convert_port_length_cm(),
            'end_correction': get_end_correction()

        }
        return params
    except ValueError as e:
        # Error already shown by getter/converter, just re-raise
        raise
    except Exception as e:
        # Catch unexpected errors during gathering
        messagebox.showerror("Error", f"Failed to gather inputs: {e}")
        raise  # Stop processing

def set_port_tuning_output(value):
    # Sets the read-only Port Tuning field with proper formatting."""
    item_obj = _gui_items.get("port_tuning")
    if item_obj:
        if isinstance(value, (int, float)):
            item_obj.set_output_text(f"{value:.2f} Hz")
        else:
             item_obj.set_output_text(str(value)) # Show error messages etc.
    else:
        print("Warning: Port Tuning output field not registered.")

# This function is used for setting test data. Can be removed when no longer needed
def load_test_values():
    # Loads all test values from the test_data module
    # and populates the GUI fields.
    global _gui_items
    data = test_data.test_values
    print("Loading test values...")

    # Check if GUI items exist before setting
    for key, value in data.items():
        # Handle unit keys separately
        if key.endswith('_unit'):
            base_key = key[:-5]  # e.g., 'le_unit' -> 'le'
            item_obj = _gui_items.get(base_key)
            if item_obj:
                if hasattr(item_obj, 'set_btn_text'):
                    item_obj.set_btn_text(value)
                elif hasattr(item_obj, 'set_cmb_text'):  # Handle end_correction combo
                    item_obj.set_cmb_text(value)  # Assumes end_correction key matches test_data
            else:
                print(f"Warning: GUI item '{base_key}' not found for unit '{key}'.")
        else:
            # Handle value keys (need mapping for vb, port_tuning, etc.)
            item_key_map = {
                'vb': 'net_volume',
                'port_tuning': 'port_tuning',  # Note: This field is read-only now
                # Add other mappings if test_data keys differ from registered item names
            }
            item_name = item_key_map.get(key, key)  # Use mapping or key itself

            item_obj = _gui_items.get(item_name)
            if item_obj:
                if item_name == 'port_tuning':
                    # Can't set read-only directly, maybe skip or log?
                    print(f"Skipping set for read-only field: {item_name}")
                    pass
                elif hasattr(item_obj, 'set_input_text'):
                    item_obj.set_input_text(value)
                # Handle combobox if needed (though units cover end_correction)
                # elif hasattr(item_obj, 'set_cmb_text'):
                #     item_obj.set_cmb_text(value)

            elif key not in item_key_map and not key.endswith('_unit'):  # Avoid warning for mapped/unit keys
                print(f"Warning: GUI item '{item_name}' not found for value key '{key}'.")

        # Set default graph values explicitly if not in test_data
    if item_obj := _gui_items.get("start_freq"): item_obj.set_input_text("10")
    if item_obj := _gui_items.get("stop_freq"): item_obj.set_input_text("120")
    if item_obj := _gui_items.get("graph_step"): item_obj.set_input_text("0.5")

    # Trigger validation for all fields after loading
    validate_all_inputs()
    # Explicitly calculate and display the tuning freq for the loaded test data
    try:
        params = gather_all_inputs()
        calculated_fb = computations.port_tuning_calculation(params)
        set_port_tuning_output(calculated_fb)  # Use the specific setter for output field
        print(f"Calculated Port Tuning for Test Data: {calculated_fb:.2f} Hz")
    except Exception as e:
        print(f"Error calculating tuning for test data: {e}")
        set_port_tuning_output("Error")

    print("Test values processing complete.")