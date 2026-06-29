import json

class Filter:
    def __init__(self, config_path="config.json"):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.keywords = [k.lower() for k in self.config.get("keywords", [])]
        self.patterns = self.config.get("patterns", [])

    def is_announcement(self, message_text):
        if not message_text:
            return False
            
        text_lower = message_text.lower()
        
        # Check patterns (emojis, etc.)
        for pattern in self.patterns:
            if pattern in message_text:
                return True
                
        # Check keywords
        for keyword in self.keywords:
            if keyword in text_lower:
                return True
                
        return False
