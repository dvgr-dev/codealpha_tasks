Warning: fs was declared with const; use let for reassignable variables.
"""Clean and summarize India's regional unemployment estimates (stdlib only)."""
from pathlib import Path
from collections import defaultdict
from datetime import datetime
import csv, json, statistics

ROOT=Path(__file__).resolve().parent
OUT=ROOT/"results"
OUT.mkdir(exist_ok=True)
monthly=defaultdict(list)
regions=defaultdict(list)
dates=[]
cleaned=0
with (ROOT/"data"/"Unemployment_in_India.csv").open(encoding="utf-8-sig",newline="") as f:
    for raw in csv.DictReader(f):
        row={key.strip(): (value.strip() if value else "") for key,value in raw.items() if key}
        try:
            date=datetime.strptime(row["Date"].strip(),"%d-%m-%Y")
            rate=float(row["Estimated Unemployment Rate (%)"])
        except (ValueError,KeyError,AttributeError):
            continue
        month=date.strftime("%Y-%m")
        monthly[month].append(rate)
        regions[row["Region"].strip()].append(rate)
        dates.append(date)
        cleaned+=1
summary=[]
for month,values in sorted(monthly.items()):
    summary.append({"month":month,"mean_state_area_rate_pct":statistics.mean(values),"median_state_area_rate_pct":statistics.median(values),"observations":len(values)})
with (OUT/"monthly_summary.csv").open("w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=summary[0].keys())
    w.writeheader()
    w.writerows(summary)
pre=[r["mean_state_area_rate_pct"] for r in summary if r["month"]<"2020-03"]
covid=[r["mean_state_area_rate_pct"] for r in summary if "2020-03"<=r["month"]<="2020-06"]
lookup={r["month"]:r["mean_state_area_rate_pct"] for r in summary}
stats={"source_file":"Unemployment_in_India.csv","rows_after_cleaning":sum(len(v) for v in monthly.values()),"date_range":[min(dates).date().isoformat(),max(dates).date().isoformat()],"monthly_metric_note":"Unweighted mean across available state-by-area observations; not an official national unemployment rate.","pre_march_2020_mean_state_area_rate_pct":round(statistics.mean(pre),3),"march_to_june_2020_mean_state_area_rate_pct":round(statistics.mean(covid),3),"april_2020_mean_state_area_rate_pct":round(lookup.get("2020-04",0),3),"may_2020_mean_state_area_rate_pct":round(lookup.get("2020-05",0),3),"seasonality_limitation":"Only 14 months are present, too short to establish recurring annual seasonality."}
(OUT/"key_findings.json").write_text(json.dumps(stats,indent=2),encoding="utf-8")
report=("# Key findings\n\n"
        f"- Cleaned **{cleaned}** state-area observations from **{min(dates).date()}** to **{max(dates).date()}**.\n"
        f"- The unweighted mean across observed state-area rates was **{stats['pre_march_2020_mean_state_area_rate_pct']:.2f}%** before March 2020 and **{stats['march_to_june_2020_mean_state_area_rate_pct']:.2f}%** from March through June 2020.\n"
        f"- The observed April and May 2020 means were **{stats['april_2020_mean_state_area_rate_pct']:.2f}%** and **{stats['may_2020_mean_state_area_rate_pct']:.2f}%**.\n\n"
        "These are unweighted averages of state-area rows, not official national estimates. The timing is descriptive and does not establish causation. The 14-month window is too short to determine recurring annual seasonality.\n")
(OUT/"findings.md").write_text(report,encoding="utf-8")
def chart(path,title,series):
    width,height,left,top,bottom=920,470,70,65,390
    vals=[v for _,v in series]
    low,high=min(0,min(vals)),max(vals)*1.12
    pts=[]
    for i,(label,val) in enumerate(series):
        x=left+i*(width-left-30)/max(1,len(series)-1)
        y=bottom-(val-low)/(high-low)*(bottom-top)
        pts.append((x,y,label,val))
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}"><rect width="100%" height="100%" fill="white"/><text x="460" y="30" text-anchor="middle" font-family="Arial" font-size="19">{title}</text><line x1="70" y1="390" x2="900" y2="390" stroke="#555"/><line x1="70" y1="65" x2="70" y2="390" stroke="#555"/>']
    s.append('<polyline fill="none" stroke="#256d85" stroke-width="3" points="'+' '.join(f'{x:.1f},{y:.1f}' for x,y,_,_ in pts)+'"/>')
    for x,y,label,val in pts:
        s.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#256d85"/><text x="{x:.1f}" y="415" text-anchor="middle" font-family="Arial" font-size="10">{label}</text>')
    s.append('</svg>')
    (OUT/path).write_text(''.join(s),encoding="utf-8")
chart("monthly_trend.svg","Unemployment estimates by month",[(r["month"],r["mean_state_area_rate_pct"]) for r in summary])
regional=sorted([(k,statistics.mean(v)) for k,v in regions.items()],key=lambda x:x[1])
height=60+len(regional)*24
bars=[f'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="{height}"><rect width="100%" height="100%" fill="white"/><text x="450" y="30" text-anchor="middle" font-family="Arial" font-size="19">Average unemployment by region</text>']
for i,(name,value) in enumerate(regional):
    y=50+i*24
    bars.append(f'<text x="180" y="{y+14}" text-anchor="end" font-family="Arial" font-size="12">{name}</text><rect x="190" y="{y}" width="{value*12:.2f}" height="17" fill="#256d85"/><text x="{200+value*12:.2f}" y="{y+14}" font-family="Arial" font-size="11">{value:.1f}%</text>')
bars.append('</svg>')
(OUT/"regional_comparison.svg").write_text(''.join(bars),encoding="utf-8")
print(json.dumps(stats,indent=2))
