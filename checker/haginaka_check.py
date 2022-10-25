from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from checker.notify.notify import rain_notify

def haginaka_checker():
  options = ChromeOptions()
  options.add_argument("--headless")


  # ブラウザを起動する
  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.get("https://www.yoyaku.city.ota.tokyo.jp/ota-user/mainservlet/UserPublic")
  time.sleep(2)

  # 戻るボタンクリック
  element = driver.find_element(By.XPATH, "//a[@href]")
  time.sleep(1)
  driver.execute_script('arguments[0].click();', element)
  time.sleep(1)

  # 施設から選択項目をクリック
  mokuji = driver.find_elements(By.XPATH, "//a[@href]")
  driver.execute_script('arguments[0].click();', mokuji[11])
  time.sleep(1)

  # 野球場をクリック
  inputs = driver.find_element(By.XPATH, "//input[@value='野球場']")
  driver.execute_script('arguments[0].click();', inputs)
  time.sleep(1)


  grounds = driver.find_elements(By.CLASS_NAME, 'BTNLR')
  driver.execute_script('arguments[0].click();', grounds[3])
  time.sleep(1)
  # HTMLを文字コードをUTF-8に変換してから取得します。
  html = driver.page_source.encode('utf-8')

  # BeautifulSoupで扱えるようにパースします
  soup = BeautifulSoup(html, "html.parser")

  conditions = soup.find_all('tr', class_='WTBL')


  rain_grounds = []  #コート不良になったグランド名

  #各球場のコンディション取得
  condition = conditions[-1].find_all('td', class_='NATR')
  #各時間帯のコンディション取得
  write_c = ''
  for j in range(len(condition)):
    #改行コードと空白を削除
    c = condition[j].get_text().replace('\n', '')
    c = c.replace('\t', '')
    c = c.replace(' ', '')
    c = c.strip()
    if j == 1:
      write_c += c + '\t'
    else:
      write_c += c
  #csvファイルにコンディションを追記
  with open('CSV/haginaka/haginaka.csv', 'a', newline='') as f:
    print(write_c, file=f)
  
  #csvファイルから読み込み
  with open('CSV/haginaka/haginaka.csv', 'r', newline='') as f:
    reader = csv.reader(f)
    conditionList = []
    for row in reader:
      conditionList.append(row)
      
    courtFlag = False
    if len(conditionList) == 1:
      if 'コート不良' in conditionList[-1][0] or '雨天中止' in conditionList[-1][0]:
        courtFlag = True
      
    else:
      if conditionList[-1] != conditionList[-2] and ('コート不良' in conditionList[-1][0] or '雨天中止' in conditionList[-1][0]):
        courtFlag = True

    if courtFlag:
      court = conditionList[-1][0].split('\t')[0]
      #print(court, 'はコート不良です。')
      rain_grounds.append(court)
        
  if courtFlag:
    rain_notify(rain_grounds)

  time.sleep(1)
  back = driver.find_elements(By.XPATH, '//a[@href]')
  time.sleep(1)
  driver.execute_script('arguments[0].click();', back[1])

  time.sleep(1)

if __name__ == '__main__':
  haginaka_checker()

