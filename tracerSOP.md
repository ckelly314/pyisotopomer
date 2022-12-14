# Processing 15N-labeled samples

[![pypi badge](https://img.shields.io/pypi/v/pyisotopomer.svg?style=popout)](https://pypi.org/project/pyisotopomer)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5031218.svg)](https://doi.org/10.5281/zenodo.5031218)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Intro

The accumulation of <sup>15</sup>N<sup>15</sup>N<sup>16</sup>O in tracer experiments requires extra steps in the data processing pipeline. Here we describe these extra steps and link to the relevant code and data processing template.


In natural abundance samples, pyisotopomer solves the following four equations to obtain $^{15}R^{\alpha}$ and $^{15}R^{\beta}$:

$$
 ^{45}R &= ^{15}R^{\alpha} + ^{15}R^{\beta} + ^{17}R 
 ^{46}R &= (^{15}R^{\alpha} + ^{15}R^{\beta})^{17}R + ^{18}R + (^{15}R^{\alpha} )(^{15}R^{\beta} ) \\
^{17}R/^{17}R_{VSMOW} &= (^{18}R/^{17}R_{VSMOW})^{\beta} \\
 ^{31}R &= \frac{(1-\gamma)^{15}R^{\alpha} + \gamma^{15}R^{\beta} + (^{15}R^{\alpha} )(^{15}R^{\beta} ) + ^{17}R(1+\gamma^{15}R^{\alpha}+(1-\gamma)^{15}R^{\beta})}{1 + \gamma^{15}R^{\alpha} + (1-\gamma)^{15}R^{\beta}} \\
\end{align}
$$

In these equations, the term $(^{15}R^{\alpha} )(^{15}R^{\beta} )$ represents the statistically expected contribution of $^{15}N^{15}N^{16}O$ to the $^{46}R$ and $^{31}R$ ion currents. The idea here is that the probability of getting $^{15}N$ in the alpha position is equal to $^{15}R^{\alpha}$, and the probability of getting $^{15}N$ in the beta position is equal to $^{15}R^{\beta}$, so the probability of getting $^{15}N$ in both alpha and beta positions = $(^{15}R^{\alpha} )(^{15}R^{\beta} )$ (see [Kaiser et al., 2004](https://link.springer.com/article/10.1007/s00216-003-2233-2)). This is a reasonable assumption for natural abundance samples, where the concentration of $^{15}N^{15}N^{16}O$ is extremely low. For $^{15}N$-labeled samples, however, we need to account for the production of $^{15}N^{15}N^{16}O$ from  $^{15}N$-labeled substrate.

To do this, we can add a term to the equations for the $^{46}R$ and $^{31}R$ ion currents:

$$
 ^{46}R &= (^{15}R^{\alpha} + ^{15}R^{\beta})^{17}R + ^{18}R + (^{15}R^{\alpha} )(^{15}R^{\beta} ) + ^{15}N^{15}N^{16}O_{excess}\\
 ^{31}R &= \frac{(1-\gamma)^{15}R^{\alpha} + \gamma^{15}R^{\beta} + (^{15}R^{\alpha} )(^{15}R^{\beta} ) + ^{17}R(1+\gamma^{15}R^{\alpha}+(1-\gamma)^{15}R^{\beta}) + ^{15}N^{15}N^{16}O_{excess}}{1 + \gamma^{15}R^{\alpha} + (1-\gamma)^{15}R^{\beta}} \\
\end{align}
$$

Where $^{15}N^{15}N^{16}R_{excess}$ represents the amount of $^{15}N^{15}N^{16}O$ in excess of that predicted by $(^{15}R^{\alpha} )(^{15}R^{\beta} )$.
