const search = document.getElementById("btnSearch");

search.addEventListener("click", () => {
    let code = document.getElementById("searchReceiveCode").value;
    if (code == ""){
        alert("please input receive code");
    }
    else{
        let url = "../receive-code/codes/" + code;
        fetch(url).then((response) => response.json()).then((data) => {
            console.log(data);
            let result = JSON.parse(data);
            console.log(result);
            let receiveCheck = document.getElementById("btnReceive");
            let id = result.purchase_detail_id;
            let qnty = result.purchase_det_number;
            let price = result.purchase_det_price;
            let storeName = result.store_name;
            let userName = result.user_name;
            let wineName = result.wine_name;
            console.log(wineName);

            if (id == -1) {
                alert("유효하지 않은 수령 코드입니다\n 다시 확인해주세요");
                receiveCheck.disabled = true;
                return false;
            }
            else {
                const infoPosition = document.getElementById("codeInfo");
                infoPosition.replaceChildren();

                let newNameCol = document.createElement("div");
                newNameCol.setAttribute("class", "col");
                let newStoreCol = document.createElement("div");
                newStoreCol.setAttribute("class", "col");
                let newWineCol = document.createElement("div");
                newWineCol.setAttribute("class", "col");
                let newQntyCol = document.createElement("div");
                newQntyCol.setAttribute("class", "col");
                let newPriceCol = document.createElement("div");
                newPriceCol.setAttribute("class", "col");
                let newPurchaseDetailId = document.createElement("input");
                newPurchaseDetailId.setAttribute("type", "hidden");
                newPurchaseDetailId.setAttribute("name", "purchaseDetailId");
                newPurchaseDetailId.setAttribute("value", id);
                let newName = document.createElement("input");
                newName.setAttribute("type", "input");
                newName.setAttribute("value", userName);
                newName.setAttribute("readonly", "True");
                let newStore = document.createElement("input");
                newStore.setAttribute("type", "input");
                newStore.setAttribute("value", storeName);
                newStore.setAttribute("readonly", "True");
                let newWine = document.createElement("input");
                newWine.setAttribute("type", "input");
                newWine.setAttribute("value", wineName);
                newWine.setAttribute("readonly", "True");
                let newQnty = document.createElement("input");
                newQnty.setAttribute("type", "input");
                newQnty.setAttribute("value", qnty + "개");
                newQnty.setAttribute("readonly", "True");
                let newPrice = document.createElement("input");
                newPrice.setAttribute("type", "input");
                newPrice.setAttribute("value", price + "원");
                newPrice.setAttribute("readonly", "True");


                newNameCol.appendChild(newName);
                newNameCol.appendChild(newStore);
                newNameCol.appendChild(newWine);
                newNameCol.appendChild(newQnty);
                newNameCol.appendChild(newPrice);


                infoPosition.appendChild(newNameCol);
                const idForm = document.getElementById("idForm");
                idForm.appendChild(newPurchaseDetailId);

                receiveCheck.disabled = false;
            }
        

        })
    }
})

