import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from ml_utils import load_model, predict, retrain
from typing import List

# defining the main app
app = FastAPI(title="Credit Score ", docs_url="/")

# calling the load_model during startup.
# this will train the model and keep it loaded for prediction.
app.add_event_handler("startup", load_model)

# class which is expected in the payload
class QueryIn(BaseModel):
    Durationinmonth: int
    Creditamount: int
    Installmentrateinpercentageofdisposableincome: int
    Presentresidencesince: int
    Ageinyears: int
    Numberofexistingcreditsatthisbank: int
    Numberofpeoplebeingliabletoprovidemaintenancefor: int


# class which is returned in the response
class QueryOut(BaseModel):
    CostMatrixRisk: str


# class which is expected in the payload while re-training
class FeedbackIn(BaseModel):
    Durationinmonth: int
    Creditamount: int
    Installmentrateinpercentageofdisposableincome: int
    Presentresidencesince: int
    Ageinyears: int
    Numberofexistingcreditsatthisbank: int
    Numberofpeoplebeingliabletoprovidemaintenancefor: int

# Route definitions
@app.get("/hackathon_group_8")
# Healthcheck route to ensure that the API is up and running
def ping():
    return {"hackathon group 8": "go through it"}


@app.post("/credit_score", response_model=QueryOut, status_code=200)
# Route to do the prediction using the ML model defined.
# Payload: QueryIn containing the parameters
# Response: QueryOut containing the risk class predicted (200)
def credit_score(query_data: QueryIn):

    return {"CostMatrixRisk": predict(query_data)}

@app.post("/feedback_loop", status_code=200)
# Route to further train the model based on user input in form of feedback loop
# Payload: FeedbackIn containing the parameters and correct Cost Matrix(Risk) class
# Response: Dict with detail confirming success (200)
def feedback_loop(data: List[FeedbackIn]):
    retrain(data)
    return {"detail": "Feedback loop successful"}


# Main function to start the app when main.py is called
if __name__ == "__main__":
    # Uvicorn is used to run the server and listen for incoming API requests on 0.0.0.0:8888
    uvicorn.run("main:app", host="127.0.0.1", port=5000, reload=True)
