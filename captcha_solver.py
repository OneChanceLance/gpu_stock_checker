import requests
import time
import base64
from PIL import Image
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ✅ Replace with your 2Captcha API Key
API_KEY = "8cec7bbdd9c4652927926017972e2447"
# ✅ **Solves Amazon CAPTCHA Using 2Captcha API**
def solve_captcha(store, driver):
    if store == "amazon":
    
        try:
            print("🛑 CAPTCHA detected! Solving with 2Captcha...")

            # ✅ **Locate the CAPTCHA Image**
            captcha_img = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'captcha')]"))
            )
            captcha_url = captcha_img.get_attribute("src")
            
            # ✅ **Download CAPTCHA Image as Base64**
            response = requests.get(captcha_url)
            if response.status_code == 200:
                img_base64 = base64.b64encode(response.content).decode("utf-8")
            else:
                print("❌ Failed to download CAPTCHA image.")
                return None

            # ✅ **Send CAPTCHA to 2Captcha API**
            captcha_payload = {
                "clientKey": API_KEY,
                "task": {
                    "type": "ImageToTextTask",
                    "body": img_base64,
                    "phrase": False,
                    "case": True,
                    "numeric": 0,
                    "math": False,
                    "minLength": 1,
                    "maxLength": 6,
                    "comment": "Enter the text you see on the image"
                },
                "languagePool": "en"
            }
            
            captcha_response = requests.post("https://api.2captcha.com/createTask", json=captcha_payload).json()

            if "taskId" not in captcha_response:
                print("❌ Failed to send CAPTCHA to 2Captcha.")
                return None

            captcha_id = captcha_response["taskId"]
            print(f"🔄 Waiting for CAPTCHA solution (Task ID: {captcha_id})...")

            # ✅ **Poll 2Captcha for Solution**
            for _ in range(10):  # Retry up to 10 times
                time.sleep(5)
                solution_response = requests.post(
                    "https://api.2captcha.com/getTaskResult",
                    json={"clientKey": API_KEY, "taskId": captcha_id}
                ).json()

                if solution_response.get("status") == "ready":
                    captcha_solution = solution_response["solution"]["text"]
                    print(f"✅ CAPTCHA Solved: {captcha_solution}")
                    break
            else:
                print("❌ CAPTCHA solving timed out.")
                return None

            # ✅ **Enter CAPTCHA Solution**
            captcha_input = driver.find_element(By.ID, "captchacharacters")
            captcha_input.clear()
            captcha_input.send_keys(captcha_solution)

            # ✅ **Submit CAPTCHA**
            submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_button.click()

            print("🚀 Submitted CAPTCHA solution!")
            return True

        except Exception as e:
            print(f"❌ Error solving CAPTCHA: {e}")
            return None
    elif store == "newegg":
    
        try:
            print("🛑 CAPTCHA detected! Solving with 2Captcha...")

            # ✅ **Locate the CAPTCHA Image**
            captcha_img = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//img[contains(@src, 'data:image')]"))
            )
            captcha_url = captcha_img.get_attribute("src")

            # ✅ **Extract Base64 from CAPTCHA Image (Fixing Issue)**
            if captcha_url.startswith("data:image"):
                img_base64 = captcha_url.split(",")[1]  # Extracts Base64 part after 'data:image/png;base64,'
            else:
                print("❌ CAPTCHA image is not in Base64 format.")
                return None

            # ✅ **Send CAPTCHA to 2Captcha API**
            captcha_payload = {
                "clientKey": API_KEY,
                "task": {
                    "type": "ImageToTextTask",
                    "body": img_base64,  # Now correctly formatted!
                    "phrase": False,
                    "case": True,
                    "numeric": 0,
                    "math": False,
                    "minLength": 1,
                    "maxLength": 6,
                    "comment": "Enter the text you see on the image"
                },
                "languagePool": "en"
            }
            
            captcha_response = requests.post("https://api.2captcha.com/createTask", json=captcha_payload).json()

            if "taskId" not in captcha_response:
                print("❌ Failed to send CAPTCHA to 2Captcha.")
                return None

            captcha_id = captcha_response["taskId"]
            print(f"🔄 Waiting for CAPTCHA solution (Task ID: {captcha_id})...")

            # ✅ **Poll 2Captcha for Solution**
            for _ in range(10):  # Retry up to 10 times
                time.sleep(5)
                solution_response = requests.post(
                    "https://api.2captcha.com/getTaskResult",
                    json={"clientKey": API_KEY, "taskId": captcha_id}
                ).json()

                if solution_response.get("status") == "ready":
                    captcha_solution = solution_response["solution"]["text"]
                    print(f"✅ CAPTCHA Solved: {captcha_solution}")
                    break
            else:
                print("❌ CAPTCHA solving timed out.")

            # ✅ **Enter CAPTCHA Solution**
            captcha_input = driver.find_element(By.ID, "userInput")
            captcha_input.clear()
            captcha_input.send_keys(captcha_solution)
            time.sleep(0.1)
            # ✅ **Submit CAPTCHA**
            submit_button = driver.find_element(By.ID, "verifyCode")
            driver.execute_script("arguments[0].click();", submit_button)
            print("🚀 Submitted CAPTCHA solution!")

        except Exception as e:
            print(f"❌ Error solving CAPTCHA: {e}")