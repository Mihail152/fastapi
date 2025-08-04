from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal
import requests
import csv

app = FastAPI()

CSV_URL = "https://docs.google.com/spreadsheets/d/1yVJPDwYKl8allprZB8hRd0FuQLJvcypvC6Tt2PTg78s/export?format=csv&gid=0"
WHITELIST = {"+33612345678", "+33798765432"}
CONFIDENCE_THRESHOLD = 8





def load_whitelist():
    response = requests.get(CSV_URL)
    response.raise_for_status()

    lines = response.text.splitlines()
    reader = csv.reader(lines)
    next(reader, None) 

    whitelist = set()
    for row in reader:
        phone = row[0].strip()
        if phone:
            whitelist.add(phone)
    return whitelist

print("Starting the application...")
# whitelist = load_whitelist()
whitelist = WHITELIST
print(f"Loaded whitelist: {whitelist}")

class CallData(BaseModel):
    PhoneNumber: str
    IsSpam: bool
    Confidence: int
    CallType: Literal["Scam", "Robocall", "Telemarketing", "Unknown", ""]

@app.post("/filter_call")
async def filter_call(data: CallData):
    phone = data.PhoneNumber

    if phone in whitelist:
        print(f"[LOG] {phone} — ALLOW (whitelisted)")
        return {"action": "ALLOW", "reason": "Whitelisted (test list)"}

    if data.IsSpam and data.Confidence >= CONFIDENCE_THRESHOLD and data.CallType.lower() in {"scam", "robocall"}:
        print(f"[LOG] {phone} — BLOCK (high confidence spam)")
        return {"action": "BLOCK", "reason": "High confidence spam"}

    print(f"[LOG] {phone} — ALLOW (not spam or low confidence)")
    return {"action": "ALLOW", "reason": "Low confidence or unknown"}