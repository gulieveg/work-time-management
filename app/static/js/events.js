export function configureSuggestionListBlurHandler() {
    document.addEventListener("click", function (event) {
        const selectors = [
            ".order-name-suggestions",
            ".order-number-suggestions",
            ".employee-data-suggestions",
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

        const dropdown = document.querySelector(".dropdown");
        const toggle = document.getElementById("toggle-dropdown");

        if (!dropdown || !toggle) return;

        if (!dropdown.contains(event.target)) {
            toggle.checked = false;
        }
    });
}


export function configureSuggestionListEscapeHandler() {
    document.addEventListener("keydown", function (event) {
        if (event.key !== "Escape") return;

        const selectors = [
            ".order-name-suggestions",
            ".order-number-suggestions",
            ".employee-data-suggestions",
            ".work-name-suggestions",
        ];

        document.querySelectorAll(selectors.join(", ")).forEach(suggestionsList => {
            if (document.body.contains(suggestionsList)) {
                suggestionsList.style.display = "none";
            }
        });

        const toggle = document.getElementById("toggle-dropdown");
        if (toggle && toggle.checked) {
            toggle.checked = false;
        }
    });
}


export function configureFilterResetHandler() {
    document.addEventListener("click", function (event) {
        const resetButton = event.target.closest(".reset-filters-button");
        if (!resetButton) return;

        const form = resetButton.closest("form");
        if (!form) return;

        const inputs = form.querySelectorAll("input[type='text'], input[type='number'], input[type='date']");
        inputs.forEach(input => input.value = "");

        const departmentCheckboxes = form.querySelectorAll(".dropdown-content input[type='checkbox'][name='departments[]']");
        departmentCheckboxes.forEach(checkbox => {
            checkbox.checked = false;
        });

        const selectedText = form.querySelector("#dropdown-selected-text");
        if (selectedText) {
            selectedText.textContent = "Все";
        }

        const toggleCheckbox = form.querySelector("#toggle-dropdown");
        if (toggleCheckbox) {
            toggleCheckbox.checked = false;
        }
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


export function configureScrollToTopButton() {
    const scrollButton = document.querySelector(".scroll-to-top");

    if (scrollButton) {
        window.addEventListener("scroll", function () {
            if (window.scrollY > 400) {
                scrollButton.style.display = "block";
            } else {
                scrollButton.style.display = "none";
            }
        });

        scrollButton.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }
}


export function configureHoursSelection() {
    const hours = document.querySelectorAll(".hours");
    const hoursTotal = document.querySelector(".hours-total");
    const resetButton = document.querySelector(".reset-hours-total-button");
    const hoursTotalContainer = document.querySelector(".hours-total-container");

    if (!hoursTotal || !resetButton || !hoursTotalContainer || hours.length === 0) return;

    function updateSum() {
        let sum = 0;
        let selectedCount = 0;

        hours.forEach(cell => {
            if (cell.classList.contains("selected")) {
                sum += parseFloat(cell.dataset.hours) || 0;
                selectedCount++;
            }
        });

        hoursTotal.textContent = sum.toFixed(2);

        if (selectedCount > 0) {
            hoursTotalContainer.style.display = "flex";
        } else {
            hoursTotalContainer.style.display = "none";
        }
    }

    hours.forEach(cell => {
        cell.style.cursor = "pointer";
        cell.addEventListener("click", () => {
            cell.classList.toggle("selected");
            updateSum();
        });
    });

    resetButton.addEventListener("click", () => {
        hours.forEach(cell => cell.classList.remove("selected"));
        updateSum();
    });
}


export function configureWorkNameDropDownHandler() {
    document.addEventListener("click", (event) => {
        const icon = event.target.closest(".show-work-names");
        if (!icon) return;

        const taskFields = icon.closest(".task-fields");
        if (!taskFields) return;

        const input = taskFields.querySelector(".work-name");
        if (!input) return;

        const suggestionsContainer = taskFields.querySelector(".work-name-suggestions");
        if (!suggestionsContainer) return;

        if (suggestionsContainer.dataset.open === "true") {
            suggestionsContainer.style.display = "none";
            suggestionsContainer.innerHTML = "";
            suggestionsContainer.dataset.open = "false";
            return;
        }

        const workNamesContainer = document.getElementById("work-names-data");
        const workNames = JSON.parse(workNamesContainer.dataset.workNames || "[]");

        workNames.forEach(work => {
            const item = document.createElement("div");
            item.classList.add("suggestion");
            item.textContent = work;

            item.addEventListener("click", () => {
                input.value = work;
                suggestionsContainer.innerHTML = "";
                suggestionsContainer.style.display = "none";
                suggestionsContainer.dataset.open = "false";
            });

            suggestionsContainer.appendChild(item);
        });

        suggestionsContainer.style.display = "block";
        suggestionsContainer.dataset.open = "true";
    });
}


export function configureDropdownCheckboxListener(dropdownId, displayId, defaultText = "Все") {
    const checkboxes = document.querySelectorAll(`#${dropdownId} input[type="checkbox"]`);
    const displayText = document.getElementById(displayId);

    if (displayText) {
        function updateDisplay() {
            const selected = Array.from(checkboxes)
                .filter(cb => cb.checked)
                .map(cb => cb.value);
            displayText.textContent = selected.length ? selected.join(", ") : defaultText;
        }

        checkboxes.forEach(cb => cb.addEventListener("change", updateDisplay));

        updateDisplay();
    }
}
