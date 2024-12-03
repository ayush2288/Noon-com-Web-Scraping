from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import matplotlib.pyplot as plt

options = webdriver.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920x1080')

brand_list = {
    "321 STRONG", "AAS ECOM", "Ab Rocket", "Ab Wheel", "ACLIX", "Acousticworld", "Actifoam", "Adidas", "AGD", "AIWANTO", "Al Jifan", 
    "Almila", "AlphaSquad", "ALSAQER", "amazon basic care", "Anmi", "Arabest", "AROAQ", "AS SEEN ON TV", "Asutra", "AURORA", "Avessa", 
    "AXOX", "Ayeeb", "ayuray", "BAHE", "BalanceFrom", "Bernessi", "Best Pilates Towel", "Better Me", "BiggYoga", "BioTech", "BJM", 
    "BLOOM", "BLOOMING TIME", "Bluelans", "Body Builder", "body heart", "BODY SCULPTURE", "BOER", "BOLDFIT", "BORTONY", "BOSU", 
    "BRIGHTLY LABS", "Buffer", "Busso", "By Leon 1982", "Captaintech", "CityRiya-Long", "Ciwaa", "CK Spor", "Clifton", "Comfort Class", 
    "Cool Baby", "Cool Baby Style", "Cosfer", "Daiso", "DAYCO", "DBLEW", "DeloPik", "Delta", "Depend", "DETREND", "Dreamzon", 
    "DubaiGallery", "DXGEARS", "Dynamic", "EBMINI", "ECVV", "ELTRAZONE", "Emfil", "Eva", "Excefore", "Exxe", "FanFox", "fashionhome", 
    "FESTNIGHT", "FFA SPORTS Fitness for All", "Fitness World", "Fizyo Shop", "Formfit", "Forwena", "Gaiam", "Gama", "General", 
    "Generic", "GENNEXT", "Gerenic", "GGEROU", "Go Fitness", "GO2CAMPS", "GoFit", "Grip", "GROIC", "GULFLINK", "Gymbit", "H PRO", 
    "Hattrick", "HaveDream", "Hepsine Rakip", "Himarry", "Holahoney", "Hugger Mugger", "Huitich", "HY", "ILI", "ioga", "IRIN", 
    "Iron Gym", "Ironsport", "Joerex", "Jolta", "joyzzz", "Kanteen Store", "Karaca", "KASTWAVE", "Katia&Bony", "KBS", "Kral Socks", 
    "KUYING", "Lela", "Leostar", "Leyaton", "Lifefit", "LIFTDEX", "limodo", "LIMOS", "LivePro", "Liveup", "Liveup Sports", "LIXADA", 
    "Long", "Longchamp", "Loquat", "Lushh", "LYNLYN", "Made2Motivate", "MahMir", "Manduka", "Masho Trend", "Maston", "Max Strength", 
    "Maxi", "MDBuddy", "MELA", "merrithew", "milano", "Miorre", "Mirza Home", "Mizuno", "Mobee", "Mood Agenda", "Motiv", "MSD", 
    "N.E.A.T by nicky", "NBB", "NeUygun", "New Balance", "NIBEMINENT", "Nike", "Nivia", "Nordmende", "OASIS-TH", "Original", 
    "Other Manufacturer", "Outlife", "Ozzy Socks", "PARTNER", "Pekial", "Povit", "PowerMax Fitness", "Prickly Pear", "Pro Hanson", 
    "ProForce", "PROMASS", "ProSource", "ProSourceFit", "QiaoKai", "Rabos", "Rainleaf", "RATSAW", "Rebuwo", "Reebok", "RIGID FITNESS", 
    "RIOXS", "Rock Pow", "RollsTimi", "Rubik", "SAPU", "Saysez", "serenity axis", "Sharpdo", "ShebSheb", "shopi.ae", "SKY-TOUCH", 
    "SkyLand", "SKYSPER", "Slazenger", "Slipt", "Socksmax", "SOWUGI", "Spa Care", "Spall", "Sportline", "SPORTS RESEARCH", "Staray", 
    "STRYVE", "Sukeen", "Suria", "Sweex", "SYOSI", "SZELAM", "TA SPORT", "TA SPORTS", "TapouT", "Tchibo", "Tezzgelsin", "The Socks Company", 
    "Thera-band", "Thoraya", "tiguar", "TOEON", "Toesox", "TOMSHOO", "Toshionics", "TPE", "TRENDI LAND ZON", "Trigger Point", "True", 
    "Tryon", "Tucketts", "Tutku", "TYCOM", "UBOYLI", "UFIT", "UKR", "ULTIMAX", "umbro", "Umiwin", "Unique", "Uniquerrs", "UNIVERSAL", 
    "VALEO", "VANDER LIFE", "VIO", "Voit", "Vparty", "Wai Lana", "WAOKN", "WENBO", "WEST BIKING", "Winmax", "Woqes", "XiuWoo", "Y&D", 
    "Yalla HomeGym", "Yameem", "YGT Ambalaj", "Yks Store", "YOGA", "YOGA DESIGN LAB", "Yoga Direct", "yoga mat", "Yogapaws", "YOMA", 
    "YooA", "YORK FITNESS", "YQbest", "Yukon", "Yuwell", "ZCM-HAPPY"
}


def scrape_noon_products():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    total_products = 0
    rank = 0


    with open('noon_products.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([
            "Date & Time", "SKU", "Title", "Brand", "Average Rating", 
            "Rating Count", "Sponsored", "Price", "Old Price", 
            "Discount", "Express", "Rank", "Link"
        ])

        try:
            for page in range(1, 90):
                driver.get(f"https://www.noon.com/uae-en/sports-and-outdoors/exercise-and-fitness/yoga-16328/?isCarouselView=false&limit=50&page={page}&sort%5Bby%5D=popularity&sort%5Bdir%5D=desc")
                
                # Wait for products to load
                products = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, 'sc-57fe1f38-0'))
                )
                total_products += len(products)
                
          
                if total_products > 400:
                    break

                for product in products:
                    try:
                       
                        date_time = product.find_element(By.CSS_SELECTOR, '.sc-d96389d1-34.bedTIK').text if len(product.find_elements(By.CSS_SELECTOR, '.sc-d96389d1-34.bedTIK')) > 0 else "N/A"
                        sku = product.find_element(By.XPATH, "//div[contains(@class, 'sc-57fe1f38-0') and contains(@class, 'eSrvHE')]/a").get_attribute("id") if len(product.find_elements(By.XPATH, "//div[contains(@class, 'sc-57fe1f38-0') and contains(@class, 'eSrvHE')]/a")) > 0 else "N/A"
                        title = product.find_element(By.CSS_SELECTOR, '[data-qa="product-name"]').text if len(product.find_elements(By.CSS_SELECTOR, '[data-qa="product-name"]')) > 0 else "N/A"
                        
                  
                        brand_fetch = title
                        brand = next((b for b in brand_list if b in brand_fetch), "N/A")
                        
                   
                        average_rating = product.find_element(By.CLASS_NAME, 'sc-9cb63f72-2').text if len(product.find_elements(By.CLASS_NAME, 'sc-9cb63f72-2')) > 0 else "N/A"
                        rating_count = product.find_element(By.CLASS_NAME, 'sc-9cb63f72-5').text if len(product.find_elements(By.CLASS_NAME, 'sc-9cb63f72-5')) > 0 else "N/A"
                        
                      
                        sponsored = "Y" if len(product.find_elements(By.CLASS_NAME, 'sc-d96389d1-24.kXouJu')) > 0 else "N"
                        
                      
                        try:
                            currency = product.find_element(By.CLASS_NAME, 'currency').text
                            price = product.find_element(By.CLASS_NAME, 'amount').text
                            current_price = f"{currency} {price}"
                        except:
                            current_price = "N/A"
                        
                        old_price = product.find_element(By.CLASS_NAME, 'oldPrice').text if len(product.find_elements(By.CLASS_NAME, 'oldPrice')) > 0 else "N/A"
                        discount = product.find_element(By.CLASS_NAME, 'discount').text if len(product.find_elements(By.CLASS_NAME, 'discount')) > 0 else "N/A"
                        
                       
                        express = "Y" if len(product.find_elements(By.CSS_SELECTOR, '[data-qa="product-noon-express"]')) > 0 else "N"
                        
                      
                        rank += 1
                        
                   
                        link = product.find_element(By.CSS_SELECTOR, '.sc-57fe1f38-0.eSrvHE a').get_attribute('href') if len(product.find_elements(By.CSS_SELECTOR, '.sc-57fe1f38-0.eSrvHE a')) > 0 else "N/A"

                        csv_writer.writerow([
                            date_time, sku, title, brand, average_rating, 
                            rating_count, sponsored, current_price, old_price, 
                            discount, express, rank, link
                        ])

                    except Exception as e:
                        print(f"Error processing product: {e}")
                        continue

        except Exception as e:
            print(f"An error occurred: {e}")
        
        finally:
            driver.quit()

    print("Scraping completed. Check noon_products.csv for results.")


if __name__ == "__main__":
    scrape_noon_products()