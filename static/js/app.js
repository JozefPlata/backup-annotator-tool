function onImageClick(e) {
    const actionNameInput = document.getElementById("action-name");
    const offsetXInput = document.getElementById("offset-x");
    const offsetYInput = document.getElementById("offset-y");

    if (!actionNameInput || !offsetXInput || !offsetYInput) {
        console.warn("Elements not loaded yet");
        return;
    }

    if (actionNameInput.value === "click") {
        offsetXInput.value = e.offsetX;
        offsetYInput.value = e.offsetY;
    }
};

document.addEventListener("htmx:beforeRequest", (evt) => {
    if (evt.detail.target.id === "screenshot-container") {
        const buttonClick = document.getElementById("button-click");
        const buttonScrollUp = document.getElementById("button-scroll-up");
        const buttonScrollDown = document.getElementById("button-scroll-down");
        const description = document.getElementById("action-description");
        const buttonSubmit = document.getElementById("button-submit");
        const finalAnswer = document.getElementById("final-answer");
        const buttonFinish = document.getElementById("button-finish");
        buttonClick.disabled = true;
        buttonScrollUp.disabled = true;
        buttonScrollDown.disabled = true;
        description.disabled = true;
        buttonSubmit.disabled = true;
        finalAnswer.disabled = true;
        buttonFinish.disabled = true;
    }
});

document.addEventListener("htmx:afterSwap", (evt) => {
    if (evt.detail.target.id === "screenshot-container") {
        const img = document.getElementById("page-img");
        if (img) {
            img.addEventListener("click", onImageClick);
        }

        const buttonClick = document.getElementById("button-click");
        const buttonScrollUp = document.getElementById("button-scroll-up");
        const buttonScrollDown = document.getElementById("button-scroll-down");
        const description = document.getElementById("action-description");
        const buttonSubmit = document.getElementById("button-submit");
        const finalAnswer = document.getElementById("final-answer");
        const buttonFinish = document.getElementById("button-finish");
        buttonClick.disabled = false;
        buttonScrollUp.disabled = false;
        buttonScrollDown.disabled = false;
        description.disabled = false;
        buttonSubmit.disabled = false;
        finalAnswer.disabled = false;
        buttonFinish.disabled = false;

        const actionNameInput = document.getElementById("action-name");
        const offsetXInput = document.getElementById("offset-x");
        const offsetYInput = document.getElementById("offset-y");
        actionNameInput.value = "";
        offsetXInput.value = -1;
        offsetYInput.value = -1;
        description.value = "";
    }
});

function pickAction(name) {
    const actionNameInput = document.getElementById("action-name");
    if (actionNameInput) {
        actionNameInput.value = name;
    }
};