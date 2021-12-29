import os, sys
import time
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


login_url="https://i.hzmbus.com/webhtml/login"
target_url = "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=%E9%A6%99%E6%B8%AF&xlmc_2=%E7%8F%A0%E6%B5%B7&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO"
target_url = "https://i.hzmbus.com/webhtml/my_order?tab1=0"

class Concert(object):
    def set_cookie(self):
       self.driver.get(login_url)
       sleep(5)
       
       while self.driver.title == '登录页' or self.driver.title == "Login Page":
           # wait in the login page until successful
           sleep(1)
       print("login successfully")
       pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb")) 
       print("save cookies")
       self.driver.get(target_url) 

    def get_cookie(self):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))#载入cookie
            for cookie in cookies:
                self.driver.add_cookie(cookie)
            print('load cookie')
        except Exception as e:
            print(e)
            
    def login(self):
        if not os.path.exists('cookies.pkl'):
            self.set_cookie()
        else:
            self.driver.get(target_url)
            self.get_cookie()
    
     
    def enter_concert(self):
        print('launtch browser') 
        self.driver = webdriver.Chrome()  
        # self.driver.maximize_window()  
        self.login()                    
        #self.driver.refresh()

    def capture(self):
        while True:
            print('capture!!')
            sleep(5)

    def choose_ticket(self, dayid=14):
        while True:
            try:
                self.driver.refresh()                   #刷新页面
                if self.driver.title == '港珠澳大桥穿梭巴士' or self.driver.title == "HZMB shuttle bus":
                    sleep(1)
                    lists = self.driver.find_elements(By.CLASS_NAME, "li")
                    if len(lists) == 47:
                        print('yes')
                    else
            except Exception as e:
                pass

    def finish(self):
        self.driver.quit()

def main():
    try:
        con = Concert()
        con.enter_concert()
        con.choose_ticket()

    except Exception as e:
        print(e)
        con.finish()

if __name__ == '__main__':
    main()
