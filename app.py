# Wichtiger Hinweis: Bitte zuerst Testdaten via 'fake_data_generator.py' generieren und in 'sales_data.json' speichern

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Datensammlung: Laden der Daten aus der JSON-Datei
df = pd.read_json('sales_data.json')
df['Datum'] = pd.to_datetime(df['Datum'])

# Datenbereinigung und -vorverarbeitung
df.fillna(method='ffill', inplace=True)  # Füllen fehlender Werte, falls vorhanden

# Datenexploration
print(df.describe())  # Statistische Zusammenfassung der Daten
print(df.corr())      # Korrelation zwischen den Produkten anzeigen

# Visualisierung der Korrelationen
plt.figure(figsize=(8, 6))
plt.title('Korrelationsmatrix der Verkaufszahlen')
sns.heatmap(df[['Reifen', 'Batterien', 'Ölfilter']].corr(), annot=True, fmt=".2f", cmap='coolwarm')
plt.show()

# Modellauswahl und -anwendung: Lineare Regression für jedes Produkt
features = ['Reifen', 'Batterien', 'Ölfilter']
models = {}
predictions = {}
mse_scores = {}

for feature in features:
    X = df.index.values.reshape(-1, 1)  # Zeit als Feature
    y = df[feature].values  # Zielvariable für jedes Produkt
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Modelltraining
    model = LinearRegression()
    model.fit(X_train, y_train)
    models[feature] = model

    # Modellvorhersage
    pred = model.predict(X_test)
    predictions[feature] = pred

    # Evaluierung
    mse = mean_squared_error(y_test, pred)
    mse_scores[feature] = mse
    print(f'Mean Squared Error for {feature}: {mse}')

# Visualisierung der Modellanpassung für jedes Produkt
plt.figure(figsize=(14, 7))
for feature in features:
    plt.plot(df['Datum'], df[feature], label=f'{feature} - Tatsächliche Verkäufe', alpha=0.5)
    plt.plot(df['Datum'], models[feature].predict(df.index.values.reshape(-1, 1)), label=f'{feature} - Modellprognose', linestyle='--')

plt.title('Verkaufszahlen und Modellprognosen für alle Produkte')
plt.xlabel('Datum')
plt.ylabel('Verkaufszahlen')
plt.legend()
plt.grid(True)
plt.show()

# Deployment und Monitoring (theoretisch)
# Hier könnte eine regelmäßige Überprüfung und Anpassung der Modelle basierend auf neuen Verkaufsdaten folgen
