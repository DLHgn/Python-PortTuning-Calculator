import math
__port_area = None
__port_length = None
__net_volume = None
__end_correction = None
__number_of_ports = None
__port_tuning = None


def set_port_area(value):
    global __port_area
    __port_area = value


def set_port_length(value):
    global __port_length
    __port_length = value


def set_net_volume(value):
    global __net_volume
    __net_volume = value


def set_end_correction(value):
    global __end_correction
    __end_correction = value


def set_number_of_ports(value):
    global __number_of_ports
    __number_of_ports = value


def set_port_tuning(value):
    global __port_tuning
    __port_tuning = value


def set_port_tuning_entry():
    global __port_tuning
    __port_tuning.set_tuning(port_tuning_calculation())


def convert_port_area_in():
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
    return 2*math.sqrt(value/math.pi)


def port_tuning_calculation():
    if __number_of_ports.get_txtfield():
        number_of_ports = 1
    else:
        number_of_ports = int(__number_of_ports.gettxtField())

    port_area_in = convert_port_area_in() * number_of_ports
    port_area_cm = convert_port_area_cm()  #does not need number_of_ports because DIY Audio equation already accounts for that
    net_volume_in = convert_net_volume_in()
    net_volume_l = convert_net_volume_liters()
    port_length_in = convert_port_length_in()
    port_length_cm = convert_port_length_cm()
    end_correction = convert_end_correction()
    port_diameter = calculate_port_diameter(port_area_cm)

    port_tuning1 = .159*math.sqrt(port_area_in*1.84E8/(net_volume_in*(port_length_in+end_correction*math.sqrt(port_area_in))))

    port_tuning2 = (153.501*port_diameter*math.sqrt(number_of_ports))/((math.sqrt(net_volume_l))*(math.sqrt(port_length_cm+end_correction*port_diameter)))

    return (port_tuning1+port_tuning2)/2
