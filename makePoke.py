import requests
import random

class Pokemon:
    def __init__(self,name,types,moves,diction):
        self.name = name
        self.type = types
        self.moves = moves
        self.stats = diction
    
def request_handler(request):
    poke_num = random.randint(1,802)
    to_send = "https://pokeapi.co/api/v2/pokemon/"+ str(poke_num) + "/"
    req = requests.get(to_send)
    stats = req.json()

    name = stats['name']
    typs = stats['types']

    types = []
    for typ in typs:
        types.append(typ['type']['name'])
    pokemon_moves = dict()
    moves = stats['moves']
    move_num = 0
    
    #pulls three moves
    while len(pokemon_moves) < 3:
        move_num+=1
        move_dict = random.choice(moves)
        move_name = move_dict['move']['name']
        if move_name in ("photon geyser","flying press"):
            continue
        move_url = move_dict['move']['url']
        req = requests.get(move_url)
        move_req = req.json()
        damage = move_req['power']
        damage_cls = move_req['damage_class']['url'] 
        if 'move-damage-class/2/' in damage_cls:
            phys_spec = "physical"
        elif 'move-damage-class/3/' in damage_cls: 
            phys_spec = "special"
#        if damage == None:
#            move_num -= 1
#            continue
        move_type = move_req['type']['name']
        pokemon_moves["move"+str(move_num)] = {"name" :move_name,
                                              "type" :move_type,
                                              "damage" : damage,
                                              "mode" : phys_spec}
    #pulls stats of pokemon
    base_stats = dict()
    for stat in stats['stats']:
        stat_name = stat['stat']['name']
        stat_num = stat['base_stat']
        base_stats[stat_name] = stat_num
      
    #Poke = Pokemon(name,types,pokemon_moves,base_stats)          
    return {'name': name, 
            'type' : types,
            'base stats' : base_stats,
            'moves' : pokemon_moves}
    
print(request_handler(9))

