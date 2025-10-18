# This new computations file will only be in charge of math functionality
import math
import cmath


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

    # wb represents angular box tuning frequency as 2*PI*port_tuning
    wb = 2.0 * math.pi * params['fb']

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

    port_vel = calculate_port_velocity(core_results, params['ap'], s, lmap)
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
    ilmap = pd / zlamp

    # Returns the peak velocity (RMS * sqrt(s))/area
    return (ilmap * math.sqrt(2)) / port_area


def calculate_cone_excursion(core_results, w):
    # Calculates cone excursion from core results
    u = core_results['u']
    return (math.sqrt(2) * u) / w