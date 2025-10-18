# Creating this file to handle the storing/retrieving of GUI objects.
import math

#this import is used for setting test data and can be removed/commented out when not needed
from . import test_data

# These global variables are meant to store the gui_items objects for use in the calculations. These are to only be used
# by this module
__port_area = None
__port_length = None
__net_volume = None
__end_correction = None
__number_of_ports = None
__port_tuning = None
__cms = None
__mms = None
__le = None
__re = None
__rms = None
__bl = None
__sd = None
__vg = None
__frequency = None

# Below are set functions that stores the given gui_items.Item object into the global variable. This allows for further
# manipulation and value storage. Included with these are corresponding get functions if there is no conversion
# function for the value
def set_port_area(value):
    #set_port_area stores the given gui_items.Item object into the port_area global variable
    #@param value is a gui_items.Item object
    global __port_area
    __port_area = value

def set_port_length(value):
    # set_port_length stores the given gui_items.Item object into the port_length global variable
    # @param value is a gui_items.Item object
    global __port_length
    __port_length = value

def set_net_volume(value):
    # set_net_volume stores the given gui_items.Item object into the net_volume global variable
    # @param value is a gui_items.Item object
    global __net_volume
    __net_volume = value

def set_end_correction(value):
    # set_end_correction stores the given gui_items.Item object into the end_correction global variable
    # @param value is a gui_items.Item object
    global __end_correction
    __end_correction = value

def set_number_of_ports(value):
    # set_number_of_ports stores the given gui_items.Item object into the number_of_ports global variable
    # @param value is a gui_items.Item object
    global __number_of_ports
    __number_of_ports = value

def set_cms(value):
    # set_cms stores the given gui_items.Item object into the cms global variable
    # @param value is a gui_items.Item object\
    # This variable represents the compliance of the driver
    global __cms
    __cms = value

def set_mms(value):
    # set_mms stores the given gui_items.Item object into the mms global variable
    # @param value is a gui_items.Item object
    # This variable represents the total mechanical mass (including air load) of the system
    global __mms
    __mms = value

def set_le(value):
    # set_le stores the given gui_items.Item object into the le global variable
    # @param value is a gui_items.Item object
    # This variable represents the inductance of all voice coils in the system
    global __le
    __le = value

def set_re(value):
    # set_re stores the given gui_items.Item object into the re global variable
    # @param value is a gui_items.Item object
    # This variable represents the DC resistance of all voice coils in the system
    global __re
    __re = value

def get_re():
    # This function is necessary to get the __re value since there isn't a conversion function that does it
    return float(__re.get_txtfield())

def set_rms(value):
    # set_rms stores the given gui_items.Item object into the rms global variable
    # @param value is a gui_items.Item object
    # This variable represents the mechanical dampening of the system
    global __rms
    __rms = value

def get_rms():
    # This function is necessary to get the __rms value since there isn't a conversion that function does it
    return float(__rms.get_txtfield())

def set_bl(value):
    # set_bl stores the given gui_items.Item object into the bl global variable
    # @param value is a gui_items.Item object
    # This variable represents total motor force of the system
    global __bl
    __bl = value

def get_bl():
    # This function is necessary to get the __bl value since there isn't a conversion that function does it
    return float(__bl.get_txtfield())

def set_sd(value):
    # set_sd stores the given gui_items.Item object into the sd global variable
    # @param value is a gui_items.Item object
    #This variable represents total cone area of the system
    global __sd
    __sd = value

def set_vg(value):
    # set_vg stores the given gui_items.Item object into the vg global variable
    # @param value is a gui_items.Item object
    # This variable represents the amplifier input voltage
    global __vg
    __vg = value

def get_vg():
    # This function is necessary to get the __vg value since there isn't a conversion that function does it
    return float(__vg.get_txtfield())

def set_p0():
    # For now this function won't be used since p0 is set to a constant 1.20095 kg/m^2 but can be expanded later to
    # allow for custom input by the user with the default being set to 1.20095. May want to allow for conversion as well
    # This variable represents air density
    global __p0
    __p0 = 1.18

def set_c(value):
    # For now this function won't be used since c is set to a constant 343.68 m/s but can be expanded later to allow
    # for custom input by the user with the default being set to 343.68. May want to allow for conversion as well.
    # This variable represents the speed of sound
    global __c
    __c = value

def set_ql(value):
    # For now this function won't be used since __ql is set to a constant 10 but can be expanded later to allow
    # for custom input by the user with the default being set to 10.
    # This variable represents Leak value of the system
    global __ql
    __ql = value

def set_port_tuning(value):
    # set_port_tuning stores the given gui_items.Item object into the port_tuning global variable
    # @param value is a gui_items.Item object
    global __port_tuning
    __port_tuning = value

def set_port_tuning_entry():
    # set_port_tuning_entry sets the port_tuning entry object to the output of port_tuning_calculation() using the
    # function Item.set_txtfield()
    global __port_tuning
    __port_tuning.set_txtfield(port_tuning_calculation())

def set_frequency(frequency):
    # This function takes the frequency currently being calculated on and setting it the global variable __frequency
    # to be used by the below functions
    global __frequency
    __frequency = frequency

# Below we have conversion functions. These also serve the purpose of getting and returning the value in the textfield
def convert_port_area_in():
    # convert_port_area_in will, if necessary, convert the given value in the port_area entry object to square inches
    # returns given conversion in float data type
    global __port_area
    unit = __port_area.get_btn()
    if unit == 'in^2':
        return float(__port_area.get_txtfield())
    elif unit == 'cm^2':
        return float(__port_area.get_txtfield()) * .155
    elif unit == 'ft^2':
        return float(__port_area.get_txtfield()) * 144
    elif unit == 'mm^2':
        return float(__port_area.get_txtfield()) * .00155
    elif unit == 'm^2':
        return float(__port_area.get_txtfield()) * 1550

def convert_port_area_cm():
    # convert_port_area_cm will, if necessary, convert the given value in the port_area entry object
    # to square centimeters
    # returns given conversion in float data type
    global __port_area
    unit = __port_area.get_btn()
    if unit == 'cm^2':
        return float(__port_area.get_txtfield())
    elif unit == 'in^2':
        return float(__port_area.get_txtfield()) * 6.4516
    elif unit == 'ft^2':
        return float(__port_area.get_txtfield()) * 929.03
    elif unit == 'mm^2':
        return float(__port_area.get_txtfield()) * .01
    elif unit == 'm^2':
        return float(__port_area.get_txtfield()) * 10000

def convert_port_area_m():
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
    global __net_volume
    unit = __net_volume.get_btn()
    if unit == 'in^3':
        return float(__net_volume.get_txtfield())
    elif unit == 'L':
        return float(__net_volume.get_txtfield()) * 61.0237
    elif unit == 'cm^3':
        return float(__net_volume.get_txtfield()) * .0610237
    elif unit == 'ft^3':
        return float(__net_volume.get_txtfield()) * 1728
    elif unit == 'mm^3':
        return float(__net_volume.get_txtfield()) * .0000610237
    elif unit == 'm^3':
        return float(__net_volume.get_txtfield()) * 61024

def convert_net_volume_liters():
    # convert_net_volume_liters will, if necessary, convert the given value in the net_volume entry object to
    # cubic liters. Returns given conversion in float data type
    global __net_volume
    unit = __net_volume.get_btn()
    if unit == 'L':
        return float(__net_volume.get_txtfield())
    elif unit == 'in^3':
        return float(__net_volume.get_txtfield()) * .0163871
    elif unit == 'cm^3':
        return float(__net_volume.get_txtfield()) * .001
    elif unit == 'ft^3':
        return float(__net_volume.get_txtfield()) * 28.3168
    elif unit == 'mm^3':
        return float(__net_volume.get_txtfield()) * .000001
    elif unit == 'm^3':
        return float(__net_volume.get_txtfield()) * 1000

def convert_net_volume_meters():
    # convert_net_volume_meters will, if necessary, convert the given value in the net_volume entry object to
    # cubic meters. Returns given conversion in float data type
    global __net_volume
    unit = __net_volume.get_btn()
    if unit == 'm^3':
        return float(__net_volume.get_txtfield())
    elif unit == 'in^3':
        return float(__net_volume.get_txtfield()) / 61024
    elif unit == 'cm^3':
        return float(__net_volume.get_txtfield()) / 1000000
    elif unit == 'ft^3':
        return float(__net_volume.get_txtfield()) / 35.315
    elif unit == 'L':
        return float(__net_volume.get_txtfield()) / 1000

def convert_port_length_in():
    # convert_port_length_in will, if necessary, convert the given value in the port_length entry object to inches
    # returns given conversion in float data type
    global __port_length
    unit = __port_length.get_btn()
    if unit == 'in':
        return float(__port_length.get_txtfield())
    elif unit == 'cm':
        return float(__port_length.get_txtfield()) * .393701
    elif unit == 'ft':
        return float(__port_length.get_txtfield()) * 12
    elif unit == 'm':
        return float(__port_length.get_txtfield()) * 39.3701
    elif unit == 'mm':
        return float(__port_length.get_txtfield()) * .0393701

def convert_port_length_cm():
    # convert_port_length_cm will, if necessary, convert the given value in the port_length entry object to centimeters
    # returns given conversion in float data type
    global __port_length
    unit = __port_length.get_btn()
    if unit == 'cm':
        return float(__port_length.get_txtfield())
    elif unit == 'in':
        return float(__port_length.get_txtfield()) * 2.54
    elif unit == 'ft':
        return float(__port_length.get_txtfield()) * 91.44
    elif unit == 'm':
        return float(__port_length.get_txtfield()) * 100
    elif unit == 'mm':
        return float(__port_length.get_txtfield()) * .1

def convert_end_correction():
    # convert_end_correction will assign value based on selected entry
    # returns given assigned value in float data type
    global __end_correction
    value = __end_correction.get_cmb()
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
    global __cms
    unit = __cms.get_btn()
    if unit == "m/N":
        return float(__cms.get_txtfield())
    elif unit == "mm/N":
        return float(__cms.get_txtfield()) * .001
    elif unit == "um/N":
        return float(__cms.get_txtfield()) * .000001

def convert_mms():
    # convert_mms will, if necessary, convert the given value in the mms entry object
    # to Kg
    # returns given conversion in float data type
    global __mms
    unit = __mms.get_btn()
    if unit == "Kg":
        return float(__mms.get_txtfield())
    elif unit == "g":
        return float(__mms.get_txtfield()) * .001

def convert_le():
    # convert_le will, if necessary, convert the given value in the le entry object
    # to H
    # returns given conversion in float data type
    global __le
    unit = __le.get_btn()
    if unit == "H":
        return float(__le.get_txtfield())
    elif unit == "mH":
        return float(__le.get_txtfield()) * .001

def convert_sd():
    # convert_sd will, if necessary, convert the given value in the sd entry object
    # to m^2
    # returns given conversion in float data type
    global __sd
    unit = __sd.get_btn()
    if unit == "m^2":
        return float(__sd.get_txtfield())
    elif unit == "cm^2":
        return float(__sd.get_txtfield()) * .0001
    elif unit == "mm^2":
        return float(__sd.get_txtfield()) * .00001
    elif unit == "in^2":
        return float(__sd.get_txtfield()) / 1550
    elif unit == "ft^2":
        return float(__sd.get_txtfield()) / 10.764

def get_port_tuning_hz():
    # This is a placeholder.
    # The port_tuning_calculation itself should be
    # moved here, but for now, we just read the value.
    if __port_tuning:
        try:
            return float(__port_tuning.get_txtfield())
        except ValueError:
            return 25.1082 # Default test value
    return 25.1082 # Default test value

def get_frequency():
    try:
        return float(__frequency.get_txtfield())
    except (ValueError, AttributeError):
        return 30.02 # Default test frequency

# Master function which creates a dictionary of GUI values
def gather_all_inputs():
    """
    Gathers all values from the GUI, converts them,
    and returns them in a simple dictionary.
    """
    params = {
        're': get_re(),
        'rms': get_rms(),
        'bl': get_bl(),
        'vg': get_vg(),
        'le': convert_le(),
        'cms': convert_cms(),
        'mms': convert_mms(),
        'sd': convert_sd(),
        'vb': convert_net_volume_meters(),
        'ap': convert_port_area_m(),
        'fb': get_port_tuning_hz(),
        'ql': 10,     # Constant
        'p0': 1.20095, # Constant
        'c': 343.68   # Constant
    }
    return params

# This function is used for setting test data. Can be removed when no longer needed
def load_test_values():
    # Loads all test values from the test_data module
    # and populates the GUI fields.

    data = test_data.test_values

    print("Loading test values...")

    # Check if GUI items exist before setting
    try:
        if __re:
            __re.set_txtfield(data['re'])
        if __le:
            __le.set_txtfield(data['le'])
            __le.set_btn_text(data['le_unit'])
        if __bl:
            __bl.set_txtfield(data['bl'])
            __bl.set_btn_text(data['bl_unit'])
        if __sd:
            __sd.set_txtfield(data['sd'])
            __sd.set_btn_text(data['sd_unit'])
        if __cms:
            __cms.set_txtfield(data['cms'])
            __cms.set_btn_text(data['cms_unit'])
        if __mms:
            __mms.set_txtfield(data['mms'])
            __mms.set_btn_text(data['mms_unit'])
        if __rms:
            __rms.set_txtfield(data['rms'])
            __rms.set_btn_text(data['rms_unit'])
        if __vg:
            __vg.set_txtfield(data['vg'])
        if __net_volume:
            __net_volume.set_txtfield(data['vb'])
            __net_volume.set_btn_text(data['vb_unit'])
        if __port_area:
            __port_area.set_txtfield(data['port_area'])
            __port_area.set_btn_text(data['port_area_unit'])
        if __port_length:
            __port_length.set_txtfield(data['port_length'])
            __port_length.set_btn_text(data['port_length_unit'])
        if __port_tuning:
            __port_tuning.set_txtfield(data['port_tuning'])
        if __frequency:
            __frequency.set_txtfield(data['frequency'])
        if __end_correction:
            __end_correction.set_cmb_text(data['end_correction'])

        print("Test values loaded successfully.")
    except Exception as e:
        print(f"Error loading test values: {e}")