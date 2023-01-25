from AllFunctions import *
import  time

username, password, pin = get_credentials()
# input text to type when adding a strike to the watchlist
input_text = 'weekly nifty 19 jan'    #used for weekly expiry
# input_text = 'nifty dec'            #used for monthly expiry
headless = False

# Create a new instance of the Firefox driver
service = webdriver.firefox.service.Service("geckodriver.exe")
service.start()
options = Options()
options.headless = headless
driver = webdriver.Remote(service.service_url, options=options)

# going to the website
root_url = 'https://kite.zerodha.com/orders'
driver.get(root_url)
# wait till the page loads
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "userid")))

# Entering the credentials
driver.find_element('id', 'userid').send_keys(username)
driver.find_element('id', 'password').send_keys(password)
driver.find_element('class name', 'actions').click()

# This time is given so you can enter the Totp
time.sleep(20)
print("Login successful")

# wait till the page loads
WebDriverWait(driver, 30).until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/div/div/span[2]/span[3]")))

# get nifty price
current_Nifty_Price = driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/div/div[2]/div/div[1]/div/div/span[2]/span[3]').text
current_Nifty_Price = int(current_Nifty_Price[0:3]) * 100

# go to first watchlist
driver.find_element('xpath', '/html/body/div[1]/div[2]/div[1]/div/ul/li[1]').click()

# adding CE strike price to the watchlist of nifty between -1000 and +1000
for i in range(current_Nifty_Price - 1000, current_Nifty_Price + 1001, 50):
    try:
        driver.find_element('xpath', '/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/input').send_keys(' {}  {} ce'.format(input_text,i))
        time.sleep(1)
        driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/div/li[1]').click()
        print(i)
    except:
        print('error')
        pass
print()

# adding PE strike price to the watchlist of nifty between -1000 and +1000
driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/div/ul/li[2]').click()
for i in range(current_Nifty_Price+1000,current_Nifty_Price-1001,-50):
    driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/div/div[1]/div/div/input').send_keys(' {} {} pe'.format(input_text,i))
    time.sleep(1)
    driver.find_element('xpath','/html/body/div[1]/div[2]/div[1]/div/div[1]/ul/div/li[1]').click()
    print(i)
print("done")

