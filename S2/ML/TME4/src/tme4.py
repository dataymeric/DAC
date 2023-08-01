import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mltools import plot_data, plot_frontiere, make_grid, gen_arti
from tqdm import tqdm


def reshape(w, X, y):
    """Reshape les entrées.

    Returns
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    y : array de taille (n, 1)
        Labels.
    """
    return w.reshape(-1, 1), X.reshape(y.shape[0], -1), y.reshape(-1, 1)


def perceptron_loss(w, X, y):
    """Renvoie le coût d'un perceptron.

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    X : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.

    Returns
    ----------
    z : array (n, 1)
        Coût du perceptron.
    """
    w, X, y = reshape(w, X, y)
    return np.maximum(0, -y * np.dot(X, w))


def perceptron_grad(w, X, y):
    """Renvoie le gradient d'un perceptron.

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    X : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.

    Returns
    ----------
    z : array (n, d)
        Gradient du perceptron.
    """
    w, X, y = reshape(w, X, y)
    return ((-y * np.dot(X, w)) > 0) * (-y * X)


def hinge_loss(w, X, y, alpha, lam):
    """Renvoie la hinge loss.

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    X : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.
    alpha : int
        Hinge.
    lam : int
        Pénalisation.

    Returns
    ----------
    z : array (n, 1)
        Hinge loss.
    """
    w, X, y = reshape(w, X, y)
    return np.maximum(0, alpha - y * np.dot(w, X)) + lam * np.linalg.norm(w) ** 2


def hinge_loss_grad(w, X, y, alpha, lam):
    """Renvoie le gradient de la hinge loss.

    Parameters
    ----------
    w : array de taille (d, 1)
        Vecteur poids.
    X : array de taille (n, d)
        Données.
    y : array de taille (n, 1)
        Labels.
    alpha : int
        Hinge.
    lam : int
        Pénalisation.

    Returns
    ----------
    z : array (n, 1)
        Hinge loss.
    """
    w, X, y = reshape(w, X, y)
    z = y * np.dot(w, X)
    if z >= alpha:
        grad = 2 * lam * w
    else:
        grad = -y * X + 2 * lam * w
    return grad


def proj_biais(X):
    """Introduit un biais."""
    biais = np.ones((X.shape[0], 1))
    return np.hstack((biais, X))


def proj_poly(X):
    """Projection polynomiale.

    $X = (x_1, x_2, ..., x_d)$ =>
    $(1, x_1, x_2, ..., x_d, x_1^2, x_1x_2, ..., x_d^2)$
    """
    n, d = X.shape
    proj = np.ones((n, 1 + d + d * (d + 1) // 2))
    for i in range(d):
        proj[:, i + 1] = X[:, i]
        # Boucle imbriquée pour ajouter les colonnes quadratiques x_i^2 et x_i*x_j
        for j in range(i, d):
            col = 1 + d + i * d + j - i * (i + 1) // 2
            if i == j:
                proj[:, col] = X[:, i] ** 2
            else:
                proj[:, col] = X[:, i] * X[:, j]
    return proj


def proj_gauss(X, base, sigma):
    """Projection gaussienne."""
    n, d = X.shape
    b, d = base.shape
    proj = np.zeros((n, b))
    for i in range(n):
        for j in range(b):
            proj[i, j] = np.exp(
                -np.linalg.norm(X[i, :] - base[j, :]) ** 2 / (2 * sigma**2)
            )
    return proj


class Lineaire(object):
    def __init__(
        self,
        loss=perceptron_loss,
        loss_g=perceptron_grad,
        max_iter=100,
        eps=0.01,
        projection=None,
        base=None,
        sigma=1,
    ):
        self.max_iter = max_iter
        self.eps = eps
        self.w = None
        self.loss = loss
        self.loss_g = loss_g
        self.projection = projection
        self.base = base
        self.sigma = sigma

    def proj(self, X):
        """Renvoie la projection des données."""
        if self.projection.__name__ in ["proj_biais", "proj_poly"]:
            return self.projection(X)
        elif self.projection.__name__ == "proj_gauss":
            return self.projection(X, self.base, self.sigma)

    def fit(self, X, y, batch_size=50, mode=None, **kwargs):
        """Performe une descente de gradient.

        Parameters
        ----------
        X : array de taille (n, d)
            Données.
        y : array de taille (n, 1)
            Labels.
        batch_size : int, default=50
            Nombre d'exemples par batchs pour la descente par mini-batch. Paramètre
            ignoré si 'mode' n'est pas 'minibatch'.
        mode : {stochastique, minibatch, None}, default='None'
            Définit l'algorithme utilisé pour la descente de gradient.

        Returns
        ----------
        w : array (d, 1)
            Vecteur poids optimal.
        weights : array(self.max_iter + 1, d, 10)
            Historique des vecteurs poids au fur et à mesure de la descente de gradient.
        losses : array(self.max_iter)
            Historique des coûts au fur et à mesure de la descente de gradient.
        scores : array(self.max_iter)
            Historique des scores (en apprentissage) au fur et à mesure de la descente
            de gradient.
        """
        X_score = X.copy()

        if self.projection is not None:
            X = self.proj(X)

        self.w = np.ones((X.shape[1], 1))
        weights = [self.w]
        losses = [self.loss(self.w, X, y, **kwargs).mean()]
        scores = [self.score(X_score, y)]

        for _ in tqdm(range(self.max_iter)):
            if mode is None:
                grad = self.loss_g(self.w, X, y, **kwargs).mean(0).reshape(-1, 1)
                self.w = self.w - self.eps * grad
            elif mode == "stochastique":
                np.random.shuffle(X)
                np.random.shuffle(y)
                for rand in range(X.shape[0]):
                    grad = (
                        self.loss_g(self.w, X[rand], y[rand], **kwargs)
                        .mean(0)
                        .reshape(-1, 1)
                    )
                    self.w = self.w - self.eps * grad
            elif mode == "minibatch":
                np.random.shuffle(X)
                np.random.shuffle(y)
                for i in range(0, X.shape[0], batch_size):
                    grad = (
                        self.loss_g(
                            self.w,
                            X[i : i + batch_size],
                            y[i : i + batch_size],
                            **kwargs
                        )
                        .mean(0)
                        .reshape(-1, 1)
                    )
                    self.w = self.w - self.eps * grad
            else:
                raise ValueError(
                    "mode must be one of {None, 'stochastique' or "
                    "'minibatch'}, got '%s' instead" % mode
                )

            weights.append(self.w)
            losses.append(self.loss(self.w, X, y, **kwargs).mean())
            scores.append(self.score(X_score, y))

        return self.w, np.array(weights), np.array(losses), np.array(scores)

    def predict(self, X):
        """Infére le label des données."""
        if self.projection is not None:
            X = self.proj(X)
        return np.sign(np.dot(X, self.w))

    def score(self, X, y):
        """Calcule le pourcentage de bonne classification sur le jeu de données
        passé en paramètre.
        """
        return np.mean(self.predict(X) == y)


def load_usps(fn):
    with open(fn, "r") as f:
        f.readline()
        data = [[float(X) for X in l.split()] for l in f if len(l.split()) > 2]
    tmp = np.array(data)
    return tmp[:, 1:], tmp[:, 0].astype(int)


def get_usps(l, X, y):
    if type(l) != list:
        resx = X[y == l, :]
        resy = y[y == l]
        return resx, resy
    tmp = list(zip(*[get_usps(i, X, y) for i in l]))
    tmpx, tmpy = np.vstack(tmp[0]), np.hstack(tmp[1])
    return tmpx, tmpy


def show_usps(data):
    plt.imshow(data.reshape((16, 16)), interpolation="nearest")


if __name__ == "__main__":
    uspsdatatrain = "../data/USPS_train.txt"
    uspsdatatest = "../data/USPS_test.txt"
    alltrainx, alltrainy = load_usps(uspsdatatrain)
    alltestx, alltesty = load_usps(uspsdatatest)
    neg = 5
    pos = 6
    datax, datay = get_usps([neg, pos], alltrainx, alltrainy)
    testx, testy = get_usps([neg, pos], alltestx, alltesty)
