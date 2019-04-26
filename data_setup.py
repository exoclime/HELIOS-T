import load_files
import numpy as np
from input import *

def find_bin_indices(x_full, bins):
    ## Finds locations of bins in x_full ##

    n1 = len(x_full)
    n2 = len(bins)
    bin_indices = np.zeros(n2)
    for i in range(n2):
        for j in range(n1):
            if x_full[j] < bins[i]:
                bin_indices[i] = j+1
            else:
                break

    return bin_indices


def data(wavenumber=True):
    """
    Produces data depending on data type.

    wavenumber : True or False
            The data type from the opacity tables. If True the input data is inverted to match the opacity data. Default is true.

    """

    ydata = transit_depth
    yerr = transit_depth_error
    n2 = len(wavelength_bins)
    wavelength_centre = np.zeros(n2-1)
    wavelength_err = np.zeros(n2-1)
    for i in range(n2-1):
        wavelength_centre[i] = 0.5 * (wavelength_bins[i] + wavelength_bins[i+1])
        wavelength_err[i] = 0.5 * (wavelength_bins[i+1] - wavelength_bins[i])

    if wavenumber is True:
        wavenumber_bins = 1e4/wavelength_bins
        wavenumber_centre = 1e4/wavelength_centre
        x = wavenumber_centre
        bins = wavenumber_bins
    else:
        x = wavelength_centre
        bins = wavelength_bins

    # Load x_full array and opacity table from binary files
    opacity_grid = {}
    x_full, opacity_grid[molecules[0]] = load_files.load_opacity_data(molecules[0])
    for molecule in molecules[1:]:
        opacity_grid[molecule] = load_files.load_opacity_data(molecule)[1]
        if molecule == '11':
            opacity_grid[molecule] = np.pad(opacity_grid[molecule], [(0,0),(0,7)], mode='constant')


    opacity_grid['cia_h2h2'] = load_files.load_sigma('H2', 'H2', x_full)  # load in CIA cross-sections
    opacity_grid['cia_h2he'] = load_files.load_sigma('H2', 'He', x_full)


    # Find locations of bins in x_full #
    bin_indices = find_bin_indices(x_full, bins)

    return x, x_full, opacity_grid, bin_indices, ydata, yerr, wavelength_centre, wavelength_err

