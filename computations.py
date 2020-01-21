import math
#the global variables are meant to store the gui_items objects for use in the calculations. These are to only be used
#by this module
__port_area = None
__port_length = None
__net_volume = None
__end_correction = None
__number_of_ports = None
__port_tuning = None


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


def set_port_tuning(value):
    # set_port_tuning stores the given gui_items.Item object into the port_tuning global variable
    # @param value is a gui_items.Item object
    global __port_tuning
    __port_tuning = value


def set_port_tuning_entry():
    # set_port_tuning_entry sets the port_tuning entry object to the output of port_tuning_calculation() using the
    #function Item.set_txtfield()
    global __port_tuning
    __port_tuning.set_txtfield(port_tuning_calculation())


def convert_port_area_in():
    #convert_port_area_in will, if necessary, convert the given value in the port_area entry object to square inches
    #returns given conversion in float data type
    global __port_area
    unit = __port_area.get_btn()
    if unit == "in^2":
        return float(__port_area.get_txtfield())
    elif unit == "cm^2":
        return float(__port_area.get_txtfield()) * .155
    elif unit == "ft^2":
        return float(__port_area.get_txtfield()) * 144
    elif unit == "mm^2":
        return float(__port_area.get_txtfield()) * .00155


def convert_port_area_cm():
    # convert_port_area_cm will, if necessary, convert the given value in the port_area entry object
    #to square centimeters
    # returns given conversion in float data type
    global __port_area
    unit = __port_area.get_btn()
    if unit == "cm^2":
        return float(__port_area.get_txtfield())
    elif unit == "in^2":
        return float(__port_area.get_txtfield()) * 6.4516
    elif unit == "ft^2":
        return float(__port_area.get_txtfield()) * 929.03
    elif unit == "mm^2":
        return float(__port_area.get_txtfield()) * .01


def convert_net_volume_in():
    # convert_net_volume_in will, if necessary, convert the given value in the net_volume entry object to cubic inches
    # returns given conversion in float data type
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


def convert_net_volume_liters():
    # convert_net_volume_liters will, if necessary, convert the given value in the net_volume entry object to Liters
    # returns given conversion in float data type
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


def calculate_port_diameter(value):
    #converts a given Port area into a port diameter. If in^2 are given, formula will return inches. cm^2 -> cm. etc.
    #@param value is the given port area
    #returns the port diameter
    return 2*math.sqrt(value/math.pi)


def port_tuning_calculation():
    #port_tuning_calculation calculates the port tuning using two different equations and takes the average of the two.
    #This method results in the closest real world value for the port tuning.
    #returns the averaged port tuning values

    #if there is no given number of ports value, assume 1
    if __number_of_ports.get_txtfield():
        number_of_ports = 1
    else:
        number_of_ports = int(__number_of_ports.gettxtField())

    port_area_in = convert_port_area_in() * number_of_ports
    port_area_cm = convert_port_area_cm()
    net_volume_in = convert_net_volume_in()
    net_volume_l = convert_net_volume_liters()
    port_length_in = convert_port_length_in()
    port_length_cm = convert_port_length_cm()
    end_correction = convert_end_correction()
    port_diameter = calculate_port_diameter(port_area_cm)

    #This is the JL Audio equation. It uses in^2 for port area, in^3 for net volume, and inches for port length.
    #number of ports is already factored into the port area for this equation
    port_tuning1 = .159*math.sqrt(port_area_in*1.84E8/(net_volume_in*(port_length_in+end_correction*math.sqrt(port_area_in))))

    #this is the DIY Audio equation. It uses port diameter instead of port area, number_ports, liters for net volume,
    #and cm for port length. This equation has a separate variable for number of ports.
    port_tuning2 = (153.501*port_diameter*math.sqrt(number_of_ports))/((math.sqrt(net_volume_l))*(math.sqrt(port_length_cm+end_correction*port_diameter)))

    return (port_tuning1+port_tuning2)/2
