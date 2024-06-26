import sys
sys.path.append("src")
from simulator import autotest
# T2.1.1: Test Change Pin
STRING_LIST1 = [
    "open_app",
    "log_in@2023123456@111111#1",
    "change_password@123456#1",
    "log_out#1",
    "log_in@2023123456@111111#1",
    "log_in@2023123456@123456#1",
    "close_app#1"
]



#T2.1.2: Test Transfer
STRING_LIST2 = [
    "create_account@222222",   
    "deposit_cash@1000",
    "open_app"
    "open_app"
    "log_in@id@222222#1", 
    "transfer_money@2023123456@400#1",
    "log_in@20231223456@111111#2",
    "query#1",    
    "query#2"               
]


#T2.2.1: Test Account Operation
STRING_LIST3 = [
    "create_account@222222",   
    "change_password@123456",
    "close_account"
    "open_app"
    "log_in@id@222222#1",     
    "log_in@id@123456#1",         
]

#T2.2.2: Test Money Operation
STRING_LIST4 = [
    "insert_card@2023123456",   
    "deposit_cash@500",      
    "withdraw_cash@200@111111", 
    "create_account@222222",  
    "transfer_money@id@100", 
    "query" 
    "return_card"
]

#T2.3.1: Test Money Operation
STRING_LIST5 = [
    "create_account@222222",   
    "change_password@123456",
    "deposit_cash@700",  
    "open_app",
    "log_in@id@123456#1", 
    "transfer_money@2023123456@400#1",
    "withdraw_cash@200@123456",  
    "query#1",
    "log_out#1",
    "close_app#1",
    "transfer_money@2023123456@100",
    "query",
    "close_account"
]

#########################
# The testcase below involves in creating account, and thus you can test with api by removing the 
# STRING_LIST in main.py with the corresponding STRING_LIST
#autotest(STRING_LIST3)
# autotest(STRING_LIST2)
# autotest(STRING_LIST4)
# autotest(STRING_LIST5)


if __name__=='__main__':
    autotest(STRING_LIST1)
