import * as Vue from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';

const search = Vue.createApp({
    delimiters: ['[[', ']]'],
    setup() {
        const result = Vue.ref({ "name": "" });
        const show = Vue.ref(false);
        const hover = Vue.ref({ "z-index": 2 });
        const unhover = Vue.ref({ "z-index": 1 });
        let selectedValue = Vue.ref("");

        const searchRelateKeyword = (event) => {
            console.log("keyup");
            const searchInput = document.getElementById("searchInput");
            const keyword = searchInput.value;
            const nameLanguage = document.getElementById("nameLanguage");
            const selectValue = nameLanguage.options[nameLanguage.selectedIndex].value;
            const url = "relatekeyword?searchword=" + keyword + "&namelanguage=" + selectValue;
            const thisElement = event.target;
            inputValue(keyword);

            if (keyword.length == 0) {
                show.value = false;

            }
            else {
                fetch(url).then((response) => response.json()).then((data) => {
                    const responseData = JSON.parse(data);
                    clearTimeout(thisElement.debounce);
                    thisElement.debounce = setTimeout(() => {
                        result.value = responseData;
                        show.value = true;
                    }, 500);


                })
            }
        }

        const clickWineName = (event) => {
            const clickElement = event.target;
            const clickValue = clickElement.value;
            inputValue(clickValue);
            show.value = false;
        }

        const inputValue = (data) => {
            selectedValue.value = data;
        }


        return { result, show, hover, unhover, selectedValue, searchRelateKeyword, clickWineName }
    }
})
search.mount("#rootDiv")