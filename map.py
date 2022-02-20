import matplotlib.pyplot as plt
import tilemapbase


def createMap(lat, long, points):
    """
    Crea mapa a partir de OpenStreetmaps y libreria tilemapbase, luego o guarda en formato png para enviarlo al usuario

    Parametros:
    ------------

    lat: float
        latitud del centro del mapa (grados)
    long: float
        longitud del centro del mapa (grados)
    points: list
        lista con puntos que quiere marcarse en el mapa (ubicacion de bancos)
    """

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
        x, y = tilemapbase.project(point[1], point[0])
        ax.plot(x, y, marker="*", color="b", linewidth=20, markersize=15)

    fig.savefig("map.png", dpi=200)






