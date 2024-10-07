let count = 0;

let number =  document.getElementById("number");  
function add(x) {
    count += x
    number.textContent = count
}

let saveEl = document.getElementById("save");

let parNumber = 0;
let result = []
function saveName() {
        let parNameInput = prompt("Enter Participant's name:")
        parNumber += 1
        let parName = parNameInput || "Participant " + parNumber
        result.push({parName: parName, count: count}) 
        saveEl.innerHTML += "<br />" + parName + ": " + count 
        count = 0
        number.innerHTML = 0
};

function end() {
    let sorted = result.sort((a, b) => b.count - a.count)
    saveEl.innerHTML = "Previous participants:"
    sorted.forEach((a) => saveEl.innerHTML += "<br />" + a.parName + ": " + a.count )
    count = 0
    number.innerHTML = 0
    parNumber = 0
    result = []
};