[See the Detailed Docs](https://callum-mccracken.github.io/npsm/build/html)

# What Is optimal_covering?

optimal_covering is an API to use to try to answer the following question:

We have a region on the Earth we want to observe, but only a finite number of observations to make. Where should we look?

More generally, we have some shape we want to cover with a finite number of other, smaller shapes. Where should we place those smaller shapes?

# Getting Started

First, run the [docker image](https://hub.docker.com/r/callummccracken/optimal-covering)

Then clone the [github repository](https://github.com/callum-mccracken/optimal_covering.git)

Then, run `tests.py`, to make sure everything worked!

# Python Modules you Should Care About

- `tests.py`: run this first, to test that everything's working well
- `genetics.py`: performs genetic algorithm
- `optimization.py`: a sample module to be adapted for other machine learning techniques
- everything else can hopefully be ignored, but let me know if you find any bugs!

# Important Notes

- Always write geometric coordinates as (lon, lat)
- Recall that longitudes range from -180 to 180, latitudes from -90 to 90
