# Evil Telegram Bot
This is basically regular chat gpt with Telegram Bot user interface. Its a test project to play around with telegram bots and promt adjustment.

### 1. Clone the Repository

Clone this repository to your local machine using:

```bash
git clone https://github.com/rifolio/EvilTelegramGptBot
```

### 2. Set Up Virtual Environment

Navigate to the project directory and set up a virtual environment by running:

```bash
python3 -m venv ai
```

### 3. Activate Virtual Environment

Activate the virtual environment using:

```bash
source ai/bin/activate
```

### 4. Install Dependencies

Install the project dependencies using pip:

```bash
pip3 install -r requirements.txt
```

The `requirements.txt` file contains the following packages:

```
telegram
langchain_community
langchain_openai
langchain
python-telegram-bot
pandas
llama-index
python-dotenv
openai
tiktoken
```

### 5. Initialize API KEY from your OPEN AI Account in .env file and Run the Project

```bash
.env:
OPENAI_API_KEY=
TELEGRAM_TOKEN=
```

Once the dependencies are installed, you can run the project using:

For Bot UI
```bash
python3 bot.py
```