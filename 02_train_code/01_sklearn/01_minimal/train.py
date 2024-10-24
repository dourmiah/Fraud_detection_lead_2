import os
import mlflow
import datetime

from PIL import Image


class ModelTrainer:
    def __init__(self):
        mlflow.log_param("Dummy_Param", 42)
        mlflow.set_tag("Author", "Philippe")

        image = Image.new("RGB", (100, 100), color="red")
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        title = f"./img/{timestamp}_dummy_artifact.png"
        image.save(title)
        mlflow.log_artifact(title)


if __name__ == "__main__":
    os.makedirs("./img", exist_ok=True)
    trainer = ModelTrainer()
