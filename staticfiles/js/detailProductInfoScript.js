const qnty = document.getElementById("qnty");
const btnBuy = document.getElementById("btnBuy");
const sellId = document.getElementById("sellId");
const sellForm = document.getElementById("sellForm");

qnty.addEventListener("change", priceCalc);
btnBuy.addEventListener("click", buyListLocation);
sellForm.addEventListener("submit", checkLogin);				
					
function priceCalc(){
	document.getElementById("purchasePrice").value 
		= document.getElementById("qnty").value * document.getElementById("sellPrice").value;
}


function buyListLocation(event){
	console.log("buylist");
	if (document.getElementById("userId").value == "None"){
		const doLogin = confirm("장바구니에 해당 상품을 추가하시려면 로그인 하셔야 합니다 \n 로그인 하시겠습니까?")
		console.log(doLogin);
		if (doLogin == false){
			event.preventDefault();
			return false;
		}

		else if(doLogin==true){
			event.preventDefault();
			window.open("../templogin", "_black", "width=500, height=700");
			return false;
		}
		
	}
	else{
		link = "../payment?sellid=" + sellId.value + "&qnty=" + document.getElementById("qnty").value;
		location.href = link;
	}
}

function checkLogin(event){
	console.log("checkLogin");
	if (document.getElementById("userId").value == "None"){
		const doLogin = confirm("장바구니에 해당 상품을 추가하시려면 로그인 하셔야 합니다 \n 로그인 하시겠습니까?")
		console.log(doLogin);
		if (doLogin == false){
			event.preventDefault();
			return false;
		}

		else if(doLogin==true){
			event.preventDefault();
			window.open("../templogin", "_black", "width=500, height=700");
			return false;
		}
		
	}
}
