# NOTE: this uses https://github.com/xiaoxiae/Voronoi
from Voronoi.voronoi import *

generate(
    path = "voronoi.pdf",
    width = 1754,
    height = 1240,
    regions = 80,
    colors = ["#000000"],
    border_size = 35,
    border_color = "#ffffff",
)
