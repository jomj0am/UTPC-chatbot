from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Serve static files from the 'home' directory
app.mount("/", StaticFiles(directory="home", html=True), name="home")

@app.post("/stream")
async def stream(request: Request):
    data = await request.json()
    prompt = data.get('prompt')

    if not prompt:
        return JSONResponse(content={"response": "No question asked"}, status_code=200)

    # Debug print to verify data
    print(f"Received prompt: {prompt}")

    # Add logic to handle your streaming here
    # For demonstration, we're just echoing back the prompt
    response_text = f"Received prompt: {prompt}"
    return JSONResponse(content={"response": response_text}, status_code=200)
