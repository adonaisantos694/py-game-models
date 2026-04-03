from db.models import Race, Skill, Guild, Player
import json
import os
from typing import Any, Dict

JSON_FILE = os.path.join(os.path.dirname(__file__), "players.json")


def main() -> None:
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        players_data: list[Any] = json.load(f)

    for player in players_data:
        if not isinstance(player, dict):
            # tentar interpretar string como JSON, se estiver nesse formato
            try:
                player = json.loads(player)
            except (json.JSONDecodeError, TypeError):
                continue  # ignora entradas inválidas

        # Processar raça
        race_data: Dict[str, Any] = player.get("race", {})
        race_obj = None
        if isinstance(race_data, dict):
            race_name = race_data.get("name")
            if race_name:
                race_obj, _ = Race.objects.get_or_create(name=race_name)

                # Criar skills da raça
                for skill_data in race_data.get("skills", []):
                    if isinstance(skill_data, dict):
                        skill_name = skill_data.get("name")
                        skill_bonus = skill_data.get("bonus")
                        if skill_name:
                            Skill.objects.get_or_create(
                                name=skill_name,
                                defaults={"bonus": skill_bonus,
                                          "race": race_obj}
                            )

        # Processar guild
        guild_data: Dict[str, Any] = player.get("guild", {})
        guild_obj = None
        if isinstance(guild_data, dict):
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
