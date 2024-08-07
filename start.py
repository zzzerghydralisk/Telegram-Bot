import time,threading
from tg_script import main_get_messages,main_processing,main_sending
from sql_script import create_database

time.sleep(0.5)
create_database('Telegram_DB.db')
time.sleep(0.5)

thread1 = threading.Thread(target=main_get_messages)
thread1.start()

thread2 = threading.Thread(target=main_processing)
thread2.start()

thread3 = threading.Thread(target=main_sending)
thread3.start()