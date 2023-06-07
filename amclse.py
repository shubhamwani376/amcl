#Particle filter and main file

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams


N = 300
mean = np.array([0,0])
covariance = np.diag([9,9])

X_start = mean

def set_plot_style():
  # plt.style.use('seaborn-dark-palette')
  rcParams['mathtext.fontset'] = 'cm'
  rcParams.update({'font.size': 12})

def format_plot(x, y):  
  plt.grid(False)
  plt.xlabel(x, fontsize=20)
  plt.ylabel(y, fontsize=20)

def finalize_plot(shape=(1, 1)):
  plt.gcf().set_size_inches(
    shape[0] * 1.5 * plt.gcf().get_size_inches()[1], 
    shape[1] * 1.5 * plt.gcf().get_size_inches()[1])
  plt.tight_layout()

def particle_samples(N_samples, mean, covariance, distribution=None):
  return np.random.multivariate_normal(mean, covariance, size=N_samples)

def plot_particle_samples(R, size=2, limits=None, grid=False, axis=True):
  
  plt.scatter(R[:, 0], R[:, 1], alpha=0.5, s=size * 20, c='blue')
  
  if not limits:

    minRx = np.min(R[:, 0]); minRy = np.min(R[:, 1]);
    maxRx = np.max(R[:, 0]); maxRy = np.max(R[:, 1]);
    
    totalx = maxRx - minRy
    totaly = maxRy - minRy

    plt.xlim([minRx - totalx / 10, maxRx + totalx / 10])
    plt.ylim([minRy - totaly / 10, maxRy + totaly / 10])

  else:
    plt.xlim([limits[0,0], limits[0,1]])
    plt.ylim([limits[1,0], limits[1,1]])
  
  if grid:
    plt.grid(grid)

  if not axis:
    plt.axis("off")

  plt.title("Particle samples over Map")
  plt.xlabel(r"$X$", fontsize=16)
  plt.ylabel(r"$Y$", fontsize=16)


set_plot_style()
Particle_states = particle_samples(N, mean, covariance)


plot_particle_samples(Particle_states, size=1.0, axis=True)
plt.plot(X_start[0], X_start[1], "*", ms=30)


X_start[0] = 3 # measurement
def likelihood_fn(R, sigma, X):
  variance = sigma ** 2 
  return np.exp(-0.5*(R[:,0]-X[0])**2/variance)


def weights_fn(R, sigma, X):
  return likelihood_fn(R, sigma, X)


weights = weights_fn(Particle_states, 1, X_start)


plot_particle_samples(Particle_states, size=weights, axis=True)
plt.plot(X_start[0], X_start[1], "*", ms=30)


# Simulate all samples forward for one second, using 10 Euler steps:
V = 5
predictions = np.copy(Particle_states)
X_new = np.copy(X_start)
for i in range(10):
  x = predictions[:,0]
  y = predictions[:,1]
  norm = np.sqrt(x**2 + y**2)
  predictions[:,0] += 0.1*y*V/norm
  predictions[:,1] += 0.1*x*V/norm

  Rx = X_new[0]
  Ry = X_new[1]
  norm_particle =  np.sqrt(Rx**2 + Ry**2)
  X_new[0] += 0.1*Ry*V/norm_particle
  X_new[1] += 0.1*Rx*V/norm_particle


plot_particle_samples(predictions, size=weights, axis=False)
plt.plot(X_new[0], X_new[1], "*", ms=30)


sample_indices = np.random.choice(N,p=weights/np.sum(weights),size=N)
samples = predictions[sample_indices]


weights = weights_fn(samples, 1, X_new)


plot_particle_samples(samples, size=weights, axis=False)
plt.plot(X_new[0], X_new[1], "*", ms=30, alpha=0.5)
plt.show()