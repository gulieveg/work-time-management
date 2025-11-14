import { updateOrderName, updateOrderNumber, configureInputField } from "./utils.js";


export function configureSuggestionInputs() {
    const selectorsMap = [
        [".employee-data", ".employee-data-suggestions", "/employees"],
        [".order-name", ".order-name-suggestions", "/orders/names"],
        [".order-number", ".order-number-suggestions", "/orders/numbers"],
    ];

    selectorsMap.forEach(([inputSelector, suggestionsListSelector, url]) => {
        const inputElements = document.querySelectorAll(inputSelector);
        const suggestionElements = document.querySelectorAll(suggestionsListSelector);

        const count = inputElements.length;

        for (let i = 0; i < count; i++) {
            configureInputField(inputElements[i], suggestionElements[i], url);
        }
    });
}


export function configureOrderSuggestionHandlers() {
    const orderNameInputs = document.querySelectorAll(".order-name");
    const orderNumberInputs = document.querySelectorAll(".order-number");

    const orderNameSuggestionsLists = document.querySelectorAll(".order-name-suggestions");
    const orderNumberSuggestionsLists = document.querySelectorAll(".order-number-suggestions");

    const count = orderNameInputs.length;

    for (let i = 0; i < count; i++) {
        const orderNameInput = orderNameInputs[i];
        const orderNumberInput = orderNumberInputs[i];

        const orderNameSuggestions = orderNameSuggestionsLists[i];
        const orderNumberSuggestions = orderNumberSuggestionsLists[i];

        orderNameSuggestions.addEventListener("click", function (event) {
            if (event.target.classList.contains("suggestion")) {
                orderNameInput.value = event.target.textContent;
                updateOrderNumber(event.target.textContent, orderNumberInput);
            }
        });

        orderNumberSuggestions.addEventListener("click", function (event) {
            if (event.target.classList.contains("suggestion")) {
                orderNumberInput.value = event.target.textContent;
                updateOrderName(event.target.textContent, orderNameInput);
            }
        });
    }
}
