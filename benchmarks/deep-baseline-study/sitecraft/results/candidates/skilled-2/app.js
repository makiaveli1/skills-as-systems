const GROUP_LABELS = {
  mixed: "Mixed pace",
  child: "Child in group",
  experienced: "Experienced only",
};

const GROUP_AUDIENCE = {
  mixed: "a mixed-pace group",
  child: "a group with a child",
  experienced: "an experienced group",
};

const SUITABILITY_RANK = {
  "best fit": 4,
  "strong fit": 3,
  "gentle option": 2,
  "not advised": 1,
  "not today": 0,
};

const UNSUITABLE_SUITABILITY = new Set(["not advised", "not today"]);

const routeGuidance = {
  mixed: {
    "rowan-loop": {
      fit: "Best fit for a mixed-pace group that needs dependable footing, signal, and early turn-back options.",
      window: "Leave within the first hour; the sheltered line stays manageable.",
      watch:
        "Keep the boardwalk pace steady, call slick timber early, and use the sheltered bends for regrouping.",
      share:
        "Rowan Loop: 4.8 km, sheltered, reliable signal, and two early turn-back points. Best shared line for a mixed-pace group today.",
      essentials: [
        {
          title: "Light waterproof shell.",
          body: "Why it matters: light rain is still likely even on the sheltered line.",
        },
        {
          title: "Footwear with grip on wet timber.",
          body: "Why it matters: the boardwalk will decide confidence before the group settles into rhythm.",
        },
        {
          title: "One shared turnaround rule.",
          body: "Why it matters: mixed pace stays manageable only if regrouping happens before the gap widens.",
        },
        {
          title: "Simple check-in message.",
          body: "Why it matters: reliable signal makes it easy to keep late joiners aligned with the plan.",
        },
      ],
    },
    "bracken-rise": {
      fit: "Closed today and removed from live planning, even though its terrain is still worth comparing.",
      window: "No set-off window while the ranger closure remains in force.",
      watch:
        "Do not brief this as the active plan; move the group back to an open route before agreeing timings.",
      share:
        "Bracken Rise is closed today because the damaged footbridge shuts the north approach. Compare it if useful, but do not plan around it.",
      essentials: [
        {
          title: "Choose a different active route.",
          body: "Why it matters: the closure applies before group pace or skill even becomes relevant.",
        },
        {
          title: "Keep the terrain note for future planning.",
          body: "Why it matters: the ridge and wet-stone descent still matter when the route reopens.",
        },
        {
          title: "Reset the group expectation early.",
          body: "Why it matters: several testers tried to pick this route after closure because the status was too easy to miss.",
        },
        {
          title: "Share the ranger update, not only the route name.",
          body: "Why it matters: the reason for closure prevents accidental fallback planning.",
        },
      ],
    },
    "tor-line": {
      fit: "Not advised for a mixed-pace group: the exposure, scrambles, and signal loss concentrate risk too quickly.",
      window: "Only consider an early start if the full group changes to experienced walkers.",
      watch:
        "The route moves at the pace of the least secure climber, so mixed confidence turns the scrambles into a planning fault line.",
      share:
        "Tor Line is open, but it is not advised for a mixed-pace group today: 12.6 km, 780 m ascent, no signal for 6 km, and two steep scrambles.",
      essentials: [
        {
          title: "Reject casual sign-up.",
          body: "Why it matters: one uncertain walker changes the risk profile for everyone on the scrambles.",
        },
        {
          title: "Name the signal loss before departure.",
          body: "Why it matters: mixed groups often assume they can solve timing problems by phone later.",
        },
        {
          title: "Keep an easier fallback ready.",
          body: "Why it matters: the route is open, but openness is not the same as suitability.",
        },
        {
          title: "Treat the gust forecast as a hard limit.",
          body: "Why it matters: exposure after 14:00 narrows recovery options fast.",
        },
      ],
    },
  },
  child: {
    "rowan-loop": {
      fit: "Best fit when one child sets the pace and the coordinator still needs a clear, low-friction plan.",
      window: "Start early enough to use the two turn-back points before attention and energy dip.",
      watch:
        "Use the landmarks as progress markers and call slippery boards before the child reaches them.",
      share:
        "Rowan Loop: child-friendly by today’s standards, with shelter, landmarks, reliable signal, and early turn-back points. Keep the pace steady, not rushed.",
      essentials: [
        {
          title: "One warm layer the child can add quickly.",
          body: "Why it matters: stops happen more often, even on a short sheltered line.",
        },
        {
          title: "Grip-first footwear.",
          body: "Why it matters: the boardwalk is the route section most likely to unsettle a child walker.",
        },
        {
          title: "A simple landmark game or checkpoint count.",
          body: "Why it matters: frequent markers keep the route feeling measurable instead of endless.",
        },
        {
          title: "Clear early turnaround promise.",
          body: "Why it matters: confidence stays higher when the group knows it can stop without failure.",
        },
      ],
    },
    "bracken-rise": {
      fit: "Closed today and unsuitable for child-inclusive planning even before the closure.",
      window: "No set-off window while the closure remains in place.",
      watch:
        "Keep this strictly in comparison mode; the closure and the wet descent both rule it out for today’s group.",
      share:
        "Bracken Rise is closed today due to the damaged footbridge and is not a child-inclusive fallback. Choose an open route instead.",
      essentials: [
        {
          title: "Rule it out immediately.",
          body: "Why it matters: the closure removes any live planning value for a child-inclusive group.",
        },
        {
          title: "Explain the closure reason to the full group.",
          body: "Why it matters: a child hearing only the route name may assume it remains an option.",
        },
        {
          title: "Use the comparison only for future judgement.",
          body: "Why it matters: terrain and timing context still help the organiser learn the options.",
        },
        {
          title: "Return to an open sheltered route.",
          body: "Why it matters: pace protection matters more than ambition here.",
        },
      ],
    },
    "tor-line": {
      fit: "Not advised with a child in the group: the scrambles, signal loss, and exposure make recovery too hard.",
      window: "No practical child-inclusive set-off window today.",
      watch:
        "Exposure and loose rock leave too little margin if pace drops or confidence breaks on the scrambles.",
      share:
        "Tor Line is open but not advised for a child-inclusive group: long exposure, two scrambles, and no signal for 6 km.",
      essentials: [
        {
          title: "Do not treat openness as permission.",
          body: "Why it matters: the route stays technically open while still being the wrong call for this group.",
        },
        {
          title: "Protect the child’s footing first.",
          body: "Why it matters: loose rock and steep moves are where the route becomes unforgiving.",
        },
        {
          title: "Keep signal-dependent safety assumptions out of the plan.",
          body: "Why it matters: 6 km without signal removes an easy recovery channel.",
        },
        {
          title: "Move the group to Rowan Loop or stand down.",
          body: "Why it matters: suitability, not difficulty labels alone, should drive the choice.",
        },
      ],
    },
  },
  experienced: {
    "rowan-loop": {
      fit: "A gentle option for experienced walkers who want an easy-weather, low-friction circuit instead of a bigger day.",
      window: "Flexible start window; weather stays manageable, but wet boards still deserve attention.",
      watch:
        "Do not let the modest distance hide the slippery boardwalk and the likelihood of relaxed pacing.",
      share:
        "Rowan Loop stays open as the gentle option: 4.8 km, 120 m ascent, reliable signal, and easy recovery if the weather worsens.",
      essentials: [
        {
          title: "Grip still matters on the boardwalk.",
          body: "Why it matters: experienced walkers are most likely to underestimate the one slick feature on the easy line.",
        },
        {
          title: "Use it deliberately as the lighter-day option.",
          body: "Why it matters: the route works best when the group wants a shorter outing, not a compromised big day.",
        },
        {
          title: "Keep the simple check-in message.",
          body: "Why it matters: reliable signal makes it the cleanest fallback if timing shifts later.",
        },
        {
          title: "Let the landmarks set an efficient pace.",
          body: "Why it matters: the route repays tidy pacing more than technical preparation.",
        },
      ],
    },
    "bracken-rise": {
      fit: "Normally a stronger half-day option, but closed today so it cannot become the active plan.",
      window: "No set-off window until the footbridge closure is lifted.",
      watch:
        "Keep the route in comparison mode only; the status, not the group's skill, is the blocker.",
      share:
        "Bracken Rise would suit experienced walkers better than mixed groups, but it is closed today because the damaged footbridge shuts the north approach.",
      essentials: [
        {
          title: "Respect the closure as absolute.",
          body: "Why it matters: route skill does not override infrastructure closure.",
        },
        {
          title: "Retain the terrain note for reopening.",
          body: "Why it matters: wet stone on descent still shapes the future risk picture.",
        },
        {
          title: "Switch planning energy to Tor Line or Rowan Loop.",
          body: "Why it matters: comparison helps, but only open routes can carry a live plan.",
        },
        {
          title: "Share the closure reason in the group message.",
          body: "Why it matters: it prevents people suggesting Bracken Rise as a late fallback.",
        },
      ],
    },
    "tor-line": {
      fit: "Strong fit for experienced walkers prepared for a long exposed day with no signal and two steep scrambles.",
      window: "Start early enough to clear the exposed ground before gusts build after 14:00.",
      watch:
        "Treat the scrambles and signal loss as the real commitment markers, not the headline distance alone.",
      share:
        "Tor Line: strong experienced-walker option today. 12.6 km, 780 m ascent, no signal for 6 km, loose rock, two scrambles, and an early-start requirement.",
      essentials: [
        {
          title: "Early-start discipline.",
          body: "Why it matters: the gust forecast after 14:00 is the day’s hard constraint.",
        },
        {
          title: "Offline timing plan.",
          body: "Why it matters: there is no signal buffer once the group commits to the middle section.",
        },
        {
          title: "Extra food and water margin.",
          body: "Why it matters: the long exposed day offers few graceful exits if the pace drifts.",
        },
        {
          title: "Shared scramble order.",
          body: "Why it matters: confident movement matters most where the route steepens abruptly.",
        },
      ],
    },
  },
};

function buildRouteRecords(root = document) {
  return Array.from(root.querySelectorAll("[data-route-section]")).map((record) => ({
    id: record.dataset.routeId,
    name: record.dataset.name,
    difficulty: record.dataset.difficulty,
    distance: record.dataset.distance,
    duration: record.dataset.duration,
    ascent: record.dataset.ascent,
    weather: record.dataset.weather,
    terrain: record.dataset.terrain,
    signal: record.dataset.signal,
    status: record.dataset.status,
    why: record.dataset.why,
    suitability: {
      mixed: record.dataset.suitabilityMixed,
      child: record.dataset.suitabilityChild,
      experienced: record.dataset.suitabilityExperienced,
    },
  }));
}

function getRouteById(routes, routeId) {
  return routes.find((route) => route.id === routeId);
}

function canConfirmRoute(route) {
  return route?.status === "open";
}

function isRouteSuitableForGroup(route, groupNeed) {
  return !UNSUITABLE_SUITABILITY.has(route?.suitability?.[groupNeed]);
}

function isRouteEligible(route, groupNeed) {
  return canConfirmRoute(route) && isRouteSuitableForGroup(route, groupNeed);
}

function getVisibleRoutes(routes, filter) {
  return routes.filter((route) => filter === "all" || route.difficulty === filter);
}

function getVisibleEligibleRoutes(routes, filter, groupNeed) {
  return getVisibleRoutes(routes, filter).filter((route) => isRouteEligible(route, groupNeed));
}

function chooseDefaultRoute(routes, groupNeed) {
  return routes
    .filter((route) => isRouteEligible(route, groupNeed))
    .sort((left, right) => {
      const rankDifference =
        SUITABILITY_RANK[right.suitability[groupNeed]] - SUITABILITY_RANK[left.suitability[groupNeed]];

      if (rankDifference !== 0) {
        return rankDifference;
      }

      return Number(left.distance) - Number(right.distance);
    })[0]?.id;
}

function buildAutoSelectionAnnouncement({
  routes,
  previousFilter,
  nextFilter,
  previousSelectedId,
  nextSelectedId,
  groupNeed,
  clearedConfirmation,
}) {
  const previousRoute = getRouteById(routes, previousSelectedId);
  const nextRoute = getRouteById(routes, nextSelectedId);
  const reasons = [];

  if (previousFilter !== nextFilter && previousFilter !== "all") {
    reasons.push(`no open ${previousFilter} routes fit ${GROUP_AUDIENCE[groupNeed]}`);
  }

  if (previousRoute && previousRoute.id !== nextRoute?.id) {
    if (previousRoute.status === "closed") {
      reasons.push(`${previousRoute.name} is closed today`);
    } else if (!isRouteSuitableForGroup(previousRoute, groupNeed)) {
      reasons.push(`${previousRoute.name} is not advised for ${GROUP_AUDIENCE[groupNeed]}`);
    } else {
      reasons.push(`${previousRoute.name} is no longer available in the current view`);
    }
  }

  if (!nextRoute || reasons.length === 0) {
    return null;
  }

  const confirmationSuffix = clearedConfirmation
    ? " Reconfirm the updated plan after checking the essentials."
    : "";

  return `${nextRoute.name} is now selected because ${reasons.join(" and ")}.${confirmationSuffix}`;
}

function reconcileContextChange(routes, state) {
  const previousSelectedId = state.selectedId;
  const previousFilter = state.filter;
  let nextFilter = state.filter;
  let eligibleVisibleRoutes = getVisibleEligibleRoutes(routes, nextFilter, state.groupNeed);

  if (eligibleVisibleRoutes.length === 0) {
    nextFilter = "all";
    eligibleVisibleRoutes = getVisibleEligibleRoutes(routes, nextFilter, state.groupNeed);
  }

  const currentSelectedEligible = eligibleVisibleRoutes.some((route) => route.id === state.selectedId);

  if (!currentSelectedEligible) {
    state.selectedId = eligibleVisibleRoutes[0]?.id ?? chooseDefaultRoute(routes, state.groupNeed);
  }

  const confirmedRoute = getRouteById(routes, state.confirmedId);
  const confirmedStillEligible = confirmedRoute
    ? eligibleVisibleRoutes.some((route) => route.id === confirmedRoute.id)
    : false;
  const clearedConfirmation = Boolean(state.confirmedId) && !confirmedStillEligible;

  if (clearedConfirmation) {
    state.confirmedId = null;
  }

  state.filter = nextFilter;

  if (state.selectedId !== previousSelectedId || nextFilter !== previousFilter || clearedConfirmation) {
    state.statusOverride = buildAutoSelectionAnnouncement({
      routes,
      previousFilter,
      nextFilter,
      previousSelectedId,
      nextSelectedId: state.selectedId,
      groupNeed: state.groupNeed,
      clearedConfirmation,
    });
    state.statusOverrideWarning = true;
  }

  return {
    selectedId: state.selectedId,
    filter: state.filter,
    confirmedId: state.confirmedId,
    statusOverride: state.statusOverride,
  };
}

function getSuitabilityLabel(route, groupNeed) {
  const audience = GROUP_AUDIENCE[groupNeed];
  const suitability = route.suitability[groupNeed];

  switch (suitability) {
    case "best fit":
      return `Best fit for ${audience}.`;
    case "strong fit":
      return `Strong fit for ${audience}.`;
    case "gentle option":
      return `Gentle option for ${audience}.`;
    case "not advised":
      return `Not advised for ${audience}.`;
    case "not today":
    default:
      return `Not available for ${audience} today.`;
  }
}

function getSummaryModel(route, groupNeed) {
  const guidance = routeGuidance[groupNeed][route.id];
  const isClosed = route.status === "closed";

  return {
    title: route.name,
    groupLabel: GROUP_LABELS[groupNeed],
    fit: guidance.fit,
    status: isClosed ? `Closed today. ${route.why}` : `Open. ${getSuitabilityLabel(route, groupNeed)}`,
    window: guidance.window,
    duration: `${route.duration} across ${route.distance} km`,
    terrain: route.terrain,
    signal: route.signal,
    why: isClosed ? `Closure reason: ${route.why}` : `Why this route: ${route.why}`,
    watch: guidance.watch,
    share: guidance.share,
    essentials: guidance.essentials,
    isClosed,
  };
}

function getConfirmButtonModel(routes, state) {
  const selectedRoute = getRouteById(routes, state.selectedId);
  const disabled = !canConfirmRoute(selectedRoute);
  const confirmed = state.confirmedId === state.selectedId && !disabled;

  if (disabled) {
    return {
      label: "Closed route cannot be confirmed",
      disabled: true,
      confirmed: false,
    };
  }

  if (confirmed) {
    return {
      label: "Group plan confirmed",
      disabled: false,
      confirmed: true,
    };
  }

  return {
    label: `Mark ${selectedRoute.name} as the group plan`,
    disabled: false,
    confirmed: false,
  };
}

function getPlanStatusMessage(routes, state) {
  if (state.statusOverride) {
    return {
      text: state.statusOverride,
      isWarning: state.statusOverrideWarning,
    };
  }

  const selectedRoute = getRouteById(routes, state.selectedId);
  const confirmedRoute = getRouteById(routes, state.confirmedId);
  const selectedAudience = GROUP_AUDIENCE[state.groupNeed];
  const selectedSuitability = selectedRoute.suitability[state.groupNeed];

  if (!state.confirmedId) {
    if (!canConfirmRoute(selectedRoute)) {
      return {
        text: `${selectedRoute.name} is closed today and cannot become the group plan. Compare it here, then choose an open route.`,
        isWarning: true,
      };
    }

    return {
      text: `${selectedRoute.name} selected for ${selectedAudience}. Confirm it to lock the shared plan.`,
      isWarning: selectedSuitability === "not advised",
    };
  }

  if (state.confirmedId === state.selectedId) {
    if (selectedSuitability === "not advised") {
      return {
        text: `${selectedRoute.name} remains confirmed, but it is not advised for ${selectedAudience}. Review before setting off.`,
        isWarning: true,
      };
    }

    return {
      text: `${selectedRoute.name} confirmed for ${selectedAudience}. Share the line, watchpoint, and essentials before setting off.`,
      isWarning: false,
    };
  }

  if (!canConfirmRoute(selectedRoute)) {
    return {
      text: `${confirmedRoute.name} remains the confirmed plan. ${selectedRoute.name} is closed today and cannot replace it.`,
      isWarning: true,
    };
  }

  return {
    text: `${confirmedRoute.name} remains confirmed. ${selectedRoute.name} is selected for ${selectedAudience}; confirm it only if the group plan has changed.`,
    isWarning: selectedSuitability === "not advised",
  };
}

function getMissingEssentialTitles(essentials, checkedEssentials) {
  return essentials
    .filter((item, index) => !checkedEssentials.has(index))
    .map((item) => item.title);
}

function confirmSelectedRoute(routes, state, essentials) {
  const selectedRoute = getRouteById(routes, state.selectedId);

  if (!canConfirmRoute(selectedRoute)) {
    return {
      ok: false,
      reason: "closed",
      statusText: `${selectedRoute.name} is closed today and cannot be confirmed. Choose an open route instead.`,
      isWarning: true,
    };
  }

  const missingEssentials = getMissingEssentialTitles(essentials, state.checkedEssentials);

  if (missingEssentials.length > 0) {
    return {
      ok: false,
      reason: "essentials",
      statusText: `Still to check for ${selectedRoute.name} / ${GROUP_LABELS[state.groupNeed]}: ${missingEssentials.join(
        "; "
      )}.`,
      isWarning: true,
    };
  }

  state.confirmedId = selectedRoute.id;
  return {
    ok: true,
    reason: "confirmed",
    statusText: `Plan confirmed: ${selectedRoute.name} for ${GROUP_LABELS[state.groupNeed]}. All essentials checked and ready to share.`,
    isWarning: false,
  };
}

function getNextOpenRouteId(routeChoices, routes, currentId, direction) {
  if (routeChoices.length === 0) {
    return currentId;
  }

  const currentIndex = routeChoices.findIndex((choice) => choice.dataset.routeId === currentId);

  if (currentIndex === -1) {
    return currentId;
  }

  for (let step = 1; step <= routeChoices.length; step += 1) {
    const nextIndex =
      direction === "next"
        ? (currentIndex + step) % routeChoices.length
        : (currentIndex - step + routeChoices.length) % routeChoices.length;
    const candidateId = routeChoices[nextIndex].dataset.routeId;
    const candidateRoute = getRouteById(routes, candidateId);

    if (!routeChoices[nextIndex].classList.contains("is-hidden") && canConfirmRoute(candidateRoute)) {
      return candidateId;
    }
  }

  return currentId;
}

function createApp(root = document) {
  const routeRecords = buildRouteRecords(root);
  const routeList = root.querySelector("[data-testid='route-list']");
  const routeChoices = Array.from(routeList.querySelectorAll("[data-route-id]"));
  const routeSections = Array.from(root.querySelectorAll("[data-route-section]"));
  const filterChips = Array.from(root.querySelectorAll("[data-filter]"));
  const groupNeedInputs = Array.from(root.querySelectorAll("input[name='group-needs']"));
  const summaryGroup = root.getElementById("summary-group");
  const summaryTitle = root.getElementById("summary-title");
  const summaryFit = root.getElementById("summary-fit");
  const summaryStatus = root.getElementById("summary-status");
  const summaryWindow = root.getElementById("summary-window");
  const summaryDuration = root.getElementById("summary-duration");
  const summaryTerrain = root.getElementById("summary-terrain");
  const summarySignal = root.getElementById("summary-signal");
  const summaryWhy = root.getElementById("summary-why");
  const summaryWatch = root.getElementById("summary-watch");
  const summaryShare = root.getElementById("summary-share");
  const essentialsList = root.getElementById("essentials-list");
  const confirmPlan = root.querySelector("[data-testid='confirm-plan']");
  const planStatus = root.getElementById("plan-status");
  const planSummary = root.getElementById("plan-summary");

  const routeChoiceViews = new Map(
    routeChoices.map((choice) => [
      choice.dataset.routeId,
      {
        element: choice,
        status: choice.querySelector("[data-route-status]"),
        suitability: choice.querySelector("[data-route-suitability]"),
      },
    ])
  );

  const state = {
    filter: "all",
    groupNeed: "mixed",
    selectedId: chooseDefaultRoute(routeRecords, "mixed"),
    confirmedId: null,
    checkedEssentials: new Set(),
    essentialsKey: "",
    statusOverride: null,
    statusOverrideWarning: false,
  };

  function renderEssentials(items) {
    const nextEssentialsKey = `${state.selectedId}:${state.groupNeed}`;

    if (state.essentialsKey !== nextEssentialsKey) {
      state.essentialsKey = nextEssentialsKey;
      state.checkedEssentials = new Set();
    }

    essentialsList.replaceChildren();

    items.forEach((item, index) => {
      const li = root.createElement("li");
      const label = root.createElement("label");
      const input = root.createElement("input");
      const copy = root.createElement("span");
      const strong = root.createElement("strong");

      label.className = "essential-item";
      input.className = "essential-item__check";
      input.type = "checkbox";
      input.checked = state.checkedEssentials.has(index);
      input.addEventListener("change", () => {
        state.statusOverride = null;
        state.statusOverrideWarning = false;

        if (input.checked) {
          state.checkedEssentials.add(index);
        } else {
          state.checkedEssentials.delete(index);
        }

        renderConfirmationState();
      });

      copy.className = "essential-item__copy";
      strong.textContent = item.title;
      copy.append(strong, ` ${item.body}`);
      label.append(input, copy);
      li.append(label);
      essentialsList.append(li);
    });
  }

  function renderSummary() {
    const route = getRouteById(routeRecords, state.selectedId);
    const model = getSummaryModel(route, state.groupNeed);

    summaryGroup.textContent = model.groupLabel;
    summaryTitle.textContent = model.title;
    summaryFit.textContent = model.fit;
    summaryStatus.textContent = model.status;
    summaryWindow.textContent = model.window;
    summaryDuration.textContent = model.duration;
    summaryTerrain.textContent = model.terrain;
    summarySignal.textContent = model.signal;
    summaryWhy.textContent = model.why;
    summaryWatch.textContent = model.watch;
    summaryShare.textContent = model.share;
    planSummary.classList.toggle("is-closed", model.isClosed);
    renderEssentials(model.essentials);
  }

  function renderRouteStates() {
    routeChoices.forEach((choice) => {
      const route = getRouteById(routeRecords, choice.dataset.routeId);
      const view = routeChoiceViews.get(route.id);
      const isVisible = state.filter === "all" || choice.dataset.difficulty === state.filter;
      const isSelected = route.id === state.selectedId;

      view.element.classList.toggle("is-selected", isSelected);
      view.element.classList.toggle("is-hidden", !isVisible);
      view.element.classList.toggle("is-closed", route.status === "closed");
      view.element.setAttribute("aria-pressed", String(isSelected));
      view.status.textContent = route.status === "closed" ? "Closed today" : "Open";
      view.status.classList.toggle("route-choice__status--closed", route.status === "closed");
      view.suitability.textContent = getSuitabilityLabel(route, state.groupNeed);
    });

    routeSections.forEach((section) => {
      const route = getRouteById(routeRecords, section.dataset.routeId);
      const isVisible = state.filter === "all" || section.dataset.difficulty === state.filter;
      const isSelected = route.id === state.selectedId;
      section.classList.toggle("is-hidden", !isVisible);
      section.setAttribute("aria-current", isSelected ? "true" : "false");
    });

    filterChips.forEach((chip) => {
      chip.classList.toggle("is-active", chip.dataset.filter === state.filter);
      chip.setAttribute("aria-current", chip.dataset.filter === state.filter ? "true" : "false");
    });

    groupNeedInputs.forEach((input) => {
      input.checked = input.value === state.groupNeed;
    });
  }

  function renderConfirmationState() {
    const buttonModel = getConfirmButtonModel(routeRecords, state);
    const statusModel = getPlanStatusMessage(routeRecords, state);

    confirmPlan.textContent = buttonModel.label;
    confirmPlan.classList.toggle("is-confirmed", buttonModel.confirmed);
    confirmPlan.classList.toggle("is-disabled", buttonModel.disabled);
    confirmPlan.setAttribute("aria-disabled", String(buttonModel.disabled));
    planStatus.textContent = statusModel.text;
    planStatus.classList.toggle("is-warning", statusModel.isWarning);
  }

  function render({ reconcile = false } = {}) {
    if (reconcile) {
      reconcileContextChange(routeRecords, state);
    }

    renderRouteStates();
    renderSummary();
    renderConfirmationState();
  }

  function activateSelection(routeId, { focusSummary = false } = {}) {
    state.statusOverride = null;
    state.statusOverrideWarning = false;
    state.selectedId = routeId;
    render();

    if (focusSummary) {
      planSummary.focus();
    }
  }

  routeChoices.forEach((choice) => {
    choice.addEventListener("click", (event) => {
      event.preventDefault();
      activateSelection(choice.dataset.routeId, { focusSummary: true });
    });

    choice.addEventListener("keydown", (event) => {
      if (event.key === " ") {
        event.preventDefault();
        activateSelection(choice.dataset.routeId, { focusSummary: true });
        return;
      }

      if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
        event.preventDefault();
        state.statusOverride = null;
        state.statusOverrideWarning = false;
        const nextRouteId = getNextOpenRouteId(
          routeChoices,
          routeRecords,
          choice.dataset.routeId,
          event.key === "ArrowRight" ? "next" : "previous"
        );
        activateSelection(nextRouteId);
        routeChoiceViews.get(nextRouteId)?.element.focus();
      }
    });
  });

  filterChips.forEach((chip) => {
    chip.addEventListener("click", (event) => {
      event.preventDefault();
      state.statusOverride = null;
      state.statusOverrideWarning = false;
      state.filter = chip.dataset.filter;
      render({ reconcile: true });
    });

    chip.addEventListener("keydown", (event) => {
      if (event.key === " ") {
        event.preventDefault();
        state.statusOverride = null;
        state.statusOverrideWarning = false;
        state.filter = chip.dataset.filter;
        render({ reconcile: true });
      }
    });
  });

  groupNeedInputs.forEach((input) => {
    input.addEventListener("change", () => {
      state.statusOverride = null;
      state.statusOverrideWarning = false;
      state.groupNeed = input.value;
      state.confirmedId = null;
      render({ reconcile: true });
    });
  });

  function handleConfirm(event) {
    event.preventDefault();
    state.statusOverride = null;
    state.statusOverrideWarning = false;
    const activeEssentials = routeGuidance[state.groupNeed][state.selectedId].essentials;
    const outcome = confirmSelectedRoute(routeRecords, state, activeEssentials);
    state.statusOverride = outcome.statusText;
    state.statusOverrideWarning = outcome.isWarning;
    renderConfirmationState();
    planStatus.focus();
    planStatus.scrollIntoView({ block: "nearest" });
  }

  confirmPlan.addEventListener("click", handleConfirm);
  confirmPlan.addEventListener("keydown", (event) => {
    if (event.key === " ") {
      handleConfirm(event);
    }
  });

  render({ reconcile: true });

  return { routeRecords, state, render };
}

if (typeof document !== "undefined") {
  createApp(document);
}

if (typeof module !== "undefined") {
  module.exports = {
    GROUP_LABELS,
    GROUP_AUDIENCE,
    SUITABILITY_RANK,
    UNSUITABLE_SUITABILITY,
    buildRouteRecords,
    canConfirmRoute,
    isRouteSuitableForGroup,
    isRouteEligible,
    getVisibleRoutes,
    getVisibleEligibleRoutes,
    chooseDefaultRoute,
    reconcileContextChange,
    getSuitabilityLabel,
    getSummaryModel,
    getConfirmButtonModel,
    getPlanStatusMessage,
    getMissingEssentialTitles,
    confirmSelectedRoute,
    getNextOpenRouteId,
  };
}
