import os
from openai import AzureOpenAI
from dotenv import load_dotenv

class Config:
    def __init__(self):
        self.setup_environment()
        self.client = self.initialize_azure_client()

    def setup_environment(self):
        """Set up environment variables and API configuration."""
        # Get subscription key
        self.subscription_key = os.getenv('AZURE_OPENAI_API_KEY')
        if self.subscription_key is None:
            print("# Loading from .env file")
            load_dotenv()
            self.subscription_key = os.getenv('AZURE_OPENAI_API_KEY')
            if self.subscription_key is None:
                raise ValueError("Environment variable AZURE_OPENAI_API_KEY is not set and not found in .env file")
        else:
            print("# Env variables already exist")

        # Get endpoint and deployment
        self.endpoint = os.getenv('ENDPOINT_URL')
        self.deployment = os.getenv('DEPLOYMENT_NAME')

        if not self.endpoint or not self.deployment:
            raise ValueError("ENDPOINT_URL or DEPLOYMENT_NAME environment variables are not set")

    def initialize_azure_client(self):
        """Initialize and return Azure OpenAI client."""
        return AzureOpenAI(
            azure_endpoint=self.endpoint,
            api_key=self.subscription_key,
            api_version="2024-12-01-preview"
        )

    def get_client(self):
        """Return the initialized Azure OpenAI client."""
        return self.client

    def get_deployment(self):
        """Return the deployment name."""
        return self.deployment