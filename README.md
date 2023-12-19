# ray-serve-poc
Ray Serve PoC

Download model (can be baked into Docker image- I did not want to push big models to GH):
- aws s3 cp s3://captify-semantics/personal/emarkou/model.onnx models/

Run Ray server locally:
- pip install -r requirements.txt 
- sudo serve run server:predictor_app (run with sudo to see CPU Flame Graph)

To call the Ray server:
- python client.py

Ray Cluster dashboard: 
- http://127.0.0.1:8265/#/overview