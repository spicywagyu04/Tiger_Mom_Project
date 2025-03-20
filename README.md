# Tiger Mom Project

## Introduction
Tiger Mom is an AI agent prototype that uses LLM to monitor user activity during their work.

🚀 If you want to see a video demo: [https://youtu.be/LbUZTz5JUIM](https://youtu.be/LbUZTz5JUIM)

### Motivation
The goal is to offer a one-click solution to avoid distractions. Unlike browser-based extensions such as **StayFocusd**, this AI agent is far more flexible as it analyzes the **actual content** on the user's screen rather than blocking entire websites.

### How It Works
1. The prototype takes **screenshots** of the user's device.
2. Calls OpenAI's **GPT-4o** model to **analyze** screenshot contents.
3. Calls OpenAI's **GPT-4o-mini** model to **compare** the screenshot content with the user's defined **focus task** and **distraction settings**.
4. **Why GPT-4o for Vision?** It is **cheaper** to inference via the API than GPT-4o-mini for vision tasks, despite GPT-4o-mini being a lighter model.

### GUI Implementation
- Built using **PyQt5** instead of web frameworks.
- A **desktop application** is necessary as it requires **local system privileges** to take screenshots.
- Future improvements include **fine-tuning and deploying a local model** to replace GPT-4o for **screenshot vision analysis**, as screenshots may contain **private information**.

## Try Our Prototype Out Yourself

### Install Dependencies
After cloning the project onto your local device, install the required dependencies:

```bash
pip install -r requirements.txt
```

It is **recommended** that you create a new development environment before doing so.

### Set Up OpenAI API Key
Since Vision LLM is **expensive**, costing around **$0.002-0.003 per screenshot analysis**, you need to set up **your own** OpenAI API key as an environment variable. Go to [OpenAI API](https://platform.openai.com/docs/overview) to create your own API key. Then, navigate to your project directory via terminal and use the commands below:

#### On macOS/Linux:
```bash
export OPENAI_API_KEY="your-api-key-here"
```

#### On Windows (Command Prompt):
```cmd
set OPENAI_API_KEY="your-api-key-here"
```

#### On Windows (PowerShell):
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

### Run the Prototype
Now you are ready to run the prototype! Navigate to the `src` folder and run:

```bash
python main.py
```

## Future Steps
- **Reduce LLM vision inference cost**
- **Enhance GUI design for a better user experience**
- **Containerize the application for easier access**

