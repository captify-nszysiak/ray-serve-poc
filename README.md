# ray-serve-poc
Ray Serve PoC

Download model (can be baked into Docker image- I did not want to push big models to GH):
- aws s3 cp s3://captify-semantics/personal/emarkou/model.onnx models/

Run Ray server locally:
- pip install -r requirements.txt
- pip install -U "ray[data,train,tune,serve]"
- 
- serve run server:predictor_app

To call the Ray server:
- python client.py

Ray Cluster dashboard: 
- http://127.0.0.1:8265/#/overview