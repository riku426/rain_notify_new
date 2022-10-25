import datetime
from get_ground_condition import GetGroundCondition
from CSV.csv_clear import csv_clear

#引数準備
url = 'https://www.yoyaku.city.ota.tokyo.jp/ota-user/mainservlet/UserPublic'
oomori = (url, 0, 'oomori', 4)
oota = (url, 1, 'oota', 1)
chofu = (url, 2, 'chofu', 1)
haginaka = (url, 3, 'haginaka', 1)
tama =  (url, 4, 'tama', 31)

#オブジェクト作成
oomori_notify = GetGroundCondition(*oomori)
oota_notify = GetGroundCondition(*oota)
chofu_notify = GetGroundCondition(*chofu)
haginaka_notify = GetGroundCondition(*haginaka)
tama_notify = GetGroundCondition(*tama)

#オブジェクト実行
oomori_notify.main()
oota_notify.main()
chofu_notify.main()
haginaka_notify.main()
tama_notify.main()


dt_now = datetime.datetime.now()
if dt_now.hour == 0:
  csv_clear()



