import pandas as pd
import numpy as np
import sklearn
from sklearn.metrics import make_scorer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import  confusion_matrix, ConfusionMatrixDisplay, classification_report


import pickle

from load_and_save import load_data, save_model

def main():
    # Load data
    X_train = load_data("data/processed/03_X-train.csv")
    y_train = load_data("data/processed/03_y-train.csv").values.ravel()
    X_test = load_data("data/processed/03_X-test.csv")
    y_test = load_data("data/processed/03_y-test.csv").values.ravel()

    # Load best model
    best_model = pickle.load(open('results/02_best-knn-model.pickle', 'rb'))

    # Train the best model
    best_model.fit(X_train, y_train)

    # Predict on test data
    prediction = best_model.predict(X_test)

    # Calculate test score
    test_score = accuracy_score(y_test, prediction)
    print("Test Score:", test_score)

    # Save predictions to a CSV file
    prediction_df = pd.DataFrame(prediction, columns=['prediction'])
    prediction_df.to_csv("results/03_knn-test-predict.csv", index=False)

if __name__ == "__main__":
    main()
