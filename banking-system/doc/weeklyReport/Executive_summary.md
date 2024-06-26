# Executive Summary Team 07 Project 2

&emsp;&emsp;Jintong Luo (Requirement), Xinyue Hu (Development), Wenlin Zhu (Validation)

---

## Introduction

&emsp;&emsp;In this project, we are developing a software that can manage a banking system correctly and safely. The system would provide a functional interface of both APP and ATM for users, that means our users could access the service both online and with the ATM machines. Through the interface, users could get services like open & close accounts, deposit & withdraw cash and transfer efficiently.

---

## Our design & basic functions

---

### Functional requirements

&emsp;&emsp;Our target customer is those who prefer online payment, since we provide the APP service which could benefit transfer a lot. We would provide the services below,

- Open account
- Close account
- Deposit cash
- Withdraw cash
- Transfer
- Transactions record

&emsp;&emsp;If we complete the development of this phase, we might add more services like,

- Online payment
- Cooperate with other institution, e.g. pay for the insurance , tuition fee online via our APP

---

### Nonfunctional requirements

&emsp;&emsp;As a banking system, our design should be both efficient and safe, that is

- The users could get clear instruction from the system UI.
- The system would protect the property of users by methods like checking passwords, asking twice before the users make his decision and saving the encoded passwords in the database.

---

## Our schedule

&emsp;&emsp;We have completed the requirement part, which you could find in our Gitlab repository, and we have been drawing the UML for development part then. After this consultation, we would start to develop our system via Python.

&emsp;&emsp;For your convenience, we will provide some useful UML then.

---

&emsp;&emsp;The participants of activities relating to banking system can be categorized into User, APP and ATM. The relationship of them are as follows:

![Class diagram](UML/class_diagram.jpg)

---

&emsp;&emsp;The relationships between the user and the banking system are shown as follows:

![Class diagram relationship](UML/class_diagram_relationship.jpg)

---

&emsp;&emsp;In addition, the system can achieve the following use cases from the user's and the bank's perspectives:

![Use case diagram](UML/use_case_diagram.jpg)

---

## Our questions

- What is the formula , i.e. input & output, for our development?
- What should be included in the system architecture? Are they releted to our development?
- If we consider the hackers who might attack our database for information, e.g. passwords, what should be the intensity of our encryption algorithm?

---

## Thank you!
