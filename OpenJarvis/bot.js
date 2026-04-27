/**
 * WhatsApp Bridge for OpenJarvis
 * 
 * This bot connects Jarvis AI agent to WhatsApp,
 * allowing you to interact with your AI assistant via chat.
 */

require('dotenv').config();
const { Client, LocalAuthStrategy } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const http = require('http');

// Configuration
const JARVIS_API_URL = process.env.JARVIS_API_URL || 'http://localhost:8000';
const ALLOWED_NUMBERS = process.env.ALLOWED_NUMBERS?.split(',') || [];

console.log('🤖 OpenJarvis WhatsApp Bot starting...');

// Initialize WhatsApp client
const client = new Client({
    authStrategy: new LocalAuthStrategy(),
    puppeteer: {
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
});

// Generate QR code for authentication
client.on('qr', (qr) => {
    console.log('\n📱 Scan this QR code with WhatsApp:');
    qrcode.generate(qr, { small: true });
});

// Client ready
client.on('ready', () => {
    console.log('✅ WhatsApp client is ready!');
    console.log('📞 Connected as:', client.info.pushname);
});

// Handle messages
client.on('message', async (message) => {
    const from = message.from;
    const body = message.body;
    
    // Check if message is from allowed number (if restriction is set)
    if (ALLOWED_NUMBERS.length > 0 && !ALLOWED_NUMBERS.includes(from)) {
        console.log(`⚠️ Blocked message from unauthorized number: ${from}`);
        return;
    }
    
    // Only respond to direct messages or mentions
    if (!message.fromMe && (body.startsWith('jarvis') || body.startsWith('Jarvis'))) {
        console.log(`📨 Received message from ${from}: ${body}`);
        
        // Send typing indicator
        await message.channel.sendStateTyping();
        
        try {
            // Call Jarvis API
            const response = await callJarvis(body);
            
            // Send response
            await message.reply(response);
            console.log(`✅ Response sent to ${from}`);
        } catch (error) {
            console.error('❌ Error calling Jarvis:', error);
            await message.reply('Sorry, I encountered an error processing your request.');
        }
    }
});

/**
 * Call Jarvis AI agent
 */
function callJarvis(prompt) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify({ prompt: prompt });
        
        const options = {
            hostname: 'localhost',
            port: 8000,
            path: '/ask',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        };
        
        const req = http.request(options, (res) => {
            let responseData = '';
            
            res.on('data', (chunk) => {
                responseData += chunk;
            });
            
            res.on('end', () => {
                try {
                    const response = JSON.parse(responseData);
                    resolve(response.response || response.message || 'Task completed');
                } catch (e) {
                    resolve(responseData || 'Task completed');
                }
            });
        });
        
        req.on('error', (error) => {
            // Fallback: If API is not available, return a simple response
            console.log('⚠️ Jarvis API not available, using fallback');
            resolve('I received your message but the AI service is currently unavailable. Please try again later.');
        });
        
        req.write(data);
        req.end();
    });
}

// Handle authentication failure
client.on('auth_failure', (msg) => {
    console.error('❌ Authentication failed:', msg);
});

// Handle disconnected
client.on('disconnected', (reason) => {
    console.log('🔌 Disconnected:', reason);
});

// Start the client
client.initialize()
    .then(() => {
        console.log('🚀 Bot initialization complete');
    })
    .catch((err) => {
        console.error('❌ Initialization error:', err);
        process.exit(1);
    });

// Graceful shutdown
process.on('SIGINT', async () => {
    console.log('\n👋 Shutting down...');
    await client.destroy();
    process.exit(0);
});
