import numpy as np
from matplotlib import pyplot as plt
# import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_json (r'.\data.json')
df.to_csv (r'.\New3.csv', index = None)


BFS = pd.read_csv("New.csv",na_values=["???","??? "])
Astar =pd.read_csv("New.csv",na_values=["???","??? "])


def drawChart(factor):
    barWidth = 0.25
    stepBFS = BFS[factor][1:41]
    stepAstar = BFS[factor][1:41]	
    fig = plt.subplots(figsize =(12, 8))
    index = []
    for i in range(0,len(stepBFS)):
            index.append(i+1)

    # set height of bar
    #IT = [12, 30, 1, 8, 22]
    #ECE = [28, 6, 16, 5, 10]
    #CSE = [29, 3, 24, 25, 17]
    
    # Set position of bar on X axis
    br1 = np.arange(len(stepBFS))
    br2 = [x + barWidth for x in br1]
    #br3 = [x + barWidth for x in br2]
    
    # Make the plot
    plt.bar(br1, stepBFS, color ='r', width = barWidth,
            edgecolor ='grey', label ='BFS')
    plt.bar(br2, stepAstar, color ='g', width = barWidth,
            edgecolor ='grey', label ='A_star')
    #plt.bar(br3, CSE, color ='b', width = barWidth,
    #        edgecolor ='grey', label ='CSE')
    
    # Adding Xticks
    ylab = ""
    if (factor == "Step"):
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

    plt.xticks([barWidth/2 + r for r in range(len(stepBFS))],index)
    if (factor == "mem_used"):
        plt.title("The amount of memory used in "  +  " Testcases")
    elif (factor == "time_used"):
        plt.title("The amount of time elapsed in "  + " Testcases")
    # elif (factor == "Node generated"):
        # plt.title("The amount of node generated in " + map + " Testcases")
    else:
        plt.title("The number of " + factor + " taken in "  + " Testcases")
    plt.legend()
    
    save = ""
    if (factor == "mem_used"):
        save = "memory"
    # elif (factor == "Step"):
    # 	save = "step"
    # elif (factor == "Node generated"):
    # 	save = "nodeGenerated"
    else:
        save = "time_used"
    plt.savefig("./" + save + "_"  + ".png")	


# drawChart("Step","MINI COSMOS")
# drawChart("Step","MICRO COSMOS")
drawChart("time_used")
# drawChart("time_used", "MICRO COSMOS")
drawChart("mem_used")
# drawChart("Memory (MB)","MICRO COSMOS")
# drawChart("Node generated","MINI COSMOS")
# drawChart("Node generated","MICRO COSMOS")

# print(len(BFS))
# print(BFS["Map"][len(BFS)-1])
#print(BFS)
#print(BFS["Step"].count())
#print(BFS["Status"].count("Completed"))