import * as Vue from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';

let selector = Vue.createApp({
    delimiters: ['[[', ']]'],

    setup() {

        const selected = Vue.ref(1)
        const criteriaList = Vue.ref([{ criteria: "최신순", sortValue: 1 }, { criteria: "높은 별점 순", sortValue: 2 }, { criteria: "낮은 별점 순", sortValue: 3 }])
        const reviewDatas = Vue.ref({})

        const changeCriteria = () => {
            const url = window.location.pathname + "/reviews?selectcode=" + selected.value
           
            fetch(url).then((response) => response.json()).then((data) => {

                reviewDatas.value = JSON.parse(data)

            })
        }
        Vue.onMounted(() => {
            const url = window.location.pathname + "/reviews?selectcode=" + selected.value
       
            fetch(url).then((response) => response.json()).then((data) => {
                reviewDatas.value = JSON.parse(data)

            })
        })
        return {
            selected, criteriaList, changeCriteria, reviewDatas
        }
    }
})

selector.mount("#selector");
