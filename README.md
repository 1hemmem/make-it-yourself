# Make It Yourself

## About this project

A Webapp that enables you to build your own domain expert chatbot, based on your provided documents (e.g: providing a guide of how to use a certain software)

It provide also a good level of flexibility when building your assistant:
- Providing a rich list of llms
- Providing multiple embedding models
- Ability to change some hyperparameters (temperature, top-p, top-k)

## Setup

### ollama-server

Copy the bash```ollama-server.ipynb``` code and put it in google colab, sign up in ngrok and get an authentication token and put it where I have commented in the code.
And finally run the code in the T4 GPU.

### backend-server

- path : bash```/app/src```
- install the required libraries: bash```pip install -r requirements.txt```
- run the api: bash```python -m uvicorn api:app --host 0.0.0.0 --port 8000```

### frontend

- path: bash```/frontend```
- bash```npm install```
- run : bash```npm run dev```
