from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
# from openai import OpenAI
from pydantic import BaseModel


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = {}

class UserQuery(BaseModel):
    query: str

@app.get("/")
async def get():
    return {"message": "Hello Duniyaa"}

@app.post("/ques/")
async def submit_form(data: UserQuery):
    return {"message": f"I love my India."}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    
    # Assign user label
    user_id = f"User{len(connected_clients) + 1}"
    connected_clients[websocket] = user_id
    print(f"{user_id} connected!")

    try:
        while True:
            data = await websocket.receive_text()
            message = f"{connected_clients[websocket]}: {data}"
            
            # Broadcast the message to all connected clients
            for client in connected_clients:
                await client.send_text(message)

    except WebSocketDisconnect:
        print(f"{connected_clients[websocket]} disconnected!")
        del connected_clients[websocket]





# def get_completion(prompt, model="gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": prompt}]
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=0, # this is the degree of randomness of the model's output
#     )
#     return response.choices[0].message["content"]

# def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
#     response = client.chat.completions.create(
#         model=model,
#         messages=messages,
#         temperature=temperature, # this is the degree of randomness of the model's output
#     )
# #     print(str(response.choices[0].message))
#     # print(response)
#     return response.choices[0].message.content


# messages =  [  
# {'role':'system', 'content':'You are a teacher having 10 year of experience, You have to resolve student query. response should be easy to understand.'},    
# {'role':'user', 'content':'what is the national sport of India'},   
# # {'role':'assistant', 'content':'Why did the chicken cross the road'},   
# # {'role':'user', 'content':'I don\'t know'}  ]
# ]
# response = get_completion_from_messages(messages, temperature=1)
# print(response)



