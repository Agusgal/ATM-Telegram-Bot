import matplotlib.pyplot as plt
import tilemapbase

tilemapbase.init(create=True)
t = tilemapbase.tiles.build_OSM()



p1 = (-34.5883513486337, -58.4108953468498)
p2 = (-34.5904634090465, -58.4083852561492)
p3 = (-34.5909053874505, -58.41486)

tol = 0.005
tolV = 0.005
tolH = 0.0065
latitud , longitud = (-34.591709, -58.411303)
ubicacion = (-58.411303709, -34.591709)

north1, east1, south1, west1 = (latitud + tolV, longitud + tolH, latitud - tolV, longitud - tolH)

extent = tilemapbase.Extent.from_lonlat(longitud - tol, longitud + tol,
                  latitud - tol, latitud + tol)
extent = extent.to_aspect(1)



fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

plotter = tilemapbase.Plotter(extent, t, width=600)
plotter.plot(ax, t)

x, y = tilemapbase.project(*ubicacion)
x1, y1 = tilemapbase.project(p1[1], p1[0])
x2, y2 = tilemapbase.project(p2[1], p2[0])
x3, y3 = tilemapbase.project(p3[1], p3[0])



ax.plot(x, y, marker="v", color="firebrick", linewidth=20, markersize=15)
ax.plot(x1, y1, marker="*", color="b", linewidth=20, markersize=15)
ax.plot(x2, y2, marker="*", color="b", linewidth=20, markersize=15)
ax.plot(x3, y3, marker="*", color="b", linewidth=20, markersize=15)


fig.savefig("test.png", dpi=200)
plt.show()


