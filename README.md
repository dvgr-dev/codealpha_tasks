Warning: fs was declared with const; use let for reassignable variables.
# CodeAlpha Data Science Internship Projects

Three completed starter projects based on the internship task brief: Iris Flower Classification, Unemployment Analysis with Python, and Sales Prediction using Python.

## Projects

1. [Iris Flower Classification](1_Iris_Flower_Classification/README.md) — compare two classifiers and evaluate the selected model on a stratified holdout set.
2. [Unemployment Analysis](2_Unemployment_Analysis/README.md) — clean and visualize Indian state and area unemployment estimates, with a cautious view of the 2020 COVID period.
3. [Sales Prediction](3_Sales_Prediction/README.md) — estimate sales from TV, radio, and newspaper advertising spend.

## Run all projects

Use Python 3.10 or newer. The analyses use Python's standard library, so no package installation is required. From this folder, run:

```bash
python 1_Iris_Flower_Classification/analyze.py
python 2_Unemployment_Analysis/analyze.py
python 3_Sales_Prediction/analyze.py
```

Each project writes metrics and SVG visualizations into its `results/` folder. Dataset notes and source links are included in each project README. Model scores are reproducible for the fixed random seeds and splits documented in the reports.

## Scope and interpretation

These are educational analyses. Iris is a small benchmark dataset. The unemployment dataset is a limited set of survey estimates through 2020 and cannot establish causation or recurring annual seasonality. The advertising sales dataset is cross-sectional and supports estimating sales for a spend mix, not time-series forecasting or causal return-on-investment claims.
