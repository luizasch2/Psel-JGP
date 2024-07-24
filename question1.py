import requests
import pandas as pd
import json

# Id's:
# CUSR0000SA0: All itens Ajusted
# CUSR0000SA0L1E: All itens Ajusted, less food and energy
# CUSR0000SETB01: gasoline

api_key = '16179ba7c8fb4ea5b7b0bd145b7d24ae'
headers = {'Content-type': 'application/json'}

data = json.dumps({"registrationkey": api_key, 
                   "seriesid": ['CUSR0000SA0','CUSR0000SA0L1E', 'CUSR0000SETB01'],
                   "startyear":"2014", 
                   "endyear":"2024"})

try:
    p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)

    json_data = json.loads(p.text)

    data_entries = []

    for series in json_data['Results']['series']:
        seriesId = series['seriesID']
        for item in series['data']:
            if 'M01' <= item['period'] <= 'M12':  
                year = item['year']
                period = item['period']
                value = item['value']

                data_entries.append({"series id": seriesId, "year": year, "period": period, "value": value})

    df = pd.DataFrame(data_entries, columns=["series id", "year", "period", "value"])

    df['Date'] = (df['year'].astype("str") + '-' + df['period'].apply(lambda x: x[1:]) + '-01').astype('datetime64[ns]')
    df.drop(['year', 'period'], axis=1, inplace=True)

    df = df.pivot(index='Date', columns='series id', values='value')
    df.columns = ['All Items', 'All Items Less Food and Energy', 'Gasoline']

    df.to_csv('CPIdata.csv')

except requests.exceptions.HTTPError as err:
    print(f"Erro HTTP ocorrido: {err}")
except requests.exceptions.RequestException as err:
    print(f"Erro de requisição ocorrido: {err}")
except Exception as err:
    print(f"Um erro ocorreu: {err}")