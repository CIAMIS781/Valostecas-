import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")
CITIZEN_ROLE_ID = 1563746594782711869
STAFF_ROLE_ID = 1563911071088255137

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot Online - {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command")
    except Exception as e:
        print(e)

@bot.tree.command(name="rate", description="Citizen kasih rating ke Staff")
async def rate(interaction: discord.Interaction, member: discord.Member, nilai: int, alasan: str):
    # Yang nge-rate harus CITIZEN
    if not any(role.id == CITIZEN_ROLE_ID for role in interaction.user.roles):
        await interaction.response.send_message("Lu bukan Citizen, ga bisa rate!", ephemeral=True)
        return

    # Yang di-rate harus STAFF
    if not any(role.id == STAFF_ROLE_ID for role in member.roles):
        await interaction.response.send_message("Yang bisa di-rate cuma Staff!", ephemeral=True)
        return

    # Ga boleh rate diri sendiri
    if member.id == interaction.user.id:
        await interaction.response.send_message("Ga bisa rate diri sendiri!", ephemeral=True)
        return

    if nilai < 1 or nilai > 10:
        await interaction.response.send_message("Nilai harus 1-10!", ephemeral=True)
        return
    
    embed = discord.Embed(title="⭐ Valostecas Rate", color=0xFFD700)
    embed.add_field(name="Staff", value=member.mention, inline=False)
    embed.add_field(name="Nilai", value=f"{nilai}/10", inline=True)
    embed.add_field(name="Di-rate oleh", value=interaction.user.mention, inline=True)
    embed.add_field(name="Alasan", value=alasan, inline=False)
    await interaction.response.send_message(embed=embed)

bot.run(TOKEN)