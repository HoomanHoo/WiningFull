const btnLogin = document.getElementById("btnLogin");
const message = document.getElementById("message");
btnLogin.addEventListener("click", tempLogin)

function tempLogin () {
    const userId = document.getElementById("userId").value;
    const passwd = document.getElementById("passwd").value;
    
    const url = "templogin";
    const init = {
        method: "POST",
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            id: userId,
            passwd: passwd
        }),
    }




    fetch(url, init).then((response)=>response.json()).then((data)=>{
        console.log(data)
        const responseData = data["message"];
        // 1 = 로그인 성공
        // -1 = 탈퇴한 회원
        // -2 = 아이디 비밀번호가 다름
        
        if (responseData == 1){
            opener.location.reload();
            window.close();
        }
        else if(responseData == -1){
            message.innerText = "탈퇴한 회원 입니다"
        }
        else if(responseData == -2){
            message.innerText = "아이디나 비밀번호가 다릅니다"
        }
    })
    
}