import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pyotp

def init_chrome(DownloadPath, mode='1'):
    chrome_options = webdriver.ChromeOptions()

    if mode == '1':
        chrome_options.add_argument("--start-maximized")
    elif mode == '2':
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("--headless=new")

    prefs = {
        "download.default_directory": DownloadPath,
        "savefile.default_directory": DownloadPath,
        "plugins.always_open_pdf_externally": True,
        "download.directory_upgrade": True
    }
    
    chrome_options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def xpathByElement(driver, element):
    xpath = driver.execute_script("""
        function getXPath(el) {
            if (el.id !== '') {
                return 'id(\"' + el.id + '\")';
            }
            if (el === document.body) {
                return el.tagName.toLowerCase();
            }
            let ix = 0;
            let siblings = el.parentNode.childNodes;
            for (let i=0; i<siblings.length; i++) {
                let sibling = siblings[i];
                if (sibling === el) {
                    return getXPath(el.parentNode) + '/' + el.tagName.toLowerCase() + '[' + (ix+1) + ']';
                }
                if (sibling.nodeType === 1 && sibling.tagName === el.tagName) {
                    ix++;
                }
            }
        }
        return getXPath(arguments[0]);
        """, element)
    return xpath

def clickButton(driver, x, by='XPATH'):
    button = 0
    while button != -1:
        try:
            if by == 'XPATH':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.XPATH, x))
                    )
                button = driver.find_element(By.XPATH, x).click()
            elif by == 'id':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.ID, x))
                    )
                button = driver.find_element(By.ID, x).click()
            elif by == 'css':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, x))
                    )
                button = driver.find_element(By.CSS_SELECTOR, x).click()
                
            elif by == 'class':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.CLASS_NAME, x))
                    )
                button = driver.find_element(By.CLASS_NAME, x).click()
                
            return button
        except:
            print('erro')

def javaScriptClick(driver, x, by='XPATH'):
    button = 0
    while button != -1:
        try:
            if by == 'XPATH':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.XPATH, x))
                    )
                button = driver.find_element(By.XPATH, x)
                driver.execute_script('arguments[0].click()', button)
            elif by == 'id':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.ID, x))
                    )
                button = driver.find_element(By.ID, x)
                driver.execute_script('arguments[0].click()', button)
            elif by == 'css':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, x))
                    )
                button = driver.find_element(By.CSS_SELECTOR, x)
                driver.execute_script('arguments[0].click()', button)
            elif by == 'class':
                wait = WebDriverWait(driver, 3600).until(
                        EC.presence_of_element_located((By.CLASS_NAME, x))
                    )
                button = driver.find_element(By.CLASS_NAME, x)
                driver.execute_script('arguments[0].click()', button)
            return button
        except:
            print('erro')

def wait_for_load(driver, element, by='xpath', time=30,trys=10):
    while trys >= 0:
        sleep(1)
        trys-=1
        try:
            if by == 'id':
                elem = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.ID, element)))
                return elem
            elif by == 'xpath' :
                elem = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.XPATH, element)))
                return elem
            elif by == 'class':
                elem = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
                return elem
            elif by == 'css':
                elem = WebDriverWait(driver, time).until(EC.presence_of_element_located((By.CSS_SELECTOR, element)))
                return elem

        except Exception:
            continue
    raise Exception("Could not find element ",element)

def LoginNeo(driver, username, password):
    try:
        wait_for_load(driver,"/html/body/div[1]/flow-container-root-2521314/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-text-field[1]/input", "xpath")
        driver.find_element("xpath", "/html/body/div[1]/flow-container-root-2521314/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-text-field[1]/input").send_keys(username)
        driver.find_element("xpath", "/html/body/div[1]/flow-container-root-2521314/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-password-field/input").send_keys(password)
        driver.find_element("xpath", "/html/body/div[1]/flow-container-root-2521314/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-text-field[2]/input").send_keys(pyotp.parse_uri('otpauth://totp/Adm%20Modelo:?secret=GQZDKNDFMVRTGLJUGU2WGLJUGU2TSLLCGBSWELJXGEYTQMRVGZSTIYLEHE======&issuer=Adm%20Modelo').now())
        driver.find_element("id", "btnLogar").click()
        sleep(2)
        try:
            text = driver.find_element("xpath", "/html/body/div[1]/flow-container-root-2521314/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-vertical-layout/div/span/center").text
            if(text =="Código autenticador inválido"):
                driver.find_element("xpath", "/html/body/div[1]/flow-container-root-2521314/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-vertical-layout/vaadin-text-field[2]/input").send_keys(pyotp.parse_uri('otpauth://totp/Adm%20Modelo:?secret=GQZDKNDFMVRTGLJUGU2WGLJUGU2TSLLCGBSWELJXGEYTQMRVGZSTIYLEHE======&issuer=Adm%20Modelo').now())
                driver.find_element("id", "btnLogar").click()
        except:
            pass
        finally:
            wait_for_load(driver,"home", by='id')
        
    except Exception as error:
        raise error
    return True

def element_exists(driver, element, by='xpath'):
        try:
            if by == 'id':
                elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.ID, element)))
                return True
            elif by == 'xpath':
                elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, element)))
                return True
            elif by == 'class':
                elem = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CLASS_NAME, element)))
                return True
        except Exception:
            return False