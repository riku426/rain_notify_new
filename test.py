from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time

options = ChromeOptions()
options.add_argument("--headless")


# ブラウザを起動する
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://www.yoyaku.city.ota.tokyo.jp/ota-user/mainservlet/UserPublic")
time.sleep(2)

element = driver.find_element(By.XPATH, "//a[@href]")
time.sleep(1)
print('element', element)
driver.execute_script('arguments[0].click();', element)
print('クリックしました')
time.sleep(1)