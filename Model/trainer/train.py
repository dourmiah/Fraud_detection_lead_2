import os
import sys
import time
import mlflow
import logging
import datetime

# import argparse
import pandas as pd
import logging.config
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt
from imblearn.over_sampling import SMOTE  # conda install imbalanced-learn
from sklearn.preprocessing import StandardScaler
from mlflow.models.signature import infer_signature
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.pipeline import Pipeline as ImbPipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve,
)

import joblib
import pickle

author = "Dominique"
nb_estimators = 150
file_path = "https://lead-program-assets.s3.eu-west-3.amazonaws.com/M05-Projects/fraudTest.csv"

mlflow.set_tracking_uri(os.environ["APP_URI"])


# Model trainer class
class ModelTrainer:

    # Constructor
    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.numeric_columns = []
        return

    # Data loading
    def load_data(self) -> pd.DataFrame:
        start_time = time.time()
        data = pd.read_csv(file_path, nrows=5000)

        # Delete first column (type identity !)
        data = data.iloc[:, 1:]

        self.logger.info(f"load_data : {round(time.time() - start_time, 2)} sec.")
        return data

    # Data preprocessing 
    def preprocess_data(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        start_time = time.time()
        X = df.drop("is_fraud", axis=1)
        y = df["is_fraud"]

        self.numeric_columns = X.select_dtypes(include="number").columns.tolist()
        self.logger.debug(f"X numeric cols : {self.numeric_columns}")

        # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
        X_train, X_test, y_train, y_test = train_test_split(X[self.numeric_columns], y, test_size=0.2, stratify=y, random_state=42)

        preprocessor = StandardScaler()
        X_train_scaled = preprocessor.fit_transform(X_train)
        X_test_scaled = preprocessor.transform(X_test)

        # Reconvert into Dataframe
        X_train = pd.DataFrame(X_train_scaled, columns=self.numeric_columns, index=X_train.index)
        X_test = pd.DataFrame(X_test_scaled, columns=self.numeric_columns, index=X_test.index)

         # Apply SMOTE to rebalance the target class 
        sm = SMOTE(random_state=50)
        X_train, y_train = sm.fit_resample(X_train, y_train)
    
        # Save the preprocessor 
        with open('preprocessor_model.pkl', "wb") as file:
            pickle.dump(preprocessor, file)

        # Log metrics and params into Mlflow
        mlflow.log_param("Train set size", len(X_train))
        mlflow.log_param("Test set size", len(X_test))
        mlflow.log_metric("preprocess_data_time", round(time.time() - start_time, 2))
        self.logger.info(f"preprocess_data : {round(time.time() - start_time, 2)} sec.")
        
        return X_train, X_test, y_train, y_test

    # Train model
    def train_model(self, X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestClassifier:
        start_time = time.time()

        # SMOTE + RandomForest in a pipeline
        # model_pipeline: ImbPipeline = ImbPipeline(
        #     steps=[
        #         ("scaler", StandardScaler()),
        #         ("smote", SMOTE(random_state=42)),
        #         ("classifier", RandomForestClassifier(n_estimators=nb_estimators, random_state=42, class_weight="balanced")),
        #     ]
        # )

        # Train model
        model = RandomForestClassifier(n_estimators=nb_estimators, random_state=42, class_weight="balanced")
        model.fit(X_train[self.numeric_columns], y_train)

        # Save model
        with open('randomforest_model.pkl', 'wb') as file:
            joblib.dump(model, file)

        # Log metrics
        mlflow.log_metric("train_model_time", round(time.time() - start_time, 2))
        self.logger.info(f"train_model : {round(time.time() - start_time, 2)} sec.")
        return model

    # Model assessment
    def evaluate_model(
        self,
        model: RandomForestClassifier,
        X_train: pd.DataFrame,
        X_test: pd.DataFrame,
        y_train: pd.Series,
        y_test: pd.Series,
    ) -> None:

        start_time = time.time()

        y_pred = model.predict(X_test[self.numeric_columns])
        y_pred_proba = model.predict_proba(X_test[self.numeric_columns])[:, 1]

        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        roc_auc = roc_auc_score(y_test, y_pred_proba)
        conf_matrix = confusion_matrix(y_test, y_pred)

        mlflow.log_metric("Accuracy", round(accuracy, 2))
        mlflow.log_metric("Precision", round(precision, 2))
        mlflow.log_metric("Recall", round(recall, 2))
        mlflow.log_metric("F1 Score", round(f1, 2))
        mlflow.log_metric("ROC AUC Score", round(roc_auc, 2))

        self.logger.info(f"Accuracy : {accuracy:.2f}")
        self.logger.info(f"Precision : {precision:.2f}")
        self.logger.info(f"Recall : {recall:.2f}")
        self.logger.info(f"F1-Score : {f1:.2f}")
        self.logger.info(f"ROC AUC Score : {roc_auc:.2f}")

        fpr, tpr, _ = roc_curve(y_test, y_pred_proba)
        plt.figure()
        plt.plot(fpr, tpr, color="blue", lw=2, label="ROC curve (area = %0.2f)" % roc_auc)
        plt.plot([0, 1], [0, 1], color="grey", lw=2, linestyle="--")
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver Operating Characteristic")
        plt.legend(loc="lower right")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        title = f"./img/{timestamp}_roc_curve.png"
        plt.savefig(title)
        mlflow.log_artifact(title)

        plt.figure()
        sns.heatmap(
            conf_matrix,
            annot=True,
            fmt="d",
            cmap="Blues",
            cbar=False,
            xticklabels=["Non-Fraud", "Fraud"],
            yticklabels=["Non-Fraud", "Fraud"],
        )
        plt.xlabel("Predicted")
        plt.ylabel("True")
        plt.title("Confusion Matrix")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        title = f"./img/{timestamp}_confusion_matrix.png"
        plt.savefig(title)
        mlflow.log_artifact(title)

        mlflow.log_metric("evaluate_model_time", round(time.time() - start_time, 2))
        self.logger.info(f"evaluate_model : {round(time.time() - start_time, 2)} sec.")

        return

    # Logs tags and parameters in MLFlow
    def log_tags_and_parameters(self) -> None:

        mlflow.log_param("N Estimators", nb_estimators)
        mlflow.set_tag("Author", author)
        mlflow.set_tag("OS", sys.platform)
       
        return

    # Logs model in MLFlow
    def log_model(self, model: RandomForestClassifier, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        start_time = time.time()

        # Infer model signature
        signature = infer_signature(X_train, y_train)

        # Log the model with MLflow
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            registered_model_name="random_forest",
            signature=signature,
        )

        # Log the time spent to log the model
        mlflow.log_metric("log_model_time", round(time.time() - start_time, 2))
        self.logger.info(f"log_model: {round(time.time() - start_time, 2)} sec.")
        return

    # Start the process
    def run(self) -> None:
        with mlflow.start_run():
            start_time = time.time()

            self.log_tags_and_parameters()
            df = self.load_data()
            X_train, X_test, y_train, y_test = self.preprocess_data(df)
            model_pipeline = self.train_model(X_train, y_train)
            self.evaluate_model(model_pipeline, X_train, X_test, y_train, y_test)
            self.log_model(model_pipeline, X_train, y_train)

            mlflow.log_metric("total_run_time", round(time.time() - start_time, 2))
            self.logger.info(f"run : {round(time.time() - start_time, 2)} sec.")

# Main
if __name__ == "__main__":

    start_time = time.time()

    current_file = Path(__file__).resolve()
    current_directory = current_file.parent
    os.chdir(current_directory)

    # Load the logging configuration from the conf file
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger(__name__)

    logger.debug(f"Current dir : {current_directory}")

    Path("./img").mkdir(parents=True, exist_ok=True)

    logger.info(f"Training started")

    trainer = ModelTrainer()
    trainer.run()

    logger.info(f"Training time : {round(time.time() - start_time, 2)} sec.")
    logger.info(f"Training stopped")
