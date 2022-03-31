import numpy as np
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt
import pandas as pd




DFS = pd.read_csv("New.csv",na_values=["???","??? "])
# Astar =pd.read_csv("New.csv",na_values=["???","??? "])


def drawChart(factor,map):
	stepDFS = []
	stepAstar = []
	stepDFS = DFS[factor][0:10]
	# stepAstar = DFS[factor][1:41]


	barWidth = 0.25
	fig = plt.subplots(figsize =(12, 8))

	index = []
	for i in range(0,len(stepDFS)):
			index.append(i+1)

	# set height of bar
	#IT = [12, 30, 1, 8, 22]
	#ECE = [28, 6, 16, 5, 10]
	#CSE = [29, 3, 24, 25, 17]
	
	# Set position of bar on X axis
	br1 = np.arange(len(stepDFS))
	br2 = [x + barWidth for x in br1]
	#br3 = [x + barWidth for x in br2]
	
	# Make the plot
	plt.bar(br1, stepDFS, color ='r', width = barWidth,
			edgecolor ='grey', label ='DFS')
	# plt.bar(br2, stepAstar, color ='g', width = barWidth,
	# 		edgecolor ='grey', label ='A_star')
	#plt.bar(br3, CSE, color ='b', width = barWidth,
	#        edgecolor ='grey', label ='CSE')
	
	# Adding Xticks
	ylab = ""
	if (factor == "steps"):
		ylab = "Step"
	elif (factor == "time_used"):
		ylab = "sec"
	# elif (factor == "Node generated"):
		# ylab = "Node"
	else:
		ylab = "Kb"

	plt.xlabel('TC', fontweight ='bold', fontsize = 15)
	plt.ylabel(ylab, fontweight ='bold', fontsize = 15)
	#plt.xticks([(r + barWidth) for r in range(len(IT))],
	#        ['2015', '2016', '2017', '2018', '2019'])

	plt.xticks([barWidth/2 + r for r in range(len(stepDFS))],index)
	if (factor == "mem_used"):
		plt.title("The amount of memory used in " + map +  " Testcases")
	elif (factor == "time_used"):
		plt.title("The amount of time elapsed in " + map + " Testcases")
	else:
		plt.title("The number of " + factor + " taken in " + map + " Testcases")
	plt.legend()
	
	save = ""
	if (factor == "mem_used"):
		save = "memory"
	elif (factor == "steps"):
		save = "step"
	else:
		save = "time_used"
	plt.savefig("./" + save + "_" + map + ".png")	



drawChart("time_used", "5x5")
drawChart("mem_used","5x5")
drawChart("steps","5x5")
