
async function getUserData(){
    const response = await fetch('/api/users');
    return response.json();
}

function loadTable(users){
    const table = document.querySelector('#result');
    for(let user of users){
        table.innerHTML += `<tr>
            <td>${user.id}</td>
            <td>${user.username}</td>
        </tr>`;
    }
}

async function main(){
    const users = await getUserData();
    loadTable(users);
}

function openNav(){
    document.getElementById("sidepanel").style.width = "25vw";
}
  
function closeNav(){
    document.getElementById("sidepanel").style.width = "0";
}

/*function closeMessage(){
    document.getElementById("error_message").style.display = "none";
}*/

main();