import samino
import secmail
from os import system
from time import sleep
from names import get_last_name
from pyfiglet import figlet_format
from webbrowser import open_new_tab
from colored import fore, style, attr
attr(0)
print(f"""{fore.RED + style.BOLD}
Script by zeviel
Github : https://github.com/zeviel""")
print(figlet_format("13MINXAVT9R3GK1LLA", font="standard", width=60))
sec_mail = secmail.SecMail()

def open_verification_link(link: str):
    system(f"termux-open-url {link}")
    open_new_tab(link)

def get_verification_link(email: str):
    sleep(3)
    verify_messageID = sec_mail.get_messages(email=email).id
    verification_link = sec_mail.read_message(
        email, verify_messageID[0]
    ).htmlBody.split('"')[13]
    print(f"-- Verification Link::: {verification_link}")
    open_verification_link(link=verification_link)

def activate_account(email: str, password: str, number: int, verification_code: int):
    client = samino.Client()
    client.login(email=email, password=password)
    client.verify_account(email=email, code=verification_code)
    print(f"[{number}]Account::: {email} is activated!")

def save_account(email: str, password: str):
    with open("accounts.txt", "a") as accounts:
        accounts.write(f"{email}:{password}\n")
        accounts.close()

def auto_register(password: str, count: int):
    for i in range(count):
        try:
            client = samino.Client() # for generating new device_id
            email = sec_mail.generate_email()
            nickname = get_last_name()
            client.register(
                email=email,
                password=password,
                nickname=nickname,
                deviceId=client.deviceId,
            )
            print(
                f"[{count}]Succesful Registered! \n-- Email::: {email}, \n-- Password::: {password}, \n-- deviceID::: {client.deviceId}"
			)
            client.send_verify_code(email=email)
            get_verification_link(email=email)
            activate_account(
                email=email,
                password=password,
                number=count,
                verification_code=input("-- Verification code::: "),
            )
            save_account(email=email, password=password)
        except Exception as e:
            print(e)

password = input("-- Password for all accounts::: ")
count = int(input("-- How many accounts?::: "))
auto_register(password=password, count=count)
