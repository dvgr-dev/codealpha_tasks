Warning: fs was declared with const; use let for reassignable variables.
# Sales Prediction using Python

## Objective

Estimate sales from TV, radio, and newspaper advertising expenditure and examine the relationship between channels and sales.

## Method

The script cleans numeric fields and fits multiple linear regression with an 80/20 holdout split (random seed 42). It reports MAE, RMSE, and R² against a mean-prediction baseline, saves holdout predictions, and writes a scatterplot as SVG. Its least-squares solver and chart generation use Python's standard library.

## Run

From the repository root:

```bash
python analyze.py
```

Outputs are written to `results/`: `metrics.json`, `holdout_predictions.csv`, `actual_vs_predicted.svg`, and `linear_model.json`. On the fixed holdout, multiple linear regression reached an R² of approximately 0.85 and RMSE of approximately 2.46 sales units; the mean-only baseline RMSE was approximately 6.40.

## Dataset and interpretation

The 200-row advertising data contain TV, Radio, Newspaper, and Sales columns. The task brief points to the [CodeAlpha Kaggle dataset](https://www.kaggle.com/datasets/bumba5341/advertisingcsv); this copy is mirrored in a public [GitHub Gist](https://gist.github.com/rparrapy/bc7804cada859938d433c25ec2a3f00c). Check the original terms before redistribution. Because rows are markets rather than dates, this model estimates sales for an observed advertising mix; it is not a time-series forecast. Correlations and model feature relationships do not prove that changing a budget will cause a particular sales increase.
