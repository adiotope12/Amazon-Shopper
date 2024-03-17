from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.support.wait import WebDriverWait
from random import *
from time import *

# This function adds items to the shopping list, and allows the use to remove items.
def addItems():
    item :str = ""
    List = []

    print("Type what you would like to purchase then press Enter\nType the same item twice to remove it\nEnter 'done' to start shopping\n")
    while (item != "done"):
        while True:
            try:
                item = input()
                if (List.count(item) != 0):
                    print("Removing",item)
                    List.remove(item)
                    print(List)
                    break
                if (item != "done"):
                    if (item !=''):
                        List.append(item)
                print (List)
                break
            except TypeError:
                print("Invalid Input\n")
                print("Type what you would like to purchase then press Enter\nType the same item twice to remove it\nEnter 'done' to start shopping\n")

    print("Would you like to start shopping?\nEnter 'yes' or 'no'\n")
    ans = input()
    while (ans != 'yes'):
        if (ans != 'no'):
            print("Invalid Input\n")
            print("Would you like to start shopping?\nEnter 'yes' or 'no'\n")
            ans = input()
        elif ans == 'no':
            List = List + addItems()
            break

    
    return List

# This function attempts to filter through the some of the search results to find the most accurate item.
def skipSponsored(driver:webdriver.Chrome):
    
    try:
        sponsored = driver.find_elements(By.XPATH,"//div[@class='a-section a-spacing-small puis-padding-left-small puis-padding-right-small']")

        if len(sponsored) == 0:
            raise NoSuchElementException
        
        for item in sponsored:
            try:
                item.find_element(By.LINK_TEXT,"Sponsored")
            except (NoSuchElementException):
                index = sponsored.index(item)
                return item.find_elements(By.XPATH,"//a[@class='a-link-normal s-no-outline']")[index]
            
    except NoSuchElementException:
        sponsored = driver.find_elements(By.XPATH,"//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-2']")
        for item in sponsored:
            try:
                item.find_element(By.LINK_TEXT,"Sponsored")
            except (NoSuchElementException):
                index = sponsored.index(item)
                return item.find_elements(By.XPATH,"//a[@class='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")[index]


    
        

aznList = addItems()
print ("Now shopping for:\n",aznList)

# detach allows the program to end without automatically closing the tab.
opt = ChromiumOptions()
opt.add_experimental_option("detach", True)

driver = webdriver.Chrome(options = opt)
driver.get('https://www.amazon.com/ap/signin?openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2Fref%3Dgw_sgn_ib%3F_encoding%3DUTF8%26pd_rd_w%3D8SVKe%26content-id%3Damzn1.sym.b297170c-a9c7-468f-92b7-ffa12c12dab9%26pf_rd_p%3Db297170c-a9c7-468f-92b7-ffa12c12dab9%26pf_rd_r%3DRKZBVEAYZF944WEJ1VJD%26pd_rd_wg%3DRCoya%26pd_rd_r%3Dcac926ef-8856-4452-bf9e-50f71d7ef197&openid.assoc_handle=usflex&openid.pape.max_auth_age=0&pf_rd_r=RKZBVEAYZF944WEJ1VJD&pf_rd_p=b297170c-a9c7-468f-92b7-ffa12c12dab9&pd_rd_r=cac926ef-8856-4452-bf9e-50f71d7ef197&pd_rd_w=8SVKe&pd_rd_wg=RCoya&ref_=pd_gw_unk')
driver.implicitly_wait(5)

wait = WebDriverWait(driver,timeout= 120)
wait.until(lambda d: driver.find_element(By.ID,"twotabsearchtextbox").is_displayed())

# This loop iterates through the list adding each item to the list.
for item in aznList:
    currItem = driver.find_element(By.ID,"twotabsearchtextbox")
    currItem.send_keys(item)
    currItem.click()

    currItem = driver.find_element(By.ID, "nav-search-submit-button")
    currItem.click()

    currItem = skipSponsored(driver)
    try:
        currItem.click()
    except AttributeError:
        print("Error searching for ",item)
        exit()
    except ElementNotInteractableException:
        driver.find_element(By.ID,"a-autoid-1-announce").click()
        continue

    currItem = driver.find_element(By.ID,"add-to-cart-button")
    currItem.click()


cart = driver.find_element(By.ID,"nav-cart-count")
cart.click()

sleep(300)
driver.quit()


