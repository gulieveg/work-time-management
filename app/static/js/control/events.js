export function configureSuggestionListBlurHandler() {
    document.addEventListener("click", function (event) {
        const selectors = [
            ".order-name-suggestions",
            ".order-number-suggestions",
            ".user-name-suggestions",
            ".user-login-suggestions",
            ".employee-name-suggestions",
            ".personnel-number-suggestions",
            ".work-name-suggestions",
        ];

        document.querySelectorAll(selectors.join(", ")).forEach(suggestionsList => {
            const inputElement = suggestionsList.previousElementSibling;

            const clickedInsideInput = inputElement && inputElement.contains(event.target);
            const clickedInsideSuggestions = suggestionsList.contains(event.target);

            if (!clickedInsideInput && !clickedInsideSuggestions) {
                suggestionsList.style.display = "none";
            }
        });
    });
}


export function configureSuggestionListEscapeHandler() {
    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") return;

        const selectors = [
            ".order-name-suggestions",
            ".order-number-suggestions",
            ".user-name-suggestions",
            ".user-login-suggestions",
            ".employee-name-suggestions",
            ".personnel-number-suggestions",
            ".work-name-suggestions",
        ];

        document.querySelectorAll(selectors.join(", ")).forEach(suggestionsList => {
            if (document.body.contains(suggestionsList)) {
                suggestionsList.style.display = "none";
            }
        });
    });
}


export function configureFilterResetHandler() {
    document.addEventListener("click", function (event) {
        const resetButton = event.target.closest(".reset-filters-button");
        if (!resetButton) return;

        const form = resetButton.closest("form");
        if (!form) return;

        const inputs = form.querySelectorAll("input");
        inputs.forEach(input => input.value = "");
    });
}


export function configurePasswordSwitchHandler() {
    const passwordSwitch = document.getElementById("password-switch");
    const passwordField = document.getElementById("password-field");

    if (!passwordSwitch || !passwordField) return;

    const passwordInput = passwordField.querySelector("input[name='user_password']");

    if (!passwordInput) return;

    passwordSwitch.addEventListener("change", function() {
        const enabled = passwordSwitch.checked;

        passwordField.style.display = enabled ? "block" : "none";

        if (enabled) {
            passwordInput.setAttribute("required", "required");
        } else {
            passwordInput.removeAttribute("required");
            passwordInput.value = "";
        }
    });
}


export function configureUserStatusSwitchHandler() {
    const switches = document.querySelectorAll(".user-status-switch");

    switches.forEach(switchEl => {
        switchEl.addEventListener("change", function() {
            const isActive = this.checked;
            const userId = this.dataset.userId;

            fetch(`/control/users/update_user_status/${userId}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(
                    {
                        is_active: isActive,
                    }
                )
            })
            .then(response => response.json())
            .then(data => console.log(data));
        });
    });
}


export function configureUserConfirmationModal() {
    const modalTexts = {
        "delete-user": {
            message: "Вы уверены, что хотите удалить пользователя?",
            button: "Удалить",
        },
        "reset-user-password": {
            message: "Вы уверены, что хотите сбросить пароль пользователя?",
            button: "Сбросить",
        },
        "delete-order": {
            message: "Вы уверены, что хотите удалить заказ?",
            button: "Удалить",
        },
        "delete-employee": {
            message: "Вы уверены, что хотите удалить работника?",
            button: "Удалить",
        },
        "delete-work": {
            message: "Вы уверены, что хотите удалить работу?",
            button: "Удалить",
        }
    };

    const modal = document.getElementById("confirmation-modal");
    if(!modal) return;

    const modalTextElem = modal.querySelector("#confirmation-modal-text");
    const closeButton = modal.querySelector(".close-modal-button");
    const cancelButton = modal.querySelector("#cancel-action");
    const confirmButton = modal.querySelector("#confirm-action");

    if (!modalTextElem || !closeButton || !cancelButton || !confirmButton) return;

    let formToSubmit = null;

    document.addEventListener("click", (event) => {
        const actionButton = event.target.closest("[data-action]");
        if (!actionButton) return;

        event.preventDefault();
        formToSubmit = actionButton.closest("form");

        const actionType = actionButton.dataset.action;
        if (!modalTexts[actionType]) return;

        modalTextElem.textContent = modalTexts[actionType].message;
        confirmButton.textContent = modalTexts[actionType].button;

        modal.style.display = "flex";
    });

    const closeModal = () => {
        modal.style.display = "none";
        formToSubmit = null;
    };

    closeButton.addEventListener("click", closeModal);
    cancelButton.addEventListener("click", closeModal);
    window.addEventListener("click", (event) => {
        if (event.target === modal) closeModal();
    });

    confirmButton.addEventListener("click", () => {
        if (formToSubmit) formToSubmit.submit();
        closeModal();
    });
}


export function configurePasswordToggle() {
    const togglePasswords = document.querySelectorAll(".toggle-password");

    togglePasswords.forEach(toggle => {
        toggle.addEventListener("click", function () {
            const passwordInput = this.previousElementSibling;

            if (passwordInput && (passwordInput.type === "password" || passwordInput.type === "text")) {
                const type = passwordInput.type === "password" ? "text" : "password";
                passwordInput.type = type;
                this.classList.toggle("fa-eye");
                this.classList.toggle("fa-eye-slash");
            }
        });
    });
}


export function configureDropDownHandler() {
    document.querySelectorAll(".dropdown").forEach(dropdown => {
        const hiddenInput = dropdown.querySelector("input[type='hidden']");
        const labelText = dropdown.querySelector(".dropdown-label span");
        const options = dropdown.querySelectorAll(".dropdown-content label");
        const toggleCheckbox = dropdown.querySelector("input[type='checkbox']");

        if (!hiddenInput || !labelText || !options.length || !toggleCheckbox) return;

        options.forEach(option => {
            option.addEventListener("click", () => {
                const value = option.getAttribute("data-value");
                const text = option.textContent;

                hiddenInput.value = value;

                labelText.textContent = text;
                labelText.classList.add("selected");

                toggleCheckbox.checked = false;
            });
        });

        document.addEventListener("click", (event) => {
            if (!dropdown.contains(event.target)) {
                toggleCheckbox.checked = false;
            }
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                toggleCheckbox.checked = false;
            }
        });
    });
}


export function configureFileUpload() {
    const container = document.querySelector(".file-upload-container");
    if (!container) return;

    const fileUpload = container.querySelector(".file-upload");
    const fileUploadLabel = container.querySelector(".file-upload-label");
    const uploadButton = container.querySelector(".upload-button");

    uploadButton.addEventListener("click", () => fileUpload.click());

    fileUpload.addEventListener("change", () => {
        if (fileUpload.files.length > 0) {
            fileUploadLabel.textContent = fileUpload.files[0].name;
        }
    });
}


export function configureWorkListHandlers() {
    const tabButtons = document.querySelectorAll(".sub-tab-button");
    const tabContents = document.querySelectorAll(".tab-content");
    const tbody = document.getElementById("works-rows");
    const addRowButton = document.getElementById("add-row-button");

    if (!tabButtons.length || !tabContents.length || !tbody || !addRowButton) return;

    tabButtons.forEach(button => {
        button.addEventListener("click", () => {
            tabButtons.forEach(btn => btn.classList.remove("active"));
            tabContents.forEach(tab => tab.classList.remove("active"));

            button.classList.add("active");
            const targetTab = document.getElementById(button.dataset.tab);
            if (targetTab) {
                targetTab.classList.add("active");
            }
        });
    });

    tbody.addEventListener("click", event => {
        const deleteRowButton = event.target.closest(".delete-row-button");
        if (deleteRowButton) {
            deleteRowButton.closest("tr").remove();
        }
    });

    addRowButton.addEventListener("click", () => {
        const newRow = document.createElement("tr");

        newRow.innerHTML = `
            <td><input type="text" name="work_name[]" autocomplete="off" required></td>
            <td><input type="text" name="work_planned_hours[]" autocomplete="off" required></td>
            <td><button type="button" class="delete-row-button">&times;</button></td>
        `;

        tbody.appendChild(newRow);
    });

    const fileInput = document.querySelector(".file-upload");
    const fileLabel = document.querySelector(".file-upload-label");
    const deleteFileButton = document.querySelector(".delete-file-button");

    if (fileInput && fileLabel && deleteFileButton) {
        fileInput.addEventListener("change", () => {
            if (fileInput.files.length) {
                fileLabel.textContent = fileInput.files[0].name;
                deleteFileButton.style.display = "inline-block";
            } else {
                fileLabel.textContent = "Таблица не выбрана";
                deleteFileButton.style.display = "none";
            }
        });

        deleteFileButton.addEventListener("click", () => {
            fileInput.value = "";
            fileLabel.textContent = "Таблица не выбрана";
            deleteFileButton.style.display = "none";
        });
    }
}
