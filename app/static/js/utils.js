export function processInput(inputElement, suggestionsList, url) {
    inputElement.addEventListener("input", function () {
        const query = inputElement.value;

        if (query.length >= 2) {
            fetch(`${url}?query=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsList.innerHTML = "";
                    if (data.length > 0) {
                        suggestionsList.style.display = "block";
                        data.forEach(item => {
                            const suggestion = document.createElement("div");
                            suggestion.classList.add("suggestion");
                            suggestion.textContent = item;
                            suggestionsList.appendChild(suggestion);
                        });
                    } else {
                        suggestionsList.style.display = "none";
                    }
                })
                .catch(error => console.error("Failed to retrieve data:", error));
        } else {
            suggestionsList.style.display = "none";
        }
    });
}


export function processSelection(inputElement, suggestionsList) {
    suggestionsList.addEventListener("click", function (event) {
        if (event.target.classList.contains("suggestion")) {
            inputElement.value = event.target.textContent;
            suggestionsList.style.display = "none";
        }
    });
}


export function configureInputField(inputElement, suggestionsList, url) {
    if (inputElement && suggestionsList) {
        processInput(inputElement, suggestionsList, url);
        processSelection(inputElement, suggestionsList);
    }
}


export function updateOrderName(orderNumber, orderNameInput) {
    fetch(`/orders/${encodeURIComponent(orderNumber)}/name`)
    .then(response => response.json())
    .then(data => {
        if (data.order_name) {
            orderNameInput.value = data.order_name;
        }
    });
}


export function updateOrderNumber(orderName, orderNumberInput) {
    fetch(`/orders/${encodeURIComponent(orderName)}/number`)
    .then(response => response.json())
    .then(data => {
        if (data.order_number) {
            orderNumberInput.value = data.order_number;
        }
    });
}
