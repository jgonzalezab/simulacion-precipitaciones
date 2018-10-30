import sys
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

class ownSimulation:

	def __init__(self, dataSource):

		self.dataSource = dataSource.lower()

	def processData(self):

		if(self.dataSource == 'cmt'):

			self.historical = np.genfromtxt('Data/RR_STAID003922.txt', delimiter = ',',
											skip_header = 21)[:, 3] 

		else: # self.dataSource == 'parayas'

			self.historical = np.genfromtxt('Data/RR_STAID003923.txt', delimiter = ',',
										    skip_header = 21)[:, 3] 

	def removeNonValid(self):

		self.historical = self.historical[self.historical >= 0]
		self.historical = self.historical[~np.isnan(self.historical)]
		self.historical = self.historical / 10 # To mm

	def transitionProb(self):

		trans = np.array(self.historical > 0, dtype = int)
		transVec = np.array([0, 0]) # Dry|Dry   Dry|Wet

		for i in range(1, len(trans)):
			
			if (trans[i - 1] == 0 and trans[i] == 0):

				transVec[0] += 1

			elif (trans[i - 1] == 1 and trans[i] == 0):

				transVec[1] += 1

		self.transVec = np.array([transVec[0] / sum(trans == 0), \
			                      transVec[1] / sum(trans == 1)])

	def generateDryWet(self, days):

		outData = np.array([round(np.random.uniform())])

		for i in range(1, days):

			outData = np.append(outData, np.random.uniform())

			if(outData[i - 1] == 0):
				outData[i] = 0 if outData[i] < self.transVec[0] else 1
			else:
				outData[i] = 0 if outData[i] < self.transVec[1] else 1

		self.outData = outData

	def generateAmount(self, distribution):

		if distribution.lower() == 'gamma':

			toFit = self.historical[self.historical > 0]

			fittedDistr = stats.gengamma.fit(toFit, loc = 0, scale = 1)
		
			resultSimu = self.outData
		
			toAmount = lambda x: stats.gengamma.rvs(fittedDistr[0], fittedDistr[1],
													fittedDistr[2], fittedDistr[3],
			                                        size = 1)
			vfunc = np.vectorize(toAmount)

			resultSimu[resultSimu == 1] = vfunc(resultSimu[resultSimu == 1])

			self.resultSimu = resultSimu

		else: # distribution == 'exponential':

			toFit = self.historical[self.historical > 0]

			fittedDistr = stats.expon.fit(toFit, loc = 0, scale = 1)
		
			resultSimu = self.outData
		
			toAmount = lambda x: stats.expon.rvs(fittedDistr[0], fittedDistr[1])
			vfunc = np.vectorize(toAmount)

			resultSimu[resultSimu == 1] = vfunc(resultSimu[resultSimu == 1])

			self.resultSimu = resultSimu 



def simulatePrecip(days, distribution, toPlot, dataSource):
	
	# Check arguments sanity
	if(days < 3):
		print('Days argument must be an integer and >= 3')
		return None

	if (not distribution.lower() in ['gamma', 'exponential']):
		print("distribution argument must be Gamma or Exponential")
		return None

	if (not toPlot.lower() in ('true', 'false')):
		print("toPlot argument must be True or False")
		return None

	if (not dataSource.lower() in ['cmt', 'parayas']):
		print("dataSource argument must be CMT or Parayas")
		return None

	simulation = ownSimulation(dataSource) #  Initialize the simulation
	simulation.processData() # Load the data
	simulation.removeNonValid() # Clean the data
	simulation.transitionProb() #  Calculate the transition probability
	simulation.generateDryWet(days = days) # Generate 0/1 simulation
	simulation.generateAmount(distribution = distribution) # Simulate the rainy days


	if(toPlot.lower() == 'true'):
		plt.plot(list(range(1, len(simulation.resultSimu) + 1)),
			     simulation.resultSimu)
		plt.show()

	print(simulation.resultSimu)
	return(simulation.resultSimu)

simulatePrecip(days = int(sys.argv[1]), distribution = sys.argv[2],
			   toPlot = sys.argv[3], dataSource = sys.argv[4])
