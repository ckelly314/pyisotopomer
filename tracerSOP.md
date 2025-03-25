# Processing $^{15}N$-labeled samples

[![pypi badge](https://img.shields.io/pypi/v/pyisotopomer.svg?style=popout)](https://pypi.org/project/pyisotopomer)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5031218.svg)](https://doi.org/10.5281/zenodo.5031218)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Theory

The accumulation of $^{15}N^{15}N^{16}O$ in tracer experiments requires extra steps in the data processing pipeline. Here we describe these extra steps and link to the relevant code and data processing template.


In natural abundance samples, pyisotopomer solves the following four equations to obtain $^{15}R^{\alpha}$ and $^{15}R^{\beta}$:

$$
\begin{align}
 ^{45}R &= ^{15}R^{\alpha} + ^{15}R^{\beta} + ^{17}R \\
 ^{46}R &= (^{15}R^{\alpha} + ^{15}R^{\beta})^{17}R + ^{18}R + (^{15}R^{\alpha} )(^{15}R^{\beta} ) \\
^{17}R/^{17}R_{VSMOW} &= (^{18}R/^{17}R_{VSMOW})^{\beta} \\
 ^{31}R &= \frac{(1-\gamma)^{15}R^{\alpha} + \kappa^{15}R^{\beta} + (^{15}R^{\alpha} )(^{15}R^{\beta} ) + ^{17}R[1+\gamma^{15}R^{\alpha}+(1-\kappa)^{15}R^{\beta}]}{1 + \gamma^{15}R^{\alpha} + (1-\kappa)^{15}R^{\beta}} \\
\end{align}
$$

In these equations, the term $(^{15}R^{\alpha} )(^{15}R^{\beta} )$ represents the statistically expected contribution of $^{15}N^{15}N^{16}O$ to the $^{46}R$ and $^{31}R$ ion currents. The idea here is that the probability of getting $^{15}N$ in the alpha position is equal to $^{15}R^{\alpha}$, and the probability of getting $^{15}N$ in the beta position is equal to $^{15}R^{\beta}$, so the probability of getting $^{15}N$ in both alpha and beta positions = $(^{15}R^{\alpha} )(^{15}R^{\beta} )$ (see [Kaiser et al., 2004](https://link.springer.com/article/10.1007/s00216-003-2233-2)). This is a reasonable assumption for natural abundance samples, where the concentration of $^{15}N^{15}N^{16}O$ is extremely low. For $^{15}N$-labeled samples, however, we need to account for the production of $^{15}N^{15}N^{16}O$ from  $^{15}N$-labeled substrate.

To do this, we can add a term to the equations for the $^{46}R$ and $^{31}R$ ion currents:

$$
\begin{align}
 ^{31}R &= \frac{(1-\gamma)^{15}R^{\alpha} + \kappa^{15}R^{\beta} + (^{15}R^{\alpha} )(^{15}R^{\beta} )_{t0} + ^{17}R(1+\gamma^{15}R^{\alpha}+(1-\kappa)^{15}R^{\beta}) + ^{15}N^{15}N^{16}O_{excess}}{1 + \gamma^{15}R^{\alpha} + (1-\kappa)^{15}R^{\beta}} \\
\end{align}
$$

Where $^{15}N^{15}N^{16}O_{excess}$ represents the amount of $^{15}N^{15}N^{16}O$ added to the sample over the course of the experiment. To quantify $^{15}N^{15}N^{16}O_{excess}$ in tracer samples, we assume that any increase in $^{46}R$ over the course of the experiment is due to added $^{15}N^{15}N^{16}O$, i.e. that $\delta^{18}O$ remains constant. This should be a reasonable assumption — while denitrification and $N_2O$ consumption will cause natural abundance-level increases in $\delta^{18}O$ and thus $^{46}R$ (10's of per mil), $N_2O$ production from $^{15}N$-labeled substrates will cause much greater increases in $^{46}R$ (100's to 1,000's of per mil). We calculate the term $^{15}N^{15}N^{16}O_{excess}$ by subtracting the mean $^{46}R$ at t0 from the measured $^{46}R$ in later timepoints in the tracer excel template. Then, the "Tracers" function in pyisotopomer takes this $^{15}N^{15}N^{16}O_{excess}$ into account when calculating isotopomers.

Note that in the equation for $^{31}R$, we account for the yield of $^{31}NO^+$ from $^{15}N^{15}N^{16}O$, but we do not account for the yield of $^{30}N_2^+$ from $^{15}N^{15}N^{16}O$. This is because the numerator and denominator for $^{31}R$ are normalized to the yield of $^{30}NO^+$ from $^{14}N^{14}N^{16}O$ (thus, the 1 in the denominator); since both the numerator and denominator are both multiplied by this yield, it cancels out, but the equation is still implicitly in terms of the fragmentation of $N_2O$ to $NO^+$. To account for the fragmentation of $N_2O$ to $N_2$, we would need to measure the more abundant masses of $N_2$, i.e. m/z ratios 28 and 29. However, we expect the yield of $^{30}N_2^+$ from $^{15}N^{15}N^{16}O$ to be small.

If you do NOT account for $^{15}N^{15}N^{16}O_{excess}$, i.e., use the natural abundance version of pyisotopomer for tracer samples, you will find that later timepoints in experiments with a lot of produced $^{15}N^{15}N^{16}O$ will have anomalously high values of $\delta^{15}N^{\alpha}$ and $\delta^{18}O$. This is because the code is trying to find sources of the excess $^{31}R$ and $^{46}R$ coming from $^{15}N^{15}N^{16}O$.

## Data Corrections

1) Calculate scrambling normally, as described in the pyisotopomer [documentation](https://github.com/ckelly314/pyisotopomer)

2) Process all experimental samples normally, with the natural abundance version of pyisotopomer, as described in the [documentation](https://github.com/ckelly314/pyisotopomer).

3) Download the tracer excel [template](https://github.com/ckelly314/pyisotopomer/blob/master/pyisotopomer_examples/00_Tracer_template.xlsx).

4) Group samples by experiment (i.e., all of the samples for a $^{15}N$-labeled ammonium experiment) and sort them by timepoint. In the tracer template, fill in columns A-C with the run date, sample ID, and incubation time for each sample. 

5) For each sample, copy and paste the $\delta^{15}N^{\alpha}$, $\delta^{15}N^{\beta}$, and $\delta^{17}O$ calculated with the natural abundance version of pyisotopomer in Step 2 into columns D-F. Column G contains $(^{15}R^{\alpha})(^{15}R^{\beta})$ calculated from $\delta^{15}N^{\alpha}$ and $\delta^{15}N^{\beta}$.

6) Copy and paste the run date and ID for each sample in columns H and I. Copy and paste the scale-normalized, size-corrected $^{31}R$, $^{45}R$, and $^{46}R$ into columns J-L. If you are able to measure $\Delta^{17}O$ in your samples, enter these values in column M; otherwise, leave the values at 0 (note this is $^{17}O$ EXCESS, which is different from $\delta^{17}O$). According to run date, copy and paste the appropriate values of $\gamma$ and $\kappa$ into columns N and O. Copy and paste concentration data into column AE.

6) Column P calculates the average t0 $\delta^{17}O$. Modify the formula in column P to reflect the average values in column F for t0 samples. Column Q calculates the average t0 $(^{15}R^{\alpha})(^{15}R^{\beta})$. Modify the formula in column Q to reflect the average values in column G for t0 samples. Column R should contain $^{46}R - ^{46}R_{t0}$ for each sample, where $^{46}R_{t0}$ is the average $^{46}R$ measured in t0 samples.

7) To calculate isotopomers, navigate to the directory containing the tracer template, and run:

```Python
Tracers(inputfile = "00_Tracer_template.xlsx", **kwargs)
```

(replace "00_Tracer_template.xlsx" with the name of your excel template)

This should create an output file with both isotopomer delta values and isotoper ratios. Copy and paste these values into columns U-AC. Isotopomer concentrations are calculated in columns AG-AI.
