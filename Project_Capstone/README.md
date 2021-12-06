# Starbucks Capstone Project

## Project Description
This project is for the Starbucks Capstone Challenge of the Data Scientist Nanodegree in Udacity. The dataset provided are simulated data that mimics customer behavior on the Starbucks rewards mobile app, i.e. whether the customer would buy a Starbucks if he/she is provided any informational or discount offer.

## Project Motivation

Once every few days, Starbucks sends out an offer to users of the mobile app. An offer can be merely an advertisement for a drink or an actual offer such as a discount or BOGO (buy one get one free). Some users might not receive any offers during certain weeks. Every offer has a validity period before the offer expires.

Based on the information given above, we can infer that any transaction made by a customer is something really desired. No matter what offer you'd provide to the customers, still, you will deserve a transaction. Therefore, this project will try to predict how much money a customer will spend.

To solve the problem, we will use all datasets provided.

We will employ several machine learning algorithms. As this will be a regression problem, we will evaluate the algorithms based on several regression metrics, i.e. mean absolute error, mean squared error, root mean squared error, and R2 score.

## Summary of the Results

I found this project challenging, mainly due to the structure of the data in the transcript dataset. My goal is to predict the amount will be spent by a customer. So, the decision-makers would know how customers behave in purchasing Starbucks products. Therefore, I need all rows with amount existing, i.e. the rows with event col equal to transaction. However, using only this subset of the dataset, in fact, the models I've implemented can't give good performance. Even, by checking the correlations among all columns, we are unable to capture any strong relationship between the amount and other columns.

For more description, you can find it in my Medium article [here](https://utomorezadwi.medium.com/how-much-will-you-spend-on-starbucks-products-242dc22c335c).

## Requirements

In order to run the project in your localhost, you are highly recommended to create a new virtual environment using either [`conda env`](https://conda.io/docs/user-guide/tasks/manage-environments.html) or [`python venv`](https://docs.python.org/3/tutorial/venv.html). Afterwards, install all dependencies packages listed below.

- Python>=3.7
- numpy
- pandas
- matplotlib
- seaborn
- scikit-learn
- [auto-sklearn](https://automl.github.io/auto-sklearn/master/installation.html) (you need Ubuntu machine to use this lib)
- [pytorch](https://pytorch.org/)

## Description of Files & Directories

- The [`data`](./data) directory contains datasets in CSV and JSON files. The raw datasets are in JSON files, whereas the CSV files are the preprocessed datasets.
- The [`README.md`](./README.md) file is this readme.
- The [`Starbucks_Capstone_notebook.ipynb`](./Starbucks_Capstone_notebook.ipynb) is the main notebook for the project analysis.

## Acknowledgements
Acknowledgement should go to Starbucks for providing the dataset. This repo is a capstone project of [Data Scientist Nanodegree on Udacity](https://www.udacity.com/course/data-scientist-nanodegree--nd025).

## License
[MIT License](../LICENSE)