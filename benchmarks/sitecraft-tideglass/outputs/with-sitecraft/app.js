const outlooks = {
  now: {
    decision: "Caution · short weather window",
    state: "caution",
    label: "Now",
    wind: "WSW 17 kn",
    gust: "Gusting 24 kn",
    swell: "1.4 m",
    period: "7 s",
    tide: "+1.2 m",
    tideTrend: "Rising",
    visibility: "6 nm",
  },
  "0700": {
    decision: "Best window · 06:40–08:10",
    state: "best",
    label: "07:00",
    wind: "WSW 13 kn",
    gust: "Gusting 18 kn",
    swell: "1.1 m",
    period: "7 s",
    tide: "+1.2 m",
    tideTrend: "Rising",
    visibility: "6 nm",
  },
  "0900": {
    decision: "Hold · conditions tightening",
    state: "hold",
    label: "09:00",
    wind: "W 22 kn",
    gust: "Gusting 31 kn",
    swell: "1.8 m",
    period: "7 s",
    tide: "+1.2 m",
    tideTrend: "Rising",
    visibility: "6 nm",
  },
};

const tabs = [...document.querySelectorAll("[role='tab']")];
const windowCard = document.querySelector(".window-card");
const announcement = document.querySelector("#selection-announcement");

const fields = {
  decision: document.querySelector("#decision-text"),
  wind: document.querySelector("#wind-value"),
  gust: document.querySelector("#gust-value"),
  swell: document.querySelector("#swell-value"),
  period: document.querySelector("#period-value"),
  tide: document.querySelector("#tide-value"),
  tideTrend: document.querySelector("#tide-trend"),
  visibility: document.querySelector("#visibility-value"),
};

function selectOutlook(tab, shouldAnnounce = true) {
  const outlook = outlooks[tab.dataset.time];

  tabs.forEach((candidate) => {
    const isSelected = candidate === tab;
    candidate.setAttribute("aria-selected", String(isSelected));
    candidate.tabIndex = isSelected ? 0 : -1;
  });

  Object.entries(fields).forEach(([key, element]) => {
    element.textContent = outlook[key];
  });

  windowCard.dataset.decision = outlook.state;

  if (shouldAnnounce) {
    announcement.textContent = `${outlook.label} selected. ${outlook.decision}. Wind ${outlook.wind}, ${outlook.gust.toLowerCase()}, swell ${outlook.swell}.`;
  }
}

tabs.forEach((tab, index) => {
  tab.addEventListener("click", () => selectOutlook(tab));

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
    tabs[nextIndex].focus();
    selectOutlook(tabs[nextIndex]);
  });
});

const form = document.querySelector("#notice-form");
const email = document.querySelector("#email");
const submitButton = form.querySelector("button[type='submit']");
const formStatus = document.querySelector("#form-status");
let submissionTimer;

function showFormStatus(message, state = "") {
  formStatus.textContent = message;
  if (state) {
    formStatus.dataset.state = state;
  } else {
    delete formStatus.dataset.state;
  }
}

function markInvalid(message) {
  email.setAttribute("aria-invalid", "true");
  showFormStatus(message, "error");
  email.focus();
}

email.addEventListener("input", () => {
  email.removeAttribute("aria-invalid");
  if (formStatus.dataset.state === "error") {
    showFormStatus("");
  }
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  window.clearTimeout(submissionTimer);

  const enteredEmail = email.value.trim();
  email.value = enteredEmail;

  if (!enteredEmail) {
    markInvalid("Enter an email address to run the local demonstration.");
    return;
  }

  if (!email.validity.valid) {
    markInvalid("Enter an address in the format name@example.com.");
    return;
  }

  email.removeAttribute("aria-invalid");
  email.disabled = true;
  submitButton.disabled = true;
  submitButton.textContent = "Running…";
  form.setAttribute("aria-busy", "true");
  showFormStatus("Running the local demonstration. Nothing is being transmitted.");

  submissionTimer = window.setTimeout(() => {
    const shouldFail = enteredEmail.toLowerCase() === "fail@demo.test";

    email.disabled = false;
    submitButton.disabled = false;
    submitButton.textContent = "Run local demo";
    form.removeAttribute("aria-busy");

    if (shouldFail) {
      showFormStatus("Local demo interrupted. Nothing was sent or stored. Check the address and try again.", "error");
      email.focus();
      return;
    }

    email.value = "";
    showFormStatus("Local demo complete. The address was not sent or retained.", "success");
  }, 900);
});
