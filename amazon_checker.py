import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from captcha_checker import is_captcha_present, solve_captcha
from config import AMAZON_USA_5080_THRESHOLD, AMAZON_USA_5090_THRESHOLD, AMAZON_CA_5090_THRESHOLD, AMAZON_CA_5080_THRESHOLD, human_delay
from amazon_checkout import checkout_amazon
from discord_notifier import send_stock_notification
from selenium.webdriver.support import expected_conditions as EC
from captcha_solver import capture_captcha, solve_captcha  # Import Captcha Functions


# ✅ **Function to Detect & Solve CAPTCHA**
def handle_amazon_captcha(driver):
    try:
        # ✅ Check if captcha is present
        captcha_image = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')]"))
        )
        print("⚠️ CAPTCHA detected. Solving...")

        # ✅ Capture image and get base64 encoding
        base64_captcha = capture_captcha(driver, captcha_image)

        # ✅ Solve captcha using 2Captcha
        solved_text = solve_captcha(base64_captcha)

        if solved_text:
            # ✅ Enter the solved text into the captcha input field
            captcha_input = driver.find_element(By.ID, "captchacharacters")
            captcha_input.send_keys(solved_text)
            print(f"✅ Entered CAPTCHA: {solved_text}")

            # ✅ Submit captcha
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()
            print("🚀 Submitted CAPTCHA! Continuing checkout...")

            time.sleep(3)  # Allow page to reload
        else:
            print("❌ Failed to solve CAPTCHA. Retrying...")

    except:
        print("✅ No CAPTCHA detected.")

# ✅ **Amazon - Get Price**
def get_amazon_price(driver):
    try:
        price_container = driver.find_element(By.ID, "corePriceDisplay_desktop_feature_div")
        price_element = price_container.find_element(By.CLASS_NAME, "a-price-whole")
        return float(price_element.text.replace("$", "").replace(",", "").strip())
    except:
        return None

# ✅ **Amazon - Check Stock & Notify**
def check_amazon_stock(driver, product_url):
    print(f"🔍 Checking stock at Amazon: {product_url}")
    driver.get(product_url)
    product_name = driver.title.split(" : Amazon")[0]
    while is_captcha_present(driver):
        solve_captcha(driver)
    if "amazon.ca" in product_url:
        price_threshold = AMAZON_CA_5080_THRESHOLD if "5080" in product_name else AMAZON_CA_5090_THRESHOLD
        gpu_price = get_amazon_price(driver)
        if gpu_price is not None:
            print(f"🟢 In stock at Amazon! Price: ${gpu_price}")
            if gpu_price <= price_threshold:
                print(f"✅ Price within budget (${gpu_price} ≤ ${price_threshold}). Proceeding to checkout...")
                send_stock_notification("Amazon", product_name, product_url, gpu_price)
                checkout_amazon(driver, product_url, product_name)
            else:
                print(f"❌ Price too high (${gpu_price} > ${price_threshold}). Skipping purchase.")
        else:
            print(f"🔴 Out of stock at Amazon: {product_url}")
    elif "amazon.com" in product_url:
        price_threshold = AMAZON_USA_5080_THRESHOLD if "5080" in product_name else AMAZON_USA_5090_THRESHOLD
        gpu_price = get_amazon_price(driver)
        if gpu_price is not None:
            print(f"🟢 In stock at Amazon! Price: ${gpu_price}")
            if gpu_price <= price_threshold:
                print(f"✅ Price within budget (${gpu_price} ≤ ${price_threshold}). Proceeding to checkout...")
                send_stock_notification("Amazon", product_name, product_url, gpu_price)
                checkout_amazon(driver, product_url, product_name)
            else:
                print(f"❌ Price too high (${gpu_price} > ${price_threshold}). Skipping purchase.")
        else:
            print(f"🔴 Out of stock at Amazon: {product_url}")