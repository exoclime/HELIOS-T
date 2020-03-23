import numpy as np
import os

## Constants ##

kboltz = 1.38064852e-16    # Boltzmann's constant
amu = 1.660539040e-24      # atomic mass unit
gamma = 0.57721
rjup = 7.1492e9            # equatorial radius of Jupiter
rsun = 6.9566e10           # solar radius
rearth = 6.378e8            # earth radius
pressure_probed = 1e-2      # probed pressure in bars
# pressure_cia = 1e-2         # pressure for cia in bars
# m = 2.4*amu                 # assummed hydrogen-dominated atmosphere
m_water = 18.0*amu          # mean molecular mass of any molecules you want to consider
m_cyanide = 27.0*amu
m_ammonia = 17.0*amu


## Planet Data ##

planet_name = 'WASP-12b'

g = 977
rstar = 1.57*rsun
r0 = 1.79
r0_uncertainty = 0.09

wavelength_bins = np.array([0.838, 0.896, 0.954, 1.012, 1.070, 1.112, 1.182, 1.251, 1.320, 1.389, 1.458, 1.527, 1.597, 1.666])
transit_depth = np.array([1.4441, 1.4422, 1.4402, 1.4428, 1.4391, 1.4386, 1.4365, 1.4327, 1.4582, 1.4600, 1.4530, 1.4475, 1.4332])
transit_depth_error = np.array([0.0069, 0.0055, 0.0052, 0.0051, 0.0053, 0.0047, 0.0045, 0.0041, 0.0040, 0.0043, 0.0045, 0.0058, 0.0055])


## Retrieval info ##

molecules = ['01', '11', '23']  # list of molecules (determines which opacity tables are loaded)
parameters = ["T", "log_xh2o", "log_xhcn", "log_xnh3", "log_kappa_cloud"]   # parameters you wish to retrieve (MUST MATCH MOLECULES)
res = 5         # resolution used for opacities
live = 1000     # live points used in nested sampling
wavenumber=True     # True if opacity given in terms of wavenumber, False if wavelength

priors = {"T": [2800, 100], "log_xh2o": [13,-13], "log_xhcn": [13,-13], "log_xnh3": [13,-13], "log_kappa_cloud": [14,-12],
          "R0": [2*r0_uncertainty,r0-r0_uncertainty], "log_P0": [4,-1], "log_kappa_0": [9,-10], "Q0": [99,1], "a": [3,3],
          "log_r_c": [6,-7], "log_p_cia": [3,-3]} # priors for all possible parameters



## info for all possible parameters ##
molecular_abundance_dict = {"01":"log_xh2o", "23":"log_xhcn", "11":"log_xnh3"}  # dictionary list of all possible molecules and corresponding abundance names

parameter_dict = {"T": 1000, "log_xh2o": "Off", "log_xhcn": "Off", "log_xnh3": "Off", "log_kappa_cloud": "Off", "R0": r0,
                  "log_P0": 1, "log_kappa_0": "Off", "Q0": "Off", "a": "Off", "log_r_c": "Off", "log_p_cia": -2}    # default parameter values used if not retrieved

molecular_mass_dict = {"01": m_water, "23": m_cyanide, "11": m_ammonia}   # dictionary of molecules and their mean molecular masses
temperature_array = np.r_[50:700:50, 700:1500:100, 1500:3100:200]
temp_dict = {'01': temperature_array, '23': temperature_array, '11': temperature_array[:22]}   # temperature values for corresponding opacity tables
temperature_array_cia = np.r_[200:3025:25]          # temperature array for CIA table
opacity_path = os.environ['HOME'] + "/Dropbox/Opacities/opacity_bin_files/"  # path to opacity binary files
cia_path = os.environ['HOME'] + "/Dropbox/Opacities/HITRAN/"      # path to CIA files

