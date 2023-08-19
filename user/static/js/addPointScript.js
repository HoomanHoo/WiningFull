import * as Vue from "https://unpkg.com/vue@3/dist/vue.esm-browser.js";

const addPoint = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const decidedValues = Vue.ref(["1만", "5만", "10만", "50만"]);
        const pointAdd = Vue.ref("");
        const selectedAccount = Vue.ref("");
        const accountList = Vue.ref("");
        const userAccountId = Vue.ref("");
        const hover = Vue.ref({ "z-index": 3, "position": "absolute", "left": "0vw", "right": "0vw", "top": "0vh", "bottom": "0vh" });
        const unHover = Vue.ref({ "z-index": 1, "position": "relative" });
        const show = Vue.ref(false);
        const isPayment = Vue.ref(true);

        const clickDecidedValue = (event) => {
            const thisElement = event.target;
            const thisValue = thisElement.value;

            if (thisValue == "1만") {
                pointAdd.value = 10000;
            }
            else if (thisValue == "5만") {
                pointAdd.value = 50000;
            }
            else if (thisValue == "10만") {
                pointAdd.value = 100000;
            }
            else if (thisValue == "50만") {
                pointAdd.value = 500000;
            }
        }

        const selectAccount = (event) => {

            if (userAccountId.value != -1) {
                const url = "account/" + userAccountId.value;
                fetch(url).then((response) => response.json()).then((data) => {
                    const responseData = JSON.parse(data);
                    accountList.value = responseData;
                    show.value = true;
                })
            }

            else if (userAccountId.value == -1) {
                console.log(userAccountId.value);
                show.value = true;
            }
        }

        const invisible = () => {
            show.value = false;
        }

        const changeDefaultAccount = (event) => {
            const thisElement = event.target;
            const thisValue = thisElement.id;
            const url = "account/" + userAccountId.value;
            const init = {
                method: "PATCH",
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    "selectedAccount": thisValue
                })
            }
            fetch(url, init).then((response) => {
                if (response.ok) {
                    return response.json();

                }
                else {
                    alert("문제가 발생하였습니다\n 나중에 다시 시도해주세요");
                }
            }).then((data) => {
                const responseData = JSON.parse(data)
                selectedAccount.value = responseData["user_account"];
                userAccountId.value = responseData["user_account_id"];
                show.value = false;
            });
        }

        const addPaymentMethod = () => {
            location.href = "payment-method";
        }

        const back = () => {
            location.href = "myPage";
        }


        Vue.onMounted(() => {
            const url = "account"
            console.log("user/static");
            fetch(url).then((response) => response.json()).then((data) => {
                const responseData = JSON.parse(data);
                selectedAccount.value = responseData["user_account"];
                userAccountId.value = responseData["user_account_id"];
                if (userAccountId.value == -1) {
                    isPayment.value = false;
                }
            })
        })






        return {
            decidedValues,
            pointAdd,
            selectedAccount,
            hover,
            unHover,
            show,
            accountList,
            userAccountId,
            back,
            invisible,
            selectAccount,
            clickDecidedValue,
            changeDefaultAccount,
            addPaymentMethod
        }
    },


})
addPoint.mount("#rootDiv");

function getCookie(name) {
    let matches = document.cookie.match(new RegExp(
        "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
    ));

    return matches ? decodeURIComponent(matches[1]) : undefined;
}