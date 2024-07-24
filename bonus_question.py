import pandas as pd
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
import csv

df = pd.read_csv('CPIdata.csv')
df['Date'] = pd.to_datetime(df['Date'])

app = FastAPI()

# Main page
@app.get("/", response_class=HTMLResponse)
async def main_page():
    return """
    <html>
        <body>
            <h1>Request CPI Data</h1>
            <ul>
            <li><a href="/data/">All data</a></li>
            </ul>
            <form action="/search-date" method="post">
                <label for="year">Year:</label>
                <select id="year" name="year">
                    <option value="2024">2024</option>
                    <option value="2023">2023</option>
                    <option value="2022">2022</option>
                    <option value="2021">2021</option>
                    <option value="2020">2020</option>
                    <option value="2019">2019</option>
                    <option value="2018">2018</option>
                    <option value="2017">2017</option>
                    <option value="2016">2016</option>
                    <option value="2015">2015</option>
                    <option value="2014">2014</option>
                    
                </select>

                <label for="month">Month:</label>
                <select id="month" name="month">
                    <option value="1">January</option>
                    <option value="2">February</option>
                    <option value="3">March</option>
                    <option value="4">April</option>
                    <option value="5">May</option>
                    <option value="6">June</option>
                    <option value="7">July</option>
                    <option value="8">August</option>
                    <option value="9">September</option>
                    <option value="10">October</option>
                    <option value="11">November</option>
                    <option value="12">December</option>
                </select>

                <button type="submit">Search</button>
            </form>
        </body>
    </html>
    """
# Search by date
@app.post("/search-date")
async def process_date(year: str = Form(...), month: str = Form(...)):
    month_padded = month.zfill(2)
    return RedirectResponse(url=f"/data/{year}-{month_padded}-01", status_code=303)

# All Data page
@app.get("/data/", response_class=HTMLResponse)
async def read_items():
    items = []
    try:
        with open('CPIdata.csv', mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                items.append(row)

        # Generating HTML table from items
        if items:
            # Create the HTML for the table header
            headers = items[0].keys()
            header_html = ''.join(f"<th>{header}</th>" for header in headers)
            header_row = f"<tr>{header_html}</tr>"

            body_html = ''.join(f"<tr>{''.join(f'<td>{row[col]}</td>' for col in row)}</tr>" for row in items) # Create the HTML for the table body
            
            table_html = f"<table border='1'>{header_row}{body_html}</table>" # Full HTML table
            
            return f"""
            <html>
                <body>
                    <h1>CPI Data Overview</h1>
                    {table_html}
                    <a href='/'>Go Home</a>
                </body>
            </html>
            """
        else:
            return """
            <html>
                <body>
                    <h1>No CPI data found.</h1> 
                    <a href='/'>Go Home</a>
                </body>
            </html>
            """
    except Exception as e:
        return f"""
        <html>
            <body>
                <h1>Error loading data: {str(e)}</h1>
                <a href='/'>Go Home</a>
            </body>
        </html>
        """

# CPI data by date
@app.get("/data/{date}", response_class=HTMLResponse)
def get_data_by_date(date: str):
    try:
        filtered_data = df[df['Date'] == pd.to_datetime(date)] # Filter data by date
        if not filtered_data.empty:
            data_html = filtered_data.iloc[0].to_frame().to_html() # Convert the data to HTML
            response_html = f"<html><body><h1>Data for {date}</h1>{data_html}<br><a href='/'>Go Home</a></body></html>" # Create the response HTML
        else:
            response_html = f"<html><body><h1>No data available for this date.</h1><a href='/'>Go Home</a></body></html>"
    except Exception as e:
        response_html = f"<html><body><h1>Error: {str(e)}</h1><a href='/'>Go Home</a></body></html>"

    return response_html