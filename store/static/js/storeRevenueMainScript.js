let term = document.getElementById("term");
const revenueList = document.getElementById("revenueList");
let pages = document.querySelectorAll("a[name=pages]");

for (var i = 0; i < pages.length; i++) {
    pages[i].addEventListener("click", paging);
}
term.addEventListener("change", paging)

function paging(e) {
    check = e.type
    let termValue = term.value;
    if (check == "click") {
        let page_num = this.id;
        url = "/store/revenue/pages/" + page_num + "/term/" + termValue
        console.log("click")
    }
    else {
        url = "/store/revenue/pages/" + 1 + "/term/" + termValue
        console.log("change")
    }

    fetch(url)
        .then((response) => response.json())
        .then((data) => {
            const resultData = JSON.parse(data)

            let pages = resultData["pages"]
            let revenues = resultData["datas"];
            let nextPage = resultData["next_page"];
            let prevPage = resultData["prev"];

            let date = "";
            revenueList.replaceChildren();
            for (let i = 0; i < revenues.length; i++) {
                let values = revenues[i].date;
                console.log(values);
                if (termValue == 0) {
                    date = values.substr(0, 10);
                }

                else if (termValue == 1) {
                    date = values.substr(0, 7) + "월";
                }

                else if (termValue == 2) {
                    const quarter = values.substr(5, 2);

                    if (quarter == "01") {
                        date = "1분기";
                    }
                    else if (quarter == "04") {
                        date = "2분기";
                    }
                    else if (quarter == "07") {
                        date = "3분기";
                    }
                    else if (quarter == "10") {
                        date = "4분기";
                    }
                }
                else if (termValue == 3) {
                    date = values.substr(0, 4) + "년";

                }
                let valueSum = revenues[i].value_sum;
                let qntySum = revenues[i].qnty_sum;

                const newRow = document.createElement("div");
                newRow.setAttribute("class", "row");

                const newDate = document.createElement("div");
                newDate.setAttribute("class", "col");
                newDate.innerText = date;

                const newValueSum = document.createElement("div");
                newValueSum.setAttribute("class", "col");
                newValueSum.innerText = valueSum + "원";

                const newQntySum = document.createElement("div");
                newQntySum.setAttribute("class", "col");
                newQntySum.innerText = qntySum + "개";


                revenueList.appendChild(newRow);
                newRow.appendChild(newDate);
                newRow.appendChild(newValueSum);
                newRow.appendChild(newQntySum);


            }
            let prev = document.getElementById("prev");
            let next = document.getElementById("next");
            if (prevPage < 1) {
                prev.className = "page-item disabled";
            }
            else {
                prev.className = "page-item";
                document.querySelector(".prev").setAttribute("id", pages[0] - 1);
            }
            if (pages.length < 5 || nextPage == 0) {
                next.className = "page-item disabled";
            }
            else {
                next.className = "page-item";
                document.querySelector(".next").setAttribute("id", pages[4] + 1);
            }
            let pageNumList = document.querySelectorAll(".page-num-list");
            for (var i = 0; i < pageNumList.length; i++) {
                pageNumList[i].remove();
            }
            for (var i = 0; i < pages.length; i++) {

                let newPages = document.createElement("li");
                newPages.setAttribute("class", "page-item page-num-list");
                let newPageNum = document.createElement("a");
                newPageNum.setAttribute("id", pages[i]);
                newPageNum.setAttribute("class", "page-link page-num");
                newPageNum.setAttribute("name", "pages");
                newPageNum.innerText = pages[i];

                newPages.appendChild(newPageNum);
                next.before(newPages);
                newPageNum.addEventListener("click", paging);
            }
        })

}