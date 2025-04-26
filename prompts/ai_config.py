from dotenv import dotenv_values
config = dotenv_values()

HOST = config.get("HOST")
PORT = config.get("PORT")
YOUR_SECRET_GROQ_TOKEN = config.get("GROQ_TOKEN")
URL = f"http://{HOST}:{PORT}/"

groq = {"YOUR_SECRET_GROQ_TOKEN" : YOUR_SECRET_GROQ_TOKEN,
        "MODEL" : "meta-llama/llama-4-maverick-17b-128e-instruct",
        "MESSAGES" : list(),
        "TEMPERATURE" : 1,
	    "MAX_COMPLETION_TOKENS": 4096,
	    "TOP_P": 1,
        "STREAM": False,
        "STOP": None,
        }
