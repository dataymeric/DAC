import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pickle
import pandas as pd
from sklearn.base import BaseEstimator


POI_FILENAME = "../data/poi-paris.pkl"
parismap = mpimg.imread("../data/paris-48.806-2.23--48.916-2.48.jpg")
## coordonnees GPS de la carte
xmin, xmax = 2.23, 2.48  # coord_x min et max
ymin, ymax = 48.806, 48.916  # coord_y min et max
coords = [xmin, xmax, ymin, ymax]


class Density(BaseEstimator):
    def fit(self, data):
        """Apprend l'estimateur sur les données passées."""
        pass

    def predict(self, data):
        """Prédit la densité."""
        pass

    def score(self, data):
        """Renvoie la log-vraisemblance de l'estimateur.

        Pour éviter de passer des valeurs nulles au log (ce qu'il n'aime pas), on ajoute
        une très petite valeur à chaque vraisemblance avant de passer au log.
        """
        density = self.predict(data) + 1e-10
        return np.sum(np.log(density))


class Histogramme(Density):
    def __init__(self, steps=10):
        Density.__init__(self)
        self.steps = steps

    def fit(self, x):
        self.density, self.bins = np.histogramdd(x, bins=self.steps, density=True)

    def to_bin(self, x):
        """Retourne l'index de la bin correspondante pour chaque valeur dans la liste
        'values' en utilisant les bords des bins d'un histogramme à d dimensions.
        """
        # Vérifier que les dimensions correspondent
        assert x.shape[-1] == len(
            self.bins
        ), "Le nombre de dimensions ne correspond pas"
        bin_indices = []
        # Parcours de toutes les dimensions
        for dim in range(x.shape[-1]):
            bin_indices.append(np.searchsorted(self.bins[dim], x[:, dim], side="right"))
            # équivalent : np.digitize(x[:,dim], self.bins[dim])
        bin_indices = np.array(bin_indices) - 1
        bin_indices = np.where(bin_indices == self.steps, self.steps - 1, bin_indices)
        return np.stack(np.array(bin_indices), axis=-1)

    def predict(self, x):
        prediction = []
        bin_indices = self.to_bin(x)
        for i in bin_indices:
            prediction.append(self.density[tuple(i)])
        return np.array(prediction)


class KernelDensity(Density):
    def __init__(self, kernel=None, sigma=0.1):
        Density.__init__(self)
        self.kernel = kernel
        self.sigma = sigma

    def fit(self, x):
        self.x = x

    def predict(self, data):
        n, d = self.x.shape
        denominateur = n * self.sigma**d
        prediction = []  # = np.zeros(len(data))
        for x in data:
            prediction.append(np.sum(self.kernel((x - self.x) / self.sigma), axis=0))
        return np.array(prediction) / denominateur


class NadarayaWatson(Density):
    def __init__(self, kernel=None, sigma=0.1):
        Density.__init__(self)
        self.kernel = kernel
        self.sigma = sigma

    def fit(self, x, y):
        self.x = x
        self.y = y

    def predict(self, data):
        prediction = []
        for x in data:
            noyau = self.kernel((x - self.x) / self.sigma) + 1e-10
            prediction.append(np.sum(self.y * noyau) / np.sum(noyau))
        return np.array(prediction)


def kernel_uniform(x):
    """Implémentation du noyau uniforme à d dimensions."""
    return np.all(np.abs(np.array(x)) <= 0.5, axis=1)


def kernel_gaussian(x):
    """Implémentation du noyau gaussien à d dimensions."""
    d = x.shape[-1]
    return (2 * np.pi) ** (-d / 2) * np.exp(-0.5 * np.linalg.norm(x, axis=1) ** 2)


def moindres_carres(y_true, y_pred):
    """Renvoie l'erreur des moindres carrés."""
    return np.sum(np.abs(y_true - y_pred) / len(y_true))


def get_density2D(f, data, steps=100):
    """Calcule la densité en chaque case d'une grille steps x steps dont les bornes sont
    calculées à partir du min/max de data. Renvoie la grille estimée et la discrétisation
    sur chaque axe."""
    xmin, xmax = data[:, 0].min(), data[:, 0].max()
    ymin, ymax = data[:, 1].min(), data[:, 1].max()
    xlin, ylin = np.linspace(xmin, xmax, steps), np.linspace(ymin, ymax, steps)
    xx, yy = np.meshgrid(xlin, ylin)
    grid = np.c_[xx.ravel(), yy.ravel()]
    res = f.predict(grid).reshape(steps, steps)
    return res, xlin, ylin


def add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    from mpl_toolkits import axes_grid1

    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1.0 / aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


def show_density(f, data, steps=100, log=False, animate=False, axis=plt):
    """Dessine la densité f et ses courbes de niveau sur une grille 2D calculée à partir
    de data, avec un pas de discrétisation de steps. Le paramètre log permet d'afficher
    la log densité plutôt que la densité brute"""
    res, xlin, ylin = get_density2D(f, data, steps)
    xx, yy = np.meshgrid(xlin, ylin)
    if not animate and axis == plt:
        plt.figure()
    im = show_img(axis=axis)
    if log:
        res = np.log(res + 1e-10)
    axis.scatter(data[:, 0], data[:, 1], alpha=0.8, s=3)
    im = show_img(res, axis=axis)
    if not animate:
        add_colorbar(im, aspect=10, pad_fraction=-3)
    else:
        plt.colorbar(im, shrink=0.66, aspect=20 * 0.66)
    axis.contour(xx, yy, res, 20)
    plt.tight_layout()


def show_img(img=parismap, axis=plt):
    """Affiche une matrice ou une image selon les coordonnées de la carte de Paris."""
    origin = "lower" if len(img.shape) == 2 else "upper"
    alpha = 0.3 if len(img.shape) == 2 else 1.0
    return axis.imshow(img, extent=coords, aspect=1.5, origin=origin, alpha=alpha)
    ## extent pour controler l'echelle du plan


def load_poi(typepoi, fn=POI_FILENAME):
    """Dictionaire POI, clé : type de POI, valeur : dictionnaire des POIs de ce type :
    (id_POI, [coordonnées, note, nom, type, prix])

    Liste des POIs : furniture_store, laundry, bakery, cafe, home_goods_store,
    clothing_store, atm, lodging, night_club, convenience_store, restaurant, bar
    """
    poidata = pickle.load(open(fn, "rb"))
    data = np.array(
        [[v[1][0][1], v[1][0][0]] for v in sorted(poidata[typepoi].items())]
    )
    note = np.array([v[1][1] for v in sorted(poidata[typepoi].items())])
    return data, note
