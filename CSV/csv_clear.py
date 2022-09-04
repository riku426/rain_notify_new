def csv_clear():
  clearList = []
  default = 'csv/'
  clearList.append('csv/chofu/chofu.csv')
  clearList.append('csv/haginaka/haginaka.csv')
  clearList.append('csv/oota/oota.csv')
  for i in range(1, 5):
    clearList.append('csv/oomori/oomori_' + str(i) + '.csv')
  for i in range(1, 32):
    clearList.append('csv/tama/tama_' + str(i) + '.csv')
    
  for c in clearList:
    with open(c, 'r+') as f:
      f.truncate(0)
      
if __name__ == '__main__':
  csv_clear()