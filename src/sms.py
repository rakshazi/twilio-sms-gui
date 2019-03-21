from twilio.rest import Client

recipients = []

def add(phone):
    recipients.append(phone)

def delete(phone):
    recipients.remove(phone)

def send(config, body, log):
    client = Client(config['accountsid'], config['authtoken'])
    for to in recipients:
        message = client.messages.create(to=to, from_=config['callerid'],body=body)
        log.setText(to + ': ' + message.sid)
