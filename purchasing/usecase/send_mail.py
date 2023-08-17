import smtplib
from email.mime.text import MIMEText
import time
from Wining import settings


def send_charge_email(user_name: str, user_email: str, charge_point: int, charge_time):
    user_subject = user_name + "님의 포인트 충전 내역입니다."
    user_message = (
        user_name
        + "님의 포인트 충전 내역입니다. \n"
        + str(charge_point)
        + "원 \n"
        + "충전 일시: "
        + str(charge_time)
    )

    smtp = smtplib.SMTP("smtp.naver.com", 587)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWD)
    msg = MIMEText(user_message)
    msg["From"] = settings.EMAIL_HOST_USER
    msg["Subject"] = user_subject
    msg["To"] = str(user_email)
    smtp.sendmail(settings.EMAIL_HOST_USER, str(user_email), msg.as_string())
    smtp.close()


def send_purchase_email(
    user_name: str,
    user_email: str,
    purchase_info_list: list,
):
    store_email_list = []
    wine_name_list = {}
    store_name_list = {}
    receive_code_list = {}
    purchase_det_number_list = {}
    purchase_det_price_list = {}
    store_address_list = {}

    customer_message = user_name + "님의 결제 내역입니다.\n"

    for purchase_info in purchase_info_list:
        wine_name = purchase_info["purchase_detail_id__sell__wine__wine_name"]
        purchase_det_number = purchase_info["purchase_detail_id__purchase_det_number"]
        purchase_det_price = purchase_info["purchase_detail_id__purchase_det_price"]
        store_name = purchase_info["purchase_detail_id__sell__store__store_name"]
        store_address = purchase_info["purchase_detail_id__sell__store__store_address"]
        store_email = purchase_info["purchase_detail_id__sell__store__store_email"]
        receive_code = purchase_info["receive_code"]

        customer_message += (
            "\n"
            + str(store_name)
            + " "
            + str(store_address)
            + " "
            + str(wine_name)
            + " "
            + str(purchase_det_number)
            + "개 "
            + str(purchase_det_price)
            + "원  수령코드: "
            + str(receive_code)
            + "\n"
        )

        if store_email not in store_email_list:
            store_email_list.append(store_email)
            wine_name_list[store_email] = [wine_name]
            store_name_list[store_email] = [store_name]
            purchase_det_number_list[store_email] = [purchase_det_number]
            receive_code_list[store_email] = [receive_code]
            purchase_det_price_list[store_email] = [purchase_det_price]
            store_address_list[store_email] = [store_address]

        elif store_email in store_email_list:
            wine_name_list[store_email].append(wine_name)
            purchase_det_number_list[store_email].append(purchase_det_number)
            receive_code_list[store_email].append(receive_code)
            purchase_det_price_list[store_email].append(purchase_det_price)
            store_address_list[store_email].append(store_address)

    subject = user_name + "님 Wining 결제 내역입니다"
    to = str(user_email)
    from_email = str(settings.EMAIL_HOST_USER)
    message = customer_message

    smtp = smtplib.SMTP("smtp.naver.com", 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWD)

    msg = MIMEText(message)
    msg["From"] = settings.EMAIL_HOST_USER
    msg["Subject"] = subject
    msg["To"] = to
    smtp.sendmail(from_email, str(user_email), msg.as_string())

    time.sleep(0.3)

    for store_email in store_email_list:
        store_message = (
            str(store_name_list[store_email][0]) + "님 " + user_name + "님의 주문 내역 입니다\n"
        )
        for idx, wine_name in enumerate(wine_name_list[store_email]):
            store_message += (
                "\n"
                + str(wine_name)
                + " "
                + str(purchase_det_number_list[store_email][idx])
                + "개 "
                + str(purchase_det_price_list[store_email][idx])
                + "원 "
                + "\n"
            )
        subject = (
            str(store_name_list[store_email][0]) + "님 " + user_name + "님의 주문 내역 입니다"
        )
        to = str(store_email)
        from_email = str(settings.EMAIL_HOST_USER)
        message = store_message

        msg = MIMEText(message)
        msg["From"] = settings.EMAIL_HOST_USER
        msg["Subject"] = subject
        msg["To"] = to
        smtp.sendmail(from_email, str(store_email), msg.as_string())
        time.sleep(0.3)

    smtp.quit()

    # django mail은 smtp 단에서 인증 오류가 발생하여 사용할 수 없음
    # result = EmailMessage(
    #     subject=subject,
    #     body=message,
    #     from_email=from_email,
    #     to=to,
    #     connection=get_connection(settings.EMAIL_BACKEND, fail_silently=False),
    # )
    # result.send()

    # seller_message = ""
    # for store_email in store_email_list:
    #     store_email = str(store_email)
    #     store_name = store_name_list[store_email]
    #     wine_name = wine_name_list[store_email]
    #     purchase_det_number = purchase_det_number_list[store_email]
    #     receive_code = receive_code_list[store_email]

    #     seller_messeage += (
    #         store_name_list[store_email]
    #         + " "
    #         + wine_name_list[store_email]
    #         + " "
    #         + purchase_det_number_list[store_email]
    #         + "개 "
    #         + purchase_det_price_list[store_email]
    #         + "원  수령코드: "
    #         + receive_code_list[store_email]
    #     )

    # subject = user_name + "님 Wining 결제 내역입니다"
    # to = [user_email]
    # from_email = settings.EMAIL_HOST_USER
    # message = customer_messeage
    # EmailMessage(subject=subject, body=message, from_email=from_email, to=to).send()
