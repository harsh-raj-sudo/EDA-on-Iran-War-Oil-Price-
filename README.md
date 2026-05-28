# 🛢️ Iran War Oil Price Analysis — EDA

> Exploratory Data Analysis of global oil price dynamics during the Iran War conflict, using verified daily data from America's 50-State Pump (published by Euronews).

---

## 📌 Overview

This project investigates the relationship between geopolitical conflict and global energy markets. Using daily oil pricing data alongside shipping activity through the **Strait of Hormuz**, the analysis reveals how armed conflict drives price volatility across the world's major crude oil benchmarks.

---

## 🎯 Objectives

1. Analyze the **impact of geopolitical events** on global oil prices
2. **Compare oil benchmarks** — Brent, WTI, and Dubai
3. Examine the **relationship between crude and retail fuel prices**
4. Analyze **shipping activity** through the Strait of Hormuz across war phases

---

## 📁 Repository Structure

```
iran-war-oil-price-eda/
├── README.md
├── file1.ipynb                        # Main analysis notebook
├── data/
│   └── iran_war_oil_prices_daily_2026.csv
├── outputs/
│   └── figures/                       # Exported chart images
└── requirements.txt
```

---

## 📊 Dataset

| Attribute | Details |
|-----------|---------|
| **Source** | 50-State Pump (USA), verified by Euronews |
| **File** | `iran_war_oil_prices_daily_2026.csv` |
| **Frequency** | Daily |
| **Coverage** | Duration of Iran War conflict phases |

### Key Columns

| Column | Description |
|--------|-------------|
| `date` | Observation date |
| `brent_usd_barrel` | Brent crude — World Benchmark (USD/barrel) |
| `wti_usd_barrel` | WTI crude — US Benchmark (USD/barrel) |
| `dubai_usd_barrel` | Dubai crude — Gulf Benchmark (USD/barrel) |
| `us_gas_avg_gallon` | Average US retail gasoline price (USD/gallon) |
| `us_diesel_avg_gallon` | Average US retail diesel price (USD/gallon) |
| `strait_hormuz_daily_ships` | Daily ship count through Strait of Hormuz |
| `iran_production_mbpd` | Iran oil production (million barrels/day) |
| `war_day` | Sequential conflict day number |
| `phase` | War phase label (categorical) |

### Derived Feature

```python
df['price_spread'] = df['brent_usd_barrel'] - df['wti_usd_barrel']
```
> Measures the Brent–WTI spread, a standard proxy for regional supply-demand imbalances.

---

## 🛠️ Tech Stack

| Library | Purpose |
|---------|---------|
| `NumPy` | Numerical computations |
| `Pandas` | Data loading, cleaning, aggregation |
| `Matplotlib` | Line, bar, histogram, pie, subplot charts |
| `Seaborn` | Statistical charts — box, violin, scatter, barplot |

---

## 🔍 Analysis Pipeline

### 1. Data Inspection
```python
df.info()          # Column types and null counts
df.shape           # Dimensions
df.describe()      # Statistical summary
df.isnull().sum()  # Missing values
```

### 2. Data Cleaning
```python
df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
df['phase'].unique()    # Explore categories
df['phase'].nunique()   # Count unique phases
```

### 3. Filtering & Slicing
```python
df[df['us_gas_avg_gallon'] < 3]                            # Gas below $3
df[(df['brent_usd_barrel'] >= 80) & (df['brent_usd_barrel'] <= 100)]  # Brent 80–100
df[df['war_day'] <= 10]                                    # First 10 war days
df.sort_values(by='price_spread')                          # Sort by spread
```

### 4. Aggregation
```python
# Average Brent price per phase
df.groupby('phase')[['brent_usd_barrel']].mean()

# Max/min per phase
df.groupby('phase')['brent_usd_barrel'].agg(['max', 'min'])

# Multi-column aggregation
df.groupby('phase').agg({
    'brent_usd_barrel': ['max', 'min', 'mean'],
    'wti_usd_barrel':   ['max', 'min', 'mean', 'count'],
    'dubai_usd_barrel': ['max', 'min', 'mean', 'sum']
})
```

---

## 📈 Visualizations

| Chart | Variables | Insight |
|-------|-----------|---------|
| **Line Chart** | Brent, WTI, Dubai over time | Benchmark synchrony and divergence |
| **Bar Chart** | Avg Brent price per phase | Phase-level price elevation |
| **Subplot (1×2)** | Oil prices + Fuel prices | Crude-to-retail correlation |
| **Histogram** | Iran oil production | Distribution shape and production range |
| **Pie Chart** | Phase distribution | Time share per war phase |
| **Seaborn Line** | Brent trend by phase | Phase-coloured price evolution |
| **Seaborn Bar** | Ships per phase (Hormuz) | Shipping activity vs. conflict intensity |
| **Scatter Plot** | Brent vs Gas (phase + ship size) | Multi-variable relationship |
| **Box Plot** | Brent distribution per phase | Spread and outliers by phase |
| **Violin Plot** | Strait of Hormuz ship count | Full density of shipping volume |
| **Catplot Bar** | Diesel price per phase | Retail fuel variation by phase |

---

## 💡 Key Findings

- 📈 **Oil prices rise continuously** during active conflict phases, reflecting supply-risk premiums
- 🔗 **Brent, WTI, and Dubai** move in tandem but with measurable spreads driven by regional logistics
- 🚢 **Strait of Hormuz shipping activity** is a leading indicator of energy market stress
- ⛽ **US retail fuel prices** closely trail crude movements with a short lag
- 📊 **Phase-level aggregations** confirm escalation periods correlate with peak price volatility

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Jupyter Notebook or JupyterLab

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/iran-war-oil-price-eda.git
cd iran-war-oil-price-eda

# 2. Install dependencies
pip install numpy pandas matplotlib seaborn jupyter

# 3. Launch the notebook
jupyter notebook file1.ipynb
```

---

## 📦 Requirements

```
numpy
pandas
matplotlib
seaborn
jupyter
```

> Save as `requirements.txt` and install with `pip install -r requirements.txt`

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- **Data**: 50-State Pump Program (USA)
- **Verification**: [Euronews](https://www.euronews.com)
- **Analysis**: Python data science ecosystem — NumPy, Pandas, Matplotlib, Seaborn

---

*Built with Python · Data Science · Geopolitical Analysis*
