import numpy as np 					# Generates Random Numbers
import math							# Used for mathematical functions e.g. Exponential
import matplotlib.pyplot as plt     # Used to plot graphs
import random
# np.random.seed(199)		    		# Use the same seed to get consistent results in plots
random.seed(199)

# Use Number of memories + 1 
# e.g. for 2048 memories this 
# value will be 2019
numMemories = 2049

# For the Gaussian workload case
# this is the standard deviation
stdDev = 20

# Processing Element Object Class
class ProcessingElement():
	def __init__(self):
		self.memRequested = -1
		self.waitCounter = 0
		self.totalRequests = 0
		self.totalWaitTime = 0

	def setMemory(self, value):
		self.memRequested = value

	def getMemory(self):
		return self.memRequested

	def setWaitCounter(self, value):
		self.waitCounter = value

	def getWaitCounter(self):
		return self.waitCounter

	def setTotalWaitTime(self, value):
		self.totalWaitTime = value

	def getTotalWaitTime(self):
		return self.totalWaitTime

	def setTotalRequests(self, value):
		self.totalRequests = value

	def getTotalRequests(self):
		return self.totalRequests


# Memory Module Object Class
class MemoryModule():
	def __init__(self):
		self.inUse = False

	def setUse(self, value):
		self.inUse = value

	def getUse(self):
		return self.inUse

# Returns a random number folllowing a uniform distribution
# in the range [0 to number of memory modules)
def uniformNumGen(numOfMemories):
	# return np.random.randint(0, numOfMemories)
	return int(round(random.uniform(0, numOfMemories - 1)))

# This function takes as input the number of memories,
# the standard deviation and a mean number. It returns
# a random number using the parameters which folllows 
# a Gaussian Distirbution. The mod % numOfMemories ensures
# that the generated number is within bounds of the memory
# modules
def gaussianNumGen(numOfMemories, mean, stdDev):
	# return int(round(np.random.normal(mean, stdDev))) % numOfMemories
	return int(round(random.gauss(mean, stdDev))) % numOfMemories


# Given parameters current average wait time
# and previous average wait time it returns
# True if values differ less than 0.02% otherwise
# it returns False
def convergence(currVal, prevVal):
	if prevVal == 0:
		return False
	# return (currVal - prevVal < 0.0002)
	return (((currVal - prevVal) / prevVal) < 0.02)


# Given an array of processing elements this function
# returns the average wait time of all processors.
def findAvgWaitTime(processingArray):
	total = 0
	for processor in processingArray:
		total += ((processor[0].getTotalWaitTime()) / processor[0].getTotalRequests())
	return total/len(processingArray)


# Given an array of processing elements this fucntion
# returns a sorted array based on proiorites of the
# processing elements
def prioritize(processingArray):
	toReturn = []
	for processor in processingArray:
		currWaitTime = processor[0].getWaitCounter()
		priority = (processor[2] + 1) / (math.exp(currWaitTime))
		toReturn.append((processor[0], priority, processor[2]))
	return sorted(toReturn, key = lambda x: x[1])


# Given number of processing elements and the type of workload
# this fucntion returns the average memory access time varied
# accross the the number of memory modules
def getAvgWaitTime(numProcessors, workload):
	# The results of average wait times (initially empty)
	avgWaitTimes = []
	for memory in range(1, numMemories):
		# print(memory)
		# Processing Array is a list of tuples (Processor, Priority, Original Index)
		processingArray = [(ProcessingElement(), i, i) for i in range(numProcessors)]
		memoryArray = [MemoryModule() for i in range(memory)]
		prevAvgWaitTime = 0
		# If the workload is guassian then create an array of 
		# random numbers using uniform distribution. This array
		# will store the means for all processor for a fixed number
		# of memory modules
		if workload == "Gaussian":
			# print('here')
			meanArray = [uniformNumGen(memory) for i in range(len(processingArray))]
		# Keep cycling until convergence
		while True:
			processingArray = prioritize(processingArray)
			for processor in processingArray:
				# If processor is not in waiting list makes a new request
				if processor[0].getMemory() == -1:
					if workload == 'Uniform':
						requestedMem = uniformNumGen(memory)
						# print("Uniform :: " + str(requestedMem))
					elif workload == 'Gaussian':
						requestedMem = gaussianNumGen(memory, stdDev, uniformNumGen(memory))
						# requestedMem = gaussianNumGen(memory, stdDev, meanArray[processor[2]])
						# print("Gaussian :: " + str(requestedMem))
					#Add to the number of requests of this processor
					processor[0].setTotalRequests(processor[0].getTotalRequests() + 1)
				# If processor is in waiting list it maintains its previous request
				else:
					requestedMem = processor[0].getMemory()
				# If memory module is in use store what memory
				# module was requested by the processor
				if memoryArray[requestedMem].getUse() == True:
					processor[0].setMemory(requestedMem)
					processor[0].setWaitCounter(processor[0].getWaitCounter() + 1)
					processor[0].setTotalWaitTime(processor[0].getTotalWaitTime() + 1)
				# If module is not in use assign this processor the memory module
				elif memoryArray[requestedMem].getUse() == False:
					processor[0].setMemory(-1)
					memoryArray[requestedMem].setUse(True)
					processor[0].setWaitCounter(0)
			# Find out if the simulation has converged or not to break
			currAvgWaitTime = findAvgWaitTime(processingArray)
			if convergence(currAvgWaitTime, prevAvgWaitTime):
				avgWaitTimes.append(currAvgWaitTime)
				break
			prevAvgWaitTime = currAvgWaitTime
			# Free all memory modules at end of cycle
			for memModule in memoryArray:
				memModule.setUse(False)
	return avgWaitTimes


if __name__ == "__main__":
	# Define the Workload Assumption
	# workload = 'Uniform'
	# workload = 'Gaussian'

	# The number of processing elements that we will be using
	numProcessors = [2] #2, 4, 8, 16, 32, 64


	# For each, number of processors compute the 
	# average wait time for all configurations of
	# the memory modules
	for processors in numProcessors:
		plt.figure(figsize = (5,5))
		avgWaitTimePlot = getAvgWaitTime(processors, "Uniform")
		plt.title("Number of Processors = " + str(processors))
		plt.plot(np.log2([i for i in range(1, numMemories)]), avgWaitTimePlot, color = 'red', label = "Gaussian")
		# plt.grid(True, linestyle = 'dotted')
		# plt.xlabel("Number of Memory Modules")
		# plt.ylabel("Average Wait Time")

	for processors in numProcessors:
		# plt.figure(figsize = (5,5))
		avgWaitTimePlot = getAvgWaitTime(processors, "Gaussian")
		plt.title("Number of Processors = " + str(processors))
		plt.plot(np.log2([i for i in range(1, numMemories)]), avgWaitTimePlot, color = 'blue', label = "Uniform")



	plt.legend(loc = "upper right")
	plt.grid(True, linestyle = 'dotted')
	plt.xlabel("Number of Memory Modules (log base 2)")
	plt.ylabel("Average Wait Time")
	plt.show()