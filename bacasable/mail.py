import yagmail, datetime
from dotenv import dotenv_values

value= dotenv_values(".env")
yag = yagmail.SMTP(value.get("USERMAIL"), value.get("PASSWORD"))
yag.send(
            to=value.get("USERMAIL"),
            subject="Hourly report from taskmaster application " + str(datetime.datetime.now()),
            contents="Find the hourly report from your taskmaster application",
            attachments=["/tmp/logs_PROCESS_STATES2023-03-06_19:04:45.732285.log"]
            )
