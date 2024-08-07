import requests,asyncio,time, json
from sql_script import add_request, read_all_rows, get_records, update_status, update_text
from gemma.NN_start import main_generate

## functions

def main_req():
    url = 'https://api.telegram.org/TOKEN_VAL/getUpdates'
    response = requests.post(url)
    return (response.content)

def get_last_id():
    upd_list = main_req()
    parsed = (json.loads(upd_list))['result']
    if len(parsed) == 0:
        return 'fake_id'
    if len(parsed) != 0:
        last_update_id = ((parsed[-1]))['update_id']
        return last_update_id

def get_index_for_new_slice(update_id):
    upd_list = main_req()
    parsed = (json.loads(upd_list))['result']
    for x in range(len(parsed)):
        if (parsed[x])['update_id']==update_id:
            return x

def get_new_messages_list(start_ind,last_ind):
    upd_list = main_req()
    parsed = (json.loads(upd_list))['result']
    sliced = parsed[start_ind:last_ind]
    return (sliced)

def get_length_updates():
    upd_list_start = main_req()
    time.sleep(1)
    parsed_start = (json.loads(upd_list_start))['result']
    return (len(parsed_start))

def processing_messages(text): 
    #result_text_to_send = 'Your message is - ' + text + ' - ...Bot is working'
    time.sleep(1)
    result_text_to_send = main_generate(text)
    time.sleep(1)
    return([result_text_to_send])

def main_req_send(chat_id,text):
    url = 'https://api.telegram.org/TOKEN_VAL/sendMessage'
    data={'chat_id': chat_id, 'text': text}
    requests.post(url,data)

## functions

## process to get new messages and save them

list_last_ids = []

def main_get_messages():

    ## script start  ##
    
    time.sleep(1)
    list_last_ids.append(get_last_id())

    ## script start ##

    ## main process ##
    while True:
        time.sleep(0.1)
        l_id = get_last_id()
        if l_id == list_last_ids[-1]:
            time.sleep(1)
            print('no new messages')
        if l_id != list_last_ids[-1]:
            print('is new message')
            time.sleep(0.1)
            new_start_ind_loop = get_index_for_new_slice(l_id)
            time.sleep(0.5)
            l_id = get_last_id()
            time.sleep(0.5)
            new_list = get_new_messages_list(new_start_ind_loop,get_length_updates())
            if len(new_list) == 0:
                continue
            if len(new_list) != 0:
                for e in new_list:
                    txt = e['message']['text']
                    tg_id = e['message']['from']['id']
                    status = 'pending'
                    add_request(txt,tg_id,status)
            list_last_ids.append(l_id) # add l_id to start new loop and wait for new messages
            if len(list_last_ids) > 10:
                list_last_ids.pop(0)
     ## main process ##


## process to get new messages and save them

## process to work with messages

async def processing_list():
        time.sleep(1)
        db_messages = get_records('Telegram_DB.db','pending','ASC')
        if len(db_messages) == 0:
            time.sleep(1)
        if len(db_messages) != 0:
            for x in db_messages:
                db_id = int(x[0])
                db_text =str(x[1])
                new_text = (processing_messages(db_text))[0] 
                update_status('Telegram_DB.db',db_id,'to_send')
                update_text('Telegram_DB.db',db_id,new_text)

def main_processing():
    while True:
        time.sleep(0.1)
        asyncio.run(processing_list())

## process to work with messages

## process to send messages back to telegram

def main_sending():
    while True:
        time.sleep(4)
        db_messages_send = get_records('Telegram_DB.db','to_send','ASC')
        if len(db_messages_send) == 0:
            time.sleep(0.5)
        if len(db_messages_send) != 0:
            time.sleep(0.5)
            sending_back = db_messages_send
            for e in sending_back:
                id_db = e[0]
                text = e[1]
                tg_id = e[2]
                main_req_send(tg_id,text)
                update_status('Telegram_DB.db',id_db,'ready')
                read_all_rows('Telegram_DB.db')
                time.sleep(0.5)
            
## process to send messages back to telegram