const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcodeTerminal = require('qrcode-terminal');
const express = require('express');
const qrcode = require('qrcode');

// ==========================================
// CONFIGURATION
// ==========================================
// Replace these with the EXACT names of the groups as they appear on your phone
const SOURCE_GROUP_NAME = 'vvhss up and hs';
const DESTINATION_GROUP_NAME = '7c vvhss';

// Set this to true if you want to forward a message with a prefix
const ADD_PREFIX = false;
const PREFIX = 'Forwarded from School Group:\n\n';
// ==========================================

// Web Server Setup
const app = express();
const PORT = process.env.PORT || 3000;

let botStatus = 'Initializing...';
let qrCodeDataURL = null;

const puppeteerOptions = {
    headless: true,
    args: [
        '--no-sandbox', 
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--no-zygote',
        '--single-process', // <- this one doesn't works in Windows
        '--disable-gpu'
    ]
};

if (process.env.PUPPETEER_EXECUTABLE_PATH) {
    puppeteerOptions.executablePath = process.env.PUPPETEER_EXECUTABLE_PATH;
}

// Initialize the client
const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: puppeteerOptions
});

let destinationChatId = null;
let sourceChatId = null;

client.on('qr', async (qr) => {
    botStatus = 'Waiting for QR scan...';
    console.log('Please scan this QR code with your WhatsApp app (Linked Devices):');
    qrcodeTerminal.generate(qr, { small: true });
    
    // Generate base64 image for the web server
    try {
        qrCodeDataURL = await qrcode.toDataURL(qr);
    } catch (err) {
        console.error('Failed to generate QR Data URL', err);
    }
});

client.on('ready', async () => {
    botStatus = 'Ready and Forwarding messages!';
    qrCodeDataURL = null; // Clear the QR code once connected
    console.log('WhatsApp Client is ready!');
    console.log(`Looking for groups: "${SOURCE_GROUP_NAME}" and "${DESTINATION_GROUP_NAME}"...`);

    const chats = await client.getChats();

    const sourceChat = chats.find(chat => chat.isGroup && chat.name === SOURCE_GROUP_NAME);
    const destChat = chats.find(chat => chat.isGroup && chat.name === DESTINATION_GROUP_NAME);

    if (sourceChat) {
        sourceChatId = sourceChat.id._serialized;
        console.log(`✅ Found Source Group: ${SOURCE_GROUP_NAME}`);
    } else {
        console.log(`❌ Could not find Source Group: "${SOURCE_GROUP_NAME}". Please check the exact name.`);
    }

    if (destChat) {
        destinationChatId = destChat.id._serialized;
        console.log(`✅ Found Destination Group: ${DESTINATION_GROUP_NAME}`);
    } else {
        console.log(`❌ Could not find Destination Group: "${DESTINATION_GROUP_NAME}". Please check the exact name.`);
    }

    if (sourceChat && destChat) {
        console.log('\n🚀 Forwarding service is ACTIVE. Listening for messages...');
    } else {
        console.log('\n⚠️ Forwarding is currently DISABLED because one or both groups were not found.');
    }
});

client.on('message', async (msg) => {
    // Only process if both groups have been found
    if (!sourceChatId || !destinationChatId) return;

    if (msg.from === sourceChatId) {
        try {
            console.log(`\n[${new Date().toLocaleTimeString()}] Received new message in ${SOURCE_GROUP_NAME}`);
            
            if (msg.hasMedia || !ADD_PREFIX) {
                await msg.forward(destinationChatId);
                console.log(`-> Forwarded successfully to ${DESTINATION_GROUP_NAME}`);
            } else {
                await client.sendMessage(destinationChatId, PREFIX + msg.body);
                console.log(`-> Copied text successfully to ${DESTINATION_GROUP_NAME}`);
            }
        } catch (error) {
            console.error(`-> Failed to forward message:`, error);
        }
    }
});

client.on('disconnected', (reason) => {
    console.log('Client was logged out', reason);
    botStatus = 'Disconnected';
});

// Start the WhatsApp Client
client.initialize();

// Setup the Express Server Routes
app.get('/', (req, res) => {
    let html = `<h1>WhatsApp Forwarder Status: ${botStatus}</h1>`;
    
    if (qrCodeDataURL) {
        html += `<p>Scan the QR code below to log in:</p>`;
        html += `<img src="${qrCodeDataURL}" alt="QR Code" />`;
    }
    
    res.send(html);
});

// Start the Express Web Server
app.listen(PORT, () => {
    console.log(`Web server running on port ${PORT}`);
});
