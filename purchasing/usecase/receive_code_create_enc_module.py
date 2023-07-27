import string
import random
import base64
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import AES
from Crypto import Random


def create_receive_code(purchase_num: str) -> str:
    """
    receive_code는 n자리의 purchase_detail_info를 16진수화 한 것과 (10 - n)자리의 무작위 라틴문자(대소문자 구별 없음),
    그리고 한 자리의 n 값으로 이루어져 있습니다
    """

    total_length = 10

    purchase_info = purchase_num
    id_length = len(str(purchase_info))
    random_key = ""
    print(purchase_info)

    for i in range(total_length - id_length):
        random_key += str(random.choice(string.ascii_letters))

    hex_base = hex(int(purchase_info))
    receive_code = hex_base + random_key + str(id_length)

    return receive_code


class EncModule:
    """
    base64만 적용, 추가 구현기간에 AES256기반 암호화 적용 예정
    """

    def __init__(self):
        self.key = "djangoProjectWiningByaws2"
        # padding(바이트 크기 맞추기 위한 의미 없는 값)설정
        self.BS = 16  # 바이트 사이즈
        self.total_length = 10

    def encrypt_receive_code(self, receive_code: str) -> str:
        """
        receive_code를 base64로 한 번, AES128 알고리즘으로 다시 한 번 암호화 해서 리턴합니다
        """
        # 암호화
        # iv = Random.new().read(AES.block_size)
        print("enc_value:  ", receive_code)
        receive_code_64_encoded = base64.b64encode(receive_code.encode("utf-8"))
        print("encoded : ", receive_code_64_encoded)

        return receive_code_64_encoded
