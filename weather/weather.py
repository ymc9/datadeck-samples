from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import requests

# Fetch weather forecast data
weather_query = '''
    select * from weather.forecast where woeid in 
        (select woeid from geo.places(1) 
            where text="Seattle, WA")'''
data = requests.get('https://query.yahooapis.com/v1/public/yql?format=json&q=' \
    + weather_query)
data_json = data.json()

# Open or create google drive file
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
file_name = 'seattleweather.csv'
files = drive.ListFile({'q': "title='{}' and trashed=false".format(file_name)}).GetList()
if files:
    gd_file = files[0]
else:
    gd_file = drive.CreateFile({'title': file_name, 'mimeType': 'text/csv'})

# Set content and upload
content = 'date,high,low\n'
for item in data_json['query']['results']['channel']['item']['forecast']:
    content += '{},{},{}\n'.format(item['date'],item['high'], item['low'])
gd_file.SetContentString(content)
gd_file.Upload()
print('File uploaded, title: {}, id: {}'.format(gd_file['title'], gd_file['id']))
