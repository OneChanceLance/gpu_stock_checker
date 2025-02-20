import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from captcha_solver import solve_captcha
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from config import DISCORD_CART_WEBHOOK_URL, NEWEGG_5090_THRESHOLD, NEWEGG_5080_THRESHOLD, human_delay
from newegg_checkout import checkout_newegg
from discord_notifier import send_stock_notification

# ✅ **Newegg Canada - Detect & Handle CAPTCHA**
def wait_for_captcha(driver):
    print("Scanning for Captcha...")
    while True:
        try:
            captcha_text = driver.find_element(By.XPATH, "//h1[contains(text(), 'Human?')]")
            print("⚠️ Captcha Detected!")
            try:
                captcha_img = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'data:image')]"))
                )
                solve_captcha("newegg", driver)
                time.sleep(5)
            except NoSuchElementException:
                print("No Captcha Image Detected")
                if captcha_text.is_displayed():
                    time.sleep(10)  # Wait and retry
                else:
                    print("Successfully Bypassed Captcha")
                    break  # Continue if CAPTCHA disappears
        except NoSuchElementException:
            break  # No CAPTCHA, continue execution

# ✅ **Newegg Canada - Get Price**
def get_newegg_price(driver):
    try:
        price_container = driver.find_element(By.CLASS_NAME, "product-price")
        price_element = price_container.find_element(By.CLASS_NAME, "price-current")
        return float(price_element.text.split()[0].replace("$", "").replace(",", ""))
    except:
        return None

# ✅ **Newegg Canada - Check Stock & Notify**
def check_newegg_stock(driver, product_url):
    print(f"🔍  Checking stock at Newegg: {product_url}")
    driver.get(product_url)
    wait_for_captcha(driver)
    product_name = driver.title.split(" - Newegg")[0]
    price_threshold = NEWEGG_5080_THRESHOLD if "5080" in product_name else NEWEGG_5090_THRESHOLD
    try:
        # ✅ Look for the "Add to Cart" button
        add_to_cart_btn = driver.find_element(By.XPATH, "//button[contains(@class, 'btn-primary') and contains(@class, 'btn-wide')]")
        if add_to_cart_btn.is_displayed():
            gpu_price = get_newegg_price(driver)
            if gpu_price is not None:
                print(f"🟢 In stock at Newegg Canada! Price: ${gpu_price}")
                send_stock_notification("Newegg Canada", product_name, product_url, gpu_price)
                if gpu_price <= price_threshold:
                    print(f"✅ Price within budget (${gpu_price} ≤ ${price_threshold}). Proceeding to checkout...")
                    checkout_newegg(driver, product_url, product_name, "420")
                else:
                    print(f"❌ Price too high (${gpu_price} > ${price_threshold}). Skipping purchase.")
        else:
            print(f"🔴 Out of stock at Newegg Canada: {product_url}")
    except NoSuchElementException:
        print(f"🔴 Out of stock at Newegg Canada: {product_url}")