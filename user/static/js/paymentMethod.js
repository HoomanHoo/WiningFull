import * as Vue from "https://unpkg.com/vue@3/dist/vue.esm-browser.js";

const background = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const userAccount1 = Vue.ref("");
        const userAccount2 = Vue.ref("");
        const userAccount3 = Vue.ref("");
        const userAccountId = Vue.ref("");
        const newPaymentMethod = Vue.ref("");
        const bankList = Vue.ref([{ "name": "KEB하나", "key": 1 }, { "name": "SC제일", "key": 2 }, { "name": "KB국민", "key": 3 }, { "name": "신한", "key": 4 }, { "name": "외환", "key": 5 }, { "name": "우리", "key": 6 }, { "name": "한국시티", "key": 7 }, { "name": "경남", "key": 8 }, { "name": "광주", "key": 9 }, { "name": "대구", "key": 10 }, { "name": "부산", "key": 11 }, { "name": "전북", "key": 12 }, { "name": "제주", "key": 13 }, { "name": "기업", "key": 14 }, { "name": "농협", "key": 15 }, { "name": "수협", "key": 16 }, { "name": "한국산업", "key": 17 }, { "name": "한국수출입", "key": 18 }]);
        const hover = Vue.ref({ "z-index": 3, "position": "absolute", "left": "0vw", "right": "0vw", "top": "0vh", "bottom": "0vh" });
        const unHover = Vue.ref({ "z-index": 1, "position": "relative" });
        const listShow = Vue.ref(true);
        const addShow = Vue.ref(false);

        const registPaymentMethod = () => {
            console.log("werwer")
            listShow.value = false;
            addShow.value = true;
        }

        const unvisible = () => {
            newPaymentMethod.value = "";
            listShow.value = true;
            show.value = false;
        }

        const back = () => {
            location.href = "addPoint";
        }

        const sendNewMethod = () => {

            let addNumber = 1;
            let initial = 0;
            if (userAccountId.value == -1) {
                addNumber = 1;
                initial = 1;
            }
            else {
                if (userAccount1.value == "") {
                    addNumber = 1;
                    initial = userAccountId.value;
                }
                else if (userAccount2.value == "") {
                    addNumber = 2;
                    initial = userAccountId.value;
                }
                else if (userAccount3.value == "") {
                    addNumber = 3;
                    initial = userAccountId.value;
                }
            }

            const url = "payment-method-api"
            const init = {
                method: "POST",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "newPaymentMethod": newPaymentMethod.value,
                    "addNumber": addNumber,
                    "isInitial": initial
                })
            }

            fetch(url, init).then((response) => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    alert("문제가 발생하였습니다\n 나중에 다시 시도해주세요")
                    return false;
                }
            }).then((data) => {
                const responseData = JSON.parse(data);
                userAccount1.value = responseData["user_account1"];
                userAccount2.value = responseData["user_account2"];
                userAccount3.value = responseData["user_account3"];
                userAccountId.value = responseData["user_account_id"];
            })
            listShow.value = true;
            addShow.value = false;

        }

        const deleteAccount = (event) => {
            const thisElement = event.target;
            const deleteTarget = thisElement.parentNode.querySelector("input[name=userAccount]");
            const deleteTargetId = deleteTarget.id;
            const url = "payment-method-api";
            const init = {
                method: "DELETE",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "deleteColumn": deleteTargetId,
                    "userAccountId": userAccountId.value
                })
            }
            fetch(url, init).then((response) => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    alert("문제가 발생하였습니다\n 나중에 다시 시도해주세요");
                    fetch(url).then((response) => response.json()).then((data) => {
                        const responseData = JSON.parse(data);
                        userAccount1.value = responseData["user_account1"];
                        userAccount2.value = responseData["user_account2"];
                        userAccount3.value = responseData["user_account3"];
                        userAccountId.value = responseData["user_account_id"];
                        alert("삭제가 완료 되었습니다");
                        console.log(userAccountId.value);
                    })
                    return false;
                }
            }).then((data) => {
                const responseData = JSON.parse(data);
                userAccount1.value = responseData["user_account1"];
                userAccount2.value = responseData["user_account2"];
                userAccount3.value = responseData["user_account3"];
                userAccountId.value = responseData["user_account_id"];
            })
        }

        const addPaymentMethod = (event) => {
            const thisElement = event.target;
            const thisValue = thisElement.value;

            newPaymentMethod.value = thisValue + " - ";
        }


        Vue.onMounted(() => {
            const url = "payment-method-api"

            fetch(url).then((response) => response.json()).then((data) => {
                const responseData = JSON.parse(data);
                userAccount1.value = responseData["user_account1"];
                userAccount2.value = responseData["user_account2"];
                userAccount3.value = responseData["user_account3"];
                userAccountId.value = responseData["user_account_id"];

                console.log(userAccountId.value);
            })
        })

        return {
            userAccountId,
            userAccount1,
            userAccount2,
            userAccount3,
            newPaymentMethod,
            bankList,
            hover,
            unHover,
            listShow,
            addShow,
            back,
            deleteAccount,
            addPaymentMethod,
            registPaymentMethod,
            sendNewMethod,
            unvisible
        }
    }
})
background.mount("#rootDiv");

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));

    return matches ? decodeURIComponent(matches[1]) : undefined;
}