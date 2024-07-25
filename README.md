# A Reward-Based, Scalable Charging Scheduling Algorithm for Community-Based Ride-Sharing Services

## Overview

This repository contains the code implementation for the paper "A Reward-Based, Scalable Charging Scheduling Algorithm for Community-Based Ride-Sharing Services". The algorithm integrates multiple constraints including energy usage, vehicle distribution, route planning, passenger-to-vehicle matching, and charging station availability to optimise the number of trips served and improve energy efficiency.

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Datasets](#datasets)
5. [License](#license)
6. [Contact](#contact)

## Introduction

The SmartMobility algorithm operates on a proactive, community-based, carbon-neutral ride-sharing model. It leverages reward-based mechanisms and integrates a vehicle routing algorithm with a vehicle charging algorithm. The system is designed to be highly scalable and efficient, handling large volumes of trip petitions and electric vehicles (EVs) in urban environments.

## Installation

### Prerequisites

- Python 3.7 or higher

### Setup

1. Clone the repository:
    ```sh
    git clone https://github.com/Nasheor/EcoRideScheduler.git
    cd ride_sharing_framework/3_Code
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

## Usage

### Running the Simulation

1. **Execute the Ride-Sharing Algorithm:**
   Run the ride-sharing algorithm to generate initial EV schedules and the charging scheduling algorithm to optimise EV 
   routes with strategic charging decisions:
   ```sh
   python run_experiments.py
   ```

### Output

- The simulation results, including the initial and optimised schedules, will be saved in the `output` directory.
- Detailed logs and performance metrics will be available in the `logs` directory.

## Datasets

The repository includes scripts to preprocess and adapt public datasets for the simulation:

1. **Google Hashcode Dataset:**
   - 10,000 trip petitions
   - 400 EVs

2. **NYC Taxi Dataset:**
   - 50,000 trip petitions
   - 1,000 EVs

The datasets are parameterised to fit the community-based ride-sharing context and can be accessed or generated through the `data_preprocessing.py` script.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions, issues, or contributions, please contact the project maintainers:

- Lead Author: [Avinash Nagarajan](mailto:avinash.nagarajan@mycit.ie)
- GitHub: [nasheor](https://github.com/nasheor)

We appreciate your feedback and contributions to improve this project.
