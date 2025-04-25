from dotenv import dotenv_values
config = dotenv_values()

HOST = config.get("HOST")
PORT = config.get("PORT")
YOUR_SECRET_GROQ_TOKEN = config.get("GROQ_TOKEN")
URL = f"http://{HOST}:{PORT}/"

groq = {"YOUR_SECRET_GROQ_TOKEN" : YOUR_SECRET_GROQ_TOKEN,
        "MODEL" : "deepseek-r1-distill-llama-70b",
        "MESSAGES" : list(),
        "TEMPERATURE" : 1,
	    "MAX_COMPLETION_TOKENS": 1024,
	    "TOP_P": 1,
        "STREAM": False,
        "STOP": None,
        }