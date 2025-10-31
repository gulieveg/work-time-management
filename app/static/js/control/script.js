import {
    configureSuggestionListBlurHandler,
    configureSuggestionListEscapeHandler,
    configureFilterResetHandler,
    configurePasswordSwitchHandler,
    configureUserStatusSwitchHandler,
    configureUserDeleteHandler,
    configurePasswordToggle,
    configureUserPrivilegesDropDownHandler
} from "./events.js";
import { configureSuggestionInputs, configureSuggestionHandlers } from "./suggestions.js"


function scheduleFlashMessageHide() {
    const message = document.getElementById("message");

    if (message) {
        setTimeout(() => message.classList.add("hide"), 8000);
    }
}


scheduleFlashMessageHide();

configureSuggestionListBlurHandler();
configureSuggestionListEscapeHandler();

configureFilterResetHandler();
configurePasswordSwitchHandler();
configureUserStatusSwitchHandler();

configureSuggestionInputs();
configureUserDeleteHandler();

configureSuggestionHandlers([
    {
        inputSelector: ".order-name",
        suggestionsSelector: ".order-name-suggestions",
        resourceType: "orders",
        urlPart: "name",
        updateTarget: {
            inputSelector: ".order-number",
            fieldName: "order_number",
            urlPart: "number"
        }
    },
    {
        inputSelector: ".order-number",
        suggestionsSelector: ".order-number-suggestions",
        resourceType: "orders",
        urlPart: "number",
        updateTarget: {
            inputSelector: ".order-name",
            fieldName: "order_name",
            urlPart: "name"
        }
    },
    {
        inputSelector: ".user-login",
        suggestionsSelector: ".user-login-suggestions",
        resourceType: "users",
        urlPart: "login",
        updateTarget: {
            inputSelector: ".user-name",
            fieldName: "user_name",
            urlPart: "name"
        }
    },
    {
        inputSelector: ".user-name",
        suggestionsSelector: ".user-name-suggestions",
        resourceType: "users",
        urlPart: "name",
        updateTarget: {
            inputSelector: ".user-login",
            fieldName: "user_login",
            urlPart: "login"
        }
    }
]);

configurePasswordToggle();
configureUserPrivilegesDropDownHandler();
