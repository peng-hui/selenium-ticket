import os, sys
import time
import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By


login_url="https://i.hzmbus.com/webhtml/login"
target_url = "https://i.hzmbus.com/webhtml/ticket_details?xlmc_1=%E9%A6%99%E6%B8%AF&xlmc_2=%E7%8F%A0%E6%B5%B7&xllb=1&xldm=HKGZHO&code_1=HKG&code_2=ZHO"

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
    def check_ticket(self, nol=47):
        order_url = "https://i.hzmbus.com/webhtml/my_order?tab1=0"
        self.driver.get(order_url)
        lists = self.driver.find_elements(By.CLASS_NAME, "li")
        if len(lists) != nol:
            print('yes')
        self.driver.get(target_url)

    def choose_ticket(self, dayid):
        count = 0
        while True:
            try:
                count += 1
                if count >10:
                    self.check_ticket()
                    count = 0

                self.driver.refresh()                   #刷新页面
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
                    print('jiantou')
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
                    print('agree')
                    agree.click()
                    sleep(1)
                    print('submit')
                    bottom.click()
                    sleep(4)
            except Exception as e:
                pass

    def finish(self):
        self.driver.quit()

def main():
    try:
        con = Concert()
        con.enter_concert()
        con.choose_ticket(int(sys.argv[1]))

    except Exception as e:
        print(e)
        con.finish()

if __name__ == '__main__':
    main()
