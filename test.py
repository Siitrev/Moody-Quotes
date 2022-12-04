import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

request_data = request.get_json()

if getsize("/home/Sitrev/users_data/users.json"):
    with open("/home/Sitrev/users_data/users.json") as file:
        users = json.load(file)
else:
    users = {}
    

# Define the transport variables
ctx = ssl.create_default_context()
password = "ngltzudrmncfnmol"    # Your app password goes here
sender = "quotegeneratorpy@gmail.com"    # Your e-mail address
receiver = request_data["email"]  # Recipient's address

# Create the message
message = MIMEMultipart("alternative")
message["Subject"] = f"Hello {request_data["username"]}"
message["From"] = sender
message["To"] = receiver

code = str(random.randint(10000,99999))

# HTML version
html = f"""\
<html>
  <body>
    <p>
        <i>Hello {request_data["username"]}</i>
    </p>
    <p>
        Here's your code for password reset: {code}
    </p>
  </body>
</html>
"""

plain = f"""\
Hello {request_data["username"]}.
Here's your code for password reset: {code}
"""

message.attach(MIMEText(plain, "plain"))
message.attach(MIMEText(html, "html"))

with smtplib.SMTP_SSL("smtp.gmail.com", port=465, context=ctx) as server:
    server.login(sender, password)
    server.sendmail(sender, receiver, message.as_string())

users[request_data["username"]]["token"] = code

with open("/home/Sitrev/users_data/users.json","w") as file:
    json.dump(users,file)
