import sqlite3
import discord
from discord.ext import commands
from cogs.logging import get_time

class MentorCog(commands.Cog, name="Mentor"):
    def __init__(self, bot, conn):
        self.bot = bot
        self.conn = conn
        self.curr = conn.cursor()
        self.curr.execute("""CREATE TABLE IF NOT EXISTS mentors (
                                user_id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL
                                skills TEXT
                            )""")
        conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"[{await get_time()}] [INITIALIZED] Mentor Cog")

    @commands.command(name="add_mentor")
    async def add_mentor(self, ctx, member: discord.Member, skills: str):
        self.curr.execute("INSERT OR REPLACE INTO mentors VALUES (?, ?, ?)",
                                    (member.id, member.display_name, skills))
        self.conn.commit()
        await ctx.send(f"Added {member.display_name} as a mentor with skills: {skills}")

    @commands.command(name="find_mentor")
    async def find_mentor(self, ctx, skills: str):
        self.cur.execute("SELECT user_id, name FROM mentors WHERE skills = ?", (skills,))
        row = self.cur.fetchone()
        if row:
            user_id, name = row
            mentor_mention = f"<@{user_id}>"
            await ctx.send(f"Found mentor: {mentor_mention} with skills: {skills}")
        else:
            await ctx.send(f"No mentor found with skills: {skills}")

    @commands.command(name="update_mentor")
    async def update_mentor(self, ctx, member: discord.Member, skills: str):
        self.curr.execute("UPDATE mentors SET skills = ? WHERE user_id = ?", (skills, member.id))
        if self.cur.rowcount:
            self.conn.commit()
            await ctx.send(f"Updated {member.display_name}'s skills to: {skills}")
        else:
            await ctx.send("Mentor not found. Please add them first.")