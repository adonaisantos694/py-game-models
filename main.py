import json
from db.models import Race, Skill, Guild, Player


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as file:
        players_data = json.load(file)

    for player_data in players_data.values():
        # RACE
        race_data = player_data.get("race", {})
        race, _ = Race.objects.get_or_create(
            name=race_data.get("name", ""),
            defaults={"description": race_data.get("description", "")},
        )

        # SKILLS
        for skill_data in race_data.get("skills", []):
            Skill.objects.get_or_create(
                name=skill_data.get("name", ""),
                defaults={
                    "bonus": skill_data.get("bonus", 0),
                    "race": race,
                },
            )

        # GUILD
        guild = None
        guild_data = player_data.get("guild")
        if guild_data:
            guild, _ = Guild.objects.get_or_create(
                name=guild_data.get("name", ""),
                defaults={"description": guild_data.get("description", "")},
            )

        # PLAYER
        nickname = player_data.get("nickname") or player_data.get("name")

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player_data.get("email", ""),
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild,
            },
        )
