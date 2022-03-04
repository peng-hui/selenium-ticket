import os, sys
import time
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


login_url="https://i.hzmbus.com/webhtml/login"
target_url = "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=%E9%A6%99%E6%B8%AF&xlmc_2=%E7%8F%A0%E6%B5%B7&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO"

class Ticket(object):
    def login(self):
        self.driver.get(login_url)
        WebDriverWait(self.driver, 10).until(EC.title_is('Login Page'))
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        # account
        account_name = ""

        inputs[0].clear()
        inputs[0].send_keys(account_name)

        passwd = ""
        inputs[2].clear()
        inputs[2].send_keys(passwd)
        login_button = self.driver.find_elements(By.CLASS_NAME, "login_btn")
        sleep(1)
        login_button[0].click()
        WebDriverWait(self.driver, 20).until(EC.title_is('HZMB shuttle bus'))

        print("login successfully")
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb")) 
        print("save your credential (cookies) into a file cookies.pkl")
        self.driver.get(target_url) 
     

    def check_ticket(self, nol=47):
        order_url = "https://i.hzmbus.com/webhtml/my_order?tab1=0"
        self.driver.get(order_url)
        lists = self.driver.find_elements(By.CLASS_NAME, "li")
        if len(lists) != nol:
            print('yes')
        self.driver.get(target_url)

    '''
    a dayid is used to control which date of the tickets.
    the scripts automatically buys the tickets with default time-in-day, i.e., I did not implement the option to select specific in-day time of tickets
    
    Also, I do not clearly know the successful page status. Currently I simply check the page title.

    The script will go into capture() when encountering unexpected page title. It might indicate a success.

    A general notice is that, the tickets can only be reserved for 15 minutes if you do not pay.
    '''
    def choose_ticket(self, dayid):
        count = 0
        while True:
            try:
                count += 1
                if count >10:
                    self.check_ticket()
                    count = 0

                self.driver.refresh() 
                WebDriverWait(self.driver, 30).until(EC.title_is('HZMB shuttle bus'))
                print('sele date')
                sleep(1)
                date = self.driver.find_elements(By.CLASS_NAME, "sele_date")
                sele_date = date[0]
                sele_date.click()
                sleep(1)

                '''
                calendar = self.driver.find_elements(By.CLASS_NAME, "wh_content_all")
                changer = self.driver.find_elements(By.CLASS_NAME, "wh_top_changge")
                array2 = self.driver.find_elements(By.CLASS_NAME, "wh_jiantou2")
                print('swift to next month')
                array2[0].click()
                '''
                print('day')
                sleep(1)
                days = self.driver.find_elements(By.CLASS_NAME, "wh_content_item")
                days[dayid].click()
                print('select day')
                sleep(1)
                inputs = self.driver.find_elements(By.TAG_NAME, "input")
                name = ""
                inputs[2].clear()
                inputs[2].send_keys(name)

                idcardnum = ""
                inputs[3].clear()
                inputs[3].send_keys(idcardnum)

                bottom = self.driver.find_elements(By.CLASS_NAME, "bottom")
                bottom = bottom[0]
                agree = self.driver.find_elements(By.CLASS_NAME, "hint_icon")
                agree = agree[0]
                print('agreement signed!')
                agree.click()
                sleep(1)
                print('submit request')
                bottom.click()
                sleep(4)
            except Exception as e:
                pass

    def finish(self):
        self.driver.quit()

def main():
    try:
        con = Ticket()
        print('launch browser') 
        con.driver = webdriver.Chrome()  
        con.login()
        con.choose_ticket(int(sys.argv[1]) + 7)
        # 22 - 15

    except Exception as e:
        print(e)
        con.finish()

if __name__ == '__main__':
    main()
