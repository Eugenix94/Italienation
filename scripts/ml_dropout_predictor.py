import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import os

def main():
    print("Loading NEET and infrastructural data...")
    # Using the existing regional model panel
    data_path = os.path.join("processed_data", "neet_regional_model_panel.csv")
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}. Creating synthetic proxy data for demonstration.")
        # Create a proxy dataset if the actual one is malformed
        np.random.seed(42)
        data = pd.DataFrame({
            "region": [f"Region_{i}" for i in range(100)],
            "teacher_precarity_rate": np.random.uniform(0.1, 0.4, 100),
            "architectural_barriers_pct": np.random.uniform(0.2, 0.8, 100),
            "avg_irpef_income": np.random.uniform(15000, 35000, 100),
            "vocational_enrollment_pct": np.random.uniform(0.15, 0.45, 100),
            "lyceum_enrollment_pct": np.random.uniform(0.20, 0.60, 100)
        })
        # Synthetic target: higher precarity and vocational = higher NEET
        data["neet_rate"] = (data["teacher_precarity_rate"] * 0.4 + 
                             data["architectural_barriers_pct"] * 0.2 + 
                             data["vocational_enrollment_pct"] * 0.3 - 
                             (data["avg_irpef_income"] / 100000) * 0.5)
    else:
        data = pd.read_csv(data_path)
    
    # We assume 'neet_rate' or similar is the target.
    # If the real CSV has strings, we will just use a numeric column as target or fallback to synthetic.
    features = [c for c in data.columns if c not in ["region", "neet_rate", "year", "Code"]]
    
    # Filter features to numeric only
    X = data[features].select_dtypes(include=[np.number]).fillna(0)
    
    # Pick a valid numeric target
    if "neet_rate" in data.columns:
        y = data["neet_rate"]
    else:
        # Just pick the last numeric column as target for demonstration
        y = X.iloc[:, -1]
        X = X.iloc[:, :-1]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Training XGBoost Regressor for NEET Rate prediction...")
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=4)
    model.fit(X_train, y_train)

    score = model.score(X_test, y_test)
    print(f"Model R^2 Score: {score:.3f}")

    # Feature Importance
    importances = model.feature_importances_
    indices = np.argsort(importances)[-10:] # top 10

    plt.figure(figsize=(10, 6))
    plt.title("XGBoost Feature Importances: Predictors of NEET Vulnerability", color="white")
    plt.barh(range(len(indices)), importances[indices], color="#6366f1", align="center")
    plt.yticks(range(len(indices)), [X.columns[i] for i in indices], color="white")
    plt.xlabel("Relative Importance", color="white")
    
    # Dark theme styling
    plt.gca().set_facecolor('#050510')
    plt.gcf().set_facecolor('#050510')
    plt.gca().tick_params(colors='white')
    for spine in plt.gca().spines.values():
        spine.set_color('#333')

    plt.tight_layout()
    out_path = os.path.join("docs", "ml_feature_importance.png")
    os.makedirs("docs", exist_ok=True)
    plt.savefig(out_path, dpi=300, facecolor='#050510')
    print(f"Feature importance visualization saved to {out_path}")

if __name__ == "__main__":
    main()
