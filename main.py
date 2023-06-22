import argparse
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options

class CustomHelpParser(argparse.ArgumentParser):
    def format_help(self):
        custom_help = """
        Welcome to passive v1.0.0

        OPTIONS:
            -fn         Search with full-name
            -ip         Search with ip address
            -u          Search with username
        """
        return custom_help

def search_by_name(full_name: str) -> dict:
    sep = full_name.split()

    options = Options()
    options.add_argument('-headless')

    driver = webdriver.Firefox(options=options)
    driver.get("https://www.pagesjaunes.fr/pagesblanches")

    adress = ""
    num = ""
    try:
        accept_cookies_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'didomi-notice-agree-button'))
        )    

        accept_cookies_button.click()
    except:
        adress = "Not Found"
        num = "Not Found"
    
    search_bar = driver.find_element(By.ID, "quoiqui")
    search_bar.send_keys(full_name)
    search_bar.send_keys(Keys.RETURN)

    time.sleep(2)

    content = driver.find_element(By.ID, 'listResults')
    div_content = content.text

    lines = div_content.split('\n')
    third_line = lines[2]
    adress = third_line.split('Voir')[0]
    
    button = driver.find_element(By.CSS_SELECTOR, '.button.btn.btn_primary.btn_full_mob.btn_tel.normal-button')
    button.click()

    time.sleep(2)

    phone_element = driver.find_element(By.XPATH, '//div[@class="number-contact"]/span[last()]')
    num = phone_element.text

    rep = "First name: " + sep[0] + "\nLast name: " + sep[1] + "\nAdresse: " + adress + "\nNumber: " + num +  "\nSaved in result.txt" 
    return rep

def search_by_ip(ip: str) -> dict:
    base_url = "http://ip-api.com/json/"
    response = requests.get(base_url + ip)
    response.raise_for_status()  # Raise an exception if the request was unsuccessful
    data = response.json()
    rep = "ISP: " + str(data.get('isp')) + "\nCity Lat/Lon:  " + str(data.get('lat')) + ", " + str(data.get('lon')) + "\nSaved in result2.txt"
    return rep

def search_by_username(username: str) -> dict:
    options = Options()
    options.add_argument('-headless')

    driver = webdriver.Firefox(options=options)
    driver.get("https://checkmarks.com/")

    input_field = driver.find_element(By.XPATH, '//input[@name="checkusername"]')
    input_field.send_keys(username)

    time.sleep(1)

    button = driver.find_element(By.XPATH, '//button[@name="checkusername"]')
    button.click()

    time.sleep(1)

    results_div = driver.find_element(By.ID, 'results')
    results_text = results_div.text

    fb = ""
    tw = ""
    inst = ""
    sn = ""
    yt = ""

    lines = results_text.split('\n')
    one = lines[0]
    if "unavailable" in one:
        fb = "yes"
    else:
        fb = "no"

    two = lines[1]
    if "unavailable" in two:
        tw = "yes"
    else:
        tw = "no"

    three = lines[2]
    if "unavailable" in three:
        inst = "yes"
    else:
        inst = "no"     

    four = lines[3]
    if "unavailable" in four:
        sn = "yes"
    else:
        sn = "no" 

    five = lines[4]
    if "unavailable" in five:
        yt = "yes"
    else:
        yt = "no"                               
    
    result = "Facebook : " + fb + "\nTwitter : " + tw + "\nInstagram : " + inst + "\nSnapchat : " + sn + "\nYoutube : " + yt + "\nSaved in result3.txt"
    return result



def save_results(results: str, filename: str):
    with open(filename, 'w') as file:
        file.write(results)

def main():
    parser = CustomHelpParser(add_help=False)
    parser.add_argument('-fn', '--fullname', type=str)
    parser.add_argument('-ip', '--ipaddress', type=str)
    parser.add_argument('-u', '--username', type=str)
    parser.add_argument('--help', action='help')

    args = parser.parse_args()

    if args.fullname:
        results = search_by_name(args.fullname)
        print(results)
        save_results(results, 'result.txt')
    elif args.ipaddress:
        results = search_by_ip(args.ipaddress)
        print(results)
        save_results(results, 'result2.txt')
    elif args.username:
        results = search_by_username(args.username)
        print(results)
        save_results(results, 'result3.txt')

if __name__ == "__main__":
    main()
