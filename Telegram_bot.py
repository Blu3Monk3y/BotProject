import json
import os
import platform
import time

from flask import jsonify
from selenium import webdriver, common
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram.ext import CommandHandler, Updater, JobQueue, CallbackContext
from datetime import datetime, timedelta
import regexp as regexp
import requests
import sqlite3, sys
import telebot
import logging
#API_KEY=os.getenv('API_KEY')
from features import user_agent, proxy
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)  # or whatever
handler = logging.FileHandler('BOT.log', 'a+', 'utf-8')  # or whatever
handler.setFormatter(logging.Formatter('%(levelname)s_%(asctime)s %(message)s'))  # or whatever
root_logger.addHandler(handler)
bot=telebot.TeleBot("5123005004:AAHGas7v4ULfiRwBCWmNWg_L6nRPOZS5NOo")
tracking=False
priceTracker={}
chat_id= []
my_token = '5123005004:AAHGas7v4ULfiRwBCWmNWg_L6nRPOZS5NOo'
updater = Updater(my_token, use_context=True)
job_queue = JobQueue()
dispatcher=updater.dispatcher
job_queue.set_dispatcher(dispatcher)

tracker=False
DB_FILENAME = "TelegramBot.db"
DB_CONNECTION = None
try:
    db_path = os.path.join(os.getcwd(), DB_FILENAME)
    DB_CONNECTION = sqlite3.connect(db_path, check_same_thread=False)
    print(f"Database succesfully connected ({db_path}) !")
except:
    print(f"Failed to connect with {db_path} ... ")
    sys.exit(1)
cursor = DB_CONNECTION.cursor()

# Create table
try:
    cursor.execute('''CREATE TABLE TrackingTable
                   (chat_id text,Link text,Nome text, Old float, New float)''')
except sqlite3.OperationalError as e:
    print('1',e)



def checkPrice(context):

    DRIVER = {
        "Chrome": {
            "Linux": {"32": None, "64": "drivers/chrome/Linux/chromedriver_linux64"},
            "Windows": {"32": "drivers/chrome/Windows/chromedriver_win32.exe", "64": None},
            "MacOS": {"32": None, "64": "drivers/chrome/MacOS/chromedriver_mac64"}
        },
        "Firefox": {
            "Linux": {"32": "drivers/firefox/Linux/geckodriver_linux32",
                      "64": "drivers/firefox/Linux/geckodriver_linux64"},
            "Windows": {"32": "drivers/firefox/Windows/geckodriver_win32.exe",
                        "64": "drivers/firefox/Windows/geckodriver_win64.exe"},
            "MacOS": {"32": "drivers/firefox/MacOS/geckodriver_macos",
                      "64": "drivers/firefox/MacOS/geckodriver_macos64"}
        }
    }

    # AVAILABLE BROWSERS
    BROWSERS = {
        "Chrome": webdriver.Chrome,
        "Firefox": webdriver.Firefox
    }
    # IDENTIFY SYSTEM
    os_ = platform.system()
    arc_ = platform.architecture()[0]
    if os_ == "Linux":
        if arc_ == "64bit":
            SETDRIVER = DRIVER["Firefox"]["Linux"]['64']
        else:
            SETDRIVER = DRIVER["Firefox"]['Linux']['32']
    elif os_ == "Windows":
        if arc_ == "64bit":
            SETDRIVER = DRIVER["Firefox"]["Windows"]['64']
        else:
            SETDRIVER = DRIVER["Firefox"]["Windows"]['32']
    else:
        macversion = platform.mac_ver()
        if 'arm64' in macversion:
            SETDRIVER = DRIVER["Firefox"]['MacOS']['64']
        elif macversion != ('', ('', '', ''), ''):
            SETDRIVER = DRIVER["Firefox"]['MacOS']['32']
        else:
            print("Something went wrong !\nUnable to identify suitable drivers")
    ip, port, country = proxy.randomHttps()
    profile = webdriver.FirefoxProfile()
    opts = FirefoxOptions()
    # opts.add_argument("--headless")
    profile.set_preference("network.proxy.https", ip)
    profile.set_preference("network.proxy.https_port", int(port))
    agent = user_agent.randomFirefox()
    print("Random User-Agent: ", agent)

    profile.set_preference("general.useragent.override", agent)
    rundriver = BROWSERS['Firefox'](firefox_profile=profile, options=opts, executable_path=SETDRIVER)

    cursor = DB_CONNECTION.cursor()
    rows = cursor.execute(
        "SELECT * FROM TrackingTable",
    ).fetchall()
    cursor.close()
    try:
        result=jsonify(rows)
    except Exception as e:
        print(e)
    print(rows)
    if len(rows) != 0:

        for row in rows:
            result={'chat_id':row[0],'link':row[1],'nome':row[2],'old':row[3],'new':row[4]}
            print(result)
            price2=0
            # r = requests.post(f'http://127.0.0.1:5000/amazon/track/{code}')
            # response = r.json()
            print(result['link'])
            rundriver.get(result['link'])
            try:
                acceptButton = rundriver.find_element(by="id", value="sp-cc-accept")
                acceptButton.click()
                # time.sleep(3)
                time.sleep(1)
                try:
                    priceDiv = rundriver.find_element(by="id",value="corePrice_feature_div")
                    priceText=priceDiv.find_element(by="class name",value="a-price")
                    print(priceText.get_attribute("text"))
                    price2 = priceText.text.replace('€', '')
                    if '\n' not in price2:
                        price3 = price2.replace(',', '.')

                    else:
                        price3 = price2.replace('\n', '.')
                    # time.sleep(10)
                    time.sleep(1)

                except common.exceptions.NoSuchElementException as e:
                    print(f"error:{e}")
                    priceDiv = rundriver.find_element(by="id", value="corePrice_feature_div")
                    priceText = priceDiv.find_element(by="class name", value="a-a-price")
                    price2 = priceText.text.replace('€', '')
                    if '\n' not in price2:
                        price3 = price2.replace(',', '.')

                    else:
                        price3 = price2.replace('\n', '.')

                    time.sleep(10)

            except common.exceptions.NoSuchElementException as e:
                acceptButton = rundriver.find_element(by="id", value="sp-cc-accept")
                acceptButton.click()
                print(f"error:{e}")


            oldprice=0;
            price=float(price3)
            if result['new']==0.0:
                try:
                    cursor = DB_CONNECTION.cursor()
                    cursor.execute(
                        "UPDATE TrackingTable set Old = ?, New = ? WHERE chat_id = ? AND Link= ?",(0.0,price,result['chat_id'],result['link'])
                    ).fetchall()

                    # prova = cursor.execute(
                    #     "SELECT * FROM TrackingTable",
                    # ).fetchall()
                    # cursor.close()
                    # print(prova)
                except Exception as e:
                    print(e)
                # priceTracker[link] =price
            else:
                if result['new']>price:
                    result['old']=result['new']
                    result['new']=price
                    try:
                        rundriver.get("https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
                        try:

                            emailInput = rundriver.find_element(by="id", value="ap_email")
                            emailInput.send_keys("j.bezzu@gmail.com")
                            continuebutton=rundriver.find_element(by="id", value="continue")
                            continuebutton.click()
                            time.sleep(2)
                            passwordInput = rundriver.find_element(by="id", value="ap_password")
                            passwordInput.send_keys("santiagofatima23")
                            loginButton=rundriver.find_element(by="id",value="signInSubmit")
                            loginButton.click()
                            rundriver.get(result['link'])
                            getLink=rundriver.find_element(by="id",value="amzn-ss-text-link")
                            getLink.click()
                            link=getLink.find_element(by="tag name",value="a")
                            link.click()
                            # time.sleep(10)
                            time.sleep(1)
                            affiliateLink=rundriver.find_element(by="id",value="amzn-ss-text-shortlink-textarea").get_attribute("value")
                            Title = rundriver.find_element(by="id", value="titleSection")
                            nome = Title.find_element(by="id", value="productTitle").text
                        except common.exceptions.NoSuchElementException as e :
                            getLink = rundriver.find_element(by="id", value="amzn-ss-text-link")
                            getLink.click()
                            time.sleep(1)
                            affiliateLink = rundriver.find_element(by="id",
                                                                   value="amzn-ss-text-shortlink-textarea").get_attribute(
                                "value")
                            Title = rundriver.find_element(by="id", value="titleSection")
                            nome = Title.find_element(by="id", value="productTitle").text
                    except common.exceptions.NoSuchElementException as e:
                        print('2' + e)
                    bot.send_message(result['chat_id'],"\U0001F50A"+"** HEY QUALCOSA È SCESO DI PREZZO **\n\n"
                                             f"\U0001F50A** NOME {nome}"
                                             f"** PRODOTTO \U0001F50E {affiliateLink}\n\n"
                                             f"** PREZZO \U0001F4B6 DA {result['old']} € A {result['new']} € **")
                    try:
                        cursor = DB_CONNECTION.cursor()
                        cursor.execute(
                            "UPDATE TrackingTable SET Old= ?, New = ? WHERE chat_id = ? AND Link= ?",
                            (result['old'], result['new'], result['chat_id'], result['link'])
                        ).fetchall()
                    except Exception as e :
                        print(e)
    rundriver.quit()


def Search(context):
    try:

        chatId=context.job.context[0]
        parameters=context.job.context[1]
    except Exception as e:
        print(e)

    DRIVER = {
        "Chrome": {
            "Linux": {"32": None, "64": "drivers/chrome/Linux/chromedriver_linux64"},
            "Windows": {"32": "drivers/chrome/Windows/chromedriver_win32.exe", "64": None},
            "MacOS": {"32": None, "64": "drivers/chrome/MacOS/chromedriver_mac64"}
        },
        "Firefox": {
            "Linux": {"32": "drivers/firefox/Linux/geckodriver_linux32",
                      "64": "drivers/firefox/Linux/geckodriver_linux64"},
            "Windows": {"32": "drivers/firefox/Windows/geckodriver_win32.exe",
                        "64": "drivers/firefox/Windows/geckodriver_win64.exe"},
            "MacOS": {"32": "drivers/firefox/MacOS/geckodriver_macos",
                      "64": "drivers/firefox/MacOS/geckodriver_macos64"}
        }
    }

    # AVAILABLE BROWSERS
    BROWSERS = {
        "Chrome": webdriver.Chrome,
        "Firefox": webdriver.Firefox
    }
    # IDENTIFY SYSTEM
    os_ = platform.system()
    arc_ = platform.architecture()[0]
    if os_ == "Linux":
        if arc_ == "64bit":
            SETDRIVER = DRIVER["Firefox"]["Linux"]['64']
        else:
            SETDRIVER = DRIVER["Firefox"]['Linux']['32']
    elif os_ == "Windows":
        if arc_ == "64bit":
            SETDRIVER = DRIVER["Firefox"]["Windows"]['64']
        else:
            SETDRIVER = DRIVER["Firefox"]["Windows"]['32']
    else:
        macversion = platform.mac_ver()
        if 'arm64' in macversion:
            SETDRIVER = DRIVER["Firefox"]['MacOS']['64']
        elif macversion != ('', ('', '', ''), ''):
            SETDRIVER = DRIVER["Firefox"]['MacOS']['32']
        else:
            print("Something went wrong !\nUnable to identify suitable drivers")
    ip, port, country = proxy.randomHttps()
    profile = webdriver.FirefoxProfile()
    opts = FirefoxOptions()
    # opts.add_argument("--headless")
    profile.set_preference("network.proxy.https", ip)
    profile.set_preference("network.proxy.https_port", int(port))
    agent = user_agent.randomFirefox()
    print("Random User-Agent: ", agent)

    profile.set_preference("general.useragent.override", agent)
    rundriver = BROWSERS['Firefox'](firefox_profile=profile, options=opts, executable_path=SETDRIVER)
    rundriver2 = BROWSERS['Firefox'](firefox_profile=profile, options=opts, executable_path=SETDRIVER)

    bot.send_message(chatId, "Vediamo cosa trovo!")

    # Ricerca con Selenium
    if parameters[0] == "deals":
        rundriver.get(
            f"https://www.amazon.it/s?k={parameters[1]}&rh=p_n_deal_type%3A26901107031&dc&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3197YB3LUDGQH&qid=1644501265&rnid=26901106031&sprefix={parameters[1]}%2Caps%2C397&ref=sr_nr_p_n_deal_type_1")
    elif parameters[0] == "full":
        rundriver.get(
            f"https://www.amazon.it/s?k={parameters[1]}&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1YLOGJUJ3UL19&sprefix={parameters[1]}%2Caps%2C96&ref=nb_sb_noss")
    deals = []

    # cookies acceptor
    try:
        acceptButton = rundriver.find_element(by="id", value="sp-cc-accept")
        acceptButton.click()
        if parameters[0] == "deals":
            rundriver.get(
                f"https://www.amazon.it/s?k={parameters[1]}&rh=p_n_deal_type%3A26901107031&dc&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3197YB3LUDGQH&qid=1644501265&rnid=26901106031&sprefix={parameters[1]}%2Caps%2C397&ref=sr_nr_p_n_deal_type_1")
        elif parameters[0] == "full":
            rundriver.get(
                f"https://www.amazon.it/s?k={parameters[1]}&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1YLOGJUJ3UL19&sprefix={parameters[1]}%2Caps%2C96&ref=nb_sb_noss")
        # form=rundriver.find_element(by="id",value="nav-search-bar-form")
        # searchBarr=rundriver.find_element(by="id",value="twotabsearchtextbox")
        # searchBarr.send_keys(parameter)
        # form.submit()
        try:
            time.sleep(1)

            # nav pag
            try:
                counter = 0

                while rundriver.find_element(by="class name", value=f's-pagination-next'):
                    price3 = ''
                    value = "s-result-item"
                    counter += 1
                    time.sleep(1)
                    resultsGrid = rundriver.find_elements(by="class name", value=value)
                    trovate = False
                    try:
                        rundriver2.get(
                            "https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
                        try:

                            emailInput = rundriver2.find_element(by="id", value="ap_email")
                            emailInput.send_keys("j.bezzu@gmail.com")
                            continuebutton = rundriver2.find_element(by="id", value="continue")
                            continuebutton.click()
                            time.sleep(1)
                            passwordInput = rundriver2.find_element(by="id", value="ap_password")
                            passwordInput.send_keys("santiagofatima23")
                            loginButton = rundriver2.find_element(by="id", value="signInSubmit")
                            loginButton.click()
                        except common.exceptions.NoSuchElementException as e:
                            print('1' + e)
                    except common.exceptions.NoSuchElementException as e:
                        print('2' + e)
                    for element in resultsGrid:
                        product = {}
                        try:
                            link = element.find_element(by="class name", value="a-link-normal")
                            print(link.get_attribute('href'))
                            rundriver2.get(link.get_attribute('href'))

                            try:
                                try:
                                    acceptButton = rundriver2.find_element(by="id", value="sp-cc-accept")
                                    acceptButton.click()
                                    time.sleep(1)
                                except common.exceptions.NoSuchElementException as e:
                                    print('3', e)
                                try:
                                    priceDiv = rundriver2.find_element(by="id", value="corePrice_feature_div")
                                    priceText = priceDiv.find_element(by="class name", value="a-price")
                                    print(priceText.get_attribute("text"))
                                    price2 = priceText.text.replace('€', '')
                                    if '\n' not in price2:
                                        price3 = price2.replace(',', '.')

                                    else:
                                        price3 = price2.replace('\n', '.')
                                    print(price2)
                                    time.sleep(1)

                                except common.exceptions.NoSuchElementException as e:
                                    print(f"error:{e}")
                                    priceDiv = rundriver2.find_element(by="id", value="corePrice_feature_div")
                                    priceText = priceDiv.find_element(by="class name", value="a-a-price")
                                    price2 = priceText.text.replace('€', '')
                                    if '\n' not in price2:
                                        price3 = price2.replace(',', '.')

                                    else:
                                        price3 = price2.replace('\n', '.')
                                    print(price3)
                                    # time.sleep(10)
                                    time.sleep(1)

                            except common.exceptions.NoSuchElementException as e:
                                try:
                                    acceptButton = rundriver2.find_element(by="id", value="sp-cc-accept")
                                    acceptButton.click()
                                except common.exceptions.NoSuchElementException as e:

                                    print(f"error:{e}")

                            # time.sleep(10)
                            time.sleep(1)
                            # affiliateLink = rundriver2.find_element(by="id",
                            #                                         value="amzn-ss-text-shortlink-textarea").get_attribute(
                            #     "value")
                            try:
                                prezzo = float(price3)
                                Title = rundriver2.find_element(by="id", value="titleSection")
                                nome = Title.find_element(by="id", value="productTitle").text
                                # if parameters[1] not in nome.lower():
                                #     pass
                                # else:
                                getLink = rundriver2.find_element(by="id", value="amzn-ss-text-link")
                                getLink.click()
                                link = getLink.find_element(by="tag name", value="a")
                                link.click()
                                affiliateLink = rundriver2.find_element(by="id",
                                                                        value="amzn-ss-text-shortlink-textarea").get_attribute(
                                    "value")
                                product['link'] = affiliateLink
                                product['nome'] = nome
                                product['prezzo'] = prezzo
                                print(product)
                                bot.send_message(chatId, "\U0001F50A" + f"** {product['nome']} **\n\n"
                                                                            f"** PRODUCT \U0001F50E {product['link']}\n\n"
                                                                            f"** PRICE \U0001F4B6 {product['prezzo']} € **")
                                bot.send_message(chatId, "\U0001F50E STO ANCORA CERCANDO....")
                            except Exception as e:
                                print(e)
                        except common.exceptions.NoSuchElementException as e:
                            print('4', e)
                    value = "s-pagination-container"
                    navigation = rundriver.find_element(by="class name", value=value)
                    value = 's-pagination-next'
                    next = navigation.find_element(by="class name", value=value)
                    try:
                        if next.get_attribute('aria-disabled') == "true":
                            bot.send_message(chatId, "** FINE RISULTATI **")
                            print("fine risultati")
                            logging.info("fine risultati")

                            break
                        else:
                            next.click()
                    except:
                        next.click()
                        # time.sleep(10)
                        time.sleep(1)
            except common.exceptions.NoSuchElementException as e:
                value = "s-result-item"
                counter += 1
                # time.sleep(10)
                time.sleep(1)
                price3 = ''
                resultsGrid = rundriver.find_elements(by="class name", value=value)
                trovate = False
                try:
                    rundriver2.get(
                        "https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
                    try:

                        emailInput = rundriver2.find_element(by="id", value="ap_email")
                        emailInput.send_keys("j.bezzu@gmail.com")
                        continuebutton = rundriver2.find_element(by="id", value="continue")
                        continuebutton.click()
                        # time.sleep(2)
                        time.sleep(1)
                        passwordInput = rundriver2.find_element(by="id", value="ap_password")
                        passwordInput.send_keys("santiagofatima23")
                        loginButton = rundriver2.find_element(by="id", value="signInSubmit")
                        loginButton.click()
                    except common.exceptions.NoSuchElementException as e:
                        print('5', e)
                except common.exceptions.NoSuchElementException as e:
                    print('6', e)
                for element in resultsGrid:
                    product = {}
                    try:
                        link = element.find_element(by="class name", value="a-link-normal")
                        print(link.get_attribute('href'))
                        rundriver2.get(link.get_attribute('href'))
                    except common.exceptions.NoSuchElementException as e:
                        try:
                            acceptButton = rundriver2.find_element(by="id", value="sp-cc-accept")
                            acceptButton.click()
                        except common.exceptions.NoSuchElementException as e:

                            print(f"error:{e}")
                    try:
                        try:
                            acceptButton = rundriver2.find_element(by="id", value="sp-cc-accept")
                            acceptButton.click()
                            # time.sleep(3)
                            time.sleep(1)
                        except common.exceptions.NoSuchElementException as e:
                            print('7', e)
                        try:
                            priceDiv = rundriver2.find_element(by="id", value="corePrice_feature_div")
                            priceText = priceDiv.find_element(by="class name", value="a-price")
                            print(priceText.get_attribute("text"))
                            price2 = priceText.text.replace('€', '')
                            if '\n' not in price2:
                                price3 = price2.replace(',', '.')

                            else:
                                price3 = price2.replace('\n', '.')
                            print(price2)
                            # time.sleep(10)
                            time.sleep(1)

                        except common.exceptions.NoSuchElementException as e:
                            print(f"error:{e}")
                            priceDiv = rundriver2.find_element(by="id", value="corePrice_feature_div")
                            priceText = priceDiv.find_element(by="class name", value="a-price")
                            price2 = priceText.text.replace('€', '')
                            if '\n' not in price2:
                                price3 = price2.replace(',', '.')

                            else:
                                price3 = price2.replace('\n', '.')
                            print(price3)
                            # time.sleep(10)
                            time.sleep(1)

                        # time.sleep(10)
                        time.sleep(1)

                        try:
                            prezzo = float(price3)
                            Title = rundriver2.find_element(by="id", value="titleSection")
                            nome = Title.find_element(by="id", value="productTitle").text
                            # if parameters[1] not in nome.lower():
                            #     pass
                            # else:
                            getLink = rundriver2.find_element(by="id", value="amzn-ss-text-link")
                            getLink.click()
                            link = getLink.find_element(by="tag name", value="a")
                            link.click()
                            affiliateLink = rundriver2.find_element(by="id",
                                                                    value="amzn-ss-text-shortlink-textarea").get_attribute(
                                "value")
                            product['link'] = affiliateLink
                            product['nome'] = nome
                            product['prezzo'] = prezzo
                            print(product)
                            bot.send_message(chatId, "\U0001F50A" + f"** {product['nome']} **\n\n"
                                                                        f"** PRODUCT \U0001F50E {product['link']}\n\n"
                                                                        f"** PRICE \U0001F4B6 {product['prezzo']} € **")
                            bot.send_message(chatId, "\U0001F50E STO ANCORA CERCANDO....")
                        except Exception as e:
                            print(e)
                    except common.exceptions.NoSuchElementException as e:
                        print('8', e)
                bot.send_message(chatId, "** FINE RISULTATI **")
                print("Fine risultati")
        except common.exceptions.NoSuchElementException as e:
            logging.error(f"Error: {e}")
            # capcha = rundriver.find_element(by="id", value="recaptcha-anchor")
            # capcha.click()



    except common.exceptions.NoSuchElementException as e:
        logging.info("coockies already accepted")
    rundriver2.quit()
    rundriver.quit()
    # return amazonAffiliateLinkCreation(rundriver2, deals)
    # return deals

    # r = requests.post(f'http://127.0.0.1:5000/amazon/{parameters[0]}/{parameters[1]}')
    # response = r.json()
    # for product in response:
    #     print(product)
    #     bot.send_message(chat_id[0], "\U0001F50A" + f"** {product['nome']} **\n\n"
    #                                                 f"** PRODUCT \U0001F50E {product['link']}\n\n"
    #                                                 f"** PRICE \U0001F4B6 {product['prezzo']} € **")
    #     bot.send_message(chat_id[0], "\U0001F50E STO ANCORA CERCANDO....")
    # bot.send_message(chat_id[0], "** FINE RISULTATI **")

@bot.message_handler(commands=['start'])
def start(message):
    reply="**BENVENUTO!**\n Sono un bot che ti aiuterà a cercare prodotti in supersconto su amazon!\n\n **AIUTO** \n/help--Per chiedere aiuto.\n\n**CREDITI**\n BOT BY GIOVANNI PULA\n"
    bot.send_message(message.chat.id,reply)

@bot.message_handler(regexp="help")
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, "**COSTRUZIONE COMANDO**\n"
                                      "/deals:<parametri ricerca> --trova offerte relative ai parametri di ricerca vedi esempi\n"
                                      "/full:<parametri ricerca> --trova tutto ciò relativo ai parametri di ricerca vedi esempi\n"
                                      "/track:<link amazon>-- tiene traccia giornalmente del prezzo del prodotto inserito e ti avverte se scende\n"
                                      "/all_tracks-- ritorna tutti i prodotti di cui sta tenendo traccia con i relativi prezzi attuali!\n"
                                      "/stop_searching:<link amazon> --interrompe l'osservazione prezzo (se presente) per il prodotto inserito\n"
                                      "**COMANDI DI ESEMPIO**\n"
                                      "/deals:headphones --cerca tutte le offerte per 'headphones' su amazon.\n"
                                      "/full:nvidia 3060 --cerca 'nvidia 3060' su amazon.\n\n"
                                      "**NOTA** \n"
                                      "Dal 28/02/2022 non saranno disponibili i comandi deals e full per manutenzione!\n\n")
# @bot.message_handler(regexp="/\w+")
# def deals(message):
#     bot.send_message(message.chat.id, "Bene, fatti un giro! A breve ti dirò cosa ho trovato!")
#     parameter=message.text[1:]
#     r = requests.post(f'http://127.0.0.1:5000/amazon/deals/{parameter}')
#     response = r.json()
#     for link in response:
#         bot.send_message(message.chat.id,link)
@bot.message_handler(commands=["stopTrack"])
def stopT(message):
    tracking=False
    print(tracking)
@bot.message_handler(regexp="/\w+")
def deals(message):
    chat_id.append(message.chat.id)
    message.chat.id
    string=message.text[1:]
    parameters=string.split(':')
    if parameters[0]=="track":
        bot.send_message(message.chat.id, "Perfetto lo tengo sotto controllo io, appena scende di prezzo ti faccio un fischio!")
        cursor = DB_CONNECTION.cursor()
        try:
            cursor.execute(
                "INSERT INTO TrackingTable (chat_id, Link,Old,New) VALUES (?,?,?,?)",
                (message.chat.id,parameters[1]+':'+parameters[2],0.0,0.0),
            )
            DB_CONNECTION.commit()
            cursor.close()
        except Exception as e:
            print(e)
        priceTracker[parameters[1]+':'+parameters[2]]=''

        # timedelta(days=1)
        if tracker==False:
            job_queue.run_repeating(checkPrice, interval=timedelta(days=1), first=1,name=str(message.chat.id)+parameters[1]+parameters[2])
        job_queue.start()
    elif parameters[0]=="all_tracks":
        msg=f"** TRACKER ATTIVI **\n\n"
        print(job_queue.jobs())
        for key in priceTracker.keys():
            msg=msg+f"\U0001F50E PRODUCT : {key}\n" \
                    f"\U0001F4B6 PRICE : {priceTracker[key]}€\n\n"
        bot.send_message(message.chat.id,f"{msg}")
    elif parameters[0]=='stop':
        current_jobs = job_queue.jobs()
        print(current_jobs)
        if not current_jobs:
            return False
        for job in current_jobs:
            if job.name==str(message.chat.id)+parameters[1]+parameters[2]:
                job.schedule_removal()
        bot.send_message(message.chat.id,f"OK! Ho interrotto la ricerca di {parameters[1]+parameters[2]}")
    elif parameters[0]=='stop_channel':
        current_jobs = job_queue.jobs()
        print(current_jobs)
        if not current_jobs:
            return False
        for job in current_jobs:
            if job.name=='-1001648226610':
                job.schedule_removal()
        bot.send_message(message.chat.id,f"OK! Ho interrotto il Canale")
    elif parameters[0] == 'start_channel':
        Channell()
        bot.send_message(message.chat.id, f"OK! Ho avviato il Canale")

    else:
        chatId=message.chat.id
        job_queue.run_once(Search,1, name=f"{message.chat.id}",context=(chatId, parameters))
        job_queue.start()



def Channell():
        parameters=[]
        parameters.append('deals')
        parameters.append('Smartphone')
        job_queue.run_repeating(Search, interval=timedelta(days=1), first=1,context=('-1001648226610',parameters ),name=f"-1001648226610")
        job_queue.start()
bot.polling()
