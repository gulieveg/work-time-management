import { processInput, processSelection, updateOrderName, updateOrderNumber } from "./utils.js";


export function configureTaskCreateHandler() {
    const addTaskButton = document.getElementById("add-form-task-button");
    const tasksContainer = document.getElementById("tasks-container");

    if (!addTaskButton || !tasksContainer) return;

    addTaskButton.addEventListener("click", () => {
        const taskNumber = tasksContainer.querySelectorAll(".task-fields").length + 1;

        const taskFields = document.createElement("div");
        taskFields.classList.add("task-fields");

        const taskNumberElement = document.createElement("p");
        taskNumberElement.classList.add("task-number");
        taskNumberElement.innerHTML = `Задание &#8470;${taskNumber}`;
        taskFields.appendChild(taskNumberElement);

        const hoursGroup = document.createElement("div");
        hoursGroup.classList.add("form-group");

        const hoursIcon = document.createElement("i");
        hoursIcon.classList.add("fa", "fa-clock");
        hoursIcon.style.left = "14px";

        const hoursInput = document.createElement("input");
        hoursInput.type = "number";
        hoursInput.name = "hours[]";
        hoursInput.min = "0";
        hoursInput.max = "8.25";
        hoursInput.step = "0.01";
        hoursInput.placeholder = "Часы работы";
        hoursInput.required = true;

        hoursGroup.appendChild(hoursIcon);
        hoursGroup.appendChild(hoursInput);
        taskFields.appendChild(hoursGroup);

        const orderNameGroup = document.createElement("div");
        orderNameGroup.classList.add("form-group");

        const orderNameIcon = document.createElement("i");
        orderNameIcon.classList.add("fa", "fa-cogs");
        orderNameIcon.style.left = "14px";

        const orderNameInput = document.createElement("input");
        orderNameInput.type = "text";
        orderNameInput.name = "order_name[]";
        orderNameInput.classList.add("order-name");
        orderNameInput.placeholder = "Наименование заказа";
        orderNameInput.autocomplete = "off";
        orderNameInput.required = true;

        const orderNameSuggestionsList = document.createElement("div");
        orderNameSuggestionsList.classList.add("order-name-suggestions", "suggestions-list");

        orderNameGroup.appendChild(orderNameIcon);
        orderNameGroup.appendChild(orderNameInput);
        orderNameGroup.appendChild(orderNameSuggestionsList);
        taskFields.appendChild(orderNameGroup);

        processInput(orderNameInput, orderNameSuggestionsList, "/orders/names");
        processSelection(orderNameInput, orderNameSuggestionsList);

        const orderNumberGroup = document.createElement("div");
        orderNumberGroup.classList.add("form-group");

        const orderNumberIcon = document.createElement("i");
        orderNumberIcon.classList.add("fa", "fa-hashtag");
        orderNumberIcon.style.left = "14px";

        const orderNumberInput = document.createElement("input");
        orderNumberInput.type = "text";
        orderNumberInput.name = "order_number[]";
        orderNumberInput.classList.add("order-number");
        orderNumberInput.placeholder = "Номер заказа";
        orderNumberInput.autocomplete = "off";
        orderNumberInput.required = true;

        const orderNumberSuggestionsList = document.createElement("div");
        orderNumberSuggestionsList.classList.add("order-number-suggestions", "suggestions-list");

        orderNumberGroup.appendChild(orderNumberIcon);
        orderNumberGroup.appendChild(orderNumberInput);
        orderNumberGroup.appendChild(orderNumberSuggestionsList);
        taskFields.appendChild(orderNumberGroup);

        processInput(orderNumberInput, orderNumberSuggestionsList, "/orders/numbers");
        processSelection(orderNumberInput, orderNumberSuggestionsList);

        orderNumberSuggestionsList.addEventListener("click", function (event) {
            if (event.target.classList.contains("suggestion")) {
                orderNumberInput.value = event.target.textContent;
                updateOrderName(event.target.textContent, orderNameInput);
            }
        });

        orderNameSuggestionsList.addEventListener("click", function (event) {
            if (event.target.classList.contains("suggestion")) {
                orderNameInput.value = event.target.textContent;
                updateOrderNumber(event.target.textContent, orderNumberInput);
            }
        });

        const isFactoryWorker = document.body.dataset.isFactoryWorker === "True";

        if (!isFactoryWorker) {
            const workTypeGroup = document.createElement("div");
            workTypeGroup.classList.add("form-group");

            const workTypeIcon = document.createElement("i");
            workTypeIcon.classList.add("fa", "fa-tools");
            workTypeIcon.style.left = "14px";

            const workTypeDropDownListIcon = document.createElement("i");
            workTypeDropDownListIcon.classList.add("fa", "fa-chevron-down", "show-work-types");
            workTypeDropDownListIcon.style.right = "4px";
            workTypeDropDownListIcon.style.padding = "10px";
            workTypeDropDownListIcon.style.cursor = "pointer";

            const workTypeInput = document.createElement("input");
            workTypeInput.type = "text";
            workTypeInput.name = "work_type[]";
            workTypeInput.classList.add("work-type");
            workTypeInput.placeholder = "Наименование работы";
            workTypeInput.autocomplete = "off";
            workTypeInput.required = true;

            const workTypeSuggestionsList = document.createElement("div");
            workTypeSuggestionsList.classList.add("work-type-suggestions", "suggestions-list");

            workTypeGroup.appendChild(workTypeIcon);
            workTypeGroup.appendChild(workTypeDropDownListIcon);
            workTypeGroup.appendChild(workTypeInput);
            workTypeGroup.appendChild(workTypeSuggestionsList);
            taskFields.appendChild(workTypeGroup);

            processInput(workTypeInput, workTypeSuggestionsList, "/employees/work-types");
            processSelection(workTypeInput, workTypeSuggestionsList);
        }

        const deleteButton = document.createElement("button");
        deleteButton.type = "button";
        deleteButton.classList.add("default-button", "delete-form-task-button");
        deleteButton.innerText = "Удалить задание";
        taskFields.appendChild(deleteButton);

        const hr = document.createElement("hr");
        taskFields.appendChild(hr);

        tasksContainer.appendChild(taskFields);
    });
}


export function configureTaskDeleteHandler() {
    const modal = document.querySelector(".modal-container");
    if (!modal) return;

    const closeButton = modal.querySelector(".close-modal-button");
    const cancelButton = document.getElementById("cancel-delete-task");
    const confirmButton = document.getElementById("confirm-delete-task");

    if (!closeButton || !cancelButton || !confirmButton) return;

    let taskToDelete = null;
    let formToSubmit = null;

    document.addEventListener("click", (event) => {
        if (event.target.closest(".delete-form-task-button")) {
            event.preventDefault();
            taskToDelete = event.target.closest(".task-fields");
            formToSubmit = null;
            modal.style.display = "flex";
        }

        if (event.target.closest(".delete-table-task-button")) {
            event.preventDefault();
            formToSubmit = event.target.closest("form");
            taskToDelete = null;
            modal.style.display = "flex";
        }
    });

    const closeModal = () => {
        modal.style.display = "none";
        taskToDelete = null;
        formToSubmit = null;
    };

    closeButton.addEventListener("click", closeModal);
    cancelButton.addEventListener("click", closeModal);

    confirmButton.addEventListener("click", () => {
        if (taskToDelete) {
            taskToDelete.remove();
            document.querySelectorAll(".task-fields").forEach((field, index) => {
                const number = field.querySelector(".task-number");
                if (number) {
                    number.innerHTML = `Задание &#8470;${index + 1}`;
                }
            });
        }

        if (formToSubmit) {
            formToSubmit.submit();
        }

        closeModal();
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });
}
