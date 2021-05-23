import json
registered_data = {}
with open('registered_data.json', 'r', encoding="utf-8") as f:
    registered_data = json.load(f)

if mtext == '記帳':
    func.sendQuickreply(event)

elif mtext in oplist:
    func.sendQuickreply2(event)
    with open('registered_data.json', 'r', encoding="utf-8") as f:
        registered_data = json.load(f)
    registered_data[uid] = {"項目":, "必要":, "金額":, "時間":}
    registered_data[uid]["項目"] = mtext
    with open('registered_data.json', 'w', encoding="utf-8") as f:
        json.dump(registered_data, f, ensure_ascii=False)

elif mtext in eslist:
    func.sendText(event)
    with open('registered_data.json', 'r', encoding="utf-8") as f:
        registered_data = json.load(f)
    registered_data[uid]["必要"] = mtext
    with open('registered_data.json', 'w', encoding="utf-8") as f:
        json.dump(registered_data, f, ensure_ascii=False)

elif str.isdigit(mtext) == True:
    with open('registered_data.json', 'r', encoding="utf-8") as f:
        registered_data = json.load(f)
    registered_data[uid]["金額"] = mtext
    registered_data[uid]["時間"] = str(time)
    with open('registered_data.json', 'w', encoding="utf-8") as f:
        json.dump(registered_data, f, ensure_ascii=False)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text="記帳成功"))






