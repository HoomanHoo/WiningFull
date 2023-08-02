import base64


class DecModule:

    """
    base64만 적용, 추가 구현기간에 AES256기반 암호화 적용 예정
    """

    def __init__(self):
        self.key = "djangoProjectWiningByaws2"
        # padding(바이트 크기 맞추기 위한 의미 없는 값)설정
        self.BS = 16  # 바이트 사이즈
        self.total_length = 10

    def decrypt_receive_code(self, enc_receive_code: str) -> str:
        """
        암호화된 receive_code를 AES128 알고리즘으로 한 번, base64로 다시 한 번 복호화 한 뒤,
        16진수화 된 purchase_detail_info를 10진수화 해서 리턴합니다
        """

        print("enc_receive_code2: ", enc_receive_code)
        # enc_receive_code = enc_receive_code.encode()
        # # enc_receive_code= bytes(enc_receive_code, "utf-8")
        # print("enc_receive_code encoded", enc_receive_code)

        # # 복호화

        m5 = base64.b64decode(enc_receive_code)
        m5 = m5.decode("utf-8")
        ren = m5[-1:]
        m6 = m5[: -(self.total_length - int(ren) + 1)]
        purchase_info = int(m6, 16)
        print("purchase_info: ", purchase_info)
        return purchase_info
