from fastapi import FastAPI

app = FastAPI(title='KhonYaai Cancel API', version='0.1.0')


@app.get('/health')
def health_check():
    return {'status': 'ok', 'service': 'khonyaai-cancel-api'}
