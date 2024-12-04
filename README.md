# Make It Yourself


## About this project

A Webapp that enables you to build your own domain expert chatbot, based on your provided documents (e.g: providing a guide of how to use a certain software)

It provide also a good level of flexibility when building your assistant:
- Providing a rich list of llms
- Providing multiple embedding models
- Ability to change some hyperparameters (temperature, top-p, top-k)

## Setup

### ollama-server

Copy the ```ollama-server.ipynb``` code and put it in google colab, sign up in ngrok and get an authentication token and put it where I have commented in the code.
And finally run the code in the T4 GPU.

### backend-server
- install ollama locally : [ollama](https://ollama.com/)
- change the path : 
```cd /app/src```
- install the required libraries:
```pip install -r requirements.txt```
- run the api:
```python -m uvicorn api:app --host 0.0.0.0 --port 8000```

### frontend

- change the path:
```cd /frontend```
- install required packages:
```npm install```
- run the react app :
```npm run dev```


## Futur work
- Implemetation of multi-instance testing
- Give more control over the workflow parameters: similarity search function, k: number of documents retrieved, document chuncking strategy
- Improving the results with hellucination check.