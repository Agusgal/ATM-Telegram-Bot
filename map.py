import matplotlib.pyplot as plt
import tilemapbase


def createMap(lat, long, points):
    tilemapbase.init(create=True)
    t = tilemapbase.tiles.build_OSM()
    tol = 0.005

    extent = tilemapbase.Extent.from_lonlat(long - tol, long + tol,
                                            lat - tol, lat + tol)
    extent = extent.to_aspect(1)

    fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    plotter = tilemapbase.Plotter(extent, t, width=600)
    plotter.plot(ax, t)

    xc, yc = tilemapbase.project(long, lat)
    ax.plot(xc, yc, marker="v", color="firebrick", linewidth=20, markersize=15)
    for point in points:
        x, y = tilemapbase.project(point[0], point[1])
        ax.plot(x, y, marker="*", color="b", linewidth=20, markersize=15)

    fig.savefig("map.png", dpi=200)


#p1 = (-34.5883513486337, -58.4108953468498)
#p2 = (-34.5904634090465, -58.4083852561492)
#p3 = (-34.5909053874505, -58.41486)

#latitud , longitud = (-34.591709, -58.411303)
#ubicacion = (-58.411303709, -34.591709)




