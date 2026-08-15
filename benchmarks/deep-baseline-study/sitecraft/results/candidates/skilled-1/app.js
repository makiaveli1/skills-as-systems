const plannerRoot = document.querySelector("#planner-app");
const routeList = document.querySelector('[data-testid="route-list"]');
const groupNeedsControl = document.querySelector('[data-testid="group-needs"]');
const filterControl = document.querySelector('[data-testid="difficulty-filter"]');
const summaryContent = document.querySelector("#summary-content");
const checklistItems = document.querySelector("#checklist-items");
const essentialsProgress = document.querySelector("#essentials-progress");
const essentialsNote = document.querySelector("#essentials-note");
const statusNode = document.querySelector("#plan-status");
const confirmButton = document.querySelector('[data-testid="confirm-plan"]');

const groupProfiles = {
  mixed: {
    label: "Mixed group",
    note: "Use this when you need a route that works for varied pace and confidence.",
  },
  child: {
    label: "Child with adults",
    note: "Guidance shifts toward landmarks, turn-back options, and shorter effort windows.",
  },
  experienced: {
    label: "Experienced walkers",
    note: "Guidance stays candid about commitment but keeps the full technical detail visible.",
  },
};

let routes = [];
let selectedRouteId = null;
let confirmedRouteId = null;
let checklistState = {};
let currentChecklistItems = [];

function getSelectedGroup() {
  return groupNeedsControl.value;
}

function getGroupSuitability(route, groupNeed) {
  return route.suitability?.[groupNeed] ?? route.suitability?.mixed ?? "check fit";
}

function isRouteOpen(route) {
  return route.status === "open";
}

function formatDifficulty(value) {
  return value.charAt(0).toUpperCase() + value.slice(1);
}

function describeDifficulty(route) {
  if (route.difficulty === "easy") {
    return "Lower effort, clearer footing, and shorter commitment.";
  }

  if (route.difficulty === "steady") {
    return "More ascent and rougher going, with a longer planning commitment.";
  }

  return "High effort, exposed terrain, and strong route commitment.";
}

function createMetric(label, value) {
  return `
    <div class="metric">
      <div class="metric-label">${label}</div>
      <div class="metric-value">${value}</div>
    </div>
  `;
}

function getFilteredRoutes() {
  const filterValue = filterControl.value;
  return routes.filter((route) => {
    return filterValue === "all" ? true : route.difficulty === filterValue;
  });
}

function getRouteRank(route, groupNeed) {
  return rankSuitability(getGroupSuitability(route, groupNeed));
}

function isRouteSuitable(route, groupNeed) {
  return getRouteRank(route, groupNeed) > 1;
}

function rankSuitability(suitability) {
  if (suitability === "best fit" || suitability === "strong fit") {
    return 3;
  }

  if (suitability === "gentle option") {
    return 2;
  }

  if (suitability === "not advised") {
    return 1;
  }

  return 0;
}

function chooseDefaultRoute(groupNeed, candidateRoutes = routes) {
  const openRoutes = candidateRoutes.filter(isRouteOpen);
  if (openRoutes.length === 0) {
    return null;
  }

  return (
    [...openRoutes].sort((left, right) => {
      return getRouteRank(right, groupNeed) - getRouteRank(left, groupNeed);
    })[0]?.id ?? null
  );
}

function getSelectedRoute() {
  return routes.find((route) => route.id === selectedRouteId) ?? null;
}

function focusStatus() {
  statusNode.focus({ preventScroll: true });
}

function setStatus(message, state, options = {}) {
  statusNode.textContent = message;
  statusNode.dataset.state = state;

  if (options.focus) {
    focusStatus();
  }
}

function ensureValidSelectedRoute(reason = "system") {
  const groupNeed = getSelectedGroup();
  const filteredRoutes = getFilteredRoutes();
  const openVisibleRoutes = filteredRoutes.filter(isRouteOpen);
  const currentRoute = getSelectedRoute();
  const currentVisible = currentRoute && filteredRoutes.some((route) => route.id === currentRoute.id);
  const currentVisibleOpen = currentVisible && isRouteOpen(currentRoute);
  const betterOpenRouteId = chooseDefaultRoute(groupNeed, filteredRoutes);
  const betterOpenRoute = routes.find((route) => route.id === betterOpenRouteId) ?? null;

  if (openVisibleRoutes.length === 0) {
    if (selectedRouteId !== null) {
      confirmedRouteId = null;
    }

    selectedRouteId = null;
    return {
      route: null,
      announcement:
        reason === "filter" || reason === "group"
          ? "No open routes remain in this view. Closed routes stay comparable only."
          : null,
      statusState: "warning",
    };
  }

  if (!currentVisibleOpen) {
    selectedRouteId = betterOpenRouteId;
    confirmedRouteId = null;

    if (reason === "filter" || reason === "group") {
      return {
        route: betterOpenRoute,
        announcement: `Plan updated to ${betterOpenRoute.name} for ${groupProfiles[groupNeed].label} because the previous route is no longer available in this view.`,
        statusState: "info",
      };
    }

    return { route: betterOpenRoute, announcement: null, statusState: "neutral" };
  }

  if (!isRouteSuitable(currentRoute, groupNeed) && betterOpenRoute && betterOpenRoute.id !== currentRoute.id) {
    selectedRouteId = betterOpenRoute.id;
    confirmedRouteId = null;

    return {
      route: betterOpenRoute,
      announcement: `Plan updated to ${betterOpenRoute.name} for ${groupProfiles[groupNeed].label} because ${currentRoute.name} is not advised for this group.`,
      statusState: "info",
    };
  }

  return {
    route: currentRoute,
    announcement: null,
    statusState: "neutral",
  };
}

function deriveRouteBrief(route, groupNeed) {
  const suitability = getGroupSuitability(route, groupNeed);
  const advisory = !isRouteOpen(route)
    ? `${route.name} is closed today and remains on the board for comparison only.`
    : suitability === "best fit"
      ? `${route.name} is the best fit for a ${groupProfiles[groupNeed].label.toLowerCase()} today.`
      : suitability === "strong fit"
        ? `${route.name} is a strong fit for experienced walkers who want a committed day out.`
        : suitability === "gentle option"
          ? `${route.name} stays viable, but it reads as a lower-commitment day for this group.`
          : `${route.name} stays selectable, but the route is not advised for this group profile.`;

  const signalNote =
    route.signal.toLowerCase().includes("none")
      ? "Agree a hard turnaround time before the signal drops."
      : route.signal.toLowerCase().includes("patchy")
        ? "Nominate a lead and tail walker before the patchy section."
        : "Use the reliable signal to confirm finish timing with the group.";

  const terrainNote =
    route.terrain.toLowerCase().includes("boardwalk")
      ? "Call out slick boardwalk sections and keep the pace even."
      : route.terrain.toLowerCase().includes("scrambles")
        ? "Confirm every walker is happy with hands-on scrambling before committing."
        : "Warn the group about wet stone on the descent and keep spacing on the ridge.";

  return { advisory, signalNote, terrainNote, suitability };
}

function getChecklistForRoute(route, groupNeed) {
  const groupSpecificLead =
    groupNeed === "child"
      ? "The group has agreed a child pace, snack stop, and early return point."
      : groupNeed === "experienced"
        ? "Everyone understands the route commitment, start time, and regroup rules before leaving."
        : "Everyone knows the route length, duration, and expected regroup points.";

  const layerReason =
    groupNeed === "experienced"
      ? "Exposure and timing still matter even for a stronger group."
      : "Mixed groups slow down quickly when one person is underdressed or chilled.";

  const foodReason =
    groupNeed === "child"
      ? "Children fade fast if breaks and easy access snacks are not planned up front."
      : "No one should be relying on a shared emergency supply for the full walk.";

  const groupChecklist = [
    {
      key: "briefed",
      title: "Distance and pace briefed",
      detail: groupSpecificLead,
    },
    {
      key: "layers",
      title: "Weather layer packed",
      detail: `Each walker carries a waterproof or warm layer. ${layerReason}`,
    },
    {
      key: "food",
      title: "Water and snacks covered",
      detail: foodReason,
    },
  ];

  const routeSpecific = [
    {
      key: "suitability",
      title: "Route fit explained to the group",
      detail: route.why,
    },
    {
      key: "signal",
      title: "Contact plan agreed",
      detail:
        route.signal.toLowerCase().includes("none")
          ? "There is no signal for a long section, so the group has an explicit fallback meeting plan."
          : route.signal.toLowerCase().includes("patchy")
            ? "The group knows where signal becomes unreliable and how the lead will manage check-ins."
            : "The group knows who will send the finish update once the walk is underway.",
    },
    {
      key: "terrain",
      title: "Terrain risk called out",
      detail: route.terrain,
    },
    {
      key: "turnaround",
      title: "Turnaround trigger set",
      detail:
        route.weather.toLowerCase().includes("gusts")
          ? "Pick a latest safe summit window before the exposed gusts build."
          : route.weather.toLowerCase().includes("lifting")
            ? "Start after the lift if visibility matters more than an early departure."
            : "Set a simple turnaround time before the sheltered route becomes a soggy slog.",
    },
  ];

  return [...groupChecklist, ...routeSpecific];
}

function renderRouteChoices() {
  const groupNeed = getSelectedGroup();
  const filteredRoutes = getFilteredRoutes();
  const activeRoutes = filteredRoutes.filter(isRouteOpen);

  if (!activeRoutes.some((route) => route.id === selectedRouteId)) {
    selectedRouteId = chooseDefaultRoute(groupNeed, filteredRoutes);
  }

  routeList.innerHTML = filteredRoutes
    .map((route) => {
      const suitability = getGroupSuitability(route, groupNeed);
      const isPressed = isRouteOpen(route) && route.id === selectedRouteId;
      const statusLabel = isRouteOpen(route) ? "Open for planning" : "Closed today";
      const routeReason = !isRouteOpen(route)
        ? route.why
        : `For ${groupProfiles[groupNeed].label.toLowerCase()}: ${suitability}.`;
      const routeGuidance = !isRouteOpen(route)
        ? "Cannot become the active plan."
        : route.why;

      return `
        <div class="route-entry" role="listitem" data-status="${route.status}">
          <button
            type="button"
            class="route-choice"
            data-route-id="${route.id}"
            aria-disabled="${isRouteOpen(route) ? "false" : "true"}"
            aria-pressed="${isPressed ? "true" : "false"}"
          >
            <div class="route-choice-head">
              <h3>${route.name}</h3>
              <span class="status-chip">${suitability}</span>
            </div>
            <p class="route-meta">${formatDifficulty(route.difficulty)} grade / ${describeDifficulty(route)}</p>
            <div class="route-metrics">
              <span class="status-chip status-chip-status" data-status="${route.status}">
                ${statusLabel}
              </span>
            </div>
            <div class="route-metrics">
              ${createMetric("Distance", `${route.distance_km} km`)}
              ${createMetric("Time", route.duration)}
              ${createMetric("Ascent", `+${route.ascent_m} m`)}
            </div>
            <p class="route-reason">${routeReason}</p>
            <p class="route-guidance">${routeGuidance}</p>
          </button>
        </div>
      `;
    })
    .join("");
}

function renderSummary(route) {
  const groupNeed = getSelectedGroup();
  if (!route) {
    summaryContent.innerHTML = `
      <p class="summary-note">
        No open routes match this filter. Closed routes remain below for comparison,
        but they cannot become the active plan.
      </p>
    `;
    return;
  }

  const brief = deriveRouteBrief(route, groupNeed);
  const isConfirmed = confirmedRouteId === route.id;
  const confirmationNote = isConfirmed
    ? "This route has been confirmed for the group."
    : "Use the checklist below to confirm the day’s plan.";
  const confirmedSummary = isConfirmed
    ? `
      <div class="summary-confirmed">
        <p class="panel-kicker">Confirmed plan</p>
        <strong>${groupProfiles[groupNeed].label} / ${route.name}</strong>
        <p class="summary-note">All essentials are checked. This is the stable summary to share with the group.</p>
      </div>
    `
    : "";

  summaryContent.innerHTML = `
    <div class="summary-lead">
      <div class="route-choice-head">
        <h3 class="summary-title">${route.name}</h3>
        <span class="status-chip">${brief.suitability}</span>
      </div>
      <p class="summary-rationale">${brief.advisory}</p>
      <p class="summary-note">${confirmationNote}</p>
    </div>

    <div class="summary-metrics">
      ${createMetric("Group", groupProfiles[groupNeed].label)}
      ${createMetric("Distance", `${route.distance_km} km`)}
      ${createMetric("Time", route.duration)}
      ${createMetric("Ascent", `+${route.ascent_m} m`)}
      ${createMetric("Signal", route.signal)}
    </div>

    <div class="summary-facts">
      <div class="fact-row">
        <strong>Route basis</strong>
        <span>${route.why}</span>
      </div>
      <div class="fact-row">
        <strong>Weather window</strong>
        <span>${route.weather}</span>
      </div>
      <div class="fact-row">
        <strong>Terrain cue</strong>
        <span>${brief.terrainNote}</span>
      </div>
      <div class="fact-row">
        <strong>Group protocol</strong>
        <span>${brief.signalNote}</span>
      </div>
    </div>

    ${confirmedSummary}

    <div class="summary-slip">
      <p><strong>Shareable summary</strong></p>
      <p>
        ${groupProfiles[groupNeed].label}: ${route.name}, ${route.distance_km} km over
        ${route.duration} with ${route.ascent_m} m ascent. ${route.why}
        ${brief.terrainNote} ${brief.signalNote}
      </p>
    </div>
  `;
}

function renderChecklist(route) {
  const groupNeed = getSelectedGroup();
  if (!route) {
    checklistItems.innerHTML = "";
    essentialsProgress.textContent = "0 / 0 ready";
    essentialsNote.textContent =
      "Choose a filter with at least one open route to build a live plan.";
    currentChecklistItems = [];
    return;
  }

  essentialsNote.textContent = groupProfiles[groupNeed].note;

  const items = getChecklistForRoute(route, groupNeed);
  currentChecklistItems = items;
  const savedState = checklistState[route.id]?.[groupNeed] ?? {};
  checklistItems.innerHTML = items
    .map((item, index) => {
      const inputId = `check-${route.id}-${item.key}`;
      return `
        <label class="check-item" for="${inputId}">
          <input
            id="${inputId}"
            name="${inputId}"
            type="checkbox"
            data-check-key="${item.key}"
            ${savedState[item.key] ? "checked" : ""}
          />
          <span class="check-label">
            <strong>${index + 1}. ${item.title}</strong>
            <small><span class="check-why">Why it matters:</span> ${item.detail}</small>
          </span>
        </label>
      `;
    })
    .join("");

  updateProgress();
}

function updateProgress() {
  const checkboxes = checklistItems.querySelectorAll('input[type="checkbox"]');
  const completed = [...checkboxes].filter((input) => input.checked).length;
  essentialsProgress.textContent = `${completed} / ${checkboxes.length} ready`;
  return { completed, total: checkboxes.length };
}

function getRemainingChecklistTitles() {
  const checkboxes = [...checklistItems.querySelectorAll('input[type="checkbox"]')];
  return currentChecklistItems
    .filter((item, index) => !checkboxes[index]?.checked)
    .map((item) => item.title);
}

function focusRouteChoice(routeId) {
  if (!routeId) {
    return;
  }

  routeList.querySelector(`[data-route-id="${routeId}"]`)?.focus();
}

function syncSelectedRoute(options = {}) {
  const route = getSelectedRoute();
  renderSummary(route);
  renderChecklist(route);

  if (!route) {
    setStatus(
      options.announcement ?? "No open route is currently available in this filter.",
      options.statusState ?? "warning",
    );
    return;
  }

  if (options.announcement) {
    setStatus(options.announcement, options.statusState ?? "info");
    return;
  }

  if (confirmedRouteId !== route.id) {
    setStatus("Select a route and work through the essentials.", "neutral");
  }
}

function rememberChecklistState() {
  if (!selectedRouteId) {
    return;
  }

  const groupNeed = getSelectedGroup();
  checklistState[selectedRouteId] ??= {};
  checklistState[selectedRouteId][groupNeed] = {};

  checklistItems.querySelectorAll('input[type="checkbox"]').forEach((input) => {
    checklistState[selectedRouteId][groupNeed][input.dataset.checkKey] = input.checked;
  });
}

async function loadRoutes() {
  const response = await fetch("data/routes.json", { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Route data request failed: ${response.status}`);
  }

  return response.json();
}

function attachEvents() {
  groupNeedsControl.addEventListener("change", () => {
    const selectionResult = ensureValidSelectedRoute("group");
    renderRouteChoices();
    syncSelectedRoute(selectionResult);
  });

  filterControl.addEventListener("change", () => {
    const selectionResult = ensureValidSelectedRoute("filter");
    renderRouteChoices();
    syncSelectedRoute(selectionResult);
  });

  routeList.addEventListener("click", (event) => {
    const button = event.target.closest("[data-route-id]");
    if (!button) {
      return;
    }

    const route = routes.find((item) => item.id === button.dataset.routeId);
    if (!route) {
      return;
    }

    if (!isRouteOpen(route)) {
      setStatus(`${route.name} is closed: ${route.why}`, "warning");
      return;
    }

    selectedRouteId = button.dataset.routeId;
    confirmedRouteId = null;
    renderRouteChoices();
    syncSelectedRoute();
  });

  routeList.addEventListener("keydown", (event) => {
    if (event.key !== "ArrowRight" && event.key !== "ArrowLeft") {
      return;
    }

    const button = event.target.closest("[data-route-id]");
    if (!button) {
      return;
    }

    const visibleOpenRoutes = getFilteredRoutes().filter(isRouteOpen);
    if (visibleOpenRoutes.length === 0) {
      return;
    }

    event.preventDefault();

    const direction = event.key === "ArrowRight" ? 1 : -1;
    const availableIds = visibleOpenRoutes.map((route) => route.id);
    const currentIndex = availableIds.indexOf(button.dataset.routeId);
    const nextIndex = currentIndex === -1
      ? direction === 1 ? 0 : availableIds.length - 1
      : (currentIndex + direction + availableIds.length) % availableIds.length;
    const nextRouteId = availableIds[nextIndex];

    selectedRouteId = nextRouteId;
    confirmedRouteId = null;
    renderRouteChoices();
    syncSelectedRoute();
    focusRouteChoice(nextRouteId);
  });

  checklistItems.addEventListener("change", () => {
    rememberChecklistState();
    const { completed, total } = updateProgress();
    const route = routes.find((item) => item.id === selectedRouteId) ?? null;

    if (confirmedRouteId === selectedRouteId && completed < total) {
      confirmedRouteId = null;
      renderSummary(route);
    }

    if (completed < total) {
      const remaining = total - completed;
      setStatus(
        `Check ${remaining} more ${remaining === 1 ? "item" : "items"} before confirming.`,
        "warning",
      );
    } else {
      setStatus("All essentials are covered. Confirm the plan when ready.", "success");
    }
  });

  confirmButton.addEventListener("click", () => {
    const route = getSelectedRoute();
    const { completed, total } = updateProgress();
    const groupNeed = getSelectedGroup();

    if (!route) {
      setStatus("No route is currently selected.", "warning", { focus: true });
      return;
    }

    if (!isRouteOpen(route)) {
      setStatus(`${route.name} cannot be confirmed because it is closed.`, "warning", { focus: true });
      return;
    }

    if (completed < total) {
      const remainingTitles = getRemainingChecklistTitles();
      setStatus(
        `${route.name} for ${groupProfiles[groupNeed].label} is not confirmed yet. Still needed: ${remainingTitles.join("; ")}.`,
        "warning",
        { focus: true },
      );
      return;
    }

    confirmedRouteId = route.id;
    renderSummary(route);
    setStatus(
      `${groupProfiles[groupNeed].label} / ${route.name} confirmed. The summary above is ready to share with the group.`,
      "success",
      { focus: true },
    );
  });
}

async function init() {
  try {
    routes = await loadRoutes();
    checklistState = Object.fromEntries(routes.map((route) => [route.id, {}]));
    selectedRouteId = chooseDefaultRoute(getSelectedGroup());
    renderRouteChoices();
    syncSelectedRoute();
    attachEvents();
    plannerRoot.hidden = false;
    document.body.classList.add("app-ready");
  } catch (error) {
    console.error(error);
    setStatus("Interactive planner unavailable. Static route notes remain below.", "warning");
  }
}

init();
