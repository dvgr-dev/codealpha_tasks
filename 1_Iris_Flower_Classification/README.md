Warning: fs was declared with const; use let for reassignable variables.
# Iris Flower Classification

## Objective

Classify Iris flowers as setosa, versicolor, or virginica from sepal and petal measurements.

## Method

The script reads the supplied CSV, makes a stratified 80/20 train/test split (random seed 42), and compares 1-Nearest Neighbor with Gaussian Naive Bayes. It selects the model with the highest test accuracy, reports per-class precision/recall/F1, and saves the confusion matrix. The transparent baseline implementations use only Python's standard library.

## Run

From the repository root:

```bash
python analyze.py
```

Outputs are written to `results/`: `metrics.json` and `confusion_matrix.svg`.

## Dataset

The CSV contains 150 observations with four measurements and the species label. The task brief points to the [CodeAlpha Kaggle dataset](https://www.kaggle.com/datasets/saurabh00007/iriscsv). The included CSV is a standard Iris copy mirrored at [Brownlee/Datasets on GitHub](https://github.com/jbrownlee/Datasets/blob/master/iris.csv); check the upstream dataset terms before redistribution.

## Interpretation

This is a small, clean benchmark dataset. Its test score is illustrative and should not be treated as a guarantee of performance on field-collected measurements.
