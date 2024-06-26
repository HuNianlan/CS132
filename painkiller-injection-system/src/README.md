# Team 7 Project 2: Painkiller System

* To run the painkiller system, please use `main.py`.
* In addition, we provide a test file `test.py` as an example for testing with txtcases.

* The standard for txtcases are as follows:

initialization: set simulation speed (real time 1s -> simulated time 2min)

case #1:
set baseline 0.01ml/min&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;set baseline as 0.01ml/min
set bolus 0.30ml/shot&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;set bolus as 0.30ml/shot
baseline On&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;trun on baseline
(simulated time: about 30min later) Request Bolus&emsp;&emsp;patient requests for bolus（success）
(simulated time: about 75min later) Request Bolus&emsp;&emsp;patient requests for bolus（fail）
baseline Off&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;trun off baseline
set baseline 0.10ml/min&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;set baseline as 0.10ml/min
baseline On&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;trun on baseline
(simulated time: about 1-3min later)  &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;  baseline reaches hour limit, stop
(simulated time: 10min later)&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;inject baseline every 10 min
(after the day limit is reached)&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;  reach day limit, stop
