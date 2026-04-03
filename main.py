from db.models import Race, Skill, Guild, Player
import json
import os

JSON_FILE = os.path.join(os.path.dirname(__file__), "players.json")


def main() -> None:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        players_data = json.load(f)

    for player in players_data:
        # Processar raça
        race_data = player.get("race")
        race_obj = None
        if race_data:
            race_name = race_data.get("name")
            if race_name:
                race_obj, _ = Race.objects.get_or_create(name=race_name)

                # Criar skills da raça
                for skill_data in race_data.get("skills", []):
                    skill_name = skill_data.get("name")
                    skill_bonus = skill_data.get("bonus")
                    if skill_name:
                        Skill.objects.get_or_create(
                            name=skill_name,
                            defaults={"bonus": skill_bonus, "race": race_obj}
                        )

        # Processar guild
        guild_data = player.get("guild")
        guild_obj = None
        if guild_data:
            guild_name = guild_data.get("name")
            if guild_name:
                guild_obj, _ = Guild.objects.get_or_create(name=guild_name)

        # Criar player
        player_name = player.get("name")
        if not player_name:
            continue
        Player.objects.get_or_create(
            name=player_name,
            defaults={
                "race": race_obj,
                "guild": guild_obj
            }
        )


if __name__ == "__main__":
    main()
