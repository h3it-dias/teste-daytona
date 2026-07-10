# Import the Daytona SDK
from daytona import Daytona, DaytonaConfig

# Define the configuration
config = DaytonaConfig(api_key="dtn_72ceb3f97e586d031ba213236234fffe58f19efb30f487674f7022dfbdbb935b") # Replace with your API key

# Initialize the Daytona client
daytona = Daytona(config)

# Create the Sandbox instance
sandbox = daytona.create()

# Run code
response = sandbox.process.code_run('print("Hello World")')
print(response.result)