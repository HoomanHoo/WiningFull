let term = document.getElementById("term");
const listDiv = document.getElementById("revenueList");

term.addEventListener("change", () => {
    let termValue = term.value;
    fetch("/store/store-revenue-term?term=" + termValue)
        .then((response) => response.json())
        .then((data) => {
            const responseData = data["result"];
            let date = "";
            console.log(responseData);
            listDiv.replaceChildren();
            for (let i = 0; i < responseData.length; i++) {
                let values = new Map(Object.entries(responseData[i]));
                console.log(values);
                if (termValue == 0) {
                    date = values.get("date").substr(0, 10);
                }

                else if (termValue == 1) {
                    console.log(values.get("date"));
                    date = values.get("date").substr(0, 7) + "월";
                    console.log(date);
                }

                else if (termValue == 2) {
                    const quarter = values.get("date").substr(5, 2);
                    console.log(quarter);
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
                    date = values.get("date").substr(0, 4) + "년";

                }
                let valueSum = values.get("value_sum");
                let qntySum = values.get("qnty_sum");

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


                listDiv.appendChild(newRow);
                newRow.appendChild(newDate);
                newRow.appendChild(newValueSum);
                newRow.appendChild(newQntySum);
            }
        })

})