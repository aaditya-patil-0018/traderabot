# Importing needed modules
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from mail import Sendmail
import sqlite3
import time

'''
Things to change
1. Mail Format
2. Sub Category has further Sub Categories
3. Select on the Filter
4. Self recheck system
5. Try to make the process recurrent
'''

class Tradera:
    def __init__(self, category, subcategory, subsubcategory=1):
        # try:
            # self.driver = webdriver.Firefox(executable_path=path)
        self.driver = webdriver.Firefox()
        # except:
        #     self.driver = webdriver.Chrome()
            # self.driver = webdriver.Chrome(executable_path="C:\\Users\\Hisret\\Desktop\\Tradera\\aaditya_patil-attachments\\chromedriver.exe")
        self.category = int(category)
        self.subcategory = int(subcategory)
        self.subsubcategory = int(subsubcategory)
        self.driver.get("https://www.tradera.com/")
        time.sleep(4)
        self.cookie()
        time.sleep(4)
        self.select_category()
        time.sleep(8)
        self.select_sub_sub_category()
        # self.check_ad()

    def cookie(self):
        cookie_customization = self.driver.find_elements_by_class_name("css-1hy2vtq")[0]
        cookie_customization.click()
        reject_all = self.driver.find_elements_by_class_name("css-10h2kwl")[0]
        reject_all.click()
        save_and_exit = self.driver.find_elements_by_class_name("css-47sehv")[1]
        save_and_exit.click()

    def select_category(self):
        category_button = self.driver.find_elements_by_class_name('btn.hamburger.hamburger--squeeze.site-dropdown__hamburger.ml-md-1.ml-lg-0.ml-xl-0.btn-sm')[0]
        category_button.click()
        time.sleep(4)
        category_names = self.driver.find_elements_by_class_name("text-left.flex-grow")
        category_names[self.category - 1].click()
        time.sleep(4)
        subcategory_names = self.driver.find_elements_by_class_name("site-dropdown__item.d-flex.flex-row.align-items-center.site-dropdown__item-default.pl-5")
        self.subcategoryname = subcategory_names[self.subcategory - 1].text
        subcategory_names[self.subcategory - 1].click()
    
    def select_sub_sub_category(self):
        sub_sub_cat = self.driver.find_elements_by_class_name("item-name--3qMBC")
        # asub_sub_cat = sub_sub_cat.find_elements_by_tag_name('li')
        # print(asub_sub_cat)
        actual_sub_sub_cat = []

        print('-'*100)
        print(self.subcategoryname)
        print('-'*100)

        tablename1 = self.subcategoryname
        tablename1 = tablename1.replace(" ","")
        if '&' in tablename1:
            tablename1 = tablename1.replace('&', '')
        if ',' in tablename1:
            tablename1 = tablename1.replace(',','')   
        if '-' in tablename1:
            tablename1 = tablename1.replace('-','')

        count = 1
        # print(len(sub_sub_cat))
        for i in sub_sub_cat:
            if count > 2:
                actual_sub_sub_cat.append(i)
                con = sqlite3.connect('category.db')
                cur = con.cursor()
                print(tablename1)
                try:
                    cur.execute(f"CREATE TABLE s{tablename1} (id integer PRIMARY KEY, subsubcategoryname text NOT NULL)")
                except:
                    pass
                # try:
                cur.execute(f"INSERT INTO s{tablename1} (id, subsubcategoryname) VALUES(?,?)", (count-2, i.text))
                # except:
                #     pass
                print(i.text)
            count += 1
        actual_sub_sub_cat[0].click()
        

    def check_ad(self):
        green_links = []
        item_cards = self.driver.find_elements_by_class_name("item-card-inner-wrapper")
        for i in range(len(item_cards)):
            website_url = self.driver.current_url
            if website_url == 'https://tradera.com/' or website_url == "https://www.tradera.com/":
                self.driver.forward()
                pass
            html = self.driver.find_element_by_tag_name('html')
            html.send_keys(Keys.END)
            time.sleep(2)
            ic = self.driver.find_elements_by_class_name("item-card-inner-wrapper")
            item = ic[i]
            item.click()
            time.sleep(2)
            buy_button = self.driver.find_elements_by_class_name("btn.btn-success.btn-fluid.mb-2.text-styled.font-weight-bold")
            if len(buy_button) == 2:
                # green_links.append(self.driver.current_url)
                # mailler = Sendmail(self.driver.current_url)
                print("Mail has been sent.")
            self.driver.back()

if __name__ == "__main__":
    # category = input("Category Index : ")
    # subcategory = input("Subcategory Index : ")
    for i in range(1, 32):
        run = True
        while run:
            for j in range(100):
                try:
                    Tradera(i+1, j+1)
                except:
                    break
            run = False
