import json
import time
import os
import qrcode
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from monitor import Monitor
from filter import Filter
from forwarder import Forwarder

def load_config(config_path="config.json"):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def setup_driver():
    print("Setting up Chrome driver (Headless)...")
    options = webdriver.ChromeOptions()
    
    # Headless arguments required for cloud servers
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    
    # Persist session to avoid logging in every time
    session_dir = os.path.join(os.getcwd(), 'whatsapp_session')
    options.add_argument(f"user-data-dir={session_dir}")
    
    # Use a normal user agent so WhatsApp doesn't block headless Chrome
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def print_qr(driver):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        # Wait for the QR code canvas to appear
        qr_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-ref]'))
        )
        data_ref = qr_container.get_attribute("data-ref")
        
        if data_ref:
            print("\n" + "="*50)
            print("SCAN THIS QR CODE WITH YOUR PHONE'S WHATSAPP")
            print("="*50 + "\n")
            
            qr = qrcode.QRCode()
            qr.add_data(data_ref)
            qr.make(fit=True)
            # invert=True helps it render better on dark terminals
            qr.print_ascii(invert=True)
            print("\n" + "="*50 + "\n")
            return True
    except Exception as e:
        # If no QR code, maybe we are already logged in
        return False
        
def main():
    print("Starting WhatsApp Forwarder Agent...")
    config = load_config()
    
    driver = setup_driver()
    driver.get("https://web.whatsapp.com/")
    print("Waiting for WhatsApp Web to load...")
    
    # Try printing QR if we are not logged in
    print_qr(driver)
    
    # Wait until user logs in (search box is present)
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    
    try:
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        print("Logged in successfully!")
    except Exception as e:
        print("Login timed out or failed. Exiting.")
        driver.quit()
        return

    monitor = Monitor(driver, config)
    msg_filter = Filter("config.json")
    forwarder = Forwarder(driver, config)
    
    poll_interval = config.get("poll_interval_seconds", 5)
    
    print(f"Monitoring '{config.get('source_group')}' for announcements...")
    
    try:
        while True:
            print("Checking for new messages...")
            new_messages = monitor.get_new_messages()
            for msg in new_messages:
                text = msg["text"]
                if msg_filter.is_announcement(text):
                    print(f"Announcement detected! Forwarding...")
                    if forwarder.forward_message(text):
                        # Switch back to source group to continue monitoring
                        monitor.go_to_group()
                        time.sleep(1)
            time.sleep(poll_interval)
    except KeyboardInterrupt:
        print("Agent stopped by user.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
