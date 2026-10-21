Warning: fs was declared with const; use let for reassignable variables.
"""Estimate sales from advertising spending with standard-library regression."""
from pathlib import Path
import csv, json, math, random, statistics

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
OUT.mkdir(exist_ok=True)
features=["TV","Radio","Newspaper"]
X=[]; y=[]
with (ROOT/"data"/"Advertising.csv").open(encoding="utf-8-sig",newline="") as f:
    for row in csv.DictReader(f):
        X.append([float(row[k]) for k in features]); y.append(float(row["Sales"]))
idx=list(range(len(y))); random.Random(42).shuffle(idx)
test=idx[:round(len(idx)*.2)]; train=idx[round(len(idx)*.2):]
def solve(a,b):
    a=[list(map(float,row))+[float(v)] for row,v in zip(a,b)]; n=len(b)
    for i in range(n):
        pivot=max(range(i,n),key=lambda r:abs(a[r][i])); a[i],a[pivot]=a[pivot],a[i]
        if abs(a[i][i])<1e-12: raise ValueError("Singular matrix")
        d=a[i][i]; a[i]=[v/d for v in a[i]]
        for r in range(n):
            if r!=i:
                factor=a[r][i]; a[r]=[u-factor*v for u,v in zip(a[r],a[i])]
    return [a[i][-1] for i in range(n)]
def design(i): return [1.0]+X[i]
xt=[design(i) for i in train]
gram=[[sum(row[i]*row[j] for row in xt) for j in range(4)] for i in range(4)]
rhs=[sum(row[j]*y[k] for row,k in zip(xt,train)) for j in range(4)]
coef=solve(gram,rhs)
pred=[sum(a*b for a,b in zip(coef,design(i))) for i in test]
actual=[y[i] for i in test]
mean=sum(y[i] for i in train)/len(train)
mae=sum(abs(a-p) for a,p in zip(actual,pred))/len(actual)
rmse=math.sqrt(sum((a-p)**2 for a,p in zip(actual,pred))/len(actual))
sst=sum((a-statistics.mean(actual))**2 for a in actual)
r2=1-sum((a-p)**2 for a,p in zip(actual,pred))/sst
base_rmse=math.sqrt(sum((a-mean)**2 for a in actual)/len(actual))
def corr(j):
    xx=[X[i][j] for i in range(len(y))]; mx=statistics.mean(xx); my=statistics.mean(y)
    return sum((a-mx)*(b-my) for a,b in zip(xx,y))/math.sqrt(sum((a-mx)**2 for a in xx)*sum((b-my)**2 for b in y))
metrics={"dataset_rows":len(y),"features":features,"target":"Sales","split":"80/20 random holdout; seed 42","linear_regression":{"intercept":coef[0],"coefficients":dict(zip(features,coef[1:])) ,"MAE":mae,"RMSE":rmse,"R2":r2},"baseline_mean_predictor_RMSE":base_rmse,"sales_feature_correlations":dict(zip(features,[corr(i) for i in range(3)])),"interpretation_note":"This cross-sectional dataset estimates sales for advertising spends; it has no dates and does not support a time-series forecast or causal ROI claim."}
(OUT/"metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
with (OUT/"holdout_predictions.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.writer(f); w.writerow(["actual_sales","predicted_sales"]); w.writerows(zip(actual,pred))
(OUT/"linear_model.json").write_text(json.dumps({"intercept":coef[0],"coefficients":dict(zip(features,coef[1:]))},indent=2),encoding="utf-8")
def scatter_svg(path,title,xs,ys,xlabel,ylabel):
    w,h=720,480; l,t,b=70,55,405; xmin,xmax=min(xs),max(xs); ymin,ymax=min(ys),max(ys)
    px=lambda x:l+(x-xmin)/(xmax-xmin)*(w-l-35)
    py=lambda y:b-(y-ymin)/(ymax-ymin)*(b-t)
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><rect width="100%" height="100%" fill="white"/><text x="360" y="28" text-anchor="middle" font-family="Arial" font-size="19">{title}</text><line x1="70" y1="405" x2="690" y2="405" stroke="#555"/><line x1="70" y1="55" x2="70" y2="405" stroke="#555"/>']
    s.append(f'<line x1="{px(xmin):.1f}" y1="{py(xmin):.1f}" x2="{px(xmax):.1f}" y2="{py(xmax):.1f}" stroke="crimson" stroke-dasharray="6 5"/>')
    for x,yv in zip(xs,ys): s.append(f'<circle cx="{px(x):.1f}" cy="{py(yv):.1f}" r="4" fill="#256d85" opacity=".75"/>')
    s.append(f'<text x="380" y="455" text-anchor="middle" font-family="Arial">{xlabel}</text><text x="18" y="230" transform="rotate(-90 18 230)" text-anchor="middle" font-family="Arial">{ylabel}</text></svg>')
    (OUT/path).write_text(''.join(s),encoding="utf-8")
scatter_svg("actual_vs_predicted.svg","Holdout actual vs predicted sales",actual,pred,"Actual Sales","Predicted Sales")
print(json.dumps(metrics,indent=2))
