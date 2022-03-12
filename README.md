# PyPSM

## Background
This project aims to create a simple interface to create artifical control groups using propensity score matching. It is intended as a way for researchers with less Python experience to have a simple tool that allows them to quickly generate control groups for their needs. Users can install pypsm by cloning and pip installing this directory. It is easy to use by following the example in the jupyter notebook. 

## Contributor
Hunter Yobei Thompson

## Installation
To install pypsm, simply clone this git repository.  
`git clone https://github.com/hunteryt17/DATA_511_Project.git`  
After cloning, navigate to the directory where the repo is located and use pip to install the package.  
`pip install .`

## Usage
For full usage, view the examples directory to see a Jupyter Notebook where a full use case is demonstrated.
Some notes about data cleaning:
- Ensure that all data is converted to numeric values (one-hot encode categorical variables)
- Remove or transform any NULL values in the data
- Make sure that treatment group is labeled as 1 and is smaller than control group (0)
- Make sure that there are at least 10 samples in the data
