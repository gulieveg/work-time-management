import {
    configureSuggestionListBlurHandler,
    configureSuggestionListEscapeHandler,
    configureFilterResetHandler,
    configurePasswordToggle,
    configureScrollToTopButton,
    configureHoursSelection,
    configureDropdownCheckboxListener
} from "./events.js";
import { configureTaskCreateHandler, configureTaskDeleteHandler } from "./tasks.js";
import { configureSuggestionInputs, configureOrderSuggestionHandlers } from "./suggestions.js";


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

configurePasswordToggle();
configureScrollToTopButton();
configureHoursSelection();

configureTaskCreateHandler();
configureTaskDeleteHandler();

configureSuggestionInputs();
configureOrderSuggestionHandlers();

configureDropdownCheckboxListener("dropdown-list", "dropdown-selected-text");
