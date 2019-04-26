from input import *
import numpy as np
from scipy.interpolate import RegularGridInterpolator



class Model:

    def __init__(self, len_x, x_full, bin_indices, parameter_dict, opacity_grid):

        self.len_x = len_x
        self.x_full = x_full
        self.bin_indices = bin_indices
        self.parameter_dict = parameter_dict
        self.opacity_grid = opacity_grid

    def molecular_opacity(self, my_temp, opacity_table):

        fn = RegularGridInterpolator((self.x_full, temperature_array), opacity_table)
        pt = (self.x_full, my_temp)
        y = fn(pt)
        return y


    def cia_cross_section(self, my_temp, cia_table):

        fn = RegularGridInterpolator((temperature_array_cia, self.x_full), cia_table)
        pt = (my_temp, self.x_full)
        y = fn(pt)
        return y


    def transit_depth(self):
        ## calculates transit depth ##

        my_temp = self.parameter_dict["T"]
        if self.parameter_dict["log_kappa_cloud"] == "Off":
            if self.parameter_dict["log_kappa_0"] == "Off":
                kappa_cloud = 0     # cloudfree case
            else:
                kappa_0 = 10 ** self.parameter_dict["log_kappa_0"]
                r_c = 10 ** self.parameter_dict["log_r_c"]
                x = 2 * np.pi * r_c * self.x_full
                kappa_cloud = kappa_0 / (self.parameter_dict["Q0"] * (x ** -(self.parameter_dict["a"])) + x ** 0.2)
        else:
            kappa_cloud = 10**self.parameter_dict["log_kappa_cloud"]

        R0 = self.parameter_dict["R0"]*rjup
        P0 = (10**self.parameter_dict["log_P0"])*1e6   # convert to cgs

        mass_fraction = []
        molecular_mass = []
        kappa = []
        for molecule in molecules:
            abundance_name = molecular_abundance_dict[molecule]
            mass_fraction.append([10**self.parameter_dict[abundance_name]])
            molecular_mass.append([molecular_mass_dict[molecule]])
            opacity = self.molecular_opacity(my_temp, self.opacity_grid[molecule])
            kappa.append([opacity])

        mass_fraction = np.array(mass_fraction)
        molecular_mass = np.array(molecular_mass)
        kappa = np.array(kappa)
        kappa = kappa.reshape(kappa.shape[0],kappa.shape[2])

        xh2 = (1 - np.sum(mass_fraction))/1.1   # calculate abundance of H2
        if 'm' not in globals():                # set mean molecular weight if not given in input
            m = 2.4*xh2*amu + np.sum(mass_fraction*molecular_mass)

        pressure_cia = 10**self.parameter_dict["log_p_cia"]

        if my_temp < 200:       # add in cia opacities
            kappa_cia = 0
        else:
            sigma_h2he = self.cia_cross_section(my_temp, self.opacity_grid['cia_h2he'])
            sigma_h2h2 = self.cia_cross_section(my_temp, self.opacity_grid['cia_h2h2'])
            ntot = pressure_cia*1e6/kboltz/my_temp
            kappa_cia = xh2 * ntot * (xh2 * sigma_h2h2 + 0.1*xh2 * sigma_h2he) / m

        sigma_rayleigh = 8.4909e-45*(self.x_full**4)        # rayleigh scattering cross-section from Vardya (1962)
        kappa_rayleigh = xh2*sigma_rayleigh/m

        kappa_total_molecules = np.sum(mass_fraction*molecular_mass*kappa, axis=0) /m  # sum opacity contributions from molecules
        kappa_total = kappa_total_molecules + kappa_cloud + kappa_cia + kappa_rayleigh      # add in cloud, rayleigh and cia opacities

        h = kboltz*my_temp/m/g
        term1 = P0*kappa_total/g
        term2 = np.sqrt(2.0*np.pi*R0/h)
        r = R0 + h * (gamma + np.log(term1 * term2))

        result = 100.0 * (r / rstar) ** 2  # return percentage transit depth
        return result


    def binned_model(self):
        ## calculates average transit depth in given bins ##

        y_full = self.transit_depth()
        y_mean = np.zeros(self.len_x)
        for i in range(self.len_x):
            j = int(self.bin_indices[i])
            k = int(self.bin_indices[i + 1])
            y_mean[i] = np.mean(y_full[k:j])   # bin transit depth
        return y_mean


