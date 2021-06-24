import json
import discord


async def dm_user_embed(ctx, embed):
    await ctx.author.send(embed=embed)


async def main(ctx, args):
    with open("modules.json", "r") as mo:
        modules = json.load(mo)

    for mo in modules:
        if mo['enabled']:
            with open(mo['help'], "r") as _help:
                help1 = json.load(_help)

            embed = discord.Embed(
                title=f"학교봇 도움말: {mo['command']}",
                color=discord.Color.blue()
            )

            for i in help1:
                embed.add_field(name=i['command'], value=i['description'], inline=False)
            await dm_user_embed(ctx, embed)

    await ctx.send(f"{ctx.author.mention}님, 메시지를 확인해주세요!")

