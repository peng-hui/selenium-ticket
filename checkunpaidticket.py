import os, sys
import time
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


login_url="https://i.hzmbus.com/webhtml/login"
target_url = "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=%E9%A6%99%E6%B8%AF&xlmc_2=%E7%8F%A0%E6%B5%B7&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO"
target_url = "https://i.hzmbus.com/webhtml/my_order?tab1=0"

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

    def choose_ticket(self):
        while True:
            try:
                self.driver.refresh()
                if self.driver.title == '港珠澳大桥穿梭巴士' or self.driver.title == "HZMB shuttle bus":
                    sleep(1)
                    lists = self.driver.find_elements(By.CLASS_NAME, "li")
                    # the length of the list is the indicator of # of tickets/itmes. 
                    # At the time of my use, if the ticket is not equal to 47, it indicates a success!
                    if len(lists) == 47:
                        print('yes')
                    else:
                        ### can send mail.

            except Exception as e:
                pass

    def finish(self):
        self.driver.quit()

def main():
    try:
        con = Ticekt()
        con.enter_website()
        con.choose_ticket()

    except Exception as e:
        print(e)
        con.finish()

if __name__ == '__main__':
    main()
