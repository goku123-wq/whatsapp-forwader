import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

class Monitor:
    def __init__(self, driver, config):
        self.driver = driver
        self.source_group = config.get("source_group")
        self.message_limit = config.get("message_limit_per_poll", 10)
        self.processed_ids = set()

    def go_to_group(self):
        try:
            # Search for the group
            search_box = WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            search_box.clear()
            search_box.send_keys(self.source_group)
            time.sleep(2)
            
            # Click the group in search results
            group_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//span[@title="{self.source_group}"]'))
            )
            group_element.click()
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Error navigating to source group: {e}")
            return False

    def get_new_messages(self):
        if not self.go_to_group():
            return []

        try:
            # Find all message elements (incoming messages)
            message_elements = self.driver.find_elements(By.XPATH, '//div[contains(@class, "message-in")]')
            
            # Get the last N messages
            recent_elements = message_elements[-self.message_limit:]
            
            new_messages = []
            for el in recent_elements:
                try:
                    # WhatsApp uses a specific class for text content
                    text_el = el.find_element(By.XPATH, './/span[contains(@class, "selectable-text")]')
                    text = text_el.text
                    
                    # Try to get a unique identifier (like data-id)
                    try:
                        msg_id = el.get_attribute("data-id")
                    except:
                        msg_id = text # Fallback
                        
                    if msg_id and msg_id not in self.processed_ids:
                        new_messages.append({"id": msg_id, "text": text})
                        self.processed_ids.add(msg_id)
                except NoSuchElementException:
                    continue # Not a text message
                
            return new_messages
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []
