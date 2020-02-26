import requests
import random
import sqlite3

def pokemon_DB():

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS pokemon (name text,
                    type text,
                    base_stats text,
                    moves text,
                    back text,
                    front text);''')

    def add_pokemon(poke_num):
        """
            function that transfers all data from pokemon api to aws dynamoDB.
            makes call to API stores info in DB to be used later.

        """

        to_send = "https://pokeapi.co/api/v2/pokemon/"+ str(poke_num) + "/"
        req = requests.get(to_send)
        stats = req.json()

        name = stats['name']
        typs = stats['types']
        types = [typ['type']['name'] for typ in typs]

        pokemon_moves = dict()
        moves = stats['moves']
        front = stats['sprites']['front_default']
        back = stats['sprites']['back_default']
        print("pokemon " + str(poke_num) + " has " + str(len(moves)) + " moves")
        all_moves = ''
        for m in moves:
            move = m['move']
            move_num = int(move['url'].split('/')[-2])
            all_moves += str(move_num) + ","

        print(all_moves)

        base_stats = dict()
        for stat in stats['stats']:
            stat_name = stat['stat']['name']
            stat_num = stat['base_stat']
            base_stats[stat_name] = stat_num

        something = {'name': str(name),
                    'type' : str(types),
                    'base stats' : str(base_stats),
                    }
        c.execute('''INSERT into pokemon VALUES (?,?,?,?,?,?);''',(str(name),str(types),str(base_stats),all_moves,front,back)) #with time

        return "DONE"

    print("filling database....")
    for num in range(1,803):
        print("adding pokemon " + str(num) + ": " )
        try:
            print(add_pokemon(num))
        except:
            print("something fucked up")

    conn.commit()
    conn.close()
    print("pokemon DB YEETED")

def move_DB():

    conn = sqlite3.connect('example.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS moves (move_number int, name text,type text, damage text, mode text,priority text);''')

    def add_move(move_num):
        """
            function that transfers all data from pokemon api to aws dynamoDB.
            makes call to API stores info in DB to be used later.

        """

        to_send = "https://pokeapi.co/api/v2/move/"+ str(move_num) + "/"
        req = requests.get(to_send)
        stats = req.json()
        name = stats['name']
        damage = stats['power']
        damage_cls = stats['damage_class']['url']
        priority = stats['priority']
        if 'move-damage-class/2/' in damage_cls:
            phys_spec = "physical"
        elif 'move-damage-class/3/' in damage_cls:
            phys_spec = "special"
        move_type = stats['type']['name']

        print("SQL Row: " + str((move_num,str(name),str(move_type),damage,damage_cls,priority)))

        c.execute('''INSERT into pokemon VALUES (?,?,?,?,?,?);''',(move_num,str(name),str(move_type),damage,phys_spec,priority)) #with time

        return "DONE"

    print("filling database....")
    for num in range(1,719):
        print("adding move  " + str(num) + ": " )

        try:
            print(add_move(num))
        except:
            print("something fucked up")

    conn.commit()
    conn.close()
    print("move DB YEETED")


if __name__ == '__main__':
    pokemon_DB()
    move_DB()
