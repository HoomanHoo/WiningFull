
import * as Vue from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
let pageNum = 1;

let callback = (entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {

      pageNum++;

      let targetUrl = "stores/" + pageNum;

      fetch(targetUrl).then((response) => response.json()).then((data) => {
        const responseData = JSON.parse(data);
        console.log(responseData);

        let test = Vue.createApp({
          delimiters: ['[[', ']]'],
          data() {
            return { "datas": responseData }
          },
          methods: {
            print() { console.log(pageNum); }
          },
        })
        test.mount("#newList");


      })

    }
  }
  )
}

const options = {
  root: null,   //대상 객체의 가시성을 확인할 때 사용되는 뷰포트 요소, null은 뷰포트를 가리킨다
  rootMargin: "0px",  //root 가 가진 여백
  thredhold: 1.0,  //대상 요소가 지정된 요소 내에서 (root 내에서) 100% 보여질 때 콜백이 호출됨을 의미
};

let observer = new IntersectionObserver(callback, options);


let target = document.querySelector("#scrollArea");
observer.observe(target);



