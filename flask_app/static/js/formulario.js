function displayTextboxOnCheck(element){
    if (element.checked) {
      document.getElementById(element.name).style.display = "block";
    } 
    else {
       document.getElementById(element.name).style.display = "none";
    }
}

function displayTextboxOnOtro(select, parent_id){
    if(select.value == "otro") {
        let otroInput = document.createElement("input");
        otroInput.id = "otro-input-" + parent_id;
        otroInput.type = "text";
        otroInput.maxLength = "15";
        otroInput.minLength = "3";
        document.getElementById(parent_id).appendChild(otroInput);
    }
    else {
        const otroInput = document.getElementById("otro-input-" + parent_id);
        if(otroInput != null) {
            document.getElementById(parent_id).removeChild(otroInput);
        }
    }
}

function updateComunas(region_select) {
    let regionId = region_select.value;
    let comunaSelect = document.getElementById('comuna-select');
    comunaSelect.innerHTML = '<option value="">--Elige una opción--</option>';
    if(regionId == "") {
        return;
    }

    fetch('/get_comunas/' + regionId)
        .then(response => response.json())
        .then(data => {
            data.forEach(comuna => {
                let option = document.createElement('option');
                option.value = comuna.id;
                option.textContent = comuna.nombre;
                comunaSelect.appendChild(option);
            });
        });
}

function resetSelect(select) {
    document.getElementById('region-select').selectedIndex = 0;
    select.selectedIndex = 0;
}