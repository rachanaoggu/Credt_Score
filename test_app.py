from fastapi.testclient import TestClient
from main import app

# test to check the correct functioning of the /ping route
def test_ping():
    with TestClient(app) as client:
        response = client.get("/hackathon_group_8")
        # asserting the correct response is received
        assert response.status_code == 200
        assert response.json() == {"hackathon group 8": "go through it"}


# test to check if Iris Virginica is classified correctly
def test_credit_score():
    # defining a sample payload for the testcase
    payload = {
      "Durationinmonth": 0,
      "Creditamount": 0,
      "Installmentrateinpercentageofdisposableincome": 0,
      "Presentresidencesince": 0,
      "Ageinyears": 0,
      "Numberofexistingcreditsatthisbank": 0,
      "Numberofpeoplebeingliabletoprovidemaintenancefor": 0
    }
    with TestClient(app) as client:
        response = client.post("/credit_score", json=payload)
        # asserting the correct response is received
        assert response.status_code == 200
        
