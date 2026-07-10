# Import the Daytona SDK
from daytona import Daytona, DaytonaConfig
import os
from dotenv import load_dotenv

load_dotenv()

CHAVE = os.getenv("DAYTONA_API_KEY")

# Define the configuration
config = DaytonaConfig(api_key=CHAVE) # Replace with your API key

# Initialize the Daytona client
daytona = Daytona(config)

# Create the Sandbox instance
sandbox = daytona.create()

# Run code
response = sandbox.process.code_run('print("Hello World")')
print(response.result)