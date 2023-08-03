import * as Vue from "https://unpkg.com/vue@3/dist/vue.esm-browser.js";
let pageNum = 0;
let oldList = [];

Vue.createApp({
  delimiters: ['[[', ']]'],
  setup() {

    let responseData = Vue.ref({ 'sell_id': '', 'sell_price': '', 'wine_name': '', 'store_name': '', 'store_address': '' });

    const fetchList = () => {
      let targetUrl = "stores/" + pageNum;

      fetch(targetUrl).then((response) => response.json()).then((data) => {
        const newData = JSON.parse(data);

        if (newData.length >= 30) {
          console.log(newData.length)
          for (var i = 0; i < newData.length; i++) {
            const rawStoreAddress = newData[i]["store_address"];
            newData[i]["store_address"] = rawStoreAddress.split("@").join(" ");
          }
          let newList = oldList.concat(newData);
          responseData.value = newList;
          oldList = newList;
        }

        else if (newData.length < 30) {
          for (var i = 0; i < newData.length; i++) {
            const rawStoreAddress = newData[i]["store_address"];
            newData[i]["store_address"] = rawStoreAddress.split("@").join(" ");
          }
          let newList = oldList.concat(newData);
          responseData.value = newList;
          oldList = newList;
          return false;
        }

        else if (oldList.length == 0) {
          return false;
        }
      })
    }

    const autoScroll = () => {
      let callback = (entries, observer) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            console.log("callback");
            next();
          }
        })
      }

      const options = {
        root: null,   //대상 객체의 가시성을 확인할 때 사용되는 뷰포트 요소, null은 뷰포트를 가리킨다
        rootMargin: "0px",  //root 가 가진 여백
        threshold: 1.0,  //대상 요소가 지정된 요소 내에서 (root 내에서) 50% 보여질 때 콜백이 호출됨을 의미
      };

      let observer = new IntersectionObserver(callback, options);

      let target = document.querySelector("#scrollArea");
      observer.observe(target);
    }

    const next = () => {
      pageNum++;
      console.log("next");
      console.log("page_num:" + pageNum);
      fetchList();
    }

    const move = function (event) {

      location.href = "../../sell/" + event[0]
    }

    Vue.onMounted(() => {
      console.log("mounted");
      autoScroll();

    })

    return { responseData, move }
  },
  //  mounted() {
  //   this.autoScroll();
  //   console.log("mounted");
  // }

}).mount("#newList");

