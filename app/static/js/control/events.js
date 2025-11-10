export function configureSuggestionListBlurHandler() {
    document.addEventListener("click", function (event) {
        const selectors = [
            ".order-name-suggestions",
            ".order-number-suggestions"
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
            ".order-number-suggestions"
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

            fetch(`update_user_status/${userId}`, {
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


export function configureUserPrivilegesDropDownHandler() {
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
