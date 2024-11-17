## SMART HOME project
The smart home system is built and operated using a Raspberry Pi 4B. Its operation principle is as follows:

### Door Access:
When an RFID card is detected and scanned by the reader, if the card is valid, the door will automatically open and close using a servo motor. The access information is then logged into the database.

### Anti-Theft Mechanism:
If the infrared sensor detects that the door is opened without a valid RFID card scan, the LED will light up, and the system will recognize this as an unauthorized intrusion. Simultaneously, the information is updated in the database, and an intrusion alert is sent to the Feed channel on Adafruit IO and via email.
