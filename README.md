# F1 rating system

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

A multiplayer assymetric rating system and Streamlit app to analyse and define the F1 GOAT and rankings for drivers and constructors in the 2024 F1 season.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)

## Background

The question that has ruined many a social event: 

> Who is the F1 greatest of all time (GOAT)?  

There are many opinions. Let's build a rating system to see if we can identify - at least - the data GOAT.

## Install

### Prerequisites

This project is built using Make, Python 3.11.19 and Poetry 1.8.3. Install these dependencies before continuing.

### Data 

Download the CSV database tables from [^1] and unzip them into `data/raw`. The table structure for these tables can be found in [^2].

### Environment

Run `make env` in a command line interface (e.g. iTerm) to install Python dependencies for this project.

## Usage

The model can be found in `src/f1_elo`. Run `make data_e2e` to build the model and predict ratings per driver and constructor for all races.

The streamlit app can be found in `src/f1_elo`. Run `make app` to explore the app locally.

## Testing

This project has no tests.

## Contributing

- Mitchell Murphy (maintainer)

This project is open to issue submissions for bugs and improvements to make this app better.

If suggesting edits to the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## Acknowledgements

The rating system built was influenced by [^3], [^4] and [^5].

[^1]: [CSV DB table download](https://ergast.com/mrd/db/#csv) (last accessed 16/11/23)
[^2]: [CSV DB table structure](https://ergast.com/docs/f1db_user_guide.txt) (last accessed 16/11/23)
[^3]: [Elo rating system](https://en.wikipedia.org/wiki/Elo_rating_system) (last accessed 13/07/24)
[^4]: [Rewarding victory with the Elo rating system](https://stanislav-stankovic.medium.com/elo-rating-system-6196cc59941e) (last accessed 15/11/23)
[^5]: [Multiplayer assymetric game rating system](https://www.snellman.net/blog/archive/2015-11-18-rating-system-for-asymmetric-multiplayer-games/) (last accessed 13/07/24)