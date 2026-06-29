# Cloud Server Setup Guide (AWS EC2)

To keep your WhatsApp forwarding agent running 24/7 without needing your laptop on, you can host it on a free AWS EC2 instance.

## Step 1: Create an AWS Account and Instance
1. Go to [aws.amazon.com](https://aws.amazon.com/) and create a free account.
2. Search for "EC2" in the AWS Console and click **Instances** -> **Launch instances**.
3. **Name:** `WhatsAppForwarder`
4. **OS Images (AMI):** Select **Ubuntu** (the free tier eligible version).
5. **Instance type:** `t2.micro` or `t3.micro` (free tier eligible).
6. **Key pair:** Click "Create new key pair", name it `whatsapp-key`, and download the `.pem` file to your computer.
7. Click **Launch instance**.

## Step 2: Connect to your Server
1. Wait for your instance to show as "Running" in the AWS Console.
2. Select the instance and click the **Connect** button at the top.
3. Choose **EC2 Instance Connect** and click Connect. A terminal window will open in your browser.
*(Alternatively, you can use SSH from your computer's terminal using the `.pem` key you downloaded).*

## Step 3: Install Dependencies on the Server
In the server terminal, run these commands one by one to install Python, Chrome, and git:

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git chromium-browser
```

## Step 4: Transfer the Code
You can clone your code if you uploaded it to GitHub, or you can create the files manually since there are only a few.

```bash
mkdir whatsapp-forwarder
cd whatsapp-forwarder
```

*(You will need to create the files `agent.py`, `monitor.py`, `filter.py`, `forwarder.py`, `config.json`, and `requirements.txt` here using a text editor like `nano` and copy-paste your code into them).*

## Step 5: Setup Python Environment
Run these commands in the `whatsapp-forwarder` directory:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Step 6: Run the Agent in the Background
To ensure the script keeps running even after you close the terminal, we will use a tool called `tmux`.

1. Start a new session:
   ```bash
   tmux new -s whatsapp
   ```
2. Run the agent:
   ```bash
   python agent.py
   ```
3. **Scan the QR Code:** The QR code will be drawn using text blocks right in your terminal. Open WhatsApp on your phone, go to Linked Devices, and scan it!
4. **Detach:** Once it says "Logged in successfully", press `Ctrl+B`, release both keys, then press `D`. This detaches you from the session, leaving it running in the background.

You can now safely close the browser window/terminal and shut down your laptop. The agent will continue forwarding messages 24/7!

To check on it later, reconnect to the server and run: `tmux attach -t whatsapp`
