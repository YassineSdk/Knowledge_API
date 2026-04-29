
import logfire
import os
from dotenv import load_dotenv, find_dotenv

# logfire configuration
load_dotenv(find_dotenv())

logfire.configure(
    token=os.getenv("logfire_key"),
    console=logfire.ConsoleOptions(verbose=True)
)