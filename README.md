This is a simple FastAPI project to filter phone calls using spam flags and a whitelist from Google Sheets.

---

pip install -r requirements.txt
uvicorn main:app --reload
http://127.0.0.1:8000/docs – API test page (Swagger UI)

Test with cURL
curl -X POST http://127.0.0.1:8000/filter_call \
  -H "Content-Type: application/json" \
  -d '{"PhoneNumber": "+33612345678", "IsSpam": true, "Confidence": 9, "CallType": "Scam"}'

Logic
Analyze spam flags like IsSpam, Confidence, and CallType
Automatically allow whitelisted test numbers
Return a decision: ALLOW, BLOCK, or LOG (for testing/audit)

