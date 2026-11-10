import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.metrics import accuracy_score, classification_report
import os

# Set path to the CSV our cleaning script created
csv_path = r"C:\Users\pc\shark-tank-decoder\data\processed\pitch_analytics_clean.csv"
images_dir = r"C:\Users\pc\shark-tank-decoder\images"
os.makedirs(images_dir, exist_ok=True)

print("📂 Loading clean dataset for Machine Learning...")
df = pd.read_csv(csv_path)

# Prepare Features (X) and Target (y)
# We want to see if Ask Amount and Equity can predict a deal
feature_cols = ['ask_amount_usd', 'ask_equity_pct', 'implied_ask_valuation_usd']
X = df[feature_cols]
y = df['deal_made']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Model
clf = DecisionTreeClassifier(max_depth=3, random_state=42)
clf.fit(X_train, y_train)

# Accuracy
y_pred = clf.predict(X_test)
print(f"\n✅ Model Accuracy: {accuracy_score(y_test, y_pred)*100:.2f}%")

# Visualize the Tree
plt.figure(figsize=(15, 8))
plot_tree(clf, feature_names=feature_cols, class_names=['Rejected', 'Funded'], filled=True, rounded=True)
plt.title("How Sharks Decide: Venture Capital Decision Tree")
plt.savefig(os.path.join(images_dir, "decision_tree.png"), dpi=300)
print(f"📊 Decision Tree chart saved to: {images_dir}")
plt.show()

# --- THE DEAL PREDICTOR ---
def simulate_pitch(amount, equity):
    val = amount / (equity / 100)
    prediction = clf.predict([[amount, equity, val]])[0]
    result = "FUNDED ✅" if prediction == 1 else "REJECTED ❌"
    print(f"🔮 Pitching ${amount:,} for {equity}%: {result}")

print("\n--- Pitch Simulator ---")
simulate_pitch(100000, 10)  # Reasonable
simulate_pitch(1000000, 2)  # Overvalued