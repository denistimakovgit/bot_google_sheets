import os
import httplib2
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
import telebot
import schedule
import time
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN=os.getenv("BOT_TOKEN")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SERVICE_ACCOUNT = os.getenv("SERVICE_ACCOUNT")
check_list = ['просрочено', 'просроченно']

bot = telebot.TeleBot(BOT_TOKEN)

def google_auth():

    creds_json = "bot-api-sheets-1fde916d8680.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)

def send_message():
    service = google_auth()
    sheet = service.spreadsheets()
    resp = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range='Текущий!A30:AG').execute()

    for elem in resp['values']:
        result = [item for item in [x.lower() for x in elem] if item in check_list]
        if result:
            notification = f'Адрес: {elem[1]}, телефон {elem[3]}, литраж {elem[4]}'
            bot.send_message(chat_id=182731743, text=notification)

#schedule.every(15).seconds.do(send_message)
schedule.every().day.at("12:00").do(send_message)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(1)