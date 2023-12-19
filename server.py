from starlette.requests import Request

from ray import serve
import onnxruntime


# replicas, which are individual copies of the class or function that are started in
# separate Ray Actors (processes). The number of replicas can be scaled up or down
# (or even autoscaled) to match the incoming request load.
@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
class ONNXDummyModel:

    def __init__(self):
        self.session = onnxruntime.InferenceSession("models/model.onnx")

    def predict(self, inputs):
        input_name = self.session.get_inputs()[0].name
        input_data = {input_name: inputs}
        result = self.session.run(None, input_data)
        return result[0]

    async def __call__(self, http_request: Request) -> str:
        model_input: str = await http_request.json()
        return self.predict(model_input)


predictor_app = ONNXDummyModel.bind()
