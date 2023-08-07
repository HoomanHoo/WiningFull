import * as Vue from "https://unpkg.com/vue@3/dist/vue.esm-browser.js";

const addPoint = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const decidedValues = Vue.ref(["1만", "5만", "10만", "50만"]);
        const pointAdd = Vue.ref("");
        const selectedAccount = Vue.ref("");
        const accountList = Vue.ref("");
        const hover = Vue.ref({ "z-index": 2, "position": "absolute", "left": "0px", "top": "0px" });
        const unHover = Vue.ref({ "z-index": 1, "position": "relative" });
        const show = Vue.ref(false);

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

            const url = "updatedefaultaccount"
            fetch(url).then((response) => response.json()).then((data) => {
                const responseData = JSON.parse(data);
                accountList.value = responseData;
                show.value = true;
            })
        }

        const invisible = () => {
            show.value = false;
        }

        const changeDefaultAccount = () => {

        }

        Vue.onMounted(() => {
            const url = "account"
            fetch(url).then((response) => response.json()).then((data) => {
                const responseData = JSON.parse(data);
                selectedAccount.value = responseData["user_account"];
            })
        })






        return { decidedValues, pointAdd, selectedAccount, hover, unHover, show, accountList, invisible, selectAccount, clickDecidedValue }
    },


})
addPoint.mount("#rootDiv");