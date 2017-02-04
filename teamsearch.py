import os
import discord
from discord.ext import commands
from .utils.dataIO import dataIO


class TeamSearch:
    """Help find other team members to jam with"""

    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/teamsearch/teamsearch.json"
        self.search_data = dataIO.load_json(self.file_path)

    @commands.command(pass_context=True)
    async def ineedateam(self, ctx, *text):
        """Add your skills "!ineedateam unity" To remove "!ineedateam\""""
        # ctx.message.author.mention will actually @ a user, best to not use
        # that to avoid spamming users
        server_id = ctx.message.server.id
        self.check_server_id_in_search_data(server_id)
        author = ctx.message.author.name
        author_unique = "{0}-{1}".format(author, ctx.message.author.discriminator)
        if len(text) == 0:
            if author_unique in self.search_data[server_id]["looking_for_team"]:
                del self.search_data[server_id]["looking_for_team"][author_unique]
                self.save_search_data()
                await self.bot.say(
                        "{0} removed your info from looking for team!".format(
                            author
                        )
                    )
            else:
                await self.bot.say(
                        "You're not in the looking for team list {0}".format(
                            author
                        )
                    )
        else:
            author_skills = " ".join(text)
            self.search_data[server_id]["looking_for_team"][author_unique] = author_skills
            self.save_search_data()
            await self.bot.say(
                    "Added your info to looking for team {0}!".format(
                        author
                    )
                )

    @commands.command(pass_context=True)
    async def whoneedsateam(self, ctx, *text):
        """Find out who needs a team and what their skills are"""
        server_id = ctx.message.server.id
        self.check_server_id_in_search_data(server_id)
        team_needers = "People who still need teams:\n"
        for k, v in self.search_data[server_id]["looking_for_team"].items():
            team_needers = "{0}\n{1}: {2}".format(team_needers, k, v)
        await self.bot.say(team_needers)

    @commands.command(pass_context=True)
    async def myteamneeds(self, ctx, *text):
        """Add team needs "!myteamneeds art" To remove "!myteamneeds\""""
        server_id = ctx.message.server.id
        self.check_server_id_in_search_data(server_id)
        author = ctx.message.author.name
        author_unique = "{0}-{1}".format(author, ctx.message.author.discriminator)
        if len(text) == 0:
            del self.search_data[server_id]["my_team_needs"][author_unique]
            self.save_search_data()
            await self.bot.say(
                    "{0} removed your info from my team needs!".format(author)
                )
        else:
            author_text = " ".join(text)
            self.search_data[server_id]["my_team_needs"][author_unique] = author_text
            self.save_search_data()
            await self.bot.say("{0} added your info!".format(author))

    @commands.command(pass_context=True)
    async def whatteamsneed(self, ctx, *text):
        """Find out what teams need"""
        server_id = ctx.message.server.id
        self.check_server_id_in_search_data(server_id)
        team_needs = "Team needs:\n"
        for k, v in self.search_data[server_id]["my_team_needs"].items():
            team_needs = "{0}\n{1}: {2}".format(team_needs, k, v)
        await self.bot.say(team_needs)

    def check_server_id_in_search_data(self, server_id):
        """Checks if the server id is already in the search_data, if not adds
        it"""
        if server_id not in self.search_data:
            self.search_data[server_id] = {
                "my_team_needs": {},
                "looking_for_team": {}
            }
            self.save_search_data()

    def save_search_data(self):
        """Write out the teamserach data to disk"""
        dataIO.save_json(self.file_path, self.search_data)
        

def check_folders():
    """Check to see if the data folder exists for teamsearch, if not create it"""
    if not os.path.exists("data/teamsearch"):
        print("Creating data/teamsearch folder...")
        os.makedirs("data/teamsearch")


def check_files():
    """Check to see if the json file for teamsearch exists, if not create it"""
    f = "data/teamsearch/teamsearch.json"
    if not dataIO.is_valid_json(f):
        print("Creating empty teamsearch.json...")
        dataIO.save_json(f, {})


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(TeamSearch(bot))
