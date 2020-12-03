########################################
#		        IMPORTS                #
########################################
import random
import math
import matplotlib.pyplot as plt
random.seed(177)

########################################
#			PROCESSOR CLASS            #
########################################
class Processor:
	def __init__(self):
		self.load = 0
		self.scheduleTime = 0

########################################
#			GLOBAL VARIABLES           #
########################################
# NUMBER OF PHYSICAL PROCESSORS
K = 1600

# INITIAL DISTRIBUTION PARAMETERS
MEAN = K // 2
STANDARD_DEV = MEAN // 3
LOWER_LOAD_LIMIT = 10
UPPER_LOAD_LIMIT = 1000

# SCHEDULING TIME BOUNDS
TIME_LOWER_BOUND = 100
TIME_UPPER_BOUND = 1000

 
# MAXIMUM NUMBER OF CYCLES (10 ^ 7)
MAX_CYCLES = 10000000

# INITIAL DISTRIBUTION TWO OPTIONS
DISTRIBUTION = "allInOne"
DISTRIBUTION = "Gaussian"
# DISTRIBUTION = "Uniform"


########################################
#			   FUNCTIONS               #
########################################
# RETURNS A RANDOM NUMBER FOLLOWING A UNIFORM DISTRIBUTION
# IN THE RANGE [LOWER_LIMIT, UPPER_LIMIT], BOTH INCLUSIVE
def uniformNumGen(lower_limit, upper_limit):
	return int(round(random.uniform(lower_limit, upper_limit)))


# THIS FUNCTION TAKES AS INPUT THE NUMBER OF PROCESSORS, THE 
# STANDARD DEVIATION AND A MEAN NUMBER. IT RETURNS A RANDOM
# NUMBER USING THE PARAMETERS WHICH FOLLLOWS  A GAUSSIAN 
# DISTIRBUTION. THE MOD % NUMPROCESSORS ENSURES THAT THE 
# GENERATED NUMBER IS WITHIN BOUNDS OF THE PROCESSING ARRAY
def gaussianNumGen(numProcessors, mean, stdDev):
	return int(round(random.gauss(mean, stdDev))) % numProcessors

 
# FUNCTION TO BALANCE NEIGHBOURS OF A PROCESSOR
# IF NOT POSSIBLE THEN THE FUNCTION DOES NOTHING
def balanceNeibor(processors, currProcessor):
	leftNeibor = (currProcessor - 1) % K
	rightNeibor = (currProcessor + 1) % K

	average = math.ceil((processors[leftNeibor].load + processors[rightNeibor].load + processors[currProcessor].load) / 3)

	requireLeft = average - processors[leftNeibor].load
	requireRight = average - processors[rightNeibor].load

	if requireLeft > 0 and requireRight > 0:
		toGive = requireLeft + requireRight
	elif requireLeft > 0:
		toGive = requireLeft
	elif requireRight > 0:
		toGive = requireRight
	else:
		toGive = 0


	# IF IT IS NOT POSSIBLE TO BALANCE THE NEIGHBOURS JUST RETURN
	if processors[currProcessor].load - toGive < 0:
		return

	else:
		if requireLeft > 0:
			processors[leftNeibor].load += requireLeft

		if requireRight > 0:
			processors[rightNeibor].load += requireRight

		processors[currProcessor].load -= toGive


# FUNCTION RETURNS TRUE IF SYSTEM IS BALANCED
def isBalancedSystem(processors):
	for i in range(K):
		if processors[i].load == 0:
			return False
	return True


# DISTRIBUTES LOAD UNITS INITIALLY ACCORDING TO A SPECIFIC DISTRIBUTION
# FIRST EACH PRPCESSOR IS PICKED ACCORDING TO A UNIFORM DISTRIBUTION
# THEN THE PROCESSOR IS ASSIGNED LOAD UNITS BASED ON A GAUSSIAN DISTRIBUTION
def distributeLoads(processors, distribution):
	if distribution == "Gaussian":
		for i in range(len(processors)):
			index = gaussianNumGen(K, MEAN, STANDARD_DEV)
			processors[index].load = uniformNumGen(LOWER_LOAD_LIMIT, UPPER_LOAD_LIMIT)
	elif distribution == "allInOne":
		index = gaussianNumGen(K, MEAN, STANDARD_DEV)
		for i in range(len(processors)):
			processors[index].load += uniformNumGen(LOWER_LOAD_LIMIT, UPPER_LOAD_LIMIT)
	elif distribution == 'Uniform':
		for i in range(len(processors)):
			index = uniformNumGen(0, K - 1)
			processors[index].load = uniformNumGen(LOWER_LOAD_LIMIT, UPPER_LOAD_LIMIT)



# ASSIGNS EACH PROCESSOR A CYCLE NUMBER INITIALLY IN 
# WHICH IT WILL PERFORM LOAD BALANCING THE
# THE ASSIGNMENT FOLLOWS A UNIFORM DISTRIBUTION
def scheduleLoadBalancing(processors):
	for i in range(len(processors)):
		processors[i].scheduleTime = uniformNumGen(TIME_LOWER_BOUND, TIME_UPPER_BOUND)


def simulate():
	# DEFINE K PROCESSORS
	processors = [Processor() for _ in range(K)]
	# DISTIBUTE LOAD UNITS INITIALLY
	distributeLoads(processors, DISTRIBUTION)
	# MAKE SURE THAT INITIAL DISTRIBUTION IS UNBALANCED
	while isBalancedSystem(processors):
		distributeLoads(processors, DISTRIBUTION)
	# SCHEDULE WHEN EACH PROCESOR WILL PERFORM LOAD BALANCING
	scheduleLoadBalancing(processors)

	# RUN UNTIL CONVERGENCE OR MAX CYCLES
	currCycle = 0
	while (not isBalancedSystem(processors) and (currCycle < MAX_CYCLES)):
		# FOR EACH PROCESSOR
		for i in range(K):
			# IF IT IS ITS TURN TO LOAD BALANCE
			if processors[i].scheduleTime == currCycle:
				# BALANCE ITS NEIGHBOURS IF POSSIBLE
				balanceNeibor(processors, i)
				# ASSIGN A NEW SCHEDULE TIME TO PROCESSOR IN FUTURE
				processors[i].scheduleTime += uniformNumGen(TIME_LOWER_BOUND, TIME_UPPER_BOUND)
		currCycle += 1

	return currCycle


########################################
#			   FUNCTIONS               #
########################################
if __name__ == "__main__":
	# totalCycles = simulate()
	# print(K, totalCycles)

	kArr = [5, 10, 50, 100, 200, 400, 600, 800, 1000, 1200, 1500]

	kArr2 = [5, 10, 50, 100, 200, 400, 600, 800, 1000, 1200, 1500 , 3000, 3500, 4000, 5000]

	cycleArr1 = [348, 1508, 3705, 3923, 6551, 7608, 16403, 29556, 34363, 46530, 60264]

	cycleArr2 = [947, 1304, 11446, 30446, 105070, 405866, 884730, 1556413, 2359848, 3396845, 5182883]

	cycleArr3 = [348, 752, 899, 1206, 1947, 2025, 1969, 2282, 1631, 1979, 2000]
	# , 2176, 1668, 1955]

	plt.figure(figsize = (7, 7))
	plt.title("Cycles to Reach Balanced State for Different Number of Processors")
	plt.plot(kArr, cycleArr1, color = 'red', label = "Gaussian")
	plt.plot(kArr, cycleArr2, color = 'blue', label = "allInOne")
	plt.plot(kArr, cycleArr3, color = 'green', label = "Uniform")
	plt.grid(True, linestyle = 'dotted')
	plt.xlabel("Number of Processors in System")
	plt.ylabel("Number of Cycles to Reach a Balanced System")
	plt.legend(loc = "upper right")
	plt.show()



		