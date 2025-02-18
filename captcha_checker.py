import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# ✅ OCR.space API Key (Free Tier)
OCR_API_KEY = "472ce23ce588957"  # Use your own key if needed

# ✅ **Function to Check if Captcha Appears**
def is_captcha_present(driver):
    try:
        driver.find_element(By.XPATH, "//img[contains(@src, 'captcha')]")
        print("🔍 Captcha detected on Amazon!")
        return True
    except NoSuchElementException:
        return False

# ✅ **Function to Solve Captcha Using OCR.space API**
def solve_captcha(driver):
    try:
        # ✅ Locate Captcha Image
        captcha_img = driver.find_element(By.XPATH, "//img[contains(@src, 'captcha')]")
        captcha_url = captcha_img.get_attribute("src")
        print(f"🖼️ Captcha Image URL: {captcha_url}")

        # ✅ Send Captcha to OCR.space for Text Recognition
        captcha_text = get_text_from_ocr_space(captcha_url)

        if captcha_text:
            print(f"✅ OCR Captcha Solution: {captcha_text}")

            # ✅ Enter Captcha & Submit
            captcha_input = driver.find_element(By.ID, "captchacharacters")
            captcha_input.clear()
            captcha_input.send_keys(captcha_text)
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()

            time.sleep(3)

            # ✅ Check if Captcha Disappeared
            if not is_captcha_present(driver):
                print("✅ Captcha Solved Successfully!")
                return True
            else:
                print("❌ Captcha Solving Failed! Retrying...")
                return False
        else:
            print("❌ Could not extract text from captcha.")
            return False

    except NoSuchElementException:
        print("ℹ️ No Captcha Detected.")
        return True

# ✅ **Send Captcha Image to OCR.space for Text Extraction**
def get_text_from_ocr_space(captcha_url):
    try:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            data={
                "apikey": OCR_API_KEY,
                "url": captcha_url,
                "language": "eng",
                "isOverlayRequired": False,
                "OCREngine": 2  # Best OCR Engine for distorted text
            }
        ).json()

        if response.get("ParsedResults"):
            return response["ParsedResults"][0]["ParsedText"].strip()
        return None

    except Exception as e:
        print(f"❌ Error contacting OCR.space: {e}")
        return None