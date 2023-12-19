from transformers import AutoTokenizer
import onnxruntime
from fastapi import Request
from ray import serve
import numpy as np


@serve.deployment(num_replicas=10, ray_actor_options={"num_cpus": 0.8, "num_gpus": 0})
class ONNXDummyModel:

    def __init__(self):
        self.model = onnxruntime.InferenceSession("models/model.onnx")
        self.tokenizer = AutoTokenizer.from_pretrained("roberta-base")
        self.threshold = 0.5

    def predict(self, data):
        inputs = self.tokenizer(data, padding=True, truncation=True, max_length=68, return_tensors="pt")
        input_ids = inputs["input_ids"].numpy()
        attention_mask = inputs["attention_mask"].numpy()

        input_ids = np.tile(input_ids, (10, 1))
        padding_columns = 68 - input_ids.shape[1]
        input_ids = np.pad(input_ids, ((0, 0), (0, padding_columns)), mode='constant')

        attention_mask = np.tile(attention_mask, (10, 1))
        padding_columns = 68 - attention_mask.shape[1]
        attention_mask = np.pad(attention_mask, ((0, 0), (0, padding_columns)), mode='constant')

        input_name = self.model.get_inputs()[0].name
        attention_mask_name = self.model.get_inputs()[1].name
        output_name = self.model.get_outputs()[0].name

        logits = self.model.run([output_name], {input_name: input_ids, attention_mask_name: attention_mask})[0]
        probabilities = 1 / (1 + np.exp(-logits))
        predictions = (probabilities > self.threshold).astype(int)

        return predictions

    async def __call__(self, http_request: Request) -> str:
        data = await http_request.json()
        predictions = self.predict(data)
        return {"predictions": predictions.tolist()}


predictor_app = ONNXDummyModel.bind()