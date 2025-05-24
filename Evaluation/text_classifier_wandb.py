import wandb
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

def run_experiment(model_name="base", C=1.0):
    # 🪄 Initialize WandB
    wandb.init(
        project="text-classification-demo",
        name=f"{model_name}-model",
        config={
            "model": model_name,
            "C": C
        }
    )
    

    # 🗂️ Load and split data
    data = fetch_20newsgroups(subset='train', categories=['rec.autos', 'sci.med'], remove=('headers', 'footers', 'quotes'))
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

    # 🧠 Vectorize text
    vectorizer = TfidfVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # 🤖 Train model
    model = LogisticRegression(C=C, max_iter=1000)
    model.fit(X_train_vec, y_train)
    y_pred = model.predict(X_test_vec)

    # 📊 Log metrics
    acc = accuracy_score(y_test, y_pred)
    wandb.log({"accuracy": acc})

    report = classification_report(y_test, y_pred, output_dict=True)
    for label, metrics in report.items():
        if isinstance(metrics, dict):
            for metric, value in metrics.items():
                wandb.log({f"{label}_{metric}": value})
                
    # Log sample predictions
    table_data = list(zip(X_test[:10], y_pred[:10], y_test[:10]))
    columns = ["Text", "Predicted", "True Label"]
    wandb.log({"predictions": wandb.Table(data=table_data, columns=columns)})
    
    wandb.finish()


# 🧪 Define experiments outside the function
experiments = [
    {"model_name": "base", "C": 1.0},
    {"model_name": "fine_tuned", "C": 3.0},
    {"model_name": "weak_reg", "C": 0.1},
    {"model_name": "overfit_risk", "C": 10.0}
]

# 🚀 Run all experiments
if __name__ == "__main__":
    for exp in experiments:
        run_experiment(**exp)
