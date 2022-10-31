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


#url: ウグイスネットURL, ground_number: 球場ボタンの位置, ground_name: 球場のアルファベット名, the_number_of_grounds: グランドの数

class GetGroundCondition:
  #コンストラクタ
  def __init__(self, url, ground_number, ground_name, the_number_of_grounds):
    self.url = url
    self.ground_number = ground_number
    self.ground_name = ground_name
    self.the_number_of_grounds = the_number_of_grounds
  
  #グラウンド状況を格納した配列を返す関数
  def get_condition(self):
    options = ChromeOptions()
    options.add_argument("--headless")


    # ブラウザを起動する
    self.driver = webdriver.Chrome(ChromeDriverManager().install())
    self.driver.get(self.url)
    time.sleep(2)

    # 戻るボタンクリック
    element = self.driver.find_element(By.XPATH, "//a[@href]")
    time.sleep(1)
    self.driver.execute_script('arguments[0].click();', element)
    time.sleep(1)

    # 施設から選択項目をクリック
    mokuji = self.driver.find_elements(By.XPATH, "//a[@href]")
    self.driver.execute_script('arguments[0].click();', mokuji[11])
    time.sleep(1)

    # 野球場をクリック
    inputs = self.driver.find_element(By.XPATH, "//input[@value='野球場']")
    self.driver.execute_script('arguments[0].click();', inputs)
    time.sleep(1)


    grounds = self.driver.find_elements(By.CLASS_NAME, 'BTNLR')
    self.driver.execute_script('arguments[0].click();', grounds[self.ground_number])
    time.sleep(1)
    # HTMLを文字コードをUTF-8に変換してから取得します。
    html = self.driver.page_source.encode('utf-8')

    # BeautifulSoupで扱えるようにパースします
    soup = BeautifulSoup(html, "html.parser")

    conditions = soup.find_all('tr', class_='WTBL')
    return conditions
  
  #csvファイルにグランド状況を上書きする関数
  def write_csv(self, condition, i):
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
    file = 'CSV/'+self.ground_name+'/'+self.ground_name+'_' + str(i+1) + '.csv'
    with open(file, 'a', newline='') as f:
      print(write_c, file=f)
      
  #csvファイルからグランド状況を読み込み関数
  def read_csv(self, i):
    file = 'CSV/'+self.ground_name+'/'+self.ground_name+'_' + str(i+1) + '.csv'
    with open(file, 'r', newline='') as f:
      reader = csv.reader(f)
      self.conditionList = []
      for row in reader:
        self.conditionList.append(row)
        
  
  
  #雨天中止かどうか判定する関数      
  def check_condition(self):
    self.rain_grounds = []
    conditions = self.get_condition()
    for i in range(self.the_number_of_grounds):
      condition = conditions[len(conditions)-i-1].find_all('td', class_='NATR')
      self.write_csv(condition, i)
      self.read_csv(i)
    
    conditions = self.get_condition()
    for i in range(self.the_number_of_grounds):
    #各球場のコンディション取得
      condition = conditions[len(conditions)-i-1].find_all('td', class_='NATR')
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
      with open('CSV/'+self.ground_name+'/'+self.ground_name+'_' + str(i+1) + '.csv', 'a', newline='') as f:
        print(write_c, file=f)
        
      self.courtFlag = False
      if len(self.conditionList) == 1:
        if 'コート不良' in self.conditionList[-1][0] or '雨天中止' in self.conditionList[-1][0]:
          self.courtFlag = True
        
      else:
        if self.conditionList[-1] != self.conditionList[-2] and ('コート不良' in self.conditionList[-1][0] or '雨天中止' in self.conditionList[-1][0]):
          self.courtFlag = True
      
      if self.courtFlag:
        court = self.conditionList[-1][0].split('\t')[0]
        self.rain_grounds.append(court)
  
  
  #雨天中止の場合LINEに通知する関数      
  def rain_notify_function(self):
    self.check_condition()
    if self.courtFlag:
      rain_notify(self.rain_grounds)
    # デバック用
    # else:
    #   rain_notify(['萩中'])
      
    time.sleep(1)
    back = self.driver.find_elements(By.XPATH, '//a[@href]')
    time.sleep(1)
    self.driver.execute_script('arguments[0].click();', back[1])

    time.sleep(1)
    self.driver.close()
    
  #実行関数
  def main(self):
    self.rain_notify_function()
      

    
    
# a = GetGroundCondition('https://www.yoyaku.city.ota.tokyo.jp/ota-user/mainservlet/UserPublic', 3)
# a.get_condition()