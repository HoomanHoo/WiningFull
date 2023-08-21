let pages = document.querySelectorAll("a[name=pages]");

for (var i = 0; i < pages.length; i++) {
	pages[i].addEventListener("click", paging);
}

function paging() {

	let url = "./" + this.id;

	fetch(url).then((response) => response.json()).then((data) => {
		let resultData = JSON.parse(data);

		let pages = resultData["pages"];
		let wines = resultData["reviews"];
		console.log(pages);
		wineList.replaceChildren();
		for (var i = 0; i < wines.length; i++) {
			let wineId = wines[i].wine_id;
			let wineName = wines[i].wine_name;
			let wineCapacity = wines[i].wine_capacity;
			let wineAlc = wines[i].wine_alc;

			let newRow = document.createElement("div");
			newRow.setAttribute("class", "row");
			let newWineInfo = document.createElement("div");
			newWineInfo.setAttribute("id", wineName);
			newWineInfo.setAttribute("class", "col wineName");
			let newWineId = document.createElement("input");
			newWineId.setAttribute("type", "hidden");
			newWineId.setAttribute("id", wineName + 1);
			newWineId.setAttribute("value", wineId);
			let newWineCapacity = document.createElement("input");
			newWineCapacity.setAttribute("type", "hidden");
			newWineCapacity.setAttribute("id", wineName + 2);
			newWineCapacity.setAttribute("value", wineCapacity);
			let newWineAlc = document.createElement("input");
			newWineAlc.setAttribute("type", "hidden");
			newWineAlc.setAttribute("id", wineName + 3);
			newWineAlc.setAttribute("value", wineAlc);

			wineList.appendChild(newRow);
			newRow.appendChild(newWineInfo);
			newWineInfo.innerText = wineName;
			newWineInfo.appendChild(newWineId);
			newWineInfo.appendChild(newWineCapacity);
			newWineInfo.appendChild(newWineAlc);

			const wineNames = document.querySelectorAll(".wineName");
			for (let i = 0; i < wineNames.length; i++) {
				wineNames[i].addEventListener("click", addElement);
			}
		}
		let prev = document.getElementById("prev");
		let next = document.getElementById("next");
		if (pages[0] < 6) {
			prev.className = "page-item disabled";
		}
		else {
			prev.className = "page-item";
			document.querySelector(".prev").setAttribute("id", pages[0] - 1);
		}
		if (pages.length < 5) {
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