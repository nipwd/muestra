from selenium import webdriver 
import chromedriver_autoinstaller 
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
chromedriver_autoinstaller.install() 
 
# Create Chromeoptions instance 
options = webdriver.ChromeOptions() 
 
# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 
options.add_extension('driver/extension_1_62_0_0.crx')

# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 
 
# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 
options.add_argument("--user-data-dir=/home/dev/.config/google-chrome/")

# Setting the driver path and requesting a page 
driver = webdriver.Chrome(options=options) 
from selenium.webdriver.common.keys import Keys
from time import sleep
import pandas as pd
import datetime
from selenium.webdriver.common.by import By

today = datetime.date.today().strftime('%d-%m-%Y')

# Changing the property of the navigator value for webdriver to undefined 
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
page = ''
driver.get(page)
actionChains = ActionChains(driver)
driver.implicitly_wait(10)
datos2 = driver.find_elements(By.XPATH, "/html/body/div[4]/div/div[4]/table/tbody/tr[2]/td[3]/div/div[3]/div/div")
ultimo_elemento = datos2[-1]
datos = actionChains.move_to_element(ultimo_elemento).perform()
actionChains.click(ultimo_elemento).perform()
print(ultimo_elemento.text)
sleep(5)
ultimo_elemento.send_keys(Keys.CONTROL, 'f')
ultimo_elemento.send_keys(Keys.CONTROL, 'a')
ultimo_elemento.send_keys(Keys.BACKSPACE)
sleep(3)

df1 = pd.read_csv('csv/excelauto.csv')
df2 = pd.read_csv('csv/hechos.csv')

# Generar una lista a partir de la columna 'name'
lista_nombres = df1['name'].tolist()

# Filtrar con los nombres de la lista
df_filtrado = df2[df2['tecnico'].isin(lista_nombres)]

# Agrupar por los valores correspondientes a hoy
df_agrupado = df_filtrado[df_filtrado['fecha'] == today]
#print(df_agrupado)
lista =[]
for index, row in df_agrupado.iterrows():
    valor = row['mac_instalado']
    tecnico = row['tecnico'] 
    if row['mac_instalado'] != 'Sin Instalado':
        lista2=[today,valor,tecnico]
        lista.append(lista2)
        find =driver.find_element(By.XPATH, '/html/body')
        find.send_keys(Keys.CONTROL, 'f')
        find.send_keys(Keys.CONTROL, 'a')
        sleep(0.5)
        find.send_keys(Keys.BACKSPACE)
        datos_buscar = driver.find_element(By.XPATH, '//*[@id="docs-findbar-input"]/table/tbody/tr/td[1]/input')
        actionChains.move_to_element(datos_buscar).perform()
        actionChains.click(datos_buscar).perform()
        sleep(0.5)
        datos_buscar.send_keys(f"{valor}")
        sleep(0.5)

        element_xpath = '/html/body/div[2]/div[8]/div[3]/div/div/div[1]/div[1]/div/div[2]/table/tbody/tr/td[2]/span'
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
        if element.text == '0 de 0':
            print(valor, tecnico)
            df = pd.DataFrame(lista)
            df.to_csv('csv/no_encontrados.csv', mode='a', header=False, index=False)
            datos_buscar.send_keys(Keys.ESCAPE)
            pass
        if element.text == '1 de 1':
                sleep(0.5)
                datos_buscar.send_keys(Keys.ESCAPE, Keys.ARROW_RIGHT, "hecho "+tecnico, Keys.ENTER)
        sleep(1)
        

print('planilla lista')
driver.close()
driver.quit()
import telebot
bot = telebot.TeleBot('')
bot.send_message(chat_id='', text="Planilla lista 🤖")
