# Processing 15N-labeled samples

[![pypi badge](https://img.shields.io/pypi/v/pyisotopomer.svg?style=popout)](https://pypi.org/project/pyisotopomer)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5031218.svg)](https://doi.org/10.5281/zenodo.5031218)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Intro

The accumulation of <sup>15</sup>N<sup>15</sup>N<sup>16</sup>O in tracer experiments requires extra steps in the data processing pipeline. Here we describe these extra steps and link to the relevant code and data processing template.


In natural abundance samples, pyisotopomer solves the following four equations for $^{15}R^{\alpha}$ and ${15}R^{\beta}$:

$$
\begin{align}

^{45}R &= ^{15}R^{\alpha} + ^{15}R^{\beta} + ^{17}R \\

^{31}R &= \frac{(1-γ)}{1+γ^{15}R^α}

\end{align}
$$