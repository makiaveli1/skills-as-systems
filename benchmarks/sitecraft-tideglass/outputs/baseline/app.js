const bands = {
  now: {
    time: "Now",
    decision: "Caution · Short weather window",
    state: "caution",
    wind: "WSW 17 kn",
    gust: "24 kn",
    swell: "1.4 m",
    note: "Conditions are workable for a short period. Build in time to turn back.",
    summary: "Caution: a short workable window before conditions tighten."
  },
  "0700": {
    time: "07:00",
    decision: "Best window · Depart prepared",
    state: "best",
    wind: "WSW 13 kn",
    gust: "18 kn",
    swell: "1.1 m",
    note: "The most sensible band this morning, subject to checks at the harbour mouth.",
    summary: "Best window: lighter wind and swell, with the departure checks complete."
  },
  "0900": {
    time: "09:00",
    decision: "Hold · Conditions tightening",
    state: "hold",
    wind: "W 22 kn",
    gust: "31 kn",
    swell: "1.8 m",
    note: "The short window has closed. Hold and reassess the plan.",
    summary: "Hold: stronger wind, higher gusts, and building swell after the window."
  }
};

const tabs = Array.from(document.querySelectorAll("[role='tab']"));
const panel = document.querySelector("#conditions-panel");
const decisionCard = document.querySelector(".decision-card");
const decisionValue = document.querySelector("#decision-value");
const decisionNote = document.querySelector("#decision-note");
const selectedTime = document.querySelector("#selected-time");
const windValue = document.querySelector("#wind-value");
const gustValue = document.querySelector("#gust-value");
const swellValue = document.querySelector("#swell-value");
const panelSummary = document.querySelector("#panel-summary");

function selectBand(tab, moveFocus = false) {
  const band = bands[tab.dataset.band];

  tabs.forEach((candidate) => {
    const selected = candidate === tab;
    candidate.classList.toggle("is-selected", selected);
    candidate.setAttribute("aria-selected", String(selected));
    candidate.tabIndex = selected ? 0 : -1;
  });

  panel.setAttribute("aria-labelledby", tab.id);
  panel.dataset.state = band.state;
  decisionCard.dataset.state = band.state;
  decisionValue.textContent = band.decision;
  decisionNote.textContent = band.note;
  selectedTime.textContent = band.time;
  windValue.textContent = band.wind;
  gustValue.textContent = band.gust;
  swellValue.textContent = band.swell;
  panelSummary.textContent = band.summary;

  if (moveFocus) tab.focus();
}

tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => selectBand(tab));
  tab.addEventListener("keydown", (event) => {
    let nextIndex;

    if (event.key === "ArrowRight" || event.key === "ArrowDown") {
      nextIndex = (index + 1) % tabs.length;
    } else if (event.key === "ArrowLeft" || event.key === "ArrowUp") {
      nextIndex = (index - 1 + tabs.length) % tabs.length;
    } else if (event.key === "Home") {
      nextIndex = 0;
    } else if (event.key === "End") {
      nextIndex = tabs.length - 1;
    } else {
      return;
    }

    event.preventDefault();
    selectBand(tabs[nextIndex], true);
  });
});

const checks = Array.from(document.querySelectorAll(".check-item input"));
const checkCount = document.querySelector("#check-count");

checks.forEach((checkbox) => {
  checkbox.addEventListener("change", () => {
    const completed = checks.filter((item) => item.checked).length;
    checkCount.textContent = `${completed} / ${checks.length}`;
  });
});

const noticeForm = document.querySelector("#notice-form");
const emailInput = document.querySelector("#email");
const formMessage = document.querySelector("#form-message");
const submitButton = noticeForm.querySelector("button[type='submit']");
const submitLabel = noticeForm.querySelector(".submit-label");
const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function setFormMessage(message, type = "") {
  formMessage.textContent = message;
  formMessage.className = `form-message${type ? ` is-${type}` : ""}`;
}

function validateEmail() {
  const value = emailInput.value.trim();

  if (!value) {
    emailInput.setAttribute("aria-invalid", "true");
    setFormMessage("Enter an email address to preview sign-up.", "error");
    return false;
  }

  if (!emailPattern.test(value)) {
    emailInput.setAttribute("aria-invalid", "true");
    setFormMessage("Enter a complete address, such as crew@example.com.", "error");
    return false;
  }

  emailInput.removeAttribute("aria-invalid");
  setFormMessage("");
  return true;
}

emailInput.addEventListener("input", () => {
  if (emailInput.getAttribute("aria-invalid") === "true") validateEmail();
});

noticeForm.addEventListener("submit", (event) => {
  event.preventDefault();
  if (!validateEmail()) {
    emailInput.focus();
    return;
  }

  noticeForm.classList.add("is-submitting");
  noticeForm.setAttribute("aria-busy", "true");
  submitButton.disabled = true;
  submitLabel.textContent = "Checking locally…";
  setFormMessage("Running the local demonstration…");

  window.setTimeout(() => {
    const previewFailure = emailInput.value.trim().toLowerCase() === "fail@example.test";
    noticeForm.classList.remove("is-submitting");
    noticeForm.removeAttribute("aria-busy");
    submitButton.disabled = false;
    submitLabel.textContent = "Preview sign-up";

    if (previewFailure) {
      setFormMessage("The preview could not be completed. Nothing was sent or retained; try another address.", "error");
      return;
    }

    setFormMessage("Preview complete. Your address was checked locally, then discarded—no notice was sent.", "success");
    emailInput.value = "";
  }, 700);
});
