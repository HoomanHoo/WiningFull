import requests

from Wining import settings


def kakao_token(code, redirect_uri, is_store):
    REST_API_KEY = getattr(settings, "KAKAO_REST_API_KEY")
    KAKAO_REDIRECT_URI = redirect_uri
    token_url = "https://kauth.kakao.com/oauth/token"
    print(KAKAO_REDIRECT_URI)
    print(code)
    request_body = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "redirect_uri": KAKAO_REDIRECT_URI,
        "code": code,
    }

    request_header = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

    token_response = requests.post(token_url, data=request_body, headers=request_header)

    token_json = token_response.json()
    print("token_json:t ", token_json)
    access_token = token_json.get(
        "access_token", None
    )  # get메서드 사용해서 access 토큰 없을 때 에러 핸들링 하도록함
    if access_token is None:
        result = {"code": -1}
        return result

    elif access_token is not None:
        scope = token_json["scope"]
        auth = f"Bearer {access_token}"

        show_token_info_url = "https://kapi.kakao.com/v1/user/access_token_info"
        token_info_request_header = {
            "Authorization": auth,
        }

        token_info_response = requests.get(
            show_token_info_url, headers=token_info_request_header
        )
        token_info_json = token_info_response.json()

        user_info_url = "https://kapi.kakao.com/v2/user/me"

        user_info_request_header = {
            "Authorization": auth,
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        user_info_response = requests.post(
            user_info_url, headers=user_info_request_header
        )
        user_info = user_info_response.json()
        print(user_info)
        user_email = user_info["kakao_account"]["email"]
        user_age_range = user_info["kakao_account"]["age_range"]
        min_age = user_age_range.split("~")[0]

        result = {"code": 1, "email": user_email, "min_age": min_age}
        return result
