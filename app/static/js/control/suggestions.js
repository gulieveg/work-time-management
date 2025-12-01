import { configureInputField, updateField } from "./utils.js";


export function configureSuggestionInputs() {
    const fields = [];

    const selectorsMap = [
        [".order-name", ".order-name-suggestions", "/control/orders/names"],
        [".order-number", ".order-number-suggestions", "/control/orders/numbers"],
        [".user-name", ".user-name-suggestions", "/control/users/names"],
        [".user-login", ".user-login-suggestions", "/control/users/logins"],
        [".employee-name", ".employee-name-suggestions", "/control/employees/names"],
        [".personnel-number", ".personnel-number-suggestions", "/control/employees/numbers"],
        [".work-name", ".work-name-suggestions", "/control/works/names"],
    ];

    selectorsMap.forEach(([inputSelector, suggestionsListSelector, url]) => {
        if (document.querySelector(inputSelector) && document.querySelector(suggestionsListSelector)) {
            fields.push([inputSelector, suggestionsListSelector, url]);
        }
    });

    fields.forEach(([inputSelector, suggestionsListSelector, url]) => {
        configureInputField(inputSelector, suggestionsListSelector, url);
    });
}


export function configureSuggestionHandlers(configs) {
    configs.forEach(cfg => {
        const input = document.querySelector(cfg.inputSelector);
        const suggestions = document.querySelector(cfg.suggestionsSelector);
        const updateTargetInput = cfg.updateTarget ? document.querySelector(cfg.updateTarget.inputSelector) : null;

        if (input && suggestions) {
            suggestions.addEventListener("click", event => {
                if (event.target.classList.contains("suggestion")) {
                    const selectedValue = event.target.textContent;

                    if (updateTargetInput) {
                        updateField(
                            cfg.resourceType,
                            selectedValue,
                            updateTargetInput,
                            cfg.updateTarget.fieldName,
                            cfg.updateTarget.urlPart
                        );
                    }
                }
            });
        }
    });
}
