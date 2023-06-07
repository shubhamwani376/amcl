import numpy as np
import matplotlib.pyplot as plt

def particle_samples(nparticles, low, high):
    return np.random.uniform(low, high, size=(nparticles,2))

def plot_particle_samples(particles,fig, ax, size=2, limits=None, grid=False, axis=True):
    ax.scatter(particles[:, 0], particles[:, 1], alpha=0.5, s=size * 20, c='blue')

def 