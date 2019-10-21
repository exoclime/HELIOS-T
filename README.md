# HELIOS-T
Atmospheric retrieval code for exoplanet transmission spectra

HELIOS-T requires [PyMultinest](http://johannesbuchner.github.io/PyMultiNest/) to run, so make sure you have this downloaded first. 

The theory paper can be found here: https://arxiv.org/abs/1809.06894

Please cite this when using HELIOS-T.

## Requirements

HELIOS-T is developed for use with Python 3 and requires the following packages:

- PyMultinest
- numpy
- scipy
- matplotlib

## PyMultinest

As the ```loglike``` function in ```ns_setup.py``` includes the additional argument ```loglike_args```, this must be added inside PyMultinest. In the ```run.py``` script, line 213 must be edited to read:

```
return LogLikelihood(cube, ndim, nparams, loglike_args)
```

Then ```loglike_args``` must also be added as an argument to the ```run``` function, e.g. line 66 should read:

```
def run(LogLikelihood,
	Prior,
	n_dims, 
	n_params = None,
	loglike_args = None,
	n_clustering_params = ...
```

Line 198 should be changed to ```nargs = 4``` and 204 to ```if nargs == 5```.

## Input File

In the ```input.py``` file you can set up HELIOS-T for whatever planet you want. Here is where you put in the planet's name, the gravity (g), the stellar radius, the planet radius and it's uncertainty, and the data. For the data, you have the ```wavelength_bins```, which refers to the edges of the bins, the ```transit_depth```, i.e. (R_p/R_s)^2 in %, and ```transit_depth_error```, the error on these values. Since ```wavelength_bins``` takes the bin **edges** (i.e. including the start of the first bin and the end of the last bin), it needs to have length one greater than ```transit_depth```.

The retrieval info section sets up what molecules you want to use in your retrieval, and which parameters to retrieve for. Here there are also the prior ranges. Every parameter is assumed to have a uniform prior, so abundances etc should be retrieved as the log quantities. 

The info for all possible parameters needs to be edited if you want to add new parameters to the model, or if you want to use your own model file for example, and you have different parameters. 

Finally you have the ```opacity_path``` and the ```cia_path```. These need to be changed to the locations of your molecular opacity files and your CIA opacity files. 

## Load Files

The ```load_files.py``` file will need to be edited depending on the format of your opacity files, i.e. to match the naming convention you have on your computer. This file is set up for use with binary files, to save space. 

## Model

The information on the model may be found in our [paper](https://arxiv.org/abs/1809.06894). If you wish to use your own model file you will need to make sure you either use the same arguments as in the functions in ```model.py```, or you will need to update ```ns_setup.py``` and ```helios-t.py```.

## Running HELIOS-T

HELIOS-T is simply run as follows:

```
python helios-t.py
```

This will then initiate the nested sampling routine from PyMultinest, using the model from HELIOS-T. The current output from HELIOS-T is the corner plot showing the posteriors. However, the ```helios-t.py``` file can easily be edited to save the samples from the posteriors, if you prefer to run your own plotting routine later. 

## Plotting

HELIOS-T is using Dan Foreman-Mackey's corner plot code, original found [here](https://github.com/dfm/corner.py/blob/master/corner/corner.py), edited to include the plot of the fit in the top right of the corner. If you prefer, you can use your own plotting routine. 

## Remarks

If you have any questions or suggestions please contact [Chloe Fisher](mailto:chloe.fisher@csh.unibe.ch).

Enjoy using HELIOS-T!

We acknowledge partial financial support from the Center for Space and Habitability (CSH), the PlanetS National Center of Competence in Research (NCCR), the University of Bern International 2021 Ph.D Fellowship, the Swiss National Science Foundation, a European Research Council (ERC) Consolidator Grant and the Swiss-based MERAC Foundation.

