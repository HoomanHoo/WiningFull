let pages = document.querySelectorAll("a[name=pages]");

for (var i = 0; i < pages.length; i++) {
	pages[i].addEventListener("click", paging);
}

function paging() {
	let reviewList = document.getElementById("reviewList");
	let url = "./reviews/" + this.id;

	fetch(url).then((response) => response.json()).then((data) => {

		const resultData = JSON.parse(data);
		let pages = resultData["pages"]
		let reviews = resultData["datas"];
		let nextPage = resultData["next_page"];
		let prevPage = resultData["prev"];

		reviewList.replaceChildren();
		for (var i = 0; i < reviews.length; i++) {
			let userId = reviews[i].user_id;
			let reviewContent = reviews[i].review_content;
			let reviewScore = reviews[i].review_score;
			let regDate = reviews[i].reg_date;

			let newRow = document.createElement("div");
			newRow.setAttribute("class", "row");

			let newUserCol = document.createElement("div")
			newUserCol.setAttribute("class", "col");
			let newReviewContentCol = document.createElement("div")
			newReviewContentCol.setAttribute("class", "col");
			let newReviewScoreCol = document.createElement("div")
			newReviewScoreCol.setAttribute("class", "col");
			let newRegDateCol = document.createElement("div")
			newRegDateCol.setAttribute("class", "col");

			reviewList.appendChild(newRow);
			newRow.appendChild(newUserCol);
			newUserCol.innerText = userId;
			newRow.appendChild(newReviewContentCol);
			newReviewContentCol.innerText = reviewContent;
			newRow.appendChild(newReviewScoreCol);
			newReviewScoreCol.innerText = reviewScore;
			newRow.appendChild(newRegDateCol);
			newRegDateCol.innerText = regDate;
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