import os, sys
import time
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


login_url="https://i.hzmbus.com/webhtml/login"
target_url = "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=%E9%A6%99%E6%B8%AF&xlmc_2=%E7%8F%A0%E6%B5%B7&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO"

class Ticket(object):
    def set_cookie(self):
       self.driver.get(login_url)
       sleep(5)
       
       while self.driver.title == '登录页' or self.driver.title == "Login Page":
           # for authentication, a user has to interact with the page and type its uname and passwd.
           # the credential will be saved as a cookie thus no more authentication is in need
           sleep(1)
       print("login successfully")
       pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb")) 
       print("save your credential (cookies) into a file cookies.pkl")
       self.driver.get(target_url) 

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            print('load cookie and try to authenticate')
        except Exception as e:
            print(e)
            
    def login(self):
        if not os.path.exists('cookies.pkl'):
            self.set_cookie()
        else:
            self.driver.get(target_url)
            self.get_cookie()
    
     
    def enter_website(self):
        print('launch browser') 
        self.driver = webdriver.Chrome()  
        self.login()                    

    def capture(self):
        while True:
            print('capture!!')
            sleep(5)

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
                if self.driver.title == '港珠澳大桥穿梭巴士' or self.driver.title == "HZMB shuttle bus":
                    print('sele date')
                    sleep(1)
                    date = self.driver.find_elements(By.CLASS_NAME, "sele_date")
                    sele_date = date[0]
                    sele_date.click()
                    sleep(1)

                    calendar = self.driver.find_elements(By.CLASS_NAME, "wh_content_all")
                    changer = self.driver.find_elements(By.CLASS_NAME, "wh_top_changge")
                    array2 = self.driver.find_elements(By.CLASS_NAME, "wh_jiantou2")
                    print('swift to next month')
                    array2[0].click()
                    print('day')
                    sleep(1)
                    days = self.driver.find_elements(By.CLASS_NAME, "wh_content_item")
                    days[dayid].click()
                    print('select day')
                    sleep(1)

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
        con.enter_website()
        con.choose_ticket(int(sys.argv[1]))

    except Exception as e:
        print(e)
        con.finish()

if __name__ == '__main__':
    main()
