from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from imblearn.over_sampling import SMOTE  # Para el sobremuestreo
import numpy as np

# Generamos un conjunto de datos desequilibrado
X, y = make_classification(n_samples=1000, n_features=20, n_classes=2, weights=[0.9, 0.1], flip_y=0, random_state=1)

# Dividimos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Aplicamos sobremuestreo a la clase minoritaria para introducir un sesgo
smote = SMOTE()
X_train_balanced, y_train_balanced = smote.fit_resample(X_train, y_train)

# Creamos el modelo RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Entrenamos el modelo con los datos balanceados (sesgados)
model.fit(X_train_balanced, y_train_balanced)

# Predicciones y evaluación del modelo
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy}")
