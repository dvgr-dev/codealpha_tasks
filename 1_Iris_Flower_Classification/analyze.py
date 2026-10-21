Warning: fs was declared with const; use let for reassignable variables.
"""Pure-Python Iris classification with reproducible holdout evaluation."""
from pathlib import Path
import csv, json, math, random

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(exist_ok=True)
names = ["setosa", "versicolor", "virginica"]
rows = []
with (ROOT / "data" / "iris.csv").open(encoding="utf-8", newline="") as f:
    for row in csv.reader(f):
        rows.append(([float(x) for x in row[:4]], names.index(row[4].replace("Iris-", ""))))
rng = random.Random(42)
by_class = {c: [r for r in rows if r[1] == c] for c in range(3)}
train, test = [], []
for group in by_class.values():
    rng.shuffle(group); n = round(len(group) * .2); test.extend(group[:n]); train.extend(group[n:])
def predict_knn(x):
    return min(train, key=lambda r: sum((a-b)**2 for a,b in zip(x,r[0])))[1]
def predict_gaussian(x):
    best = None
    for c in range(3):
        group = [v for v, label in train if label == c]
        means = [sum(r[j] for r in group)/len(group) for j in range(4)]
        variances = [max(1e-6, sum((r[j]-means[j])**2 for r in group)/(len(group)-1)) for j in range(4)]
        logp = math.log(len(group)/len(train))
        for j in range(4): logp += -.5*math.log(2*math.pi*variances[j]) - (x[j]-means[j])**2/(2*variances[j])
        if best is None or logp > best[0]: best = (logp,c)
    return best[1]
models = {"1-Nearest Neighbor": predict_knn, "Gaussian Naive Bayes": predict_gaussian}
scores, reports = {}, {}
for name, fn in models.items():
    pred = [fn(x) for x, _ in test]; scores[name] = sum(p==y for p,(_,y) in zip(pred,test))/len(test)
    cm = [[sum(1 for p,(x,y) in zip(pred,test) if y==a and p==b) for b in range(3)] for a in range(3)]
    per_class = {}
    for i, label in enumerate(names):
        tp=cm[i][i]; support=sum(cm[i]); predicted=sum(cm[r][i] for r in range(3))
        precision=tp/predicted if predicted else 0; recall=tp/support if support else 0
        per_class[label]={"precision":precision,"recall":recall,"f1":2*precision*recall/(precision+recall) if precision+recall else 0,"support":support}
    reports[name]={"confusion_matrix":cm,"per_class":per_class}
best=max(scores,key=scores.get); cm=reports[best]["confusion_matrix"]
metrics={"dataset":"Iris: 150 rows, 4 measurements, 3 classes","split":"80/20 stratified, seed 42","model_accuracy":scores,"selected_model":best,"selected_accuracy":scores[best],"classification_reports":reports,"note":"Educational baseline models implemented with Python's standard library."}
(OUT/"metrics.json").write_text(json.dumps(metrics,indent=2),encoding="utf-8")
colors=["#eff6ff","#dbeafe","#93c5fd","#3b82f6"]; cell=90; pad=110
s=['<svg xmlns="http://www.w3.org/2000/svg" width="520" height="470"><rect width="100%" height="100%" fill="white"/><text x="260" y="35" text-anchor="middle" font-family="Arial" font-size="20">Iris Confusion Matrix</text>']
for i,label in enumerate(names): s += [f'<text x="{pad+i*cell+45}" y="{pad-15}" text-anchor="middle" font-family="Arial">{label}</text>',f'<text x="{pad-12}" y="{pad+i*cell+48}" text-anchor="end" font-family="Arial">{label}</text>']
for i,row in enumerate(cm):
    for j,v in enumerate(row): s.append(f'<rect x="{pad+j*cell}" y="{pad+i*cell}" width="{cell}" height="{cell}" fill="{colors[min(v,3)]}"/><text x="{pad+j*cell+45}" y="{pad+i*cell+51}" text-anchor="middle" font-family="Arial" font-size="20">{v}</text>')
s.append('</svg>'); (OUT/"confusion_matrix.svg").write_text(''.join(s),encoding="utf-8")
print(json.dumps({"model_accuracy":scores,"selected_model":best,"accuracy":scores[best]},indent=2))
