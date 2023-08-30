const btnCheck = document.getElementById("btnCheck");

btnCheck.addEventListener("click", () => {
    const url = "/store/drop-store";
    const passwd = document.getElementById("passwd").value;

    const init = {
        method: "POST",
        header: {
            "X-CSRFToken": getCookie("csrftoken"),
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            passwd: passwd,
        }),
    };

    fetch(url, init)
        .then((response) => response.json())
        .then((data) => {
            let responseData = data;

            if (responseData["code"] == -1) {
                alert(responseData["result"]);
                return false;
            }
            else if (responseData["code"] == 1) {
                alert(responseData["result"])
                location.href = "../../search/main";
            }
        });

});
function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));
    return matches ? decodeURIComponent(matches[1]) : undefined;
}

