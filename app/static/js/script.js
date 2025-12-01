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

document.addEventListener("click", function(event) {
    // --- Открытие модалки ---
    if (event.target.classList.contains("add-works-button")) {
        const taskFields = event.target.closest(".task-fields");
        const orderNameInput = taskFields.querySelector(".order-name");
        const orderNumberInput = taskFields.querySelector(".order-number");

        const orderName = orderNameInput.value.trim();
        const orderNumber = orderNumberInput.value.trim();

        orderNameInput.classList.remove("field-error");
        orderNumberInput.classList.remove("field-error");
        void orderNameInput.offsetWidth;
        void orderNumberInput.offsetWidth;

        let hasError = false;
        if (!orderName) {
            orderNameInput.classList.add("field-error");
            hasError = true;
        }
        if (!orderNumber) {
            orderNumberInput.classList.add("field-error");
            hasError = true;
        }
        if (hasError) {
            if (!orderName) orderNameInput.focus();
            else if (!orderNumber) orderNumberInput.focus();
            return;
        }

        fetch(`/orders/${orderNumber}/works`)
            .then(response => response.json())
            .then(data => {
                const modal = document.querySelector(".works-modal-container");
                const tbody = modal.querySelector("tbody");

                const modalTitle = modal.querySelector("#works-modal-title");
                modalTitle.textContent = `Заказ №${orderNumber}`; // Можно добавить и название: `${orderName} (№${orderNumber})`

                tbody.innerHTML = "";

                const hiddenContainer = document.querySelector("#hidden-work-hours-container");

                data.forEach(work => {
                    // ищем существующий скрытый input
                    const hiddenInputName = `work_hours[${orderNumber}][${work.work_name}]`;
                    let existingInput = hiddenContainer.querySelector(`input[name="${hiddenInputName}"]`);

                    // если нет — создаем
                    if (!existingInput) {
                        existingInput = document.createElement("input");
                        existingInput.type = "hidden";
                        existingInput.name = hiddenInputName;
                        hiddenContainer.appendChild(existingInput);
                    }

                    // берем значение из существующего инпута
                    const value = existingInput.value || "";

                    // создаем строку в модалке
                    const row = document.createElement("tr");
                    row.innerHTML = `
                        <td>${work.work_name}</td>
                        <td>${work.planned_hours}</td>
                        <td>${work.spent_hours}</td>
                        <td>${work.remaining_hours}</td>
                        <td>
                            <input
                                type="number"
                                name="work_hours[${orderNumber}][${work.work_name}]"
                                min="0"
                                step="0.01"
                                value="${value}"
                            />
                        </td>
                    `;

                    row.querySelector("input").addEventListener("input", event => {
                        existingInput.value = event.target.value;
                    });

                    tbody.appendChild(row);
                });

                modal.style.display = "block";
            });
    }

    if (event.target.classList.contains("close-works-modal") ||
        event.target.closest(".close-works-modal")) {
        document.querySelector(".works-modal-container").style.display = "none";
    }

    const modal = document.querySelector(".works-modal-container");
    if (modal && event.target === modal) {
        modal.style.display = "none";
    }
});

document.addEventListener("keydown", function(event) {
    if (event.key === "Escape") {
        const modal = document.querySelector(".works-modal-container");
        if (modal.style.display === "block") {
            modal.style.display = "none";
        }
    }
});


document.querySelector("#save-works").addEventListener("click", function() {
    document.querySelector(".works-modal-container").style.display = "none";
});
