import sys
sys.path.append('/location/to/file/')
import json

with open("config.json") as f:
    data = json.loads(f.read())

back_color = data['back_color']
fruit_color = data['fruit_color']   
block_color = data['block_color']
cell_size = data['cell_size']
block_cells = data['block_cells']
table_size = data['table_size']
height = data['height']
width = data['width']
snake = data['snake']
sx = data['sx']
sy = data['sy']
keys = data["keys"]