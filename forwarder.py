import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

class Forwarder:
    def __init__(self, driver, config):
        self.driver = driver
        self.destination_group = config.get("destination_group")

    def forward_message(self, message_text):
        try:
            # Search for the destination group
            search_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            # Send Ctrl+A and Backspace to clear it out
            search_box.send_keys(Keys.CONTROL + "a")
            search_box.send_keys(Keys.BACKSPACE)
            search_box.send_keys(self.destination_group)
            time.sleep(2)
            
            # Click the group in search results
            group_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//span[@title="{self.destination_group}"]'))
            )
            group_element.click()
            time.sleep(2)
            
            # Type and send message
            message_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            formatted_message = f"📢 *Forwarded Announcement* 📢\n\n{message_text}"
            
            # Send message line by line to handle newlines
            for line in formatted_message.split('\n'):
                message_box.send_keys(line)
                message_box.send_keys(Keys.SHIFT + Keys.ENTER)
                
            # Press enter to send
            message_box.send_keys(Keys.ENTER)
            time.sleep(1) # Wait for send
            print(f"Forwarded: {formatted_message[:50]}...")
            return True
        except Exception as e:
            print(f"Error forwarding message: {e}")
            return False
