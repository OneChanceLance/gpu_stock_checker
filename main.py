import csv
import time
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from amazon_checker import check_amazon_stock
from bestbuy_checker import check_bestbuy_stock
from newegg_checker import check_newegg_stock
from config import stock_check_interval, get_random_user_agent

# ✅ **Configure Edge WebDriver for Fast Stock Checking**
def init_driver():
    options = Options()

     # ✅ **User Data to Maintain Session**
    options.add_argument(f"user-data-dir=C:/Users/Jakem/AppData/Local/Microsoft/Edge/User Data")
    options.add_argument("profile-directory=Default")  # Modify if using a different profile


    # ✅ **User-Agent Spoofing**
    user_agent = get_random_user_agent()
    options.add_argument(f"user-agent={user_agent}")

    # ✅ **Anti-Bot Evasion Flags**
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--start-maximized")

    # ✅ **Disable WebRTC (Prevents IP Leak)**
    options.add_experimental_option("prefs", {"webrtc.ip_handling_policy": "disable_non_proxied_udp"})

    driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

    # ✅ **Modify Navigator Properties (Bot Evasion)**
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver

# ✅ **Load Product URLs from CSV**
def load_product_urls():
    with open("product_urls.csv", mode="r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))

# ✅ **Fast Stock Checking (One Browser, No Restarting)**
def check_stock(driver):
    product_list = load_product_urls()
    
    for item in product_list:
        site, url = item["website"], item["url"]
        
        if site == "amazon":
            check_amazon_stock(driver, url)
        elif site == "bestbuy":
            check_bestbuy_stock(driver, url)
        elif site == "newegg":
            check_newegg_stock(driver, url)

        # ✅ **Fastest possible transition to next product**

# ✅ **Start Stock Checking with One Browser**
def run_checker():
    driver = init_driver()
    
    while True:
        check_stock(driver)
        sleep_time = stock_check_interval()
        print(f"⏳ Waiting {sleep_time} seconds before checking again...")
        time.sleep(sleep_time)  # **Wait before next full loop**

# ✅ **Run the script**
if __name__ == "__main__":
    run_checker()
