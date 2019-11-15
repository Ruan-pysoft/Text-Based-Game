import items, tiles, json

_world = {}
starting_position = [0, 0]

def save():
    world = {}
    for k, v in _world.items():
        if v != None: world[k] = v.save()
        else: world[k] = None
    return world

def load(data):
    #print(data)
    for k, v in data.items():
        _world[k] = tiles.MapTile.load(v)
        if v != None:
            if _world[k].start:
                global starting_position
                starting_position = k

def load_tiles(world):
    """Parses a file that describes the world space into the _world object"""
    with open('resources/'+str(world)+'.map', 'r') as m:
        rows = m.readlines()
    x_max = len(rows[0].split('\t')) # Assumes all rows contain the same number of tabs
    for y in range(len(rows)):
        cols = rows[y].split('\t')
        for x in range(x_max):
            tile_name = cols[x].replace('\n', '') # Windows users may need to replace '\r\n'
            _world[json.dumps([x,y])] = None if tile_name == '' else getattr(__import__('tiles'), tile_name)(x, y)
            if _world[json.dumps([x, y])] != None:
                if _world[json.dumps([x, y])].start:
                    global starting_position
                    starting_position = [x, y]

def tile_exists(x, y):
    return _world.get(json.dumps([x, y]))
