
import * as Vue from 'https://unpkg.com/vue@3/dist/vue.esm-browser.js';
let pageNum = 1;
let oldList = [];

Vue.createApp({
  delimiters: ['[[', ']]'],
  setup(){
    
    let responseData = Vue.ref({'sell_id': 55, 'sell_price': 32000, 'wine_name': '와인 55', 'store_name': '더미', 'store_address': '더어어어미이이이 '});

    const fetchList = () => {
      let targetUrl = "stores/" + pageNum;

      fetch(targetUrl).then((response) => response.json()).then((data) => {
        if (pageNum == 2){
          if(oldList.length > 1){
            oldList  = JSON.parse(data);
            setTimeout(() => {
              responseData.value = oldList;
            }, 1000);     //setTimeout 함수 수치 조절해서 적당히 보이도록 해주기
          }
          else if(oldList.length == 1){
            return false;
          }
        }
        else if(pageNum > 2){

          let newList = oldList.concat(JSON.parse(data));
          console.log(newList)
          setTimeout(() => {
            responseData.value = newList;
          }, 1000);
          
          oldList = newList;
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

    const next = ()=>{
      pageNum ++;
      console.log("next");
      console.log("page_num:" + pageNum);
      fetchList();
    }

    const move = function (event) {
      console.log(event);
      console.log(event[0]);
      location.href = "../../sell/" + event[0]
    }

    Vue.onMounted(()=> {
      autoScroll();
      console.log("mounted");
    })

    return {responseData, move}
  },
  //  mounted() {
  //   this.autoScroll();
  //   console.log("mounted");
  // }

}).mount("#newList");

 