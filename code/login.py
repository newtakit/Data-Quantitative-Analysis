import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import time

# ตั้งค่าบัญชีและเซิร์ฟเวอร์
account = *********
password = '********'
server = '********'
# ส่วนในการเชื่อมต่อ
if not mt5.initialize():
    print("MT5 เชื่อมต่อไม่สำเร็จ")
    mt5.shutdown()
else:
    print("MT5 เชื่อมต่อสำเร็จ")

# ในส่วน การ Login to MT5 account
if not mt5.login(account, password, server):
    print("MT5 loginไม่สำเร็จ")
    mt5.shutdown()
else:
    print("MT5 loginสำเร็จ")

#ส่วนในการดูสถานะต่างๆในAC.

    account_info = mt5.account_info()
if account_info is not None:
        print("Balance:", account_info.balance)
        print("Equity:", account_info.equity) 
        print("Profit:",account_info.profit) 
else:
        print("ดึงข้อมูลบัญชีไม่สำเร็จ")