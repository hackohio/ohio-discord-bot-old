import multiprocessing
import discord
import web

if __name__ == "__main__":
    discord_process = multiprocessing.Process(target=discord.start)
    web_process = multiprocessing.Process(target=web.start)
    discord_process.start()
    web_process.start()
