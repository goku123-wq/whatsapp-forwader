# WhatsApp Announcement Forwarding Agent

An AI agent that automatically forwards announcement messages from a school WhatsApp group to a class WhatsApp group.

## Prerequisites
- Python 3.8+
- Google Chrome installed

## Setup Instructions

1. **Install Dependencies:**
   Open a terminal in this directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Group Names:**
   Open `config.json` and change the `source_group` and `destination_group` values to exactly match the group names as they appear on your WhatsApp.
   You can also tweak the polling interval and the keywords/patterns used to identify announcements.

3. **Run the Agent:**
   Execute the agent script:
   ```bash
   python agent.py
   ```

4. **Login:**
   A Chrome window will open with WhatsApp Web. You need to scan the QR code using your phone to log in. Once logged in, the agent will begin monitoring.

## How it Works
- The agent polls the source group every `poll_interval_seconds`.
- It reads the latest messages and filters them based on the `keywords` and `patterns` defined in `config.json`.
- If an announcement is found that hasn't been forwarded yet, it will switch to the destination group and send the message, prefixing it with an "Announcement Forwarded" tag.
