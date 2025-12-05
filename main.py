from flask import Flask, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
CORS(app)

# Google Sheets 인증
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

SHEET_KEY = "여기에_너_구글시트_키_입력"  # 스프레드시트 URL에서 d/ ~ /edit 사이

@app.route("/get-data", methods=["GET"])
def get_data():
    try:
        sheet = client.open_by_key(SHEET_KEY).worksheet("Sheet1")
        data = sheet.get_all_records()
        return jsonify({"status": "ok", "data": data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route("/update", methods=["POST"])
def update():
    try:
        body = request.json
        row = body.get("row")
        col = body.get("col")
        value = body.get("value")

        sheet = client.open_by_key(SHEET_KEY).worksheet("Sheet1")
        sheet.update_cell(row, col, value)

        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run()
