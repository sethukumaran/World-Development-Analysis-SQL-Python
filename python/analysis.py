import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; OUT=ROOT/"visualizations"; OUT.mkdir(exist_ok=True)
hdi=pd.read_csv(DATA/"hdi_2021_clean.csv")
hdi_ts=pd.read_csv(DATA/"hdi_timeseries.csv")
wb=pd.read_csv(DATA/"worldbank_clean.csv")

print("HDI shape:",hdi.shape)
print("World Bank shape:",wb.shape)
print("\nHDI categories:\n",hdi["hdicode"].value_counts(dropna=False))
print("\nTop missing-value rates:\n",hdi.isna().mean().sort_values(ascending=False).head(10))

ranked=hdi.dropna(subset=["hdi_rank_2021"]).sort_values("hdi_rank_2021")
print("\nTop 10:\n",ranked[["country","hdi_2021","hdi_rank_2021"]].head(10).to_string(index=False))
print("\nBottom 10:\n",ranked[["country","hdi_2021","hdi_rank_2021"]].tail(10).sort_values("hdi_rank_2021",ascending=False).to_string(index=False))

region_hdi=hdi.dropna(subset=["region","hdi_2021"]).groupby("region")["hdi_2021"].agg(["count","mean"]).sort_values("mean",ascending=False)
print("\nRegional HDI:\n",region_hdi)

wide=hdi_ts.pivot(index=["iso3","country","region"],columns="year",values="hdi").reset_index()
wide["hdi_change_1990_2021"]=wide[2021]-wide[1990]
print("\nLargest HDI improvements:\n",wide.dropna(subset=["hdi_change_1990_2021"]).sort_values("hdi_change_1990_2021",ascending=False)[["country","region",1990,2021,"hdi_change_1990_2021"]].head(15).to_string(index=False))

plt.figure(figsize=(10,6)); plt.hist(hdi.hdi_2021.dropna(),bins=20,edgecolor="black"); plt.title("Distribution of Human Development Index (2021)"); plt.xlabel("HDI"); plt.ylabel("Number of countries"); plt.tight_layout(); plt.savefig(OUT/"01_hdi_distribution_2021.png",dpi=160); plt.close()

top10=ranked.head(10).sort_values("hdi_2021")
plt.figure(figsize=(10,6)); plt.barh(top10.country,top10.hdi_2021); plt.title("Top 10 Countries by HDI (2021)"); plt.xlabel("HDI"); plt.tight_layout(); plt.savefig(OUT/"02_top10_hdi_2021.png",dpi=160); plt.close()

bottom10=ranked.tail(10).sort_values("hdi_2021")
plt.figure(figsize=(10,6)); plt.barh(bottom10.country,bottom10.hdi_2021); plt.title("Bottom 10 Countries by HDI (2021)"); plt.xlabel("HDI"); plt.tight_layout(); plt.savefig(OUT/"03_bottom10_hdi_2021.png",dpi=160); plt.close()

rh=region_hdi.sort_values("mean")
plt.figure(figsize=(9,5)); plt.barh(rh.index,rh["mean"]); plt.title("Average HDI by Region (2021)"); plt.xlabel("Average HDI"); plt.tight_layout(); plt.savefig(OUT/"04_region_average_hdi.png",dpi=160); plt.close()

global_hdi=hdi_ts.groupby("year").hdi.mean()
plt.figure(figsize=(10,6)); plt.plot(global_hdi.index,global_hdi.values,marker="o",markersize=3); plt.title("Average HDI Trend Across Countries"); plt.xlabel("Year"); plt.ylabel("Average HDI"); plt.grid(alpha=.25); plt.tight_layout(); plt.savefig(OUT/"05_hdi_trend_1990_2021.png",dpi=160); plt.close()

wb18=wb[wb.year==2018]
merged=wb18.merge(hdi[["iso3","country","region","hdi_2021"]],left_on="country_code",right_on="iso3",how="inner")

p=merged[["hdi_2021","gdp_per_capita_usd"]].dropna()
plt.figure(figsize=(9,6)); plt.scatter(p.gdp_per_capita_usd,p.hdi_2021,alpha=.65); plt.xscale("log"); plt.title("HDI 2021 vs GDP per Capita (World Bank 2018)"); plt.xlabel("GDP per capita (USD, log scale)"); plt.ylabel("HDI 2021"); plt.grid(alpha=.25); plt.tight_layout(); plt.savefig(OUT/"06_hdi_vs_gdp_per_capita.png",dpi=160); plt.close()

p=merged[["hdi_2021","internet_pct"]].dropna()
plt.figure(figsize=(9,6)); plt.scatter(p.internet_pct,p.hdi_2021,alpha=.65); plt.title("HDI 2021 vs Internet Usage (World Bank 2018)"); plt.xlabel("Individuals using the Internet (% of population)"); plt.ylabel("HDI 2021"); plt.grid(alpha=.25); plt.tight_layout(); plt.savefig(OUT/"07_hdi_vs_internet.png",dpi=160); plt.close()

corr=merged[["hdi_2021","gdp_per_capita_usd","internet_pct","population_density","unemployment_pct"]].corr().hdi_2021.sort_values(ascending=False)
print("\nCorrelation with HDI 2021:\n",corr)

ranked[["country","region","hdi_2021","hdi_rank_2021"]].head(10).to_csv(DATA/"top10_hdi_2021.csv",index=False)
ranked[["country","region","hdi_2021","hdi_rank_2021"]].tail(10).sort_values("hdi_rank_2021",ascending=False).to_csv(DATA/"bottom10_hdi_2021.csv",index=False)
region_hdi.reset_index().rename(columns={"mean":"avg_hdi_2021"}).to_csv(DATA/"regional_hdi_summary.csv",index=False)
merged.to_csv(DATA/"hdi_worldbank_2018_join.csv",index=False)
print("\nAnalysis complete.")
