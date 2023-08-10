import * as Vue from "https://unpkg.com/vue@3/dist/vue.esm-browser.js";

const background = Vue.createApp({
    setup() {
        const userAccount1 = Vue.ref("");
        const userAccount2 = Vue.ref("");
        const userAccount3 = Vue.ref("");
        const userAccountId = Vue.ref("");
        const newPaymentMethod = Vue.ref("");

        const addPaymentMethod = () => {
            console.log(userAccount1.value);
            console.log(userAccount2.value);
            console.log(userAccount3.value);

            let addNumber = 1;
            if (userAccount1.value == "") {
                addNumber = 1;
            }
            else if (userAccount2.value == "") {
                addNumber = 2;
            }
            else if (userAccount3.value == "") {
                addNumber = 3;
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
                    "addNumber": addNumber
                })
            }
            console.log(newPaymentMethod.value);
            console.log(addNumber);
            fetch(url, init).then((response) => {
                if (response.ok) {
                    return response.json();
                }
                else {
                    alert("������ �߻��Ͽ����ϴ�\n ���߿� �ٽ� �õ����ּ���")
                }
            }).then((data) => {
                const responseData = JSON.parse(data);
                userAccount1.value = responseData["user_account1"];
                userAccount2.value = responseData["user_account2"];
                userAccount3.value = responseData["user_account3"];
                userAccountId.value = responseData["user_account_id"];
            })

        }



        Vue.onMounted(() => {
            const url = "payment-method-api"
            console.log(url);
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
            addPaymentMethod
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