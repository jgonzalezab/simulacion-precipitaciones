These scripts contain the code (R and Python) to simulate precipitations in Santander.
## Do not modify the directory Data, this change will break the relative path contained in the scripts ##

#### R implementation ####
- It is contained in a jupyter notebook (M1964_panorama_practica.ipynb)
- You will need a valid Jupyter installation and its correspondent R kernel
- Libraries used:
	- ggplot2 

	
	
#### Python implementation ####
- All the code is contained in simulation.py.
- To execute yhis script you will need:
	- Python 3.X
	- Numpy
	- Scipy
	- Matplotlib
	
- You can execute the script from shell in the following way:
	~/simulacion-precipitaciones$: python simulation.py -days -distribution -toPlot -dataSource
	- days: days to simulate
	- distribution: distribution to simulate the rainy days (gamma or exponential)
	- toPlot: True to plot the simulation
	- dataSource: data to use (CMT or Parayas)
	
	Example:
		~/simulacion-precipitaciones: python simulation.py 365 Exponential True Parayas