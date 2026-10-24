"""สร้าง index.html จาก data/laptop_price.csv และ template.html
วิธีรัน:  pip install pandas  &&  python build_dashboard.py
"""
import json
import pandas as pd

df = pd.read_csv("data/laptop_price.csv", encoding="latin1")

# Data cleaning: แปลงข้อความเป็นตัวเลข
df["ram"] = df["Ram"].str.replace("GB", "").astype(int)
df["kg"] = df["Weight"].str.replace("kg", "").astype(float)

companies = sorted(df["Company"].unique())
types = sorted(df["TypeName"].unique())
products = list(df["Product"].unique())
cpu_labels = ["Core i3 / อื่นๆ", "Core i5", "Core i7"]

def cpu_family(cpu: str) -> int:
    return 1 if "Core i5" in cpu else 2 if "Core i7" in cpu else 0

rows = [
    [companies.index(r.Company), types.index(r.TypeName), int(r.ram), r.Inches,
     r.kg, round(r.Price_euros), products.index(r.Product),
     cpu_family(r.Cpu), int("SSD" in r.Memory)]
    for r in df.itertuples()
]

data = json.dumps(
    {"c": companies, "t": types, "p": products, "f": cpu_labels, "rows": rows},
    ensure_ascii=False, separators=(",", ":"),
)
html = open("template.html", encoding="utf-8").read().replace("__DATA__", data)
open("index.html", "w", encoding="utf-8").write(html)
print("สร้าง index.html สำเร็จ:", len(rows), "รุ่น")
