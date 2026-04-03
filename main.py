import json
from db.models import Race, Skill, Guild, Player


def main() -> None:
    with open("players.json", "r", encoding="utf-8") as file:
        players_data = json.load(file)

    unknown_count = 0  # contador para players sem nickname ou name

    for player_data in players_data.values():
        # --- RACE ---
        race_data = player_data.get("race", {})
        race_name = race_data.get("name", "")
        race_description = race_data.get("description", "")

        race, _ = Race.objects.get_or_create(
            name=race_name,
            defaults={"description": race_description},
        )

        # --- SKILLS ---
        for skill_data in race_data.get("skills", []):
            skill_name = skill_data.get("name", "")
            Skill.objects.get_or_create(
                name=skill_name,
                defaults={
                    "bonus": skill_data.get("bonus", 0),
                    "race": race,
                },
            )

        # --- GUILD ---
        guild_data = player_data.get("guild")
        guild = None
        if guild_data:
            guild_name = guild_data.get("name", "")
            guild_description = guild_data.get("description", "")
            guild, _ = Guild.objects.get_or_create(
                name=guild_name,
                defaults={"description": guild_description},
            )

        # --- PLAYER ---
        nickname = player_data.get("nickname") or player_data.get("name")
        if not nickname:
            unknown_count += 1
            nickname = f"UnknownPlayer{unknown_count}"

        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": player_data.get("email", ""),
                "bio": player_data.get("bio", ""),
                "race": race,
                "guild": guild,
            },
        )


if __name__ == "__main__":
    main()
