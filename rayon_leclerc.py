import undetected_chromedriver as uc
import pickle
import pandas as pd

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

if __name__ == '__main__':
    options = Options()
    options.add_experimental_option('detach', True)

    path ="C:\Program Files (x86)\chromedriver.exe"
    driver = uc.Chrome() 

    driver.get("https://www.leclercdrive.fr/")
    driver.maximize_window()
    time.sleep(2)
    try:
        
        button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'onetrust-pc-btn-handler'))
        )
        button.click()
        time.sleep(2)

        refuse = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'ot-pc-refuse-all-handler'))
        )
        refuse.click()
        time.sleep(4)

        search_location = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, 'txtWPAD344_RechercheDrive'))
        )
        search_location.send_keys("82000")
        time.sleep(2)
        search_location.send_keys(Keys.RETURN)
        time.sleep(3)

        drive = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "ctrlMapLAD__cartouches--titres"))
        )
        drive.click()
        time.sleep(2)

        choisir = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "popinDriveMagasin__BtnChoix"))
        )
        choisir.click()

        time.sleep(2)

        url_loc = driver.current_url



        cookies = pickle.load(open("cookies.pkl", "rb"))

        for cookie in cookies: 

            try :
                driver.add_cookie(cookie)
            except Exception as e:
                print(e)


        
        driver.get(url_loc)
        time.sleep(2)

        btn_rayon = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/form/div[4]/div[7]/div[2]/div/div[1]/div[1]/div/div[1]/ul/li[1]/a"))
        )
        btn_rayon.click()
        time.sleep(2)


#scrap nom rayons et les liens
        rayons_p = driver.find_elements(by = By.CLASS_NAME, value= "rayon-droite")
        time.sleep(2)
      
        list_rayons = []
        
        for rayon in rayons_p:
            rayon_p = rayon.find_element(by = By.CLASS_NAME, value= "rayon-droite-titre")

            rayons_s = rayon.find_elements(by = By.TAG_NAME, value ="a")

            for rayon_s in rayons_s:

                dict_rayons={
                    'rayon principal' : rayon_p.text,
                    'rayon secondaire': rayon_s.text,
                    'lien rayon secondaire' : rayon_s.get_attribute('href')
                }
                list_rayons.append(dict_rayons)
             
        df_rayons = pd.DataFrame(list_rayons)
        #df_rayons.to_csv("list_all_rayon.csv")
        time.sleep(2)
        print(df_rayons['lien rayon secondaire'])

#scrap produits
        list_produits=[]
        for i, lien_rayon in enumerate(df_rayons['lien rayon secondaire']):
            print(lien_rayon)
            driver.get(lien_rayon)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(6)
            produits = driver.find_elements(by = By.CLASS_NAME, value = 'divWCRS310_Content')
            

            for produit in produits:
                nom_produit = produit.find_element(by = By.CLASS_NAME, value ="pWCRS310_Desc")
                #print(nom_produit)

                prix_ent_produit = produit.find_element(by = By.CLASS_NAME,value = "pWCRS310_PrixUnitairePartieEntiere")
                #print(prix_ent_produit)
                prix_dec_produit = produit.find_element(by = By.CLASS_NAME,value = "pWCRS310_PrixUnitairePartieDecimale")
                #print(prix_dec_produit)

                prix_produit = prix_ent_produit.text + prix_dec_produit.text
                #print(prix_produit)

                
                prix_rat_produit = produit.find_element(by = By.CLASS_NAME,value = "pWCRS310_PrixUniteMesure")
                #print(prix_rat_produit)
                

                dict_produits={
                    'rayon principal' : df_rayons.iloc[i]['rayon principal'],
                    'rayon secondaire': df_rayons.iloc[i]['rayon secondaire'],
                    'lien rayon secondaire' : df_rayons.iloc[i]['lien rayon secondaire'],
                    'nom_produit' : nom_produit.text,
                    'prix_produit' : prix_produit,
                    'prix_rat_produit' : prix_rat_produit.text
                }
                #print("--------------------------------")
                #print(dict_produits)
                list_produits.append(dict_produits)
        df_produits = pd.DataFrame(list_produits)
        df_produits.to_csv("list_all_produits.csv")
    except:
        driver.quit()

