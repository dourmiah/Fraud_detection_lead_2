import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from train import ModelTrainer

# Fixture pour instancier la classe ModelTrainer
@pytest.fixture
def trainer():
    return ModelTrainer()


# Test load_data
@patch("pandas.read_csv")
def test_load_data(mock_read_csv):
    
    file_path = file_path = "https://dom-jedha-bucket.s3.eu-west-3.amazonaws.com/data/fraudTest.csv"
    mock_data = pd.DataFrame({
        "id": [1, 2, 3],
        "col2": [4, 5, 6],
        "is_fraud": [0, 1, 0],
    })
    mock_read_csv.return_value = mock_data

    trainer = ModelTrainer()
    data = trainer.load_data()

    mock_read_csv.assert_called_once_with(file_path, nrows=5000)
    assert isinstance(data, pd.DataFrame)
    assert "id" not in data.columns
    assert "col2" in data.columns
    assert "is_fraud" in data.columns


# # Test preprocess_data
def test_preprocess_data():
   
    mock_data = pd.DataFrame({
    "col1": [1, 2, 3, 4, 5, 6],
    "col2": [5, 6, 7, 8, 9, 10],
    "is_fraud": [0, 1, 0, 1, 0, 1],  
})

    X_train, X_test, y_train, y_test = trainer.preprocess_data(mock_data)

    assert isinstance(X_train, pd.DataFrame)
    assert isinstance(X_test, pd.DataFrame)
    assert isinstance(y_train, pd.Series)
    assert isinstance(y_test, pd.Series)
    assert X_train.shape[0] > 0
    assert y_train.shape[0] > 0
    assert "col1" in X_train.columns
    assert "is_fraud" not in X_train.columns


# # Test pour la fonction `train_model`
# @patch("sklearn.ensemble.RandomForestClassifier.fit")
# def test_train_model(mock_fit):
#     # Mock des données
#     mock_X_train = pd.DataFrame({
#         "col1": [1, 2, 3],
#         "col2": [4, 5, 6],
#     })
#     mock_y_train = pd.Series([0, 1, 0])
    
#     # Mock de la méthode `fit`
#     mock_fit.return_value = None
    
#     # Initialiser ModelTrainer
#     trainer = ModelTrainer()
#     trainer.numeric_columns = ["col1", "col2"]  # Définir les colonnes numériques manuellement
    
#     # Appeler la méthode à tester
#     trainer.train_model(mock_X_train, mock_y_train)

#     # Vérifier si la méthode fit a été appelée
#     assert mock_fit.called
