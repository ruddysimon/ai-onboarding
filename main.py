import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
import openai
import os

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Set up OpenAI API
openai.api_key = os.environ.get("CHATGPT") 

@app.get("/", response_class=HTMLResponse)
async def chat_view(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chatbot")
async def chatbot(request: Request):
    data = await request.json()
    user_message = data.get("prompt")

    prompt = """Answer the question as truthfully as possible using the provided text, and if the answer is not contained within the text below, say 'I don't know'

Context: We need to help users generate an HTML table based plan for self motivation or group motivation to complete a task or group of tasks as a challenge.

The mission of GetMotivatedBuddies is to leverage technology to measurably improve well-being for individuals and society. 

Well-being measures quality of life across different domains. We focus on:

Autonomy – You feel you can make meaningful choices in your life.
Competence – You feel competent doing meaningful activities.
Relatedness – You have meaningful relationships with others.
System
GetMotivatedBuddies is a system that aims to measurably improve autonomy, competence and relatedness for individuals and groups.

Principles
We believe meaningful human relationships are at the core of individual and social change.
We believe the power of the internet can be used to improve wellbeing.
We believe technology overlooks the most potent technology accessible to everyone: our minds and our relationships.
We believe there is a mental health crisis and a lack of available resources for people to get help.
We believe the ad based business model on the internet creates bad incentives.
We believe the ad based business model has deleterious consequences for an individual’s attention and wellbeing.
We believe the deluge of information the internet has created makes life next to impossible to navigate and radically shifts our priorities.
We believe the negative consequences of the internet can be mitigated.
We believe human beings fundamentally have more in common with one another than that which separates them.
We believe simply showing up is the greatest form of courage.
We believe self-reflection leads to self-development.
We believe in a spectrum of privacy. Some things are private and other things are public.
We believe people and businesses have shared goals.
We believe there is a space to connect with others meaningfully that sits between therapy and family and friends.

"""
    prompt += request.prompt

    try:
        response = openai.Completion.create(
            prompt=prompt,
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0,
            model="text-davinci-003"
        )
        chat_response = response.choices[0].text.strip()
        return JSONResponse({"response": chat_response})

    except openai.error.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        return JSONResponse({"response": "Sorry... The AI chatbot is not available at the moment."})

    except Exception as e:
        print(f"An error occurred during chatbot processing: {e}")
        return JSONResponse({"response": "Sorry... An error occurred during chat processing."})
