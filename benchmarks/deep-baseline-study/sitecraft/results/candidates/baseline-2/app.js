(function () {
  const root = document.documentElement;
  root.classList.remove("no-js");

  const dataNode = document.getElementById("route-data");
  if (!dataNode) {
    return;
  }

  let routes;
  try {
    routes = JSON.parse(dataNode.textContent);
  } catch (error) {
    return;
  }

  const state = {
    filter: "all",
    groupNeeds: "mixed",
    selectedId: null,
  };

  const groupMeta = {
    mixed: {
      label: "Mixed group",
      fitLead: "Plan for the least experienced walker first and treat cohesion as the priority.",
      paceLabel: "The group agrees to walk to the slowest safe pace.",
      paceWhy:
        "This keeps the mixed group together and stops early fatigue from turning into poor decisions later.",
    },
    child: {
      label: "Group with child",
      fitLead: "Short duration, shelter, and easy turn-back points matter more than ambition today.",
      paceLabel: "The child sets the rhythm and the whole group accepts the slower pace.",
      paceWhy:
        "Children burn energy unevenly, so the plan has to stay comfortable before attention and footing drop.",
    },
    experienced: {
      label: "Experienced group",
      fitLead: "Experienced walkers can take on more ground, but closures and comms gaps still overrule ambition.",
      paceLabel: "The group agrees its pace still leaves margin for exposure, stops, and a clean turnaround.",
      paceWhy:
        "A capable group can move faster, but only if it protects the time margin that keeps the route honest.",
    },
  };

  const routeChoices = Array.from(document.querySelectorAll("[data-route-id][role='button']"));
  const routeCards = Array.from(document.querySelectorAll("[data-route-card]"));
  const filterButtons = Array.from(document.querySelectorAll("[data-filter]"));
  const groupRadios = Array.from(document.querySelectorAll("input[name='group-needs']"));
  const form = document.getElementById("plan-form");
  const checklist = Array.from(form.querySelectorAll("input[type='checkbox']"));
  const confirmButton = form.querySelector("[data-testid='confirm-plan']");
  const status = document.getElementById("plan-status");

  const guideNodes = new Map(
    Array.from(document.querySelectorAll("[data-route-guide]")).map((node) => [node.dataset.routeGuide, node])
  );
  const fitNodes = new Map(
    Array.from(document.querySelectorAll("[data-route-fit]")).map((node) => [node.dataset.routeFit, node])
  );
  const noteNodes = new Map(
    Array.from(document.querySelectorAll("[data-route-note]")).map((node) => [node.dataset.routeNote, node])
  );
  const statusBadgeNodes = new Map(
    Array.from(document.querySelectorAll("[data-route-status-badge]")).map((node) => [
      node.dataset.routeStatusBadge,
      node,
    ])
  );

  const routeMap = new Map(routes.map((route) => [route.id, route]));

  const summary = {
    group: document.querySelector("[data-summary-group]"),
    name: document.querySelector("[data-summary-name]"),
    fit: document.querySelector("[data-summary-fit]"),
    status: document.querySelector("[data-summary-status]"),
    suitability: document.querySelector("[data-summary-suitability]"),
    demand: document.querySelector("[data-summary-demand]"),
    terrain: document.querySelector("[data-summary-terrain]"),
    weather: document.querySelector("[data-summary-weather]"),
    signal: document.querySelector("[data-summary-signal]"),
    why: document.querySelector("[data-summary-why]"),
    departure: document.querySelector("[data-summary-departure]"),
  };

  const essentials = {
    paceLabel: document.querySelector("[data-essential-pace-label]"),
    paceWhy: document.querySelector("[data-essential-pace-why]"),
    checkinWhy: document.querySelector("[data-essential-checkin-why]"),
    routeLabel: document.querySelector("[data-route-essential]"),
    routeWhy: document.querySelector("[data-route-essential-why]"),
  };

  initializeSelection();
  bindEvents();
  render();

  function bindEvents() {
    routeChoices.forEach((choice) => {
      choice.addEventListener("click", (event) => {
        event.preventDefault();
        handleRouteIntent(choice.dataset.routeId);
      });

      choice.addEventListener("keydown", (event) => {
        if (event.key === "ArrowRight" || event.key === "ArrowLeft") {
          event.preventDefault();
          moveRouteSelection(choice.dataset.routeId, event.key === "ArrowRight" ? 1 : -1);
          return;
        }

        if (event.key === " " || event.key === "Enter") {
          event.preventDefault();
          handleRouteIntent(choice.dataset.routeId);
        }
      });
    });

    filterButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.filter === state.filter));
      button.addEventListener("click", () => {
        const previousId = state.selectedId;
        state.filter = button.dataset.filter;
        const normalization = normalizeSelection(previousId);
        render();
        announceNormalization(normalization, `Showing ${filterLabel(state.filter)} routes.`);
      });
    });

    groupRadios.forEach((radio) => {
      radio.addEventListener("change", () => {
        if (!radio.checked) {
          return;
        }

        const previousId = state.selectedId;
        state.groupNeeds = radio.value;
        const normalization = normalizeSelection(previousId);
        render();
        announceNormalization(normalization, `${groupMeta[state.groupNeeds].label} lens applied.`);
      });
    });

    checklist.forEach((checkbox) => {
      checkbox.addEventListener("change", () => {
        setDefaultStatus();
      });
    });

    form.addEventListener("submit", (event) => {
      event.preventDefault();

      const route = selectedRoute();
      if (!route || !isSelectable(route)) {
        setStatus("Choose an open route before confirming the field plan.", "is-error", true);
        return;
      }

      const unchecked = checklist.filter((checkbox) => !checkbox.checked);
      if (unchecked.length > 0) {
        setStatus(`Complete these essentials: ${remainingEssentials(unchecked).join("; ")}.`, "is-error", true);
        return;
      }

      setStatus(planMessage(route), "is-success", true);
    });
  }

  function initializeSelection() {
    const initialHash = window.location.hash.replace("#route-", "");
    if (routeMap.has(initialHash) && isSelectable(routeMap.get(initialHash))) {
      state.selectedId = initialHash;
      return;
    }

    state.selectedId = bestAvailableRouteId(visibleOpenRoutes()) || null;
  }

  function visibleRoutes() {
    return routes.filter((route) => state.filter === "all" || route.difficulty === state.filter);
  }

  function visibleOpenRoutes() {
    return visibleRoutes().filter(isSelectable);
  }

  function selectedRoute() {
    return state.selectedId ? routeMap.get(state.selectedId) : null;
  }

  function isSelectable(route) {
    return route && route.status === "open";
  }

  function isSuitable(route) {
    return route && suitabilityScore(suitabilityValue(route)) >= 2;
  }

  function suitabilityValue(route) {
    return route.suitability[state.groupNeeds];
  }

  function bestAvailableRouteId(candidates) {
    if (!candidates.length) {
      return null;
    }

    const suitableCandidates = candidates.filter(isSuitable);
    const pool = suitableCandidates.length ? suitableCandidates : candidates;

    return pool
      .slice()
      .sort((left, right) => {
        const scoreGap = suitabilityScore(right.suitability[state.groupNeeds]) - suitabilityScore(left.suitability[state.groupNeeds]);
        if (scoreGap !== 0) {
          return scoreGap;
        }

        return left.distance_km - right.distance_km;
      })[0].id;
  }

  function normalizeSelection(previousId) {
    const selected = selectedRoute();
    const previousRoute = previousId ? routeMap.get(previousId) : selected;
    const visible = visibleRoutes();
    const visibleOpen = visible.filter(isSelectable);
    const visibleOpenIds = new Set(visibleOpen.map((route) => route.id));
    const bestId = bestAvailableRouteId(visibleOpen);
    const selectedVisible = selected && visible.some((route) => route.id === selected.id);
    const selectedValid = selected && isSelectable(selected) && selectedVisible;
    const selectedSuitable = selectedValid && isSuitable(selected);

    if (selectedValid && selectedSuitable) {
      return { changed: false, routeId: state.selectedId, reason: null };
    }

    state.selectedId = bestId;

    return {
      changed: state.selectedId !== previousId,
      routeId: state.selectedId,
      reason: normalizationReason(previousRoute, selectedVisible, selectedValid, selectedSuitable, visibleOpenIds.size),
    };
  }

  function handleRouteIntent(routeId) {
    const route = routeMap.get(routeId);
    if (!route) {
      return;
    }

    if (!isSelectable(route)) {
      focusRouteCard(routeId);
      setStatus(`${route.name} is closed and cannot become the active plan. ${route.why}`, "is-error");
      return;
    }

    state.selectedId = routeId;
    render();

    if (window.history && typeof window.history.replaceState === "function") {
      window.history.replaceState(null, "", `#route-${routeId}`);
    }

    setDefaultStatus();
  }

  function render() {
    updateFilterControls();
    updateGroupControls();
    updateRouteViews();
    updateSummary();
    updateEssentials();
    updateConfirmState();
  }

  function updateFilterControls() {
    filterButtons.forEach((button) => {
      const active = button.dataset.filter === state.filter;
      button.classList.toggle("is-active", active);
      button.setAttribute("aria-pressed", String(active));
    });
  }

  function updateGroupControls() {
    groupRadios.forEach((radio) => {
      radio.checked = radio.value === state.groupNeeds;
      radio.parentElement.classList.toggle("is-active", radio.checked);
    });
  }

  function updateRouteViews() {
    const shownIds = new Set(visibleRoutes().map((route) => route.id));

    routeChoices.forEach((choice) => {
      const route = routeMap.get(choice.dataset.routeId);
      const selected = route && choice.dataset.routeId === state.selectedId;
      const visible = shownIds.has(choice.dataset.routeId);
      choice.hidden = !visible;
      choice.classList.toggle("is-selected", selected);
      choice.classList.toggle("is-closed", !isSelectable(route));
      choice.setAttribute("aria-pressed", String(selected));
      choice.setAttribute("aria-disabled", String(!isSelectable(route)));
      choice.tabIndex = visible ? 0 : -1;

      const guideNode = guideNodes.get(choice.dataset.routeId);
      if (guideNode && route) {
        guideNode.textContent = choiceGuide(route);
      }
    });

    routeCards.forEach((card) => {
      const route = routeMap.get(card.dataset.routeId);
      const selected = route && card.dataset.routeId === state.selectedId;
      const visible = shownIds.has(card.dataset.routeId);
      card.hidden = !visible;
      card.classList.toggle("is-selected", selected);
      card.classList.toggle("is-closed", route && !isSelectable(route));

      const fitNode = fitNodes.get(card.dataset.routeId);
      if (fitNode && route) {
        fitNode.textContent = routeFitText(route);
      }

      const noteNode = noteNodes.get(card.dataset.routeId);
      if (noteNode && route) {
        noteNode.textContent = routeNote(route);
      }

      const badgeNode = statusBadgeNodes.get(card.dataset.routeId);
      if (badgeNode && route) {
        badgeNode.textContent = capitalize(route.status);
        badgeNode.classList.toggle("is-open", route.status === "open");
        badgeNode.classList.toggle("is-closed", route.status !== "open");
      }
    });
  }

  function updateSummary() {
    const route = selectedRoute();
    summary.group.textContent = `Planning lens: ${groupMeta[state.groupNeeds].label}`;

    if (!route) {
      summary.name.textContent = "No open route";
      summary.fit.textContent = "The current filter leaves only closed routes. Compare them, then widen the filter to confirm a plan.";
      summary.status.textContent = "No active route available";
      summary.suitability.textContent = "No open route matches this view";
      summary.demand.textContent = "Adjust the ground filter to restore an open option.";
      summary.terrain.textContent = "Closed routes remain visible for comparison only.";
      summary.weather.textContent = "No weather call until an open route is selected.";
      summary.signal.textContent = "No comms call until an open route is selected.";
      summary.why.textContent = "The active plan cannot be closed.";
      summary.departure.textContent = "Choose an open route before agreeing a departure call.";
      return;
    }

    summary.name.textContent = route.name;
    summary.fit.textContent = `${groupMeta[state.groupNeeds].fitLead} ${suitabilitySentence(suitabilityValue(route), route)}`;
    summary.status.textContent = route.status === "open" ? "Open" : `Closed: ${route.why}`;
    summary.suitability.textContent = `${groupMeta[state.groupNeeds].label}: ${capitalizePhrase(suitabilityValue(route))}`;
    summary.demand.textContent = routeDemand(route);
    summary.terrain.textContent = route.terrain;
    summary.weather.textContent = route.weather;
    summary.signal.textContent = routeSignal(route);
    summary.why.textContent = route.why;
    summary.departure.textContent = routeDeparture(route);
  }

  function updateEssentials() {
    const route = selectedRoute();
    const group = groupMeta[state.groupNeeds];

    essentials.paceLabel.textContent = group.paceLabel;
    essentials.paceWhy.textContent = group.paceWhy;

    if (!route) {
      essentials.checkinWhy.textContent = "Pick an open route first so the group can agree a real check-in and turn-back point.";
      essentials.routeLabel.textContent = "Choose an open route before the final route-specific briefing.";
      essentials.routeWhy.textContent = "The specific ground warning depends on the route that can actually be confirmed.";
      return;
    }

    essentials.checkinWhy.textContent = checkinReason(route);
    essentials.routeLabel.textContent = routeEssentialLabel(route);
    essentials.routeWhy.textContent = routeEssentialWhy(route);
  }

  function updateConfirmState() {
    const route = selectedRoute();
    confirmButton.disabled = !route || !isSelectable(route);
  }

  function routeDemand(route) {
    return `${capitalize(route.difficulty)} / ${route.distance_km.toFixed(1)} km / ${route.duration} / ${route.ascent_m} m ascent`;
  }

  function routeSignal(route) {
    if (route.signal.toLowerCase() === "reliable") {
      return "Reliable signal throughout";
    }

    return route.signal;
  }

  function routeDeparture(route) {
    if (route.status !== "open") {
      return "Closed routes stay on the board for comparison only.";
    }

    if (route.id === "rowan-loop") {
      return "A good choice when the group needs short duration, shelter, and obvious turn-back options.";
    }

    if (route.id === "tor-line") {
      return "Commit early enough to stay ahead of the exposed gust window and keep the turnaround call strict.";
    }

    const match = route.weather.match(/after\s+(\d{1,2}:\d{2})/i);
    if (match) {
      return `Wait for the better weather window after ${match[1]} before committing.`;
    }

    return "Recheck the conditions at the trailhead before committing the group.";
  }

  function routeFitText(route) {
    return `${groupMeta[state.groupNeeds].label}: ${capitalizePhrase(suitabilityValue(route))}`;
  }

  function routeNote(route) {
    if (route.status !== "open") {
      return `Closed today. ${route.why}`;
    }

    return `${groupMeta[state.groupNeeds].label}: ${capitalizePhrase(suitabilityValue(route))}. ${route.why}`;
  }

  function choiceGuide(route) {
    if (route.status !== "open") {
      return "Closed today";
    }

    return `${shortGroupLabel(state.groupNeeds)}: ${suitabilityValue(route)}`;
  }

  function suitabilitySentence(value, route) {
    if (value === "best fit") {
      return `${route.name} is the best fit for this group.`;
    }

    if (value === "strong fit") {
      return `${route.name} is the strongest open option if the group wants the bigger day.`;
    }

    if (value === "gentle option") {
      return `${route.name} stays viable, but it will feel deliberately gentle for this group.`;
    }

    if (value === "not advised") {
      return `${route.name} is open, but the ground and duration are not advised for this group.`;
    }

    return `${route.name} is not available for planning today.`;
  }

  function checkinReason(route) {
    if (route.signal.toLowerCase() === "reliable") {
      return "Reliable signal and early decision points make it straightforward to turn back cleanly if the group fades.";
    }

    if (route.signal.toLowerCase().includes("none")) {
      return "No signal for part of the route means the turn-back point and outside check-in have to be agreed before departure.";
    }

    return "Patchy signal means the group needs a clear turn-back point and a named contact before the coverage drops.";
  }

  function routeEssentialLabel(route) {
    if (route.id === "rowan-loop") {
      return "Boardwalk footing and the sheltered turn-back options are called out before the group sets off.";
    }

    if (route.id === "tor-line") {
      return "The scrambles, loose rock, and no-signal stretch are called out before the group commits.";
    }

    return "The route-specific ground hazard is called out before the group sets off.";
  }

  function routeEssentialWhy(route) {
    if (route.id === "rowan-loop") {
      return "The hazards are moderate, but naming them upfront makes the first awkward moments predictable for new walkers and children.";
    }

    if (route.id === "tor-line") {
      return "This route only works if everyone understands the commitment before the group reaches the exposed ground.";
    }

    return "The key hazard should be named before departure so the group meets it with the right expectation.";
  }

  function planMessage(route) {
    return `${route.name} confirmed for ${groupMeta[state.groupNeeds].label.toLowerCase()}: ${capitalizePhrase(
      suitabilityValue(route)
    )}. ${route.distance_km.toFixed(1)} km, ${route.duration}, ${route.ascent_m} m ascent. ${route.weather}. ${route.terrain}. ${routeSignal(route)}.`;
  }

  function setDefaultStatus() {
    const route = selectedRoute();
    if (!route) {
      setStatus("Choose an open route before confirming the field plan.", "is-error");
      return;
    }

    setStatus("Review why each essential matters, then confirm the field plan.", "");
  }

  function setStatus(message, tone, moveFocus) {
    status.textContent = message;
    status.classList.remove("is-error", "is-success");

    if (tone) {
      status.classList.add(tone);
    }

    if (moveFocus) {
      focusStatus();
    }
  }

  function focusRouteCard(routeId) {
    const card = document.getElementById(`route-${routeId}`);
    if (!card) {
      return;
    }

    card.focus({ preventScroll: true });
    card.scrollIntoView({ block: "nearest" });
  }

  function suitabilityScore(value) {
    if (value === "best fit") {
      return 4;
    }

    if (value === "strong fit") {
      return 3;
    }

    if (value === "gentle option") {
      return 2;
    }

    if (value === "not advised") {
      return 1;
    }

    return 0;
  }

  function moveRouteSelection(currentId, direction) {
    const visibleChoices = routeChoices.filter((choice) => !choice.hidden);
    if (!visibleChoices.length) {
      return;
    }

    const currentVisibleIndex = visibleChoices.findIndex((choice) => choice.dataset.routeId === currentId);
    if (currentVisibleIndex === -1) {
      return;
    }

    for (let offset = 1; offset <= visibleChoices.length; offset += 1) {
      const nextIndex = (currentVisibleIndex + direction * offset + visibleChoices.length) % visibleChoices.length;
      const nextChoice = visibleChoices[nextIndex];
      const nextRoute = routeMap.get(nextChoice.dataset.routeId);

      if (!isSelectable(nextRoute)) {
        continue;
      }

      state.selectedId = nextChoice.dataset.routeId;
      render();

      if (window.history && typeof window.history.replaceState === "function") {
        window.history.replaceState(null, "", `#route-${nextChoice.dataset.routeId}`);
      }

      nextChoice.focus();
      setDefaultStatus();
      return;
    }
  }

  function normalizationReason(previousRoute, wasVisible, wasValid, wasSuitable, visibleOpenCount) {
    if (!visibleOpenCount) {
      return "No visible open route remains under this filter.";
    }

    if (!previousRoute) {
      return "The plan selected the strongest visible open route for this view.";
    }

    if (!wasVisible) {
      return `${previousRoute.name} is outside the current ground filter.`;
    }

    if (!wasValid) {
      return `${previousRoute.name} is not available as an open route.`;
    }

    if (!wasSuitable) {
      return `${previousRoute.name} is ${suitabilityValue(previousRoute)} for ${groupMeta[state.groupNeeds].label.toLowerCase()}.`;
    }

    return "The plan selected the strongest visible open route for this view.";
  }

  function announceNormalization(normalization, fallbackMessage) {
    const nextRoute = normalization.routeId ? routeMap.get(normalization.routeId) : null;

    if (normalization.changed && nextRoute) {
      setStatus(`Plan updated to ${nextRoute.name} for ${groupMeta[state.groupNeeds].label.toLowerCase()}. ${normalization.reason}`, "");
      return;
    }

    if (normalization.changed && !nextRoute) {
      setStatus(normalization.reason, "is-error");
      return;
    }

    setStatus(fallbackMessage, "");
  }

  function remainingEssentials(unchecked) {
    return unchecked.map((checkbox) => {
      const copy = checkbox.parentElement.querySelector("strong");
      return copy ? copy.textContent.trim() : checkbox.value;
    });
  }

  function focusStatus() {
    status.focus({ preventScroll: true });
  }

  function shortGroupLabel(value) {
    if (value === "experienced") {
      return "Experienced";
    }

    if (value === "child") {
      return "Child";
    }

    return "Mixed";
  }

  function filterLabel(value) {
    if (value === "all") {
      return "all";
    }

    return value;
  }

  function capitalize(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
  }

  function capitalizePhrase(value) {
    return value.charAt(0).toUpperCase() + value.slice(1);
  }
})();
