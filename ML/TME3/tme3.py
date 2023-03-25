import numpy as np
import matplotlib.pyplot as plt
from mltools import plot_data, plot_frontiere, make_grid, gen_arti


def reshape(w, x, y):
    """Reshape les entrées.

    Parameters
    ----------
    w : array
        Vecteur poids.
    x : array
        Données.
    y : array
        Labels.

    Returns
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    x : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.
    """
    return w.reshape(-1, 1), x.reshape(y.shape[0], w.shape[0]), y.reshape(-1, 1)


def mse(w, x, y):
    """Renvoie le coût des moindres carrés pour une fonction linéaire.

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    x : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.

    Returns
    ----------
    z : array (n, 1)
        Coût des moindres carrés.
    """
    return (np.dot(x, w) - y) ** 2


def mse_grad(w, x, y):
    """Renvoie le gradient des moindres carrés sous forme d'une matrice (n, d).

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    x : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.

    Returns
    ----------
    z : array (n, 1)
        Gradient des moindres carrés.
    """
    return 2 * x * (np.dot(x, w) - y)


def reglog(w, x, y):
    """Renvoie le coût de la régression logistique.

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    x : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.

    Returns
    ----------
    z : array (n, 1)
        Coût de la régression logistique..
    """
    return np.log(1 + np.exp(-y * np.dot(x, w)))


def reglog_grad(w, x, y):
    """Renvoie le gradient de la régression logistique sous forme d'une matrice

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    x : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.

    Returns
    ----------
    z : array (n, 1)
        Gradient de la régression logistique.
    """
    return (-y * x) / (1 + np.exp(y * np.dot(x, w)))


def check_fonctions():
    ## On fixe la seed de l'aléatoire pour vérifier les fonctions
    np.random.seed(0)
    datax, datay = gen_arti(epsilon=0.1)
    wrandom = np.random.randn(datax.shape[1], 1)
    assert np.isclose(mse(wrandom, datax, datay).mean(), 0.54731, rtol=1e-4)
    assert np.isclose(reglog(wrandom, datax, datay).mean(), 0.57053, rtol=1e-4)
    assert np.isclose(mse_grad(wrandom, datax, datay).mean(), -1.43120, rtol=1e-4)
    assert np.isclose(reglog_grad(wrandom, datax, datay).mean(), -0.42714, rtol=1e-4)
    np.random.seed()


def grad_check(f, f_grad, N=100):
    pass


def descente_gradient(x, y, f_loss, f_grad, eps, iter):
    """Performe une descente de gradient.

    Parameters
    ----------
    x : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.
    f_loss : callable
        Fonction de coût.
    f_grad : callable
        Gradient de la fonction de coût.
    eps : float
        Pas d'apprentissage.
    iter : int
        Nombre d'itérations.

    Returns
    ----------
    w : array (d, 1)
        Vecteur poids optimal.
    weights : array(self.max_iter + 1, d, 10)
        Historique des vecteurs poids au fur et à mesure de la descente de gradient.
    losses : array(self.max_iter)
        Historique des coûts au fur et à mesure de la descente de gradient.
    """
    w = np.random.randn(x.shape[1], 1)
    weights = [w]  # liste des w
    losses = []  # valeurs de la fonction de coût
    for _ in range(iter):
        w -= eps * f_grad(w, x, y).mean()
        # if np.allclose(w, weights[i], rtol=1e-4):
        #     break  # convergence du gradient
        losses.append(f_loss(w, x, y).mean())
        weights.append(w)
    return w, np.array(weights), np.array(losses)


if __name__ == "__main__":
    ## Tirage d'un jeu de données aléatoire avec un bruit de 0.1
    datax, datay = gen_arti(epsilon=0.1)
    ## Fabrication d'une grille de discrétisation pour la visualisation de la fonction de coût
    grid, x_grid, y_grid = make_grid(xmin=-2, xmax=2, ymin=-2, ymax=2, step=100)

    plt.figure()
    ## Visualisation des données et de la frontière de décision pour un vecteur de poids w
    w = np.random.randn(datax.shape[1], 1)
    plot_frontiere(datax, lambda x: np.sign(x.dot(w)), step=100)
    plot_data(datax, datay)

    ## Visualisation de la fonction de coût en 2D
    plt.figure()
    plt.contourf(
        x_grid,
        y_grid,
        np.array([mse(w, datax, datay).mean() for w in grid]).reshape(x_grid.shape),
        levels=20,
    )
