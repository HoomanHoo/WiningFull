from django.db.models.query import QuerySet


def pagenation(
    show_length: int,
    page_num: int,
    end_page: int,
    start_page: int,
    datas: dict,
) -> dict:
    """
    show_length = 한 페이지당 보여주고 싶은 row 수
    page_num = 페이지 번호
    end_page = show_length * page_num
    start_page = end_page - show_length
    datas = datas[0] - db에서 가져온 row 수
            datas[1] - db에서 가져온 data

    -> pages_count = 페이지 번호 리스트
       db_data = db에서 가져온 data
    """
    list_length = datas[0]
    db_data = datas[1]
    if list_length == 0:
        state = -1
        pages_count = [0]

        result = {"pages_count": pages_count, "db_data": db_data, "state": state}
    else:
        if (list_length % show_length) == 0:
            page_length = list_length // show_length
            print(page_length)
            print("1")
        else:
            page_length = (list_length // show_length) + 1
            print(page_length)
            print("2")

        if 0 < page_num and page_num < 6:
            start_page = 1
            print("3")
        elif page_num % 5 == 0:
            start_page = page_num - 4
            print("4")
        else:
            start_page = page_num - (page_num % 5) + 1
            print("5")

        if page_length - page_num < 5 and page_length - start_page < 5:
            end_page = page_length + 1
            next_page = 0
            print(end_page)
            print("6")
        else:
            end_page = start_page + 5
            next_page = end_page
            print("7")
        pages_count = [i for i in range(start_page, end_page)]
        prev = start_page - 1
        state = 1

        result = {
            "pages_count": pages_count,
            "db_data": db_data,
            "state": state,
            "prev": prev,
            "next_page": next_page,
        }

    return result


def db_preprocessing(
    db_data: QuerySet,
    end_page: int,
    start_page: int,
) -> list:
    list_info = []
    list_length = db_data.count()
    list_info.append(list_length)
    if list_length > 1:
        list_info.append(db_data[start_page:end_page])

    # elif list_length == 1:
    #     list_info.append(db_data)

    else:
        list_info.append(db_data)

    return list_info
