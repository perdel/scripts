import numpy as np
import matplotlib.pyplot as plt

# Constants
num_atoms = 100
lattice_spacing = 1.0
gamma = 1.0  # Controls the strength of the hopping (t)
sigma = 1.0  # Width of the Gaussian potential
energy_shift = 0.0


def overlap_matrix_element(i, j):
    return np.exp(-0.5 * ((i - j) * lattice_spacing) ** 2 / sigma**2)


def hamiltonian_matrix_element(i, j, gamma):
    if i == j:
        return energy_shift  # On-site energy term (for simplicity, we assume it to be constant)
    else:
        return gamma * np.exp(-0.5 * ((i - j) * lattice_spacing) ** 2 / sigma**2)


def build_matrices(num_atoms, gamma):
    overlap_matrix = np.zeros((num_atoms, num_atoms))
    hamiltonian_matrix = np.zeros((num_atoms, num_atoms))

    for i in range(num_atoms):
        for j in range(num_atoms):
            overlap_matrix[i, j] = overlap_matrix_element(i, j)
            hamiltonian_matrix[i, j] = hamiltonian_matrix_element(i, j, gamma)

    return overlap_matrix, hamiltonian_matrix


def calculate_band_structure(hamiltonian_matrix, overlap_matrix):
    overlap_inv = np.linalg.inv(overlap_matrix)
    h_eff = np.dot(
        np.dot(overlap_inv, hamiltonian_matrix), overlap_inv
    )  # Effective Hamiltonian
    energies, _ = np.linalg.eigh(h_eff)  # Eigenvalues give the energy bands
    return energies


def main():
    gamma_values = [0.1, 0.5, 1.0, 2.0]  # Different values of hopping parameter (gamma)
    plt.figure(figsize=(8, 6))

    for gamma in gamma_values:
        overlap_matrix, hamiltonian_matrix = build_matrices(num_atoms, gamma)
        energies = calculate_band_structure(hamiltonian_matrix, overlap_matrix)

        plt.plot(np.linspace(0, 1, num_atoms), energies, label=f"γ = {gamma}")

    plt.title("Gaussian s-Band Structure")
    plt.xlabel("k (Wavevector)")
    plt.ylabel("Energy")
    plt.legend()
    plt.grid(True)
    plt.show()


# Run the main function
if __name__ == "__main__":
    main()
