import json
from db.models import Race, Skill, Player, Guild


def main() -> None:
    with open("players.json") as f:
        players_data = json.load(f)

    for nickname, data in players_data.items():
        email = data.get("email")
        bio = data.get("bio")

        # Race (verifica se existe antes)
        race_data = data.get("race")
        race_obj = None
        if race_data:
            race_name = race_data.get("name")
            race_desc = race_data.get("description")
            race_obj, _ = Race.objects.get_or_create(
                name=race_name, defaults={"description": race_desc}
            )

            # Skills (nome único globalmente)
            for skill_data in race_data.get("skills", []):
                skill_name = skill_data.get("name")
                skill_bonus = skill_data.get("bonus")
                # Se a skill já existe, não cria duplicado
                skill_obj, _ = Skill.objects.get_or_create(
                    name=skill_name,
                    defaults={"bonus": skill_bonus}
                )
                # Associar skill à raça se ainda não estiver associada
                if race_obj not in skill_obj.race_set.all():
                    skill_obj.race_set.add(race_obj)

        # Guild (verifica se existe)
        guild_data = data.get("guild")
        guild_obj = None
        if guild_data:
            guild_name = guild_data.get("name")
            guild_desc = guild_data.get("description")
            guild_obj, _ = Guild.objects.get_or_create(
                name=guild_name, defaults={"description": guild_desc}
            )

        # Player
        Player.objects.get_or_create(
            nickname=nickname,
            defaults={
                "email": email,
                "bio": bio,
                "race": race_obj,
                "guild": guild_obj,
            },
        )
