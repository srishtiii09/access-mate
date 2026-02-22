async function simplifyText(){

    let url = document.getElementById("urlInput").value;

    if(!url){
        alert("Please paste website link");
        return;
    }

    try{

        document.getElementById("output").innerText =
        "Processing... Please wait";

        let response = await fetch("/simplify", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body: JSON.stringify({url:url})
        });

        let data = await response.json();

        document.getElementById("output").innerText =
            data.simplified;

    }catch(error){
        alert("Error occurred");
    }
}
function toggleContrast(){
    document.body.classList.toggle("highContrast");
}