from checker.oomori_check import oomori_checker
from checker.oota_check import oota_checker
from checker.chofu_check import chofu_checker
from checker.haginaka_check import haginaka_checker
from checker.tama_check import tama_checker
import datetime
from CSV.csv_clear import csv_clear

oomori_checker()
oota_checker()
chofu_checker()
haginaka_checker()
tama_checker()

dt_now = datetime.datetime.now()
if dt_now.hour == 0:
  csv_clear()



