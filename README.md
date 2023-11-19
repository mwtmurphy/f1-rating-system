# F1 Elo

[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

This project uses a modified Elo scoring formula and Streamlit to create an interactive app for identifying the highest ranked F1 racing drivers over time.

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [Acknowledgements](#acknowledgements)
- [Ideas](#ideas)

## Background

The question that has ruined many a social event: 

> Who is the F1 greatest of all time (GOAT)?  

There are many opinions. Is it Fangio, Senna, Michael Schumacher, Hamilton. Let's apply some data science to the problem to see if we can identify - at least - the data GOAT.

## Install

### Prerequisites

This project is built using Make, Python 3.10.12 and Poetry 1.5.0. Install these dependencies before continuing.

### Data 

Download the CSV database tables from [^1] and unzip them into `data/raw`. The table structure for these tables can be found in [^2].

### Code

Run `make env` in a command line interface (e.g. iTerm) to install package dependencies for this project.

## Usage

Exploratory data analysis (EDA) can be found in `notebooks/eda.ipynb`. The method used to score race outcomes is based on a modified ELO formula found in [^3].

The streamlit app built from this EDA is found in `src/f1_elo`.

Run `make app` to explore the app locally.

## Testing

No testing added currently. 

## Contributing

- Mitchell Murphy (maintainer)

This project is open to issue submissions for bugs and improvements to make this app better.

If suggesting edits to the README, please conform to the [standard-readme](https://github.com/RichardLitt/standard-readme) specification.

## Acknowledgements

Hat tip to my dad for annoying a family friend at a recent birthday party to give me the motivation to build this.

## Ideas

1. Add 1950 - 1985 data for teams with multiple drivers.
2. Add sprint races.
3. Add DNFs and type of DNFs (e.g. crashes = penalty, mechanical failures = no penalty).
4. Scale score change dependent on number of races in a season (less races = less chance to improve).
5. Add weighting dependent on constructors finishing position for year (e.g. expected points - realised points).
6. Add distance apart for finishers (points scored for 25s diff > points scored for 5s).
7. Scale initial Elo score dependent on racing history pre-F1.

[^1]: [CSV DB table download](https://ergast.com/mrd/db/#csv) (last accessed 16/11/23)
[^2]: [CSV DB table structure](https://ergast.com/docs/f1db_user_guide.txt) (last accessed 16/11/23)
[^3]: [ELO ranking formula](https://stanislav-stankovic.medium.com/elo-rating-system-6196cc59941e) (last accessed 15/11/23)