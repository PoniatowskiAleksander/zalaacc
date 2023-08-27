from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
from imap_tools import MailBox, AND
from pytz import timezone
import os
#from src import undetected_chromdriver as uc
from random import randint
from password_generator import PasswordGenerator
import ipchanger
import time
from seleniumbase import Driver
import undetected_chromedriver as uc

#driver.get('www.nowsecure.nl')


def minusPolishSigns(word):
    word = word.lower()
    word = word.replace('ą', 'a').replace('ć', 'c').replace('ę', 'e').replace('ł', 'l').replace('ń', 'n').replace('ó', 'o').replace('ś', 's')
    word = word.replace('ź', 'z').replace('ż', 'z')
    return word


with open('pass.txt', 'r', encoding='utf-8') as f:
    PASSWORD = f.read()


with open(r'C:/overallData/men.csv', 'r', encoding='utf-8') as f:
    men = f.read()

with open(r'C:/overallData/women.csv', 'r', encoding='utf-8') as f:
    women = f.read()

with open(r'C:/overallData/menSurnames.csv', 'r', encoding='utf-8') as f:
    menSurnames = f.read()

with open(r'C:/overallData/womenSurnames.csv', 'r', encoding='utf-8') as f:
    womenSurnames = f.read()


men = men.split(',')
women = women.split(',')
menSurnames = menSurnames.split(',')
womenSurnames = womenSurnames.split(',')

def randomize(list1, list2):
    return list1[randint(0, len(list1)-2)], list2[randint(0, len(list2)-2)]


#sleep(2)
def main():
    counter = 0



    start = time.time()
    sex = randint(0,1)
    if sex:
        firstname, lastname = randomize(men, menSurnames)
    else:
        firstname, lastname = randomize(women, womenSurnames)

    firstname = minusPolishSigns(firstname)
    lastname = minusPolishSigns(lastname)
    numsNumber = randint(0, 4)
    emailNumRandom = randint(0, numsNumber*10)
    emailNumRandom = '' if emailNumRandom == 0 else str(emailNumRandom)
    email = firstname + lastname + emailNumRandom 
    email = email.lower()

    email = list(email)

    for i in range(len(email)):
        if email[i] in '!$%^@#&*()_+{}|:\">?<,./;\'[]\= ':
            email[i] = '0'

        if ord(email[i]) < 97 and ord(email[i]) > 122:
            email[i] = '0'



    email = ''.join(email)

    email += '@mojmail.com.pl'

    pwo = PasswordGenerator()
    pwo.excludeschars = "!$%^@#&*()_+{}|:\">?<,./;'[]\="
    pwo.minlen = 10 # (Optional)
    pwo.maxlen = 12 # (Optional)
    password = pwo.generate()

    print(firstname, lastname)
    print(email)
    print(password)

    #driver = uc.Chrome()#driver_exectuable_path=ChromeDriverManager().install())
    driver = Driver(uc=True, headless=True)

    print('cos')

    driver.get('https://www.zalando.pl/myaccount/')
    #driver.find_element(By.XPATH, '/html/body/div[4]/div/x-wrapper-re-1-4/div/div/div[1]/div/div/div/div[3]/div/div[1]/a/div/div/button').click()

    sleep(5)

    sleep(2)
    script = 'document.querySelector("#sso > div > section > div > div._134xl > div > button").click()'
    #document.querySelector("#register\\.firstname").value = "John";document.querySelector("#register\\.lastname").value = "smith";'
    driver.execute_script(script)
    sleep(1)

    driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[1]/div/div/input').send_keys(firstname) #name
    driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[2]/div/div/input').send_keys(lastname) #lastname
    driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[3]/div/div/input').send_keys(email) # email
    driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[4]/div/div[1]/input').send_keys(password) # password
    driver.find_element(By.XPATH, '//*[@id="section-register"]/div/form/div[6]/div').click() #newsletter

    sleep(5)
    driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div[2]/div/div/div/form/div[7]/button').click() #register
    
    sleep(3)

    with MailBox('serwer2340135.home.pl').login('serwer2340135', PASSWORD) as mailbox:
        STARTING = time.time()
        def checkForMsg():
            for msg in mailbox.fetch(f'TO "{email}"'):
                print(msg.html)
                # with open('a.html', 'w', encoding='utf-8') as f:
                #     f.write(msg.html)

                link = msg.html.split('zalando-newsletter/')[1].split('" target="_blank')[0]
                link = 'https://www.zalando.pl/zalando-newsletter/' + link
                print('awjfawfawfiawfiawihfahwifhhawifhiahwhfiaw---------------------------------------------------------------------')
                driver.switch_to.new_window('tab')
                driver.get(link)
                return
            else:
                
                print('0')
                sleep(1)
                if time.time() - STARTING > 45 or 'Wystąpił błąd' in driver.page_source: 
                    driver.quit()
                    os.system('taskkill /f /im chrome.exe')


                    raise Exception('timed out')
                checkForMsg()

        checkForMsg()


    with open('emails.csv', 'a') as f:
        f.write(f'\n{firstname},{lastname},{email},{password}')
    sleep(8)
    driver.quit()
    ipchanger.changeIp()
    print('donnmeeeee')
    sleep(3)
    print(time.time() - start)

    os.system('taskkill /f /im chrome.exe')


    if counter == 16:
        counter = 0
        sleep(60)