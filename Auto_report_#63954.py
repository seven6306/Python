from selenium import webdriver
from time import sleep, strftime
from selenium.webdriver.common.keys import Keys

def currentDate():
	date = strftime("%m/%d")
	w_dict = {'0': '日', '1': '一', '2': '二', '3': '三', '4': '四', '5': '五', '6': '六'}
	if date[0] == '0':
		date = date[1:]
	if date[-2] == '0':
		date = date.replace('0', '')
	return(date + ';' + w_dict[strftime("%w")])
try:
	while(1):
		print('Exit: ctrl + c')
		e_count = input('Please input drive erase count: ')
		if e_count.isdigit():
			break
		else:
			print('Invalid drive erase count number')
except KeyboardInterrupt:
	raise SystemExit
comment1 = '\n{0} ({1}) (RAID 0：Continuous Recording)'.format(currentDate().split(';')[0], currentDate().split(';')[1])
comment2 = """
1. 64 ch 錄影資料正常沒有斷檔 - Pass
2. SATADOM erase count: {}""".format(e_count)
driver = webdriver.Chrome(executable_path=r'C:\Python35\driver\chromedriver.exe')
driver.get('http://dqa02/issues/63954')
print(driver.title + ' has been connected')

driver.find_element_by_id('username').send_keys('blake.liou')
driver.find_element_by_id('password').send_keys('1qaz@WSX')
driver.find_element_by_name('login').click()
sleep(5)
driver.find_element_by_xpath('//*[@class="icon icon-edit"]').click()
sleep(3)
print('Paste below comment to Rich Text Editor:\n' + comment1 + '\n' + comment2)
#driver.find_element_by_id('cke_99').click()
#sleep(1)
editor = driver.find_element_by_xpath('//*[@title="Rich Text Editor, issue_notes"]')
	
editor.send_keys(comment1)
editor.send_keys(Keys.HOME)
editor.send_keys(Keys.BACK_SPACE)
editor.send_keys(Keys.CONTROL,'a')
editor.send_keys(Keys.CONTROL,'b')
editor.send_keys(Keys.END)
editor.send_keys(Keys.ENTER)
editor.send_keys(Keys.CONTROL,'b')
editor.send_keys(comment2)
sleep(1)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(1)
driver.find_element_by_xpath('//*[@value="Submit"]').click()
sleep(5)
driver.quit()
