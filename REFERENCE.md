# Twilio Toolkit


|             |                |
|-------------|----------------|
| Name        | twilio |
| Package     | arcade_twilio |
| Repository  | None   |
| Version     | 0.1.0      |
| Description | A twilio integration to send SMS and WhatsApps.  |
| Author      | sdserranog@gmail.com      |


| Tool Name   | Description                                                             |
|-------------|-------------------------------------------------------------------------|
| SendSms | Send an SMS/text message to a phone number |
| SendWhatsapp | Send a WhatsApp message to a phone number |


### SendSms
Send an SMS/text message to a phone number

#### Parameters
- `phone_number`*(string, required)* The phone number to send the message to. Use 'my_phone_number' when a phone number is not specified or when the request implies sending to the user themselves
- `message`*(string, required)* The text content to be sent via SMS

---

### SendWhatsapp
Send a WhatsApp message to a phone number

#### Parameters
- `phone_number`*(string, required)* The phone number to send the message to. Use 'my_phone_number' when a phone number is not specified or when the request implies sending to the user themselves
- `message`*(string, required)* The text content to be sent via WhatsApp
