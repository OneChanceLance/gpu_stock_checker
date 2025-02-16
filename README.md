
---

# **GPU Stock Checker - Setup Guide**  

Welcome to **GPU Stock Checker**! Follow the steps below to properly set up and run this script. This guide assumes you're using **Windows**.  

---

## **1. Create the Project Folder**  
1. Navigate to your **Desktop**.  
2. Create a new folder and name it **gpu_stock_checker**.  

---

## **2. Install Necessary Software**  

### **2.1 Install Git**  
Git is needed to download updates from this repository.  
1. Download Git from: [Git Official Website](https://git-scm.com/downloads)  
2. Run the installer and follow the default setup.  
3. After installation, open **Command Prompt** (`Win + R`, type `cmd`, and press Enter).  
4. Type `git --version` and press **Enter**. If it displays a version number, Git is installed correctly.  

---

### **2.2 Install Visual Studio Code**  
This will be used to edit and run the script.  
1. Download VS Code from: [Visual Studio Code](https://code.visualstudio.com/)  
2. Run the installer and follow the setup instructions.  

---

### **2.3 Install Python and Pip**  
Python is required to run the script, and **pip** is a package manager for installing dependencies.  
1. Download Python from: [Python Official Website](https://www.python.org/downloads/)  
2. Run the installer and **check the box** that says **"Add Python to PATH"**, then complete the installation.  
3. Open **Command Prompt** (`Win + R`, type `cmd`, and press Enter).  
4. Type `python --version` and press **Enter**. If it displays a version number, Python is installed correctly.  
5. Type `pip --version` and press **Enter** to verify that pip is installed.  

---

## **3. Install Required Python Packages**  
Open **Command Prompt** and run the following command:  

```
pip install selenium webdriver-manager requests beautifulsoup4
```

This will install all the necessary Python libraries.

---

## **4. Set Up WebDriver**  

### **4.1 Create WebDriver Folder**  
1. Open **File Explorer** (`Win + E`).  
2. Navigate to **C:/** (your main drive).  
3. Create a new folder and name it **WebDriver**.  

### **4.2 Install Edge WebDriver**  
1. Download **Stable Channel Edge WebDriver** from:  
   [Microsoft Edge WebDriver Download](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/?form=MA13LH)  
2. Once downloaded, **extract the ZIP file**.  
3. Locate **msedgedriver.exe** inside the extracted folder.  
4. Move **msedgedriver.exe** into the **C:\WebDriver** folder you created earlier.  

---

## **5. Clone the Repository and Get the Script Files**  
1. Open **Command Prompt** (`Win + R`, type `cmd`, and press Enter).  
2. Navigate to your **Desktop** using the command:  
   ```
   cd Desktop/gpu_stock_checker
   ```
3. Clone the repository using Git:  
   ```
   git clone [YOUR_GITHUB_REPO_URL] .
   ```
   (Replace `[YOUR_GITHUB_REPO_URL]` with the actual GitHub repository URL.)  

4. When updates are available, you can run:  
   ```
   git pull
   ```
   to update your local files.  

---

## **6. Modify the Script to Use Your Windows Profile Name**  
1. Open **Visual Studio Code**.  
2. Open the **gpu_stock_checker** folder inside VS Code.  
3. Locate and open **main.py**.  
4. Find this line inside `main.py`:  

   ```
   options.add_argument(f"user-data-dir=C:/Users/YOURUSER/AppData/Local/Microsoft/Edge/User Data")
   ```

5. Replace **YOURUSER** with your actual Windows profile name.  
   - To find your username, open **Command Prompt** and type:  
     ```
     echo %USERNAME%
     ```
   - Use the displayed name in **main.py**.  
6. Save the file and close VS Code.  

---

## **7. Set Up Environment Variable for WebDriver**  
1. Open **Start Menu**, search for **"Environment Variables"**, and open **"Edit the system environment variables"**.  
2. Click **"Environment Variables"**.  
3. Under **System Variables**, click **New**.  
4. Set **Variable Name** to:  
   ```
   C:\WebDriver\
   ```
5. Click **OK** to save the changes.  

---

## **8. Run the Script**  
1. Open **Command Prompt** (`Win + R`, type `cmd`, and press Enter).  
2. Navigate to your script folder:  
   ```
   cd Desktop/gpu_stock_checker
   ```
3. Run the script:  
   ```
   python main.py
   ```
4. If everything is set up correctly, the script should start running!  

---

## **Troubleshooting**  
- If you get an error about missing modules, try running:  
  ```
  pip install selenium webdriver-manager requests beautifulsoup4
  ```
- If the script fails to run due to WebDriver issues, ensure **msedgedriver.exe** is correctly placed in `C:\WebDriver\`.  
- Restart your computer if changes to environment variables don’t take effect.  

---
