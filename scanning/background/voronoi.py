# NOTE: this uses https://github.com/xiaoxiae/Voronoi
from Voronoi.voronoi import *

generate(
    path = "voronoi.pdf",
    width = 4960,
    height = 3508,
    regions = 80,
    colors = ["#000000"],
    border_size = 80,
    border_color = "#ffffff",
)
