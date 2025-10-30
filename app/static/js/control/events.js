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


export function configureUserDeleteHandler() {
    const modal = document.querySelector(".modal-container");
    if (!modal) return;

    const closeButton = modal.querySelector(".close-modal-button");
    const cancelButton = document.getElementById("cancel-delete-user");
    const confirmButton = document.getElementById("confirm-delete-user");

    if (!closeButton || !cancelButton || !confirmButton) return;

    let formToSubmit = null;

    document.addEventListener("click", (event) => {
        const deleteButton = event.target.closest(".delete-user-button");
        if (deleteButton) {
            event.preventDefault();
            formToSubmit = deleteButton.closest("form");
            modal.style.display = "flex";
        }
    });

    const closeModal = () => {
        modal.style.display = "none";
        formToSubmit = null;
    };

    closeButton.addEventListener("click", closeModal);
    cancelButton.addEventListener("click", closeModal);

    confirmButton.addEventListener("click", () => {
        if (formToSubmit) {
            formToSubmit.submit();
        }
        closeModal();
    });

    window.addEventListener("click", (e) => {
        if (e.target === modal) closeModal();
    });
}
