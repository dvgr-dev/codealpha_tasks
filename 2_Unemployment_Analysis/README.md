Warning: fs was declared with const; use let for reassignable variables.
# Unemployment Analysis with Python

## Objective

Explore unemployment estimates across Indian states and rural/urban areas, emphasizing changes around the COVID-19 lockdown period.

## Method

The script skips empty or malformed records, parses dates, converts rates to numbers, and aggregates the mean and median across available state-area observations by month. It also compares regional averages and saves clean monthly summary data plus key findings. The analysis and SVG chart generation use only Python's standard library.

## Run

From the repository root:

```bash
python analyze.py
```

Outputs are written to `results/`: `findings.md`, `key_findings.json`, `monthly_summary.csv`, `monthly_trend.svg`, and `regional_comparison.svg`.

## Dataset and limits

The supplied data are the two public CSVs referenced by the task brief's [Kaggle dataset](https://www.kaggle.com/datasets/gokulrajkmv/unemployment-in-india). This analysis uses `Unemployment_in_India.csv`, with monthly state and rural/urban observations from May 2019 through June 2020. A public [GitHub analysis repository](https://github.com/les-k/unemployment-india) documents the companion files and their coverage. This project's monthly metric is an unweighted mean of state-area observations, **not an official national rate**. State estimates are not equally representative of population or labour force. The series is short, so it cannot establish annual seasonality. The timing is descriptive and does not prove lockdown caused the change.

Review the dataset's original terms before redistribution.
