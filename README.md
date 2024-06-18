# Currency Exchange Rate Chat Application

This project includes a web-based chat application that allows users to query currency exchange rates from PrivatBank. The application includes a simple client interface and a WebSocket server to handle the requests.

## Features

- Fetch exchange rates for specified currencies and days.
- View available currencies.
- Log commands executed in the chat.
- Display command help on initial load.

## Files

- `index.html`: The main HTML file for the chat client interface.
- `main.css`: CSS file for styling the chat client interface.
- `main.js`: JavaScript file for handling WebSocket communication and client-side logic.
- `main.py`: Python script for the console utility to fetch exchange rates.
- `server.py`: Python script for the WebSocket server to handle chat commands and fetch exchange rates.

## Setup

### Requirements

- Python 3.12+
- aiohttp
- aiofile
- aiopath
- websockets

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/currency-exchange-chat.git
cd currency-exchange-chat
```

2. Install the required Python packages:

```bash
pip install aiohttp aiofile aiopath websockets
```

## Usage

### Running the WebSocket Server

1. Start the WebSocket server:

    ```bash
    python server.py
    ```

### Running the Console Utility

1. Fetch exchange rates for the last 2 days for EUR and USD:

    ```bash
    python main.py 2 --currencies EUR USD
    ```

### Running the Chat Client

1. Open `index.html` in your web browser.

2. The help section will display the available commands and currencies.

3. Use the chat input to enter commands, for example:

    ```text
    exchange 2 EUR USD
    ```
