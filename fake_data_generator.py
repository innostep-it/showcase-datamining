import pandas as pd
import numpy as np
import json

# Setzen des Zufallsseeds für die Reproduzierbarkeit
np.random.seed(42)

# Erstellen eines Datumsbereichs für ein Jahr
dates = pd.date_range(start='2023-01-01', periods=365, freq='D')

# Einführung eines linearen Trends
trend = np.linspace(0, 5, 365)

# Generierung von Verkaufsdaten mit saisonalen Schwankungen und Trend
sales_data = {
    'Datum': dates,
    'Reifen': np.random.poisson(lam=20, size=365) + np.abs(np.sin(dates.dayofyear / 365 * 2 * np.pi) * 20).astype(int) + trend,
    'Batterien': np.random.poisson(lam=10, size=365) + np.abs(np.sin(dates.dayofyear / 365 * 2 * np.pi + 0.5) * 10).astype(int) + trend,
    'Ölfilter': np.random.poisson(lam=15, size=365) + np.abs(np.cos(dates.dayofyear / 365 * 2 * np.pi) * 15).astype(int) + trend
}

df = pd.DataFrame(sales_data)
df['Datum'] = df['Datum'].dt.strftime('%Y-%m-%d')  # Formatieren des Datums als String für JSON-Kompatibilität

# Konvertieren des DataFrames in ein JSON-Format
json_data = df.to_json(orient='records', lines=False)

# Optional: Speichern der Daten in einer JSON-Datei
with open('sales_data.json', 'w') as file:
    file.write(json_data)

print("JSON data generated and saved successfully.")
