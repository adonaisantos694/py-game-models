import json
from db.models import Player, Race, Guild


def main():
    with open("players.json") as f:
        players_data = json.load(f)

    for data in players_data:
        nickname = data.get("nickname") or "UnknownPlayer"
        email = data.get("email")
        bio = data.get("bio")
        race_name = data.get("race")
        guild_name = data.get("guild")

        race = Race.objects.get(name=race_name) if race_name else None
        guild = Guild.objects.get(name=guild_name) if guild_name else None

        Player.objects.create(
            nickname=nickname,
            email=email,
            bio=bio,
            race=race,
            guild=guild
        )
