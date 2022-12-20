import math
import cmath

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
# for now this is set to a constant but can be a user set variable
__p0 = 1.20095
# for now this is set to a constant but can be a user set variable
__c = 343.68
# for now this is set to a constant but can be a user set variable
__ql = 10
# These global variables are meant to store calculated values that are used more than once. These are to only be used
# by this module.
__wb = None
__w = None
__s = None
__ccab = None
__ral = None
__lmap = None
__frequency = None

# the variables will be for testing purposes only and should be deleted after testing
__zb = None
__port_velocity = None
__cone_excursion = None
__frequency_response = None
__u = None
__pd = None
__i = None
__zccab = None
__iccab = None
__zlmap = None
__ilmap = None


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
        return float(__sd.get_txtfield()) * .00001
    elif unit == "mm^2":
        return float(__sd.get_txtfield()) * .000001
    elif unit == "in^2":
        return float(__sd.get_txtfield()) / 1550
    elif unit == "ft^2":
        return float(__sd.get_txtfield()) / 10.764


# Below we have calculating functions that take the variables set/converted above and run them through equations
def calculate_port_diameter(value):
    # converts a given Port area into a port diameter. If in^2 are given, formula will return inches. cm^2 -> cm. etc.
    # @param value is the given port area
    # returns the port diameter
    return 2*math.sqrt(value/math.pi)


def port_tuning_calculation():
    # port_tuning_calculation calculates the port tuning using two different equations and takes the average of the two.
    # This method results in the closest real world value for the port tuning.
    # returns the averaged port tuning values

    # if there is no given number of ports value, assume 1
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

    # This is the JL Audio equation. It uses in^2 for port area, in^3 for net volume, and inches for port length.
    # number of ports is already factored into the port area for this equation
    port_tuning1 = .159*math.sqrt(port_area_in*1.84E8/(net_volume_in*(port_length_in+end_correction*math.sqrt(port_area_in))))

    # This is the DIY Audio equation. It uses port diameter instead of port area, number_ports, liters for net volume,
    # and cm for port length. This equation has a separate variable for number of ports.
    port_tuning2 = (153.501*port_diameter*math.sqrt(number_of_ports))/((math.sqrt(net_volume_l))*(math.sqrt(port_length_cm+end_correction*port_diameter)))

    return (port_tuning1+port_tuning2)/2


def set_frequency(frequency):
    # This function takes the frequency currently being calculated on and setting it the global variable __frequency
    # to be used by the below functions
    global __frequency
    __frequency = frequency


def calculate_and_set_wb():
    # This function calculates and sets the value __wb which represents angular box tuning frequency as 2*PI*port_tuning
    # The default frequency is the test frequency when working through this with Janne Ahonen
    global __wb

    # if box tuning hasn't been calculated yet, use the default
    if __port_tuning is None:
        __wb = 2 * math.pi * 25.1082
    # else use the calculated box tuning
    else:
        __wb = 2.0 * math.pi * float(__port_tuning.get_txtfield())

    print("wb ", __wb)


def calculate_and_set_w():
    # This function calculates and sets the value __w which represents angular tuning frequency as 2*PI*frequency
    # Note this is distinctly different than wb which is angular box tuning. This value is used during analysis and will
    # change based and the frequency we're calculating for at the time.
    global __w
    __w = 2.0 * math.pi * float(__frequency.get_txtfield())

    print("w ", __w)


def calculate_and_set_s():
    # This function calculates and sets the value __s which represents the common abbreviation for j*__w where
    # j is an imaginary number. The default frequency is the test frequency when working through this with Janne Ahonen
    global __s

    if __w is None:
        calculate_and_set_w()

    __s = cmath.sqrt(-1) * __w

    print("s ", __s)


def calculate_and_set_ccab():
    # This function calculates and sets the value __ccab which represents the
    # acoustic compliance of the enclosure volume
    global __ccab
    __ccab = convert_net_volume_meters() / (__p0 * math.pow(__c,2))

    print("\n", "Calculation for Ccab:")
    print("Net volume in m^3: ", convert_net_volume_meters())
    print("Air density: ", __p0)
    print("c^2: ", math.pow(__c,2))
    print("ccab ", __ccab)


def calculate_and_set_ral():
    # This function calculates and sets the value __ral which represents the acoustic resistance modeling air leak
    # The default frequency is the test frequency when working through this with Janne Ahonen
    global __ral

    # If __wb wasn't set, calculate and set __wb using the default
    if __wb is None:
        calculate_and_set_wb()
    # If __ccab wasn't set, calculate and set __ccab
    if __ccab is None:
        calculate_and_set_ccab()

    __ral = __ql / (__wb * __ccab)

    print("\n", "Calculation for Ral: ")
    print("Ql: ", __ql)
    print("wb: ", __wb)
    print("Ccab: ", __ccab)
    print("ral ", __ral)


def calculate_and_set_lmap():
    # This function calculates and sets the value w which represents angular frequency as 2*PI*frequency
    # The default frequency is the test frequency when working through this with Janne Ahonen
    global __lmap

    # If __wb wasn't set, calculate and set __wb using the default
    if __wb is None:
        calculate_and_set_wb()
    # If __ccab wasn't set, calculate and set __ccab
    if __ccab is None:
        calculate_and_set_ccab()

    __lmap = 1 / (math.pow(__wb,2) * __ccab)

    print("\n", "lmap:" , __lmap)


def calculate_and_set_zb():
    # This function will calculate and set Zb which represents the total impedance of the driver acoustical and
    # box portion fo the circuit model

    # if __s wasn't set, calculate and set __s
    if __s is None:
        calculate_and_set_s()
    # If __ccab wasn't set, calculate and set __ccab
    if __ccab is None:
        calculate_and_set_ccab()
    # If __ral wasn't set, calculate and set __ral
    if __ral is None:
        calculate_and_set_ral()
    # If __lmap wasn't set, calculate and set __lmap
    if __lmap is None:
        calculate_and_set_lmap()

    test = 1/(__s * __ccab + (1 / __ral) + (1/(__s * __lmap)))
    print("\n", "Calculation for zb:")
    print("zb (complex): ", test)
    print("zb (polar): ", cmath.polar(test))

    return 1/(__s * __ccab + (1 / __ral) + (1/(__s * __lmap)))


def calculate_and_set_pd():
    # This function will calculate and set Pd which represents the voltage across loop mesh of the driver acoustical and
    # box portion of the circuit model

    if __s is None:
        calculate_and_set_s()

    # Pd is a long equation using a lot of the same variables. I have broken the equation apart so that I can assign
    # chunks of it as local variables then do further calculating on these variables. This will make the equations
    # easier to follow and troubleshoot if necessary.

    zb = calculate_and_set_zb()
    cms = convert_cms()
    mms = convert_mms()
    le = convert_le()
    re = get_re()
    rms = get_rms()
    bl = get_bl()
    sd = convert_sd()
    vg = get_vg()

    x1 = zb * cms * __s * vg * bl * sd
    x2 = cms * le * sd**2 * zb * __s**2
    x3 = cms * le * mms * __s**3
    x4 = cms * re * sd**2 * zb * __s
    x5 = cms * le * rms * __s**2
    x6 = cms * mms * re * __s**2
    x7 = cms * bl**2 * __s
    x8 = cms * re * rms * __s
    x9 = le * __s

    test = x1/(x2+x3+x4+x5+x6+x7+x8+x9+re)
    print("\n", "Calculations for Pd: ")

    print("---Initial Givens: ")
    print("Zb: ", zb)
    print("Cms: ", cms)
    print("Mms: ", mm)
    print("Le: ", le)
    print("Re: ", re)
    print("Rms: ", rms)
    print("Bl: ", bl)
    print("Sd: ", sd)
    print("Vg: ", vg)

    print("---Calculation Chunks: ")
    print("X1: ", x1)
    print("X2: ", x2)
    print("X3: ", x3)
    print("X4: ", x4)
    print("X5: ", x5)
    print("X6: ", x6)
    print("X7: ", x7)
    print("X8: ", x8)
    print("X9: ", x9)

    print("Pd: ", cmath.polar(test))

    return x1/(x2+x3+x4+x5+x6+x7+x8+x9+re)


def calculate_and_set_i():
    # This function will calculate and set I which represents the loop mesh current of the amplifier/driver
    # electrical portions of the circuit model.

    # if __s wasn't set, calculate and set __s
    if __s is None:
        calculate_and_set_s()

    # 'I' is a long equation using a lot of the same variables. I have broken the equation apart so that I can assign
    # chunks of it as local variables then do further calculating on these variables. This will make the equations
    # easier to follow and troubleshoot if necessary.

    cms = convert_cms()
    mms = convert_mms()
    le = convert_le()
    re = get_re()
    rms = get_rms()
    bl = get_bl()
    sd = convert_sd()
    vg = convert_net_volume_meters()
    pd = calculate_and_set_pd()

    y1 = bl * sd * pd * __s * cms
    y2 = cms * mms * vg * __s**2
    y3 = cms * rms * vg * __s
    y4 = cms * le * mms * __s**3
    y5 = cms * le * rms * __s**2
    y6 = cms * mms * re * __s**2
    y7 = bl**2 * cms * __s
    y8 = cms * re * rms * __s
    y9 = le * __s

    test = (y1 + y2 + y3 + vg)/(y4 + y5 + y6 + y7 + y8 + y9 + re)
    print("i ", cmath.polar(test))

    return (y1 + y2 + y3 + vg)/(y4 + y5 + y6 + y7 + y8 + y9 + re)


def calculate_and_set_u():
    # This function will calculate and set U which represents the loop mesh current of the driver mechanical
    # portions of the circuit model.

    # if __s wasn't set, calculate and set __s
    if __s is None:
        calculate_and_set_s()

    # Setting local variables to use within the equation.

    cms = convert_cms()
    mms = convert_mms()
    rms = get_rms()
    bl = get_bl()
    sd = convert_sd()
    pd = calculate_and_set_pd()
    i = calculate_and_set_i()

    # U is a long equation using a lot of the same variables. I have broken the equation apart so that I can assign
    # chunks of it as local variables then do further calculating on these variables. This will make the equations
    # easier to follow and troubleshoot if necessary.

    z1 = bl * i
    z2 = sd * pd
    z3 = __s * cms
    z4 = __s**2 * mms * cms
    z5 = rms * __s * cms

    test = ((z1 - z2) * z3)/(z4 + z5 +1)
    print("u ", cmath.polar(test))

    return ((z1 - z2) * z3)/(z4 + z5 + 1)


def calculate_zccab():
    # This function will calculate and return Zccab which represents the impedance across the Ccab component of the
    # circuit model. Zccab is returned in rectangular coordinates

    # If __w wasn't set, calculate and set __w
    if __w is None:
        calculate_and_set_w()
    # If __ccab wasn't set, calculate and set __ccab
    if __ccab is None:
        calculate_and_set_ccab()

    # AC resistance of the capacitor
    xccab = 1/(__w * __ccab)

    test = 1/(__w * __ccab)
    print("xccab ", cmath.polar(test))

    # impedance of capacitors is represented as (xccab < -90). -90 = -PI/2 radians
    return cmath.rect(xccab, (-1 * math.pi/2))


def calculate_iccab():
    # This function will calculate and return Iccab which represents the current through the Ccab component of the
    # circuit model. Iccab is returned in rectangular coordinates.

    e = calculate_and_set_pd()
    zccab = calculate_zccab()

    test = e / zccab
    print("iccab ", cmath.polar(test))

    return e / zccab


def calculate_zlmap():
    # This function will calculate and return Zlmap which represents the impedance across the Lmap component of the
    # circuit model. Lmap is returned in rectangular coordinates.

    # If __w wasn't set, calculate and set __w
    if __w is None:
        calculate_and_set_w()
    # If __lmap wasn't set, calculate and set __lmap
    if __lmap is None:
        calculate_and_set_lmap()

    # AC resistance of an inductor
    xlmap = __w * __lmap

    test = __w * __lmap
    print("xlmap ", cmath.polar(test))

    # impedance of inductors is represented as (xlmap < 90). 90 = PI/2 radians
    return cmath.rect(xlmap, (math.pi/2))


def calculate_ilmap():
    # This function will calculate and return Ilmap which represents the current through the Lmap component of the
    # circuit model. Ilmap is returned in rectangular coordinates.

    e = calculate_and_set_pd()
    zlmap = calculate_zlmap()

    test = e / zlmap
    print("ilmap ", cmath.polar(test))

    return e / zlmap


def calculate_port_velocity():
    # This function calculates and returns port velocity in m/s

    port_area = convert_port_area_m()
    ilmap = calculate_ilmap()

    test = (math.sqrt(2) * ilmap) / port_area
    print("port_v ", cmath.polar(test))

    return (math.sqrt(2) * ilmap) / port_area


def calculate_cone_excursion():
    # This function calculates and returns cone excursion in m

    u = calculate_and_set_u()

    test = (math.sqrt(2) * u) / __w
    print("cone_ex ", cmath.polar(test))

    return (math.sqrt(2) * u) / __w


def calculate_frequency_response():
    # This function calculates and returns the output at a given frequency in dB

    iccab = calculate_iccab()

    test = (__w * 1.2 * iccab) / .00002
    print("freq_resp ", cmath.polar(test))

    return (__w * 1.2 * iccab) / .00002

