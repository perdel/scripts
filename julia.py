import numpy as np
import matplotlib.pyplot as plt
import argparse


def julia_set(
    x: float, y: float, c_real: float, c_imag: float, max_iter: int = 255
) -> int:
    """
    Calculates the Julia set for the given x and y coordinates.

    Parameters
    ----------
    x : float
        The x coordinate.
    y : float
        The y coordinate.
    c_real : float
        The real part of the complex number c
    c_imag : float
        The imaginary part of the complex number c
    max_iter : int
        The maximum number of iterations

    Returns
    -------
    int
        The Julia set value for the given coordinates.
    """
    z_r = x
    z_i = y
    for i in range(max_iter):
        z_r2 = z_r * z_r
        z_i2 = z_i * z_i
        if (z_r2 + z_i2) > 4:
            return i
        z_i = 2 * z_r * z_i + c_imag
        z_r = z_r2 - z_i2 + c_real
    return max_iter


def main():
    parser = argparse.ArgumentParser(
        description="A script to generate and plot Julia sets .",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-r", type=float, default=0.5, help="Real part of complex number"
    )

    parser.add_argument(
        "-i", type=float, default=0.001, help="Imaginary part of complex number"
    )

    args = parser.parse_args()

    x = np.linspace(-2, 2, 1000)
    y = np.linspace(-2, 2, 1000)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            Z[i, j] = julia_set(x=X[i, j], y=Y[i, j], c_real=args.r, c_imag=args.i)
    plt.imshow(Z, cmap="magma", extent=(-2, 2, -2, 2))
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    main()
