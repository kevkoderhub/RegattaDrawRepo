from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Set up Google Sheets API credentials
###scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#creds = ServiceAccountCredentials.from_json_keyfile_name("path/to/credentials.json", scope)
#client = gspread.authorize(creds)

# Function to fetch data from Google Sheets
def fetch_data(sheet_url):
    sheet = client.open_by_url(sheet_url).sheet1
    data = sheet.get_all_records()
    return data

# Endpoint to get races for a specific racer
@app.route('/races', methods=['GET'])
def get_races():
    racer_name = request.args.get('racer')
    sheet_url = request.args.get('sheet_url')
    data = fetch_data(sheet_url)
    
    # Filter data for the specified racer
    racer_races = [row for row in data if racer_name in row['Crew']]
    
    return jsonify(racer_races)

# Endpoint to display a DataFrame
@app.route('/show_dataframe')
def show_dataframe():
    # Create a DataFrame with two columns and five rows
    data = {
        'Numbers': [1, 2, 3, 4, 5],
        'Letters': ['A', 'B', 'C', 'D', 'E']
    }
    df = pd.DataFrame(data)
    
    # Convert DataFrame to HTML
    html_table = df.to_html(classes='table table-striped')
    
    # Render the HTML table
    return render_template_string('''
        <html>
        <head>
            <title>DataFrame</title>
            <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
        </head>
        <body>
            <div class="container">
                <h1>DataFrame</h1>
                {{ table | safe }}
            </div>
        </body>
        </html>
    ''', table=html_table)

if __name__ == '__main__':
    app.run(debug=True)
