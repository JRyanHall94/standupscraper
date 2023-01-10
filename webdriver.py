#   Planning to use the selenium webdriver to control Chrome to automate the
# collection of data pertaining to stand-up comedy. It is possible and should
# be kept in mind that you can connect to a webdriver remotely which could be
# useful in the future, but I think the way I would probably utilize it is
# writing scripts and structures and work out their function on my own computer
# then upload and run it from the server.
#
# using: ChromeDriver 108.0.5359.71; executable file placed in '/usr/local/bin'
#
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
driver.get('https://www.google.com')
# be sure to utilize 'if' and 'assert' statements to control the flow of
# automation throughout the traversal of the site.
LOGO_SELECTOR = 'body > div.L3eUgb > div.o3j99.LLD4me.yr19Zb.LS8OJ > div > img'
logo = driver.find_element(By.CSS_SELECTOR, LOGO_SELECTOR)
logo_src = logo.get_attribute('src')
filename = logo_src.split('/')[-1]

r = requests.get(logo_src, allow_redirects=True)
open(filename, 'wb').write(r.content)

driver.close()
