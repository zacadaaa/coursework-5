from flask import Flask, render_template, request, url_for, redirect, jsonify
from equipment import Equipment
from classes import unit_classes
from base import Arena
from unit import PlayerUnit, EnemyUnit, BaseUnit

app = Flask(__name__)

heroes = {
    "player": BaseUnit,
    "enemy": BaseUnit
}

arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template("index.html")



@app.route("/fight/")
def start_fight():
    arena.start_game(player=heroes["player"], enemy=heroes["enemy"])
    return render_template("fight.html", heroes=heroes)

@app.route("/fight/hit")
def hit():
    """Кнопка атаки"""
    if arena.game_is_running:
        result = arena.player_hit()
        return render_template("fight.html", heroes=heroes, result=result)

    return render_template("fight.html", heroes=heroes, result=arena.battle_result)


@app.route("/fight/use-skill")
def use_skill():
    """Кнопка навыка"""
    if arena.game_is_running:
        result = arena.player_use_skill()
    else:
        result = arena.battle_result

    return render_template("fight.html", heroes=heroes, result=result)

@app.route("/fight/pass-turn")
def pass_turn():
    """Кнопка пропустить ход"""
    if arena.game_is_running:
        result = arena.next_turn()
    else:
        result = arena.battle_result

    return render_template("fight.html", heroes=heroes, result=result)


@app.route("/fight/end-fight")
def end_fight():
    """кнопка завершить игру"""
    return render_template("index.html", heroes=heroes)


@app.route("/choose-hero/", methods=['post', 'get'])
def choose_hero():
    """кнопка выбор героя"""
    if request.method == "GET":
        result = {
            "classes": unit_classes,
            "weapons": equipment.get_weapons_names(),
            "armors": equipment.get_armors_names(),
            "header": "Выберите героя",
        }
        return render_template("hero_choosing.html", result=result)

    elif request.method == "POST":
        name = request.form.get("name")
        unit_class = request.form.get("unit_class")
        weapon_name = request.form.get("weapon")
        armor_name = request.form.get("armor")

        player = PlayerUnit(name=name, unit_class=unit_classes.get(unit_class))

        if weapon_name not in equipment.get_weapons_names() or armor_name not in equipment.get_armors_names():
            return jsonify(error="Не хватает данных для начала игры. "), 400

        player.equip_weapon(equipment.get_weapon(weapon_name))
        player.equip_armor(equipment.get_armor(armor_name))

        heroes["player"] = player
        return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    if request.method == "GET":
        result = {
            "classes": unit_classes,
            "weapons": equipment.get_weapons_names(),
            "armors": equipment.get_armors_names(),
            "header": "Выберите противника",
        }
        return render_template("hero_choosing.html", result=result)

    elif request.method == "POST":
        name = request.form.get("name")
        unit_class = request.form.get("unit_class")
        weapon_name = request.form.get("weapon")
        armor_name = request.form.get("armor")

        enemy = EnemyUnit(name=name, unit_class=unit_classes.get(unit_class))

        if weapon_name not in equipment.get_weapons_names() or armor_name not in equipment.get_armors_names():
            return jsonify(error="Не хватает данных для начала игры. "), 400

        enemy.equip_weapon(equipment.get_weapon(weapon_name))
        enemy.equip_armor(equipment.get_armor(armor_name))

        heroes["enemy"] = enemy
        return redirect(url_for("start_fight"))


if __name__ == "__main__":
    app.run()