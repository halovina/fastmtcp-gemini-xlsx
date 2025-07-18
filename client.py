import asyncio
from fastmcp import Client
import google.generativeai as genai
import os

# Local Python script
client = Client("server.py")

async def main():
    async with client:
        """
        Connects to the MCP server, retrieves CSV data,
        and sends it to the Gemini API for analysis.
        """
        
        ping = await client.ping()
        print(f"Server ping result: {ping}")

        result = await client.call_tool("get_source_data", {})
        print(f"Source Data: {result.content[0].text}")

        # Configure the Gemini API key
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

        # Initialize the Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Create a prompt for analysis
        prompt = f"""
        Analyze the following sales data and provide a brief summary of the trends.
        What is the projected sales figure for 2025 based on this data?

        Data:
        {result.content[0].text}
        """

        # Generate content using the Gemini model
        response = model.generate_content(prompt)

        print("--- Gemini Analysis ---")
        print(response.text)
        print("-----------------------")


if __name__ == "__main__":
    asyncio.run(main())