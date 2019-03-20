# Twilio SMS GUI with contacts

Simple gui to send SMS via Twilio, using predefined contact list.

## Install

```bash
pip install -r requirements.txt
```

## Config

Create `config.yml` file and place it near `gui.py`:
```yml
api:
  accountsid: YourAccountSID
  authtoken: YourAuthToken
  callerid: "YourTwilioPhone"
contacts:
  Contact: "phone"
  Contact2: "phone"
  #...
```

Example:

```yml
api:
  accountsid: ACn6233a2f6ad54844daa770fsfasfas
  authtoken: 39af9safsfafafsfasfafasf221fsafs
  callerid: "+12345678910"
contacts:
  Johny: "+79012345678"
  Sergey: "+79123456789"
```

## Usage

Just run `python3 gui.py`
