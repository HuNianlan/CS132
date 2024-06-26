---
marp: true
math: mathjax
---

# Executive Summary Team 07 Project 1
&emsp;&emsp;Xinyue Hu (Requirement), Wenlin Zhu (Development), Jintong Luo (Validation)

---

## Introduction

- In this project, we are developing a software that can control and schedule the movement of two cooperate elevators in a three-floor building according to people’s need.
- By providing interconnected interfaces to passengers outside and inside the elevators, the system can provide security guarantees and work efficiently.
---

# Our Design

---

## the basic requirement for the elevator:

- Open/close door according to users' needs
- bring user to his/her taget floor

---

## decision-making system && system processor

- all signals should be handled by the system processor
- give information to UI
- two elevator works indepandently
  - one failure may not affect the other
- the system should be user-friendly
- the system should work efficiently and safely 

---

## the system should be user-friendly

- easy to access
- good location
- provide currect information !!!
  -  InternalUI should be consistent with ExternalUI 
  -  systemUI should be consistent with the real state
- efficiency
- safety

---

### efficiency

- optimal solution for common case (e.g. compared to walking upstairs/downstairs)
- shedule the two elevator to meets the users’ needs as fast as possible
- energy cost ( `least significant`)



---

### safety
- user safety
  - alarm button
  - monitor system

- "hardware" safety (or safe control) 
  <!-- 打引号是因为并不是真正的硬件，而是由软件控制的一些物理世界的参数 -->
  - safe moving speed
  - safe open time (without close button on)
  - safe maximum weight

---
<!-- _color: red-->

- software safety
  - ban third party modification
  - software update
    - integrity 
    <!-- not modified or deleted in an unauthorized and undetected manner -->
    - authentication
    - (confidentiality)
  <!--  authentication: The process of establishing confidence in the identity of users or information systems.  
   The property that sensitive information is not disclosed to unauthorized individuals, entities, or processes.
  -->



---
<!-- _color: red-->
## possible update

-  adaptive model (collect data and update system)
    - may cause privacy concern


---
## Our questions

- Is a database necessary? 
- Is the part `software safety` necessary?

---
## Our schedule

&emsp;&emsp;We have completed the basic requirement part, which you could find in our Gitlab repository, and we have been drawing the UML for development part then. After this consultation, we would start to develop our system via Python.

---
# Thank You!