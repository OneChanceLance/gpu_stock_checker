import csv
import time
import requests
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service 
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait

# ✅ Discord Webhooks
DISCORD_PURCHASE_WEBHOOK_URL = "https://discord.com/api/webhooks/1338578389480505414/1hCOS03gIr-cKcL8d6amO9oAS4VQB4cIDGfCzrwl8tgk5dJK08RkuNAEOAfdsghTf2Q6"
DISCORD_CART_WEBHOOK_URL = "https://discord.com/api/webhooks/1338875358350540850/iL8zpFlwvPn2pt1zD0zrTTjwwQLDOTR07l6qpKtItf4SOBETLrJ8vgTaJtUvE5JcSLxQ"

# ✅ Price Thresholdsr 
PRICE_THRESHOLD = 4490  # Default for all GPUs
RTX_5080_THRESHOLD = 2199  # Special threshold for RTX 5080 GPUs
CVV = "420"

# ✅ Ensure Edge Profile Path is Correct
EDGE_PROFILE_PATH = r"C:\Users\Jakem\AppData\Local\Microsoft\Edge\User Data"
PROFILE_NAME = "Default"


# ✅ Configure Edge WebDriver (Keeps You Logged In)
edge_options = Options()
edge_options.add_argument(f"user-data-dir={EDGE_PROFILE_PATH}")
edge_options.add_argument(f"profile-directory={PROFILE_NAME}")
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--disable-blink-features=AutomationControlled")
edge_options.add_argument("--start-maximized")

# ✅ Initialize Edge WebDriver
service = Service(EdgeChromiumDriverManager().install())
driver = webdriver.Edge(service=service, options=edge_options)

# ✅ **Determine Price Threshold Based on Product Name**
def get_price_threshold(product_name):
    if "5080" in product_name or "RTX 5080" in product_name.upper():
        print(f"🟡 Detected RTX 5080. Using threshold: ${RTX_5080_THRESHOLD}")
        return RTX_5080_THRESHOLD
    else:
        print(f"🟢 Using default threshold: ${PRICE_THRESHOLD}")
        return PRICE_THRESHOLD

# ✅ **Universal In-Stock Notification for All Stores**
def send_stock_notification(store, product_name, product_url, price):
    webhook_url = DISCORD_CART_WEBHOOK_URL  # Use cart webhook for in-stock alerts
    message_type = "🟢 **In Stock!**"

    data = {
        "content": f"@everyone {message_type}\n\n**Product:** {product_name}\n**Price:** ${price} CAD\n**Store:** {store}\n🔗 [View Product]({product_url})"
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print(f"✅ Sent Discord notification for in-stock item at {store}!")
    else:
        print(f"❌ Failed to send Discord notification: {response.status_code}")

# ✅ **Send Message to Discord Webhook**
def send_discord_notification(product_name, product_url, store, purchased=False):
    webhook_url = DISCORD_PURCHASE_WEBHOOK_URL if purchased else DISCORD_CART_WEBHOOK_URL
    message_type = "🛒 **Added to Cart!**" if not purchased else "✅ **Purchased!**"
    
    data = {
        "content": f"@everyone {message_type}\n\n**Product:** {product_name}\n**Store:** {store}\n🔗 [View Product]({product_url})"
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print(f"✅ Sent Discord notification to {'PURCHASE' if purchased else 'CART'} webhook!")
    else:
        print(f"❌ Failed to send Discord notification: {response.status_code}")

# ✅ **Load product URLs from CSV file**
def load_product_urls(filename="product_urls.csv"):
    product_list = []
    with open(filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            product_list.append((row["website"], row["url"]))
    return product_list

# ✅ **Amazon - Check Price & Stock**
def check_amazon_stock_and_price(product_url):
    driver.get(product_url)
    time.sleep(3)

    product_name = driver.title.split(" : Amazon")[0]
    price_threshold = get_price_threshold(product_name)
    gpu_price = get_amazon_price()

    if gpu_price is not None:
        print(f"🟢 In stock at Amazon! Price: ${gpu_price}")

        # ✅ Send in-stock Discord notification
        send_stock_notification("Amazon", product_name, product_url, gpu_price)

        # ✅ Proceed to checkout if price is within budget
        if gpu_price <= price_threshold:
            print(f"✅ Price is within budget: ${gpu_price} (Threshold: ${price_threshold})")
            checkout_amazon(product_name, product_url)
        else:
            print(f"❌ Price too high: ${gpu_price} (Threshold: ${price_threshold})")

# ✅ **Amazon - Checks Price**
def get_amazon_price():
    try:
        # ✅ Locate the price container inside `corePriceDisplay`
        price_container = driver.find_element(By.ID, "corePriceDisplay_desktop_feature_div")
        price_element = price_container.find_element(By.CLASS_NAME, "a-price-whole")

        # ✅ Extract price, remove commas, and convert to float
        price = price_element.text.replace(",", "").strip()
        return float(price)
    
    except NoSuchElementException:
        return None
# ✅ **Amazon - Add to Cart & Checkout**
def checkout_amazon(product_name, product_url):
    driver.get(product_url)
    time.sleep(3)

    try:
        add_to_cart_btn = driver.find_element(By.ID, "add-to-cart-button")
        add_to_cart_btn.click()
        print("✅ Product added to cart.")

        driver.get("https://www.amazon.ca/gp/cart/view.html")
        time.sleep(2)

        try:
            proceed_to_checkout_btn = driver.find_element(By.NAME, "proceedToRetailCheckout")
            proceed_to_checkout_btn.click()
            print("✅ Proceeding to checkout...")
        except NoSuchElementException:
            print("❌ Could not find the 'Proceed to Checkout' button.")

        time.sleep(4)
        continue_to_checkout_amazon()
        place_order_amazon(product_name, product_url)

    except Exception as e:
        print(f"❌ Error in Amazon checkout process: {e}")

# ✅ **Amazon - Click "Continue to Checkout" Button**
def continue_to_checkout_amazon():
    time.sleep(3)

    try:
        continue_btn = driver.find_element(By.XPATH, "//input[@aria-labelledby='bottomSubmitOrderButtonId-announce']")
        driver.execute_script("arguments[0].click();", continue_btn)
        print("✅ Clicked 'Continue to Checkout'!")
        time.sleep(2)
    except NoSuchElementException:
        print("ℹ️ No 'Continue to Checkout' button detected.")

# ✅ **Amazon - Place Order**
def place_order_amazon(product_name, product_url):
    try:
        place_order_btn = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "placeOrder"))
        )
        print("✅ Found 'Place Your Order' button.")

        driver.execute_script("arguments[0].click();", place_order_btn)
        print("✅ Order Placed Successfully!")

        send_discord_notification(product_name, product_url, "Amazon", purchased=True)

    except TimeoutException:
        print("❌ Timeout: 'Place Your Order' button did not appear in time.")
    except Exception as e:
        print(f"❌ Could not place the order: {e}")

def get_bestbuy_price():
    try:
        # ✅ Locate the main price container
        price_container = driver.find_element(By.CSS_SELECTOR, 'span[data-automation="product-price"]')

        # ✅ Extract the actual price from inside the div
        price_element = price_container.find_element(By.TAG_NAME, "div")

        # ✅ Extract price text & format correctly
        price_text = price_element.text.replace("$", "").replace(",", "").strip()

        return float(price_text)

    except NoSuchElementException:
        print("❌ Could not retrieve price from Best Buy.")
        return None

# ✅ **Best Buy - Check Stock & Add to Cart**
def check_bestbuy_stock(product_url):
    driver.get(product_url)
    time.sleep(3)
    try:
        # ✅ Locate the Add-to-Cart button container
        container = driver.find_element(By.CLASS_NAME, "addToCartButtonContainer_3kNch")
        
        # ✅ Find the actual Add-to-Cart button inside the container
        add_to_cart_btn = container.find_element(By.CLASS_NAME, "addToCartButton_3HRhU")

        # ✅ Check if button is enabled (means it's in stock)
        return add_to_cart_btn.is_enabled()
    except:
        return False  # Out of stock

def add_to_cart_bestbuy(product_url):
    driver.get(product_url)
    time.sleep(3)  # Wait for page to load

    try:
        # ✅ Find the "Add to Cart" button using data-automation="addToCartButton"
        add_to_cart_btn = driver.find_element(By.XPATH, "//button[@data-automation='addToCartButton']")

        # ✅ Click the "Add to Cart" button
        add_to_cart_btn.click()
        print("✅ Added to cart at BestBuy Canada!")

        # ✅ Extract product name
        product_name = driver.title.split(" - Best Buy")[0]
        send_discord_notification(product_name, product_url, "Best Buy")

        time.sleep(2)
        # ✅ Proceed to checkout
        # checkout_bestbuy()

    except Exception as e:
        print(f"❌ Could not add to cart at BestBuy Canada: {e}")

# ✅ **Newegg Canada - Check Price & Stock**
def check_newegg_stock_and_price(product_url):
    driver.get(product_url)
    time.sleep(3)

    product_name = driver.title.split(" - Newegg")[0]
    price_threshold = get_price_threshold(product_name)

    try:
        out_of_stock_element = driver.find_element(By.CLASS_NAME, "btn-message")
        if "OUT OF STOCK" in out_of_stock_element.text.upper():
            print(f"🔴 Out of stock at Newegg Canada: {product_url}")
            return
    except NoSuchElementException:
        pass

    # ✅ Extract price if in stock
    gpu_price = get_newegg_price()

    if gpu_price is not None:
        print(f"🟢 In stock at Newegg Canada! Price: ${gpu_price}")

        # ✅ Send in-stock Discord notification
        send_stock_notification("Newegg Canada", product_name, product_url, gpu_price)

        # ✅ Proceed to checkout if price is within budget
        if gpu_price <= price_threshold:
            print(f"✅ Price is within budget: ${gpu_price} (Threshold: ${price_threshold})")
            add_to_cart_newegg(product_name, product_url)
        else:
            print(f"❌ Price too high: ${gpu_price} (Threshold: ${price_threshold})")

# ✅ **Newegg Canada - Add to Cart & Checkout**
def checkout_newegg(product_name, product_url, cvv_code):
    driver.get(product_url)
    time.sleep(3)

    try:

        # ✅ Click "Add to Cart"
        add_to_cart_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
        add_to_cart_btn.click()
        print("✅ Added to cart at Newegg Canada!")

        time.sleep(1)

        # ✅ Handle "No Thanks" for Protection Plan (if appears)
        try:
            no_thanks_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'No, thanks')]")
            no_thanks_btn.click()
            print("✅ Clicked 'No Thanks' on protection popup.")
        except NoSuchElementException:
            print("ℹ️ No protection plan popup detected.")

        time.sleep(1)

        # ✅ Proceed to Cart
        driver.get("https://secure.newegg.ca/shop/cart")
        time.sleep(1)

        # ✅ Click "Proceed to Checkout"
        try:
            proceed_to_checkout_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
            proceed_to_checkout_btn.click()
            print("✅ Proceeding to checkout...")
        except NoSuchElementException:
            print("❌ Could not find 'Proceed to Checkout' button.")
            return

        time.sleep(1)

        # ✅ Enter CVV Code (Uses Correct Input Field)
        try:
            cvv_input = driver.find_element(By.NAME, "cvvNumber")  # Correct CVV field

            # ✅ Click to focus the input field
            cvv_input.click()

            # ✅ Clear existing value (if any)
            cvv_input.clear()


            # ✅ Attempt to send keys
            cvv_input.send_keys(cvv_code)

            # ✅ Verify if the input was entered correctly
            entered_value = cvv_input.get_attribute("value")
            if entered_value != cvv_code:
                print("⚠️ Normal send_keys() failed, using JavaScript instead.")
                driver.execute_script("arguments[0].value = arguments[1];", cvv_input, cvv_code)
                time.sleep(0.5)

            print(f"✅ Entered CVV code: {cvv_code}")

        except NoSuchElementException:
            print("❌ Could not find CVV input field.")

        time.sleep(2)

        # ✅ Click "Use This Payment Method"
        try:
            use_payment_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Use This Payment Method')]")
            use_payment_btn.click()
            print("✅ Selected payment method.")
        except NoSuchElementException:
            print("❌ Could not find 'Use This Payment Method' button.")

        # ✅ Click "Place Order"
        try:
            place_order_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]")
            driver.execute_script("arguments[0].click();", place_order_btn)  # Ensures hidden elements get clicked
            print("✅ Order Placed Successfully!")
            send_discord_notification(product_name, product_url, "Newegg Canada", purchased=True)
        except NoSuchElementException:
            print("❌ Could not find 'Place Order' button.")

    except Exception as e:
        print(f"❌ Error during Newegg checkout: {e}")


# ✅ **Newegg - Get Price**
def get_newegg_price():
    try:
        # ✅ Locate the price inside the main product price container
        price_container = driver.find_element(By.CLASS_NAME, "product-price")
        price_element = price_container.find_element(By.CLASS_NAME, "price-current")
        
        # ✅ Extract price & format correctly
        price_text = price_element.text.split()[0].replace("$", "").replace(",", "")
        return float(price_text)
    except:
        print("❌ Could not retrieve price from Newegg Canada.")
        return None

# ✅ **Newegg - Add to Cart**
def add_to_cart_newegg(product_name, product_url):
    try:
        driver.find_element(By.CLASS_NAME, "btn-primary").click()
        print("✅ Added to cart at Newegg!")

        # ✅ Proceed to checkout (Optional)
        checkout_newegg(product_name, product_url, CVV)

    except:
        print("❌ Could not add to cart.")

# 🔄 **Main Loop: Keep Checking All Products**
if __name__ == "__main__":
    product_list = load_product_urls()

    while True:
        print("🔄 Checking stock for all products...")
        for website, url in product_list:
            if website.lower() == "amazon":
               check_amazon_stock_and_price(url)
            
            # if website.lower() == "bestbuy":
            #     if check_bestbuy_stock(url):
            #         print(f"🟢 In stock at Best Buy! Adding to cart...")
            #         add_to_cart_bestbuy(url)
            #     else:
            #         print(f"🔴 Out of stock at Best Buy: {url}")
            #         time.sleep(random.randint(5,60))
            elif website.lower() == "newegg":
                check_newegg_stock_and_price(url)
        time.sleep(random.randint(5,10))