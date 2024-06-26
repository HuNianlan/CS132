import sys
sys.path.append("src")
from simulator import autotest

#T3.1.1: Test “ATM Deposit Cash”
STRING_LIST1 = [
    "insert_card@2023123456",   
    "deposit_cash@500",       
    "query"                  
]


#T3.1.2: Test “ATM Withdraw Cash”
STRING_LIST2 = [
    "insert_card@2023123456",    
    "deposit_cash@1000",      
    "withdraw_cash@300@111111",
    "query"          
]


#T3.1.3: Test “ATM Transfer”
STRING_LIST3 = [
    "insert_card@2023123456",    
    "deposit_cash@1000", 
    "create_account@222222",   
    "transfer_money@id@400", 
    "query", 
    "open_app",           
    "log_in@id@222222#1",
    "query#1", 
    "close_app#1"
]

#T3.1.4: Test “ATM Query Account”
STRING_LIST4 = [
    "insert_card@2023123456",   
    "deposit_cash@500",      
    "withdraw_cash@200@111111", 
    "create_account@222222",  
    "transfer_money@id@100", 
    "query"  
]

#T3.2.1: Test “APP Reset Information”
STRING_LIST5 = [
    "open_app",
    "log_in@2023123456@111111#1",
    "change_password@123456#1",
    "log_out#1",
    "log_in@2023123456@111111#1",
    "log_in@2023123456@123456#1",
    "close_app#1"
]

#T3.2.2: Test “APP Transfer”
STRING_LIST6 = [
    "create_account@222222",   
    "deposit_cash@1000",
    "open_app",
    "open_app",
    "log_in@id@222222#1", 
    "transfer_money@2023123456@400#1",
    "log_in@20231223456@111111#2",
    "query#1",           
    "query#2",
    "close_app#1"               
]

#T3.2.3: Test “APP Query Account”
STRING_LIST7 = [
    "create_account@222222"
    "deposit_cash@500"
    "open_app",
    "log_in@id@222222#1",
    "transfer_money@2023123456@100#1", 
    "query#1",
    "close_app#1"
]

#########################
# The testcase below involves in creating account, and thus you can test with api by removing the 
# STRING_LIST in main.py with the corresponding STRING_LIST
# STRING_LIST3
# STRING_LIST4
# STRING_LIST6
# STRING_LIST7

if __name__=='__main__':
    # autotest(STRING_LIST1)
    # autotest(STRING_LIST2)
    autotest(STRING_LIST5)

