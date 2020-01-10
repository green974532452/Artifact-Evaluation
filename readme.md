**Introduction**

This program randomly generates synthetic job sets, calculates the makespan for each generated job set, stores the experimental data, and eventually draws the figures (e.g., Fig.4 to 6) in the paper. Note that we only prepare simplified experiments (e.g., by reducing the number of samples over which the results are averaged) with shorter running times. Although the generated figures and data may be slightly different from those in the paper, the overall trend of the data is same.

**Quick-start**

Before attempting to run Artifact Evaluation on Windows, you must have the following installed:

l Python 3.7.3  64bit（must be on your PATH）

l  Numpy package,Pandas package and Matplotlib package Installed:

Ø `pip install pandas`

Ø `python -m pip install -U pip`

Ø `Python -m pip install -U matplotlib `

Run the Artifact Evaluation source program:

l Double click the start-up.bat file to input the Artifact Evaluation folder path to run the source program.(For example: the Artifact Evaluation folder is placed in the G root directory)

Ø `Please enter Artifact Evaluation folder file path:G:\`` `

Program running time is about 50 seconds.

Run the Artifact Evaluation test program:

l Double click the start-up-test.bat file to input the Artifact Evaluation folder path to run the test program.(For example: the Artifact Evaluation folder is placed in the G root directory)

Ø `Please enter Artifact Evaluation folder file path:G:\`

```
Run: 100 tests in: 2.44 seconds
Impt-I Success: 100
Impt-I Errors: 0
Impt-I* Success: 100
Impt-I* Errors: 0
Impt-II Success: 100
Impt-II Errors: 0
Impt-B Success: 100
Impt-B Errors: 0
```

 

**Requirement**

To compile Artifact Evaluation:

-  Artifact Evaluation (If the package name is not “Artifact Evaluation”, change it to “Artifact Evaluation”. otherwise the script may run wrong.)


-  [Python](https://www.python.org/)  https://www.python.org/


-  Matplotlib  https://matplotlib.org/


-  Numpy  https://pypi.org/project/numpy/


-  Pandas


To test Artifact Evaluation:

- test 


-  start-up-test.bat


Computer system environment：

- System: Windows 10 x64


-  Processor: Intel(R) Core(TM) i5-7500 CPU @ 3.40GHz 3.41 GHz


- RAM: 8.00GB


**Description**

The artefact evaluation contains four folders, i.e., source, test, data, and figures. 

# source

The folder “source” contains the programs that randomly generate synthetic job sets, calculate the makespans for the generated job sets, and automatically draw the figures (e.g., Fig.4-6) used in the paper. There are two folders in the folder “source”, namely, “linear” and “nonlinear”, which respectively deal with the linear-speedup jobs and nonlinear-speedup jobs. In the following, we introduce the files in the folder “linear” (and “nonlinear”).

  generator.py:  generate the synthetic job sets

  alpha.py :     calculate the makespan by using Impl-I and Impl-I*

  ABalg.py :     calculate the makespan by using Impl-II

  appr.py :      calculate the makespan by using Impl-B

  drawJob.py:  draw Fig. 4

  drawCore.py: draw Fig. 5

  drawBeta.py: draw Fig. 6

  globalVarJob.py: store the global variables used to draw Fig. 4

  globalVarCore.py: store the global variables used to draw Fig. 5

  globalVarBeta.py: store the global variables used to draw Fig. 6

  mainJob.py:  work for Fig. 4 

  mainCore.py: work for Fig. 5

  mainBeta.py : work for Fig. 6

The program runs in the following way. First, generater.py generates random job sets. Then, alpha.py, ABalg.py and appr.py calculate the makespan for the generated job sets, and store the experimental data to excel files in folder "data". Using the stored data, drawJob.py, drawCore.py and drawBeta.py eventually draw the figures in folder "figures". 

# test

In the test, we randomly generate 100 job sets with job number ranging from 10 to 100, core number ranging from 4 to 64, and beta ranging from 0.1 to 1, and then use alpha.py, ABalg.py and appr.py to solve the 100 job sets.

# data

In the folder “data”, “Fig.xxx.xlsx” stores the data that is used to generate “Fig.xxx” in the paper. In each excel table, the first column is the index of the random example. The second column is the makespan calculated by Impl-I. The third column is the makespan calculated by Impl-I*. The fourth column is the makespan calculated by Impl-II.  The fifth column is the makespan calculated by Impl-B. The sixth column is the lower bound of the makespan. 

#  figures

In the folder “figures”, the file namely “Fig.xxx.png” corresponds to the figure Fig.xxx in the paper.

 