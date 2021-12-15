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

# Just some Random Kinda Important Stuff
#---------------------------------------
# category = int(category)
# subcategory = int(subcategory)
# subsubcategory = int(subsubcategory)
# time.sleep(4)
# self.cookie()
# time.sleep(4)
# self.select_category()
# time.sleep(8)
# self.select_sub_sub_category()
# self.check_ad()

#########################################################################
#                       ACTUAL CODE STARTS HERE ;)                      #
#########################################################################

# Starting the Webdriver and Opening hte Website
driver = webdriver.Firefox()
driver.get("https://www.tradera.com/")

# Waiting the Website to start
time.sleep(4)

# Customizign the Cookie Stuff
cookie_customization = driver.find_elements_by_class_name("css-1hy2vtq")[0]
cookie_customization.click()
reject_all = driver.find_elements_by_class_name("css-10h2kwl")[0]
reject_all.click()
save_and_exit = driver.find_elements_by_class_name("css-47sehv")[1]
save_and_exit.click()

# Waiting for the Page to Load
time.sleep(4)

# category = 1
# subcategory = 1

# Selecting the Category
category_button = driver.find_elements_by_class_name('btn.hamburger.hamburger--squeeze.site-dropdown__hamburger.ml-md-1.ml-lg-0.ml-xl-0.btn-sm')[0]
category_button.click()

time.sleep(4)

category_names = driver.find_elements_by_class_name("text-left.flex-grow")

# for i in category_names:
    # print(i.text)

for category in range(len(category_names)):

    if category > 0:
        category_button = driver.find_elements_by_class_name('btn.hamburger.hamburger--squeeze.site-dropdown__hamburger.ml-md-1.ml-lg-0.ml-xl-0.btn-sm')[0]
        category_button.click()
        time.sleep(4)
        category_names = driver.find_elements_by_class_name("text-left.flex-grow")

    category += 1
    category_names[category - 1].click()

    con = sqlite3.connect('category.db')
    cur = con.cursor()

    print('-'*100)
    print(category_names[category - 1].text)
    print('-'*100)

    tablename = category_names[ category - 1].text.replace(" ","")
    if '&' in tablename:
        tablename = tablename.replace('&', '')
    if ',' in tablename:
        tablename = tablename.replace(',','')   
    if '-' in tablename:
        tablename = tablename.replace('-','')

    # try:
    #     cur.execute(f"CREATE TABLE {tablename} (id integer PRIMARY KEY, categoryname text NOT NULL)")
    # except:
    #     pass

    time.sleep(4)

    subcategory_names = driver.find_elements_by_class_name("site-dropdown__item.d-flex.flex-row.align-items-center.site-dropdown__item-default.pl-5")
    
    # c = 1
    # for sc in subcategory_names:
    #     cur.execute(f"INSERT INTO {tablename} (id, categoryname) VALUES(?,?)", (c, sc.text))
    #     c += 1

    # con.commit()
    # con.close()


    for subcategory in range(len(subcategory_names)):

        if subcategory != 0:
            category_button = driver.find_elements_by_class_name('btn.hamburger.hamburger--squeeze.site-dropdown__hamburger.ml-md-1.ml-lg-0.ml-xl-0.btn-sm')[0]
            category_button.click()
            time.sleep(4)
            category_names = driver.find_elements_by_class_name("text-left.flex-grow")
            category_names[category - 1].click()
            time.sleep(4)
            subcategory_names = driver.find_elements_by_class_name("site-dropdown__item.d-flex.flex-row.align-items-center.site-dropdown__item-default.pl-5")

        subcategory += 1

        subcategoryname = subcategory_names[subcategory - 1].text
        subcategory_names[subcategory - 1].click()

        print(f'>>>> {subcategoryname}')
        print('-'*100)

        # Waiting for the Page to Load
        time.sleep(4)

        # Selecting the SUB SUB Categories    
        sub_sub_cat = driver.find_elements_by_class_name("item-name--3qMBC")

        actual_sub_sub_cat = []

        tablename1 = subcategoryname
        tablename1 = tablename1.replace(" ","")
        if '&' in tablename1:
            tablename1 = tablename1.replace('&', '')
        if ',' in tablename1:
            tablename1 = tablename1.replace(',','')   
        if '-' in tablename1:
            tablename1 = tablename1.replace('-','')

        count = 1
        for i in range(len(sub_sub_cat)):
            time.sleep(8)
            sub_sub_cat = driver.find_elements_by_class_name("item-name--3qMBC")
            i = sub_sub_cat[i]
            if count > 2:
                actual_sub_sub_cat.append(i)
                con = sqlite3.connect('subcategory.db')
                cur = con.cursor()
                
                try:
                    cur.execute(f"CREATE TABLE {tablename}{tablename1} (id integer PRIMARY KEY, subsubcategoryname text NOT NULL)")
                except:
                    pass
                
                cur.execute(f"INSERT INTO {tablename}{tablename1} (id, subsubcategoryname) VALUES(?,?)", (count-2, i.text))

                con.commit()
                con.close()
                
                print(i.text)
                try:
                    if i.text.replace(' ', '') != '':
                        i.click()
                        
                        tablename2 = i.text
                        tablename2 = tablename2.replace(" ","")
                        if '&' in tablename2:
                            tablename2 = tablename2.replace('&', '')
                        if ',' in tablename2:
                            tablename2 = tablename2.replace(',','')
                        if '-' in tablename2:
                            tablename2 = tablename2.replace('-','') 


                        time.sleep(4)
                        
                        sub_sub_sub_cat = driver.find_elements_by_class_name("item-name--3qMBC")
                        
                        con1 = sqlite3.connect('subsubcategory.db')
                        cur1 = con1.cursor()

                        try:
                            cur1.execute(f"CREATE TABLE {tablename}{tablename1}{tablename2} (id integer PRIMARY KEY, subsubsubcategoryname text NOT NULL)")
                        except:
                            pass

                        c2 = 1
                        for j in sub_sub_sub_cat:
                            if c2 > 2:
                                print('\t>', j.text)
                                cur1.execute(f"INSERT INTO {tablename}{tablename1}{tablename2} (id, subsubsubcategoryname) VALUES(?,?)", (c2, j.text))
                                con1.commit()
                            c2 += 1
                        con1.close()
                        driver.back()
                except:
                    print('Got Error Here!!')
                    pass
            count += 1

        driver.back()

    driver.back()

driver.quit()
# actual_sub_sub_cat[0].click()

'''        
# Checking the Ads
green_links = []
item_cards = driver.find_elements_by_class_name("item-card-inner-wrapper")
for i in range(len(item_cards)):
    website_url = driver.current_url
    if website_url == 'https://tradera.com/' or website_url == "https://www.tradera.com/":
        driver.forward()
        pass
    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.END)
    time.sleep(2)
    ic = driver.find_elements_by_class_name("item-card-inner-wrapper")
    item = ic[i]
    item.click()
    time.sleep(2)
    buy_button = driver.find_elements_by_class_name("btn.btn-success.btn-fluid.mb-2.text-styled.font-weight-bold")
    if len(buy_button) == 2:
        print("Mail has been sent.")
    driver.back()
'''
