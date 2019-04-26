import pymultinest
import numpy as np
from input import *
from asthetics import *
import data_setup
import ns_setup
import model
from matplotlib import pyplot as plt
import cornerplot
import time
import json
import os
import csv

start = time.time()

n_params = len(parameters)

output_directory = 'out/'
os.makedirs(os.path.dirname(output_directory), exist_ok=True)

x, x_full, opacity_grid, bin_indices, ydata, yerr, wavelength_centre, wavelength_err = data_setup.data()
len_x = len(x)


## Run PyMultinest ##
b = ns_setup.Priors(1, n_params)
pymultinest.run(b.loglike, b.prior, n_params,
                loglike_args=[len_x, x_full, bin_indices, opacity_grid, ydata, yerr],
                outputfiles_basename=output_directory + planet_name + '_',
                resume=False, verbose=True,
                n_live_points=live)


json.dump(parameters, open(output_directory+planet_name+'_params.json', 'w'))  # save parameter names

a = pymultinest.Analyzer(outputfiles_basename=output_directory+planet_name+'_', n_params=n_params)
samples = a.get_equal_weighted_posterior()[:, :-1]
bestfit_params = a.get_best_fit()
stats = a.get_stats()

## set up results ##
retrieved_results = list(map(lambda v: (v[1], v[2] - v[1], v[1] - v[0]), zip(*np.percentile(samples, [16, 50, 84], axis=0))))


plot_percentiles = []
new_param_dict = parameter_dict
retrieved_parameters_full = {}
retrieved_parameters_list = []
for i in range(n_params):
    retrieved_parameters_full[parameters[i]] = retrieved_results[i]
    new_param_dict[parameters[i]] = bestfit_params['parameters'][i]
    retrieved_parameters_list.append(retrieved_results[i][0])
    plot_percentiles.append(retrieved_results[i])


print("""PyMultinest result:""")
for param in parameters:
    print(param,' = ',retrieved_parameters_full[param][0],' +',retrieved_parameters_full[param][1],' -',retrieved_parameters_full[param][2])

a_lnZ = a.get_stats()['global evidence']
log_evidence = a_lnZ/np.log(10)

print
print ('************************')
print ('MAIN RESULT: Evidence Z ')
print ('************************')
print ('  log Z for model = %.1f' % (log_evidence))
print


## compute model for retrieved results ##
y = model.Model(len_x, x_full, bin_indices, new_param_dict, opacity_grid)
yfit = y.transit_depth()
yfit_binned = y.binned_model()


## change to wavelength ##
if wavenumber is True:
    x_full_plot = 1.0 / (x_full * 1e-4)  # convert to wavelength
else:
    x_full_plot = x_full


## plot posteriors ##
retrieved_parameter_labels = []
posterior_ranges = []
color_list = []
for param in parameters:
    posterior_ranges.append(parameter_ranges[param])
    retrieved_parameter_labels.append(parameter_labels[param])
    color_list.append(parameter_colors[param])

fig = cornerplot.corner(samples, x_full_plot, wavelength_centre, yfit, yfit_binned, ydata, wavelength_err, yerr, posterior_ranges, color_list,
                       labels=retrieved_parameter_labels, truths=plot_percentiles, max_n_ticks=3, label_kwargs={"fontsize": 34})
fig.savefig('pymultinest-corner.eps', format='eps')


end = time.time()
print("time = ",end-start)

