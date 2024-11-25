# Make It Yourself

```
⚠️ This repository is still in construction ⚠️
```

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

- path : ```/app/src```
- install the required libraries: ```pip install -r requirements.txt```
- run the api: ```python -m uvicorn api:app --host 0.0.0.0 --port 8000```

### frontend

- path: ```/frontend```
- install required packages: ```npm install```
- run : ```npm run dev```
