import argparse
import sys
import time

from selenium import webdriver
import os
import threading
import flask
from flask import Flask, request, jsonify, Response
import argparse, platform, schedule
import os, sys, requests, json, random
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
from time import sleep as delay
from random import randint
from features import proxy,user_agent,numThread
from features.numThread import numThreadTest
from threading import Thread, Lock, current_thread
from queue import Queue
import logging


app = Flask(__name__)

def streamingTask(rundriver, parameter):
    rundriver.get("https://eurostreaming.bet/")
    try:
        # search for coockie
        rundriver.implicitly_wait(20)
        searchForm = rundriver.find_element(by="class name", value="search-form")
        inputField = rundriver.find_element(by="class name", value="search-field")
        inputField.send_keys(parameter)
        searchForm.submit()
        time.sleep(10)
        list=rundriver.find_element(by="class name", value="recent-posts")
        rundriver.implicitly_wait(30)
        for lelement in list.find_elements_by_tag_name('a'):
            print(lelement.text)
            if lelement.text.lower()==parameter:
                lelement.click()
                # click on episode unlocker
                try:
                    wait = WebDriverWait(rundriver, 10)
                    episodesUnlocker = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nano_cp_button')))
                    episodesUnlocker.click()
                    elements = rundriver.find_element(by="tag name", value="a")
                    print(elements.text)


                except common.exceptions.NoSuchElementException as e:
                    logging.error(f"Error: No elements found for  ({parameter})")
                # capcha = rundriver.find_element(by="id", value="recaptcha-anchor")
                # capcha.click()


    except common.exceptions.NoSuchElementException as e:
        logging.error(f"Error: No elements found for  ({parameter})")
    except common.exceptions.StaleElementReferenceException as e:
        list = rundriver.find_element(by="class name", value="recent-posts")
        for lelement in list.find_elements_by_tag_name('a'):
            print(lelement.text)
            if lelement.text.lower() == parameter:
                print("trovato")
                lelement.click()
                break
        try:
            wait = WebDriverWait(rundriver, 10)
            episodesUnlocker = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'nano_cp_button')))
            episodesUnlocker.click()
            elements=rundriver.find_element(by="tag name",value="a")
            print (elements.text)


        except common.exceptions.NoSuchElementException as e:
            logging.error(f"Error: No elements found for  ({parameter})")
def amazonAffiliateLinkCreation(rundriver2,deals):
    links=[]
    rundriver2.get("https://www.amazon.it/ap/signin?openid.return_to=https%3A%2F%2Fprogramma-affiliazione.amazon.it%2Fhome&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=amzn_associates_it&openid.mode=checkid_setup&marketPlaceId=APJ6JRA9NG5V4&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0")
    time.sleep(5)
    print(deals)
    try:
        form=rundriver2.find_element(by="name",value="signIn")
        emailInput=rundriver2.find_element(by="id",value="ap_email")
        emailInput.send_keys("j.bezzu@gmail.com")
        passwordInput = rundriver2.find_element(by="id", value="ap_password")
        passwordInput.send_keys("santiagofatima23")
        rememberMe = rundriver2.find_element(by="name", value="rememberMe")
        rememberMe.click()
        form.submit()
        # print(rundriver2.get_cookies())
    except common.exceptions.NoSuchElementException as e:
        print("already logged in")
        logging.info("already logged in")
    time.sleep(3)
    print(len(deals))
    for id in deals:
        time.sleep(3)
        try:
            search_product_field = rundriver2.find_element(by="id", value="ac-quicklink-search-product-field")
            search_product_field.send_keys(id)
            time.sleep(3)
        except common.exceptions.NoSuchElementException as e:
            search_product_field = rundriver2.find_element(by="id", value="ac-quicklink-search-product-field")
            search_product_field.send_keys(id)
            time.sleep(3)
        # sform.submit()
        try:
            # sform = rundriver2.find_element(by="class name", value="search-form")
            # sform.submit()
             button=rundriver2.find_element(by="xpath",value="/html/body/div[1]/div[4]/div[3]/div/div/div/div[2]/div[1]/div/div/div[1]/div/div/form/div[2]/span/span/span/input")
             button.click()
        except common.exceptions.StaleElementReferenceException as stale:
            # sform = rundriver2.find_element(by="class name", value="search-form")
            # sform.submit()
             button = rundriver2.find_element(by="xpath", value="/html/body/div[1]/div[4]/div[3]/div/div/div/div[2]/div[1]/div/div/div[1]/div/div/form/div[2]/span/span/span/input")
             button.click()
        time.sleep(3)
        try:
            result=rundriver2.find_element(by="class name",value="search-result-body")
            getLink=result.find_element(by="class name",value="a-button-text")
            getLink.click()
        except common.exceptions.StaleElementReferenceException as stale:
            result = rundriver2.find_element(by="class name", value="search-result-body")
            getLink = result.find_element(by="class name", value="a-button-text")
            getLink.click()
        time.sleep(3)
        try:
            justTet=rundriver2.find_element(by="id",value="productlinks-text-header")
            justTet.click()
        except common.exceptions.StaleElementReferenceException as stale:
            justTet = rundriver2.find_element(by="id", value="productlinks-text-header")
            justTet.click()
        time.sleep(3)
        try:
            radioButton=rundriver2.find_element(by="xpath",value="/html/body/div[1]/div[4]/div[2]/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/div/span/fieldset/div[2]")
            # for element in radioButtons:
            #     if element.get_attribute("value")=="link":
            #         element.click()
            #         break
            radioButton.click()
        except common.exceptions.StaleElementReferenceException as stale:
            radioButtons = rundriver2.find_elements(by="name", value="format_ac-productlinks-ad-code-panel-text")
            # for element in radioButtons:
            #     if element.get_attribute("value")=="link":
            #         element.click()
            #         break
            radioButton.click()
        time.sleep(1)
        textArea = rundriver2.find_element(by="class name", value="ac-ad-code-link")
        links.append(textArea.get_attribute("value"))
        print(links)
        #print(textArea.get_attribute("value"))
        rundriver2.get("https://programma-affiliazione.amazon.it/home")
    rundriver2.quit()
    return links
def amazonTask(rundriver,rundriver2, parameter,flag):
    if flag=="deals":
        rundriver.get(f"https://www.amazon.it/s?k={parameter}&rh=p_n_deal_type%3A26901107031&dc&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3197YB3LUDGQH&qid=1644501265&rnid=26901106031&sprefix={parameter}%2Caps%2C397&ref=sr_nr_p_n_deal_type_1")
    else:
         rundriver.get(f"https://www.amazon.it/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-{parameter}%2522%252C%2522departments%2522%253A%255B%25221497228031%2522%255D%252C%2522sorting%2522%253A%2522BY_SCORE%2522%257D")
    deals=[]

    #cookies acceptor
    try:
        acceptButton=rundriver.find_element(by="id",value="sp-cc-accept")
        acceptButton.click()
        rundriver.get(
            f"https://www.amazon.it/s?k={parameter}&rh=p_n_deal_type%3A26901107031&dc&__mk_it_IT=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3197YB3LUDGQH&qid=1644501265&rnid=26901106031&sprefix={parameter}%2Caps%2C397&ref=sr_nr_p_n_deal_type_1")

        # form=rundriver.find_element(by="id",value="nav-search-bar-form")
        # searchBarr=rundriver.find_element(by="id",value="twotabsearchtextbox")
        # searchBarr.send_keys(parameter)
        # form.submit()
        try:
            time.sleep(3)

            #nav pag
            try:
                counter=0

                while rundriver.find_element(by="class name",value=f's-pagination-next'):
                    price3 = ''
                    value = "s-result-item"
                    counter +=1
                    time.sleep(3)
                    resultsGrid=rundriver.find_elements(by="class name",value=value)
                    trovate=False
                    try:
                        rundriver2.get(
                            "https://www.amazon.it/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.it%2F%3Fref_%3Dnav_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=itflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
                        try:

                            emailInput = rundriver2.find_element(by="id", value="ap_email")
                            emailInput.send_keys("j.bezzu@gmail.com")
                            continuebutton = rundriver2.find_element(by="id", value="continue")
                            continuebutton.click()
                            time.sleep(2)
                            passwordInput = rundriver2.find_element(by="id", value="ap_password")
                            passwordInput.send_keys("santiagofatima23")
                            loginButton = rundriver2.find_element(by="id", value="signInSubmit")
                            loginButton.click()
                        except common.exceptions.NoSuchElementException as e :
                            print(e)
                    except common.exceptions.NoSuchElementException as e:
                        print(e)
                    for element in resultsGrid:
                        product = {}
                        try:
                            link=element.find_element(by="class name",value="a-link-normal")
                            print(link.get_attribute('href'))
                            rundriver2.get(link.get_attribute('href'))

                            try:
                                try:
                                    acceptButton = rundriver2.find_element(by="id", value="sp-cc-accept")
                                    acceptButton.click()
                                    time.sleep(3)
                                except common.exceptions.NoSuchElementException as e:
                                    print(e)
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
                                    time.sleep(10)

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
                                    time.sleep(10)

                            except common.exceptions.NoSuchElementException as e:
                                try:
                                    acceptButton = rundriver2.find_element(by="id", value="sp-cc-accept")
                                    acceptButton.click()
                                except common.exceptions.NoSuchElementException as e:

                                    print(f"error:{e}")

                            getLink = rundriver2.find_element(by="id", value="amzn-ss-text-link")
                            getLink.click()
                            link = getLink.find_element(by="tag name", value="a")
                            link.click()
                            time.sleep(10)
                            affiliateLink = rundriver2.find_element(by="id",value="amzn-ss-text-shortlink-textarea").get_attribute("value")
                            prezzo=float(price3)
                            Title = rundriver2.find_element(by="id", value="titleSection")
                            nome=Title.find_element(by="id",value="productTitle").text
                            product['link']=affiliateLink
                            product['nome']=nome
                            product['prezzo']=prezzo
                            print(product)
                            deals.append(product)
                        except common.exceptions.NoSuchElementException as e:
                            print(e)
                    value="s-pagination-container"
                    navigation=rundriver.find_element(by="class name",value=value)
                    value='s-pagination-next'
                    next=navigation.find_element(by="class name",value=value)
                    try:
                        if next.get_attribute('aria-disabled') =="true":
                            print("fine risultati")
                            logging.info("fine risultati")

                            break
                        else:
                            next.click()
                    except:
                        next.click()
                    time.sleep(5)
            except common.exceptions.NoSuchElementException as e:
                value = "s-result-item"
                counter += 1
                time.sleep(3)
                price3=''
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
                        time.sleep(2)
                        passwordInput = rundriver2.find_element(by="id", value="ap_password")
                        passwordInput.send_keys("santiagofatima23")
                        loginButton = rundriver2.find_element(by="id", value="signInSubmit")
                        loginButton.click()
                    except common.exceptions.NoSuchElementException as e:
                        print(e)
                except common.exceptions.NoSuchElementException as e:
                    print(e)
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
                            time.sleep(3)
                        except common.exceptions.NoSuchElementException as e:
                            print(e)
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
                            time.sleep(10)

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
                            time.sleep(10)



                        getLink = rundriver2.find_element(by="id", value="amzn-ss-text-link")
                        getLink.click()
                        link = getLink.find_element(by="tag name", value="a")
                        link.click()
                        time.sleep(10)
                        affiliateLink = rundriver2.find_element(by="id",
                                                                value="amzn-ss-text-shortlink-textarea").get_attribute(
                            "value")
                        prezzo = float(price3)
                        Title=rundriver2.find_element(by="id",value="titleSection")
                        nome = Title.find_element(by="id", value="productTitle").text
                        product['link'] = affiliateLink
                        product['nome'] = nome
                        product['prezzo'] = prezzo
                        print(product)
                        deals.append(product)
                    except common.exceptions.NoSuchElementException as e:
                        print(e)

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
    return deals

def amazonPriceCheck(rundriver, rundriver2, parameter, flag):
    rundriver.get(
        f"https://www.amazon.it/deals?ref_=nav_cs_gb&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-{parameter}%2522%252C%2522departments%2522%253A%255B%25221497228031%2522%255D%252C%2522sorting%2522%253A%2522BY_SCORE%2522%257D")
    deals = []
    # cookies acceptor
    try:
        acceptButton = rundriver.find_element(by="id", value="sp-cc-accept")
        acceptButton.click()
        form = rundriver.find_element(by="id", value="nav-search-bar-form")
        searchBarr = rundriver.find_element(by="id", value="twotabsearchtextbox")
        searchBarr.send_keys(parameter)
        form.submit()
        time.sleep(3)
        try:
            price=rundriver.find_element(by="xpath",value="/html/body/div[1]/div[2]/div[1]/div[1]/div/span[3]/div[2]/div[2]/div/div/div/div/div[2]/div[3]/div[2]/a/span[1]/span[2]/span[1]")
            price2=price.text.replace('€','')
            print(price2)
            time.sleep(10)
            rundriver.quit()
            return jsonify(price=price2)
        except common.exceptions.NoSuchElementException as e:
            logging.info(f"error : {e}")
            print(e)
            return jsonify(price=price2)

    except common.exceptions.NoSuchElementException as e:
        acceptButton = rundriver.find_element(by="id", value="sp-cc-accept")
        acceptButton.click()
        print(f"error:{e}")
        return jsonify(price=price2)
        rundriver.quit()

def runThread(browser,parameter,BROWSERS,SERVICES,SETDRIVER):
    ip, port, country = proxy.randomHttps()

    print(
        f"""
PROXY CONFIGURATION FOR THIS TASK
Ip Address: {ip}
Port: {port}
Country: {country}
Current thread: {current_thread().name}
Parameter: {parameter}
""")
    logging.info(f"Task configuration for {parameter}: proxy {ip}:{port} from {country}")
    if browser == "Firefox":
        profile = webdriver.FirefoxProfile()
        opts = FirefoxOptions()
        #opts.add_argument("--headless")
        profile.set_preference("network.proxy.https", ip)
        profile.set_preference("network.proxy.https_port", int(port))
        agent = user_agent.randomFirefox()
        print("Random User-Agent: ", agent)
        logging.info(f"{parameter} use {agent}")
        profile.set_preference("general.useragent.override", agent)
        try:
            rundriver = BROWSERS[browser](firefox_profile=profile, options=opts, executable_path=SETDRIVER)
            rundriver2 = BROWSERS[browser](firefox_profile=profile, options=opts, executable_path=SETDRIVER)
        except Exception as e:
            logging.error(f"Error: unable to set Firefox browser option. {e}")
            print(e)
            sys.exit(0)
    elif browser == "Chrome":
        options = Options()
        agent = user_agent.randomChrome()
        options.add_argument(f"user-agent={agent}")
        print("Random User-Agent: ", agent)
        logging.info(f"{parameter} use {agent}")
        rundriver = BROWSERS[browser](chrome_options=options, executable_path=SETDRIVER)
    else:
        print("Something went wrong !\nUnable to set browser options ! ")
        logging.error("Something went wrong ! Unable to set browser options ! ")
        sys.exit(1)
    if SERVICES['Streaming']:
        logging.info(f"Execute Streaming task with {browser} on {parameter}")
        print(f"Execute Snapchat task with {browser}...")
        streamingTask(rundriver, parameter)
    if SERVICES['Deals']:
        logging.info(f"Execute Deals task on Amazon with {browser}")
        print(f"Execute Deals task on Amazon with {browser}...")
        flag='deals'
        return amazonTask(rundriver,rundriver2, parameter,flag)
    if SERVICES['Full']:
        logging.info(f"Execute Full research task on Amazon with {browser}")
        print(f"Execute Full research task on Amazon with {browser}...")
        flag='full'
        return amazonTask(rundriver, rundriver2, parameter,flag)
    if SERVICES['Track']:
        logging.info(f"Execute Price Check task on Amazon with {browser}")
        print(f"Execute Price Check task on Amazon with {browser}...")
        flag='full'
        return amazonPriceCheck(rundriver, rundriver2, parameter,flag)

@app.route("/amazon/<function>/<parameter>", methods=['POST'])
def Search(function,parameter):
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--browser", "-b", required=True)
    # parser.add_argument("--parameters", "-p", required=True)
    # # parser.add_argument("--register", "-r", required=True)
    # args = parser.parse_args()
    browser = 'firefox'.capitalize()
    parameters = parameter
    # if os.path.isfile(args.register):
    #    register_file = args.register
    # else:
    #    print(f"File {args.register} not exits !")
    #    sys.exit(1)

    # PATH TO LOCAL SELENIUM WEB DRIVER
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

    if browser not in BROWSERS.keys():
        print("Invalid browser: ", browser)
        sys.exit(1)

    # AVAILABLE SERVICE
    SERVICES = {
        "Streaming": False,
        "Deals": False,
        "Full": False,
        "Nike": False,
    }
    if function=='deals':
        SERVICES['Deals']=True
    if function=='full':
        SERVICES['Full']=True
    if function=='track':
        SERVICES['Track']=True

    # IDENTIFY SYSTEM
    os_ = platform.system()
    arc_ = platform.architecture()[0]

    if os_ == "Linux":
        if arc_ == "64bit":
            SETDRIVER = DRIVER[browser]["Linux"]['64']
        else:
            SETDRIVER = DRIVER[browser]['Linux']['32']
    elif os_ == "Windows":
        if arc_ == "64bit":
            SETDRIVER = DRIVER[browser]["Windows"]['64']
        else:
            SETDRIVER = DRIVER[browser]["Windows"]['32']
    else:
        macversion = platform.mac_ver()
        if 'arm64' in macversion:
            SETDRIVER = DRIVER[browser]['MacOS']['64']
        elif macversion != ('', ('', '', ''), ''):
            SETDRIVER = DRIVER[browser]['MacOS']['32']
        else:
            print("Something went wrong !\nUnable to identify suitable drivers")
            sys.exit(1)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)  # or whatever
    handler = logging.FileHandler('automatedsms.log', 'a+', 'utf-8')  # or whatever
    handler.setFormatter(logging.Formatter('%(levelname)s_%(asctime)s %(message)s'))  # or whatever
    root_logger.addHandler(handler)
    # logging.basicConfig(filename="automatedsms.log", encoding="utf-8", level=logging.INFO, format="%(levelname)s_%(asctime)s %(message)s", datefmt="%Y/%m/%d %I:%M:%S")
    print(
        f"""
Running {sys.argv[0]}...
OS: {os_}
Arch: {arc_}
Browser: {browser}
Driver's path: {SETDRIVER}
Parameters: {parameters}



"""
    )
    logging.info(f"Start {sys.argv[0]} with {browser} parameters: {parameters}")
    runThread(browser,parameters,BROWSERS,SERVICES,SETDRIVER)
    # threads = Queue()
    # tmp_thread = Thread(name=f"NewThread", target=runThread, args=(threads,browser,parameters,BROWSERS,SERVICES,SETDRIVER), daemon=True)
    # threads.put(tmp_thread)
    # tmp_thread.start()
    # work_v2()
    # schedule.every(int(timewait)).seconds.do(work_v2)

    # while True:
    #     schedule.run_pending()
    #     delay(0.1)