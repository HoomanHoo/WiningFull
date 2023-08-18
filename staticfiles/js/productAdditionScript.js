
const wineNames = document.querySelectorAll(".wineName");
const productAdd = document.getElementById("productAdd");
const srhByName = document.getElementById("srhByName");
const wineList = document.getElementById("wineList");
const btnDeletes = document.querySelectorAll("input[name=btnDelete]")
let pages = document.querySelectorAll("a[name=pages]");

for (var i = 0; i < pages.length; i++) {
	pages[i].addEventListener("click", paging);
}

function paging() {
	let modify = document.getElementById("modify");
	let url = "../product/pages/" + this.id;

	if (document.getElementById("srhByName").value){
		const srhKeyWord = document.getElementById("srhByName").value;
		url = "../product/pages/" + this.id + "?srhkeyword=" + srhKeyWord
	}

	fetch(url).then((response) => response.json()).then((data) => {
		let resultData = JSON.parse(data);

		let pages = resultData["pages"];
		let wines = resultData["wines"];
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

function deleteRow() {
	const row = this.parentNode;
	row.replaceChildren();
}

function deleteDefaultRow() {
	const row = this.parentNode;
	wineId = row.querySelector("input[name=wineId]").value
	url = "/store/discontinue-product?wineid=" + wineId
	fetch(url).then((response) => response.json()).then((data) => alert(data["result"]))

	row.replaceChildren();
}

function searchByName() {
	const srhKeyWord = this.value;
	const url = "../product/pages/1?srhkeyword=" + srhKeyWord
	const xhttp = new XMLHttpRequest();

	xhttp.onreadystatechange = () => {
		if (xhttp.readyState === XMLHttpRequest.DONE) {
			if (xhttp.status === 200) {
				const result = xhttp.response;
				let resultData = JSON.parse(result);

				let pages = resultData["pages"];
				let wines = resultData["wines"];
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

			}
			else if (xhttp.status === 500) {
				console.log("서버에 문제가 발생했습니다. 잠시 뒤 다시 시도해주세요");
			}
			else {
				alert("문제가 발생했습니다 잠시 뒤 다시 시도해주세요");
			}
		}

	};

	xhttp.open("GET", url);
	xhttp.responseType = "json";
	xhttp.send();
}

function checkValue(){
	prices = document.querySelectorAll("input[name=sellPrice]");
	promots = document.querySelectorAll("input[name=sellPromot]");

	for (var i = 0; i < prices.length; i++){
		if(! prices[i].value){
			alert("판매하고자 하는 상품의 가격을 입력해주세요");
			return false;
		}
		else if(! promots[i].value){
			alert("상품 설명을 입력해주세요");
			return false;
		}
	}
}

function addElement() {
	const tid = this.id;
	const tid1 = tid + 1;
	const tid2 = tid + 2;
	const tid3 = tid + 3;
	const tid4 = tid + 4;
	const tid5 = tid + 5;
	const tid6 = tid + 6;

	if (document.getElementById(tid4)) {
		alert("이미 추가된 상품입니다")
	}
	else {
		const wineId = document.getElementById(tid1);
		const wineCapacity = document.getElementById(tid2);
		const wineAlc = document.getElementById(tid3);

		const newRow = document.createElement("div");
		newRow.setAttribute("id", tid4);
		newRow.setAttribute("class", "row");

		const newCol = document.createElement("div");
		newCol.setAttribute("id", tid5);
		newCol.setAttribute("class", "col");

		const newPdtId = document.createElement("input");
		newPdtId.setAttribute("type", "hidden");
		newPdtId.setAttribute("name", "wineId");
		newPdtId.setAttribute("value", wineId.value);
		newPdtId.setAttribute("readonly", "true")

		const newPdtName = document.createElement("input");
		newPdtName.setAttribute("type", "text");
		newPdtName.setAttribute("class", "col");
		newPdtName.setAttribute("name", "wineName");
		newPdtName.setAttribute("value", tid);
		newPdtName.setAttribute("readonly", "true")

		const newPdtCpcity = document.createElement("input");
		newPdtCpcity.setAttribute("type", "text");
		newPdtCpcity.setAttribute("class", "col-1");
		newPdtCpcity.setAttribute("name", "wineCapacity");
		newPdtCpcity.setAttribute("value", wineCapacity.value);
		newPdtCpcity.setAttribute("readonly", "true");

		const newPdtAlc = document.createElement("input");
		newPdtAlc.setAttribute("type", "text");
		newPdtAlc.setAttribute("class", "col-1");
		newPdtAlc.setAttribute("name", "wineAlc");
		newPdtAlc.setAttribute("value", wineAlc.value);
		newPdtAlc.setAttribute("readonly", "true");

		const newPdtPrice = document.createElement("input");
		newPdtPrice.setAttribute("type", "number");
		newPdtPrice.setAttribute("class", "col-1");
		newPdtPrice.setAttribute("name", "sellPrice");
		newPdtPrice.setAttribute("maxlength", "5")

		const newPdtPromot = document.createElement("input");
		newPdtPromot.setAttribute("type", "text");
		newPdtPromot.setAttribute("class", "col");
		newPdtPromot.setAttribute("name", "sellPromot");


		const newDelBtn = document.createElement("input");
		newDelBtn.setAttribute("type", "button");
		newDelBtn.setAttribute("id", tid6)
		newDelBtn.setAttribute("class", "col-1");
		newDelBtn.setAttribute("value", "삭제");

		productAdd.appendChild(newRow);
		document.getElementById(tid4).appendChild(newPdtId);
		document.getElementById(tid4).appendChild(newPdtName);
		document.getElementById(tid4).appendChild(newPdtCpcity);
		document.getElementById(tid4).appendChild(newPdtAlc);
		document.getElementById(tid4).appendChild(newPdtPrice);
		document.getElementById(tid4).appendChild(newPdtPromot);
		document.getElementById(tid4).appendChild(newDelBtn);

		document.getElementById(tid6).addEventListener("click", deleteRow);
	}
}

for (var i = 0; i < btnDeletes.length; i++) {
	btnDeletes[i].addEventListener("click", deleteDefaultRow)
}

for (var i = 0; i < wineNames.length; i++) {
	wineNames[i].addEventListener("click", addElement);
}


srhByName.addEventListener("keyup", searchByName)

