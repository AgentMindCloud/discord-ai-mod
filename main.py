import os
import discord
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

GROK_API_KEY = os.getenv("GROK_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

client = OpenAI(
    api_key=GROK_API_KEY,
    base_url="https://api.x.ai/v1"
)

@bot.event
async def on_ready():
    print(f"{bot.user} is now running as a Grok-powered Discord AI moderator!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    try:
        response = client.chat.completions.create(
            model="grok-beta",
            messages=[{"role": "user", "content": message.content}],
            temperature=0.7
        )
        reply = response.choices[0].message.content
        await message.channel.send(reply)
    except Exception as e:
        await message.channel.send(f"Error: {str(e)}")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
