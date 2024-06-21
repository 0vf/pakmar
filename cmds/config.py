# pakmar - discord moderation bot
# Copyright (C) 2024 0vf
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Bot
from typing import Literal
import utils.db as db

class config(commands.Cog):
	def __init__(self, bot: Bot) -> None:
		self.bot = bot

	@app_commands.command()
	@app_commands.describe(channel="Set new logging channel (provide channel id)")
	@app_commands.checks.has_permissions(manage_guild=True)
	async def set_log_channel(self,interaction: discord.Interaction, channel: str):
		try:
			try:
				channel_obj = await self.bot.fetch_channel(channel)
				if channel_obj.guild.id == interaction.guild.id:
					try:
						db.set_log_channel(interaction.guild.id, channel)
						await interaction.response.send_message(f"Set log channel to {channel_obj}")
					except Exception as e:
						await interaction.response.send_message(f"Unhandled exception caught:\n```\n{e}\n```", ephemeral=True)
			except Exception:
				await interaction.response.send_message(f"Invalid channel provided", ephemeral=True)
		except Exception as e:
			await interaction.response.send_message(f"Unhandled exception caught:\n```\n{e}\n```", ephemeral=True)

async def setup(bot):
	await bot.add_cog(config(bot))