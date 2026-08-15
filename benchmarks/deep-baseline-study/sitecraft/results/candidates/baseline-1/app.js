(function () {
  const CAIRN = {
    groupLabels: {
      mixed: 'mixed group',
      child: 'group with a child',
      experienced: 'experienced group',
    },

    difficultyDescriptions: {
      easy: 'Shortest and least committing on terrain and navigation.',
      steady: 'More time, ascent, or exposure than the easy option.',
      hard: 'Longer, more exposed, or more technical with higher consequences.',
    },

    suitabilityPriority: {
      'best fit': 4,
      'strong fit': 3,
      'gentle option': 2,
      'not advised': 1,
      'not today': 0,
    },

    essentialItems: [
      'Layer and waterproof packed',
      'Water and food accounted for',
      'At least one charged phone shared',
      'Everyone knows the turnaround rule',
    ],

    normalizeRoute(route) {
      return {
        ...route,
        difficulty: String(route.difficulty || '').toLowerCase(),
        status: String(route.status || 'open').toLowerCase(),
        suitability: route.suitability || {},
      };
    },

    readStaticRoutes(routeList) {
      return Array.from(routeList.querySelectorAll('[data-route-id]')).map((button) =>
        CAIRN.normalizeRoute({
          id: button.dataset.routeId,
          name: button.querySelector('strong')?.textContent?.trim() || 'Route',
          difficulty: button.dataset.difficulty,
          distance_km: Number.parseFloat(button.dataset.distanceKm),
          duration: button.dataset.duration,
          ascent_m: Number.parseInt(button.dataset.ascentM, 10),
          weather: button.dataset.weather,
          terrain: button.dataset.terrain,
          signal: button.dataset.signal,
          status: button.dataset.status,
          why: button.dataset.why,
          suitability: {
            mixed: button.dataset.suitabilityMixed,
            child: button.dataset.suitabilityChild,
            experienced: button.dataset.suitabilityExperienced,
          },
        })
      );
    },

    getSuitability(route, groupNeeds) {
      return route?.suitability?.[groupNeeds] || 'review';
    },

    getSuitabilityRank(route, groupNeeds) {
      return CAIRN.suitabilityPriority[CAIRN.getSuitability(route, groupNeeds)] || 0;
    },

    isSuitabilityValid(route, groupNeeds) {
      return CAIRN.getSuitabilityRank(route, groupNeeds) >= 2;
    },

    isRoutePlannable(route) {
      return Boolean(route) && route.status === 'open';
    },

    isRouteVisibleForFilter(route, difficultyFilter) {
      return difficultyFilter === 'all' || route?.difficulty === difficultyFilter;
    },

    formatDifficulty(difficulty) {
      return difficulty.charAt(0).toUpperCase() + difficulty.slice(1);
    },

    formatStatus(status) {
      return status.charAt(0).toUpperCase() + status.slice(1);
    },

    getRouteTone(route, groupNeeds) {
      const fit = CAIRN.getSuitability(route, groupNeeds);
      const label = CAIRN.groupLabels[groupNeeds] || 'group';

      if (!route) {
        return 'Choose a route to compare.';
      }

      if (route.status === 'closed') {
        return `${route.name} is closed for every group today.`;
      }

      if (fit === 'best fit') {
        return `Best fit for this ${label}.`;
      }

      if (fit === 'strong fit') {
        return `Strong fit if this ${label} wants a bigger day.`;
      }

      if (fit === 'gentle option') {
        return `A gentle option for this ${label}.`;
      }

      if (fit === 'not advised') {
        return `Not advised for this ${label}.`;
      }

      return `Review carefully for this ${label}.`;
    },

    getRouteSummary(route, groupNeeds) {
      if (!route) {
        return 'No route selected.';
      }

      const difficultyMeaning = CAIRN.difficultyDescriptions[route.difficulty] || '';

      if (route.status === 'closed') {
        return `${route.name} is closed today. ${route.why}`;
      }

      return `${CAIRN.getRouteTone(route, groupNeeds)} ${route.why} ${difficultyMeaning}`;
    },

    chooseBestOpenRoute(routes, groupNeeds) {
      return routes
        .filter(CAIRN.isRoutePlannable)
        .sort((a, b) => {
          const fitDelta = CAIRN.getSuitabilityRank(b, groupNeeds) - CAIRN.getSuitabilityRank(a, groupNeeds);

          if (fitDelta !== 0) {
            return fitDelta;
          }

          if (a.distance_km !== b.distance_km) {
            return a.distance_km - b.distance_km;
          }

          return a.ascent_m - b.ascent_m;
        })[0] || null;
    },

    getMissingEssentials(checkedEssentials) {
      return CAIRN.essentialItems.filter((item) => !checkedEssentials.includes(item));
    },

    chooseContextRoute(routes, groupNeeds, difficultyFilter) {
      const filteredRoutes = routes.filter((route) =>
        CAIRN.isRouteVisibleForFilter(route, difficultyFilter)
      );
      const filteredSuitableOpenRoutes = filteredRoutes.filter(
        (route) =>
          CAIRN.isRoutePlannable(route) && CAIRN.isSuitabilityValid(route, groupNeeds)
      );
      const suitableOpenRoutes = routes.filter(
        (route) =>
          CAIRN.isRoutePlannable(route) && CAIRN.isSuitabilityValid(route, groupNeeds)
      );
      const filteredOpenRoutes = filteredRoutes.filter(CAIRN.isRoutePlannable);
      const openRoutes = routes.filter(CAIRN.isRoutePlannable);
      const pool =
        filteredSuitableOpenRoutes.length > 0
          ? filteredSuitableOpenRoutes
          : suitableOpenRoutes.length > 0
            ? suitableOpenRoutes
            : filteredOpenRoutes.length > 0
              ? filteredOpenRoutes
              : openRoutes;

      return CAIRN.chooseBestOpenRoute(pool, groupNeeds);
    },

    resolveContextChange({
      routes,
      plannedRouteId,
      reviewedRouteId,
      groupNeeds,
      difficultyFilter,
    }) {
      const currentPlannedRoute = routes.find((route) => route.id === plannedRouteId) || null;
      const currentReviewedRoute = routes.find((route) => route.id === reviewedRouteId) || null;
      const recommendedRoute = CAIRN.chooseContextRoute(routes, groupNeeds, difficultyFilter);
      const filteredRoutes = routes.filter((route) =>
        CAIRN.isRouteVisibleForFilter(route, difficultyFilter)
      );
      const filteredSuitableOpenRoutes = filteredRoutes.filter(
        (route) =>
          CAIRN.isRoutePlannable(route) && CAIRN.isSuitabilityValid(route, groupNeeds)
      );
      const currentPlanIsValid =
        Boolean(currentPlannedRoute) &&
        CAIRN.isRoutePlannable(currentPlannedRoute) &&
        CAIRN.isRouteVisibleForFilter(currentPlannedRoute, difficultyFilter) &&
        CAIRN.isSuitabilityValid(currentPlannedRoute, groupNeeds);
      const nextPlannedRoute = currentPlanIsValid ? currentPlannedRoute : recommendedRoute;
      const visibleRouteIds = new Set(filteredRoutes.map((route) => route.id));

      if (nextPlannedRoute) {
        visibleRouteIds.add(nextPlannedRoute.id);
      }

      const nextReviewedRoute =
        currentReviewedRoute && visibleRouteIds.has(currentReviewedRoute.id)
          ? currentReviewedRoute
          : nextPlannedRoute;
      const forcedVisiblePlannedRoute =
        Boolean(nextPlannedRoute) &&
        !CAIRN.isRouteVisibleForFilter(nextPlannedRoute, difficultyFilter);
      const planChanged =
        Boolean(nextPlannedRoute) && nextPlannedRoute.id !== currentPlannedRoute?.id;

      let message = '';
      if (planChanged && nextPlannedRoute) {
        if (filteredSuitableOpenRoutes.length === 0 && difficultyFilter !== 'all') {
          message = `No suitable ${difficultyFilter} route is open for a ${CAIRN.groupLabels[groupNeeds]}. Active plan updated to ${nextPlannedRoute.name} and kept visible.`;
        } else {
          message = `Active plan updated to ${nextPlannedRoute.name} for a ${CAIRN.groupLabels[groupNeeds]}.`;
        }
      } else if (forcedVisiblePlannedRoute && nextPlannedRoute) {
        message = `Keeping ${nextPlannedRoute.name} visible because no suitable open route matches the current filter for a ${CAIRN.groupLabels[groupNeeds]}.`;
      }

      return {
        plannedRouteId: nextPlannedRoute?.id || plannedRouteId,
        reviewedRouteId: nextReviewedRoute?.id || reviewedRouteId,
        visibleRouteIds: Array.from(visibleRouteIds),
        forcedVisiblePlannedRoute,
        planChanged,
        message,
      };
    },

    getNavigableRouteId({ routes, currentRouteId, visibleRouteIds, direction }) {
      const visibleIds = new Set(visibleRouteIds);
      const startIndex = routes.findIndex((route) => route.id === currentRouteId);
      const fallbackIndex = startIndex >= 0 ? startIndex : 0;
      const step = direction === 'previous' ? -1 : 1;

      if (!routes.some((route) => visibleIds.has(route.id) && CAIRN.isRoutePlannable(route))) {
        return null;
      }

      for (let offset = 1; offset <= routes.length; offset += 1) {
        const nextIndex = (fallbackIndex + step * offset + routes.length) % routes.length;
        const candidate = routes[nextIndex];

        if (candidate && visibleIds.has(candidate.id) && CAIRN.isRoutePlannable(candidate)) {
          return candidate.id;
        }
      }

      return null;
    },

    reviewRoute({ routes, routeId, plannedRouteId }) {
      const route = routes.find((item) => item.id === routeId) || null;
      const plannedRoute = routes.find((item) => item.id === plannedRouteId) || null;

      if (!route) {
        return {
          reviewedRouteId: plannedRouteId,
          plannedRouteId,
          compareOnly: false,
          message: 'Choose a route from the list.',
        };
      }

      if (!CAIRN.isRoutePlannable(route)) {
        return {
          reviewedRouteId: route.id,
          plannedRouteId,
          compareOnly: true,
          message: `${route.name} is closed: ${route.why} Current active plan remains ${
            plannedRoute?.name || 'unset'
          }.`,
        };
      }

      return {
        reviewedRouteId: route.id,
        plannedRouteId: route.id,
        compareOnly: false,
        message: 'Route updated. Confirm once the essentials are complete.',
      };
    },

    buildSummary({
      plannedRoute,
      reviewedRoute,
      groupNeeds,
      groupSize,
      departureTime,
      turnaroundTime,
      meetingPoint,
      notes,
      essentialsCount,
    }) {
      if (!plannedRoute) {
        return 'No open route is currently available to confirm as a field plan.';
      }

      const label = CAIRN.groupLabels[groupNeeds] || 'group';
      const essentialsText =
        essentialsCount === CAIRN.essentialItems.length
          ? 'All essentials confirmed.'
          : `${essentialsCount} of ${CAIRN.essentialItems.length} essentials confirmed.`;
      const noteSentence = notes ? ` Notes: ${notes}` : '';
      const compareSentence =
        reviewedRoute && reviewedRoute.id !== plannedRoute.id
          ? ` Comparing ${reviewedRoute.name}, but the active plan remains ${plannedRoute.name}.`
          : '';

      return `${plannedRoute.name} for a ${label} of ${groupSize} walkers. Meet at ${meetingPoint} by ${departureTime}, keep a ${turnaroundTime} turnaround, and expect ${plannedRoute.weather.toLowerCase()}, ${plannedRoute.terrain.toLowerCase()}, and signal noted as ${plannedRoute.signal.toLowerCase()}. Suitability: ${CAIRN.getSuitability(plannedRoute, groupNeeds)}. ${essentialsText}${compareSentence}${noteSentence}`;
    },

    validatePlan({
      plannedRoute,
      groupSize,
      departureTime,
      turnaroundTime,
      meetingPoint,
      checkedEssentials = null,
      essentialsCount,
    }) {
      const issues = [];
      const resolvedEssentialsCount =
        Array.isArray(checkedEssentials) ? checkedEssentials.length : essentialsCount || 0;
      const missingEssentials = Array.isArray(checkedEssentials)
        ? CAIRN.getMissingEssentials(checkedEssentials)
        : [];

      if (!plannedRoute) {
        issues.push('Choose an open route.');
      } else if (!CAIRN.isRoutePlannable(plannedRoute)) {
        issues.push('Closed routes cannot become the plan.');
      }

      if (!groupSize || Number(groupSize) < 2) {
        issues.push('Set at least 2 walkers.');
      }

      if (!departureTime) {
        issues.push('Add a departure time.');
      }

      if (!turnaroundTime) {
        issues.push('Add a turnaround time.');
      }

      if (!meetingPoint || !meetingPoint.trim()) {
        issues.push('Add a meeting point.');
      }

      if (resolvedEssentialsCount !== CAIRN.essentialItems.length) {
        issues.push(
          Array.isArray(checkedEssentials)
            ? `Remaining essentials: ${missingEssentials.join('; ')}.`
            : 'Complete all essential checks.'
        );
      }

      return issues;
    },
  };

  if (typeof module !== 'undefined' && module.exports) {
    module.exports = CAIRN;
  }

  if (typeof document === 'undefined') {
    return;
  }

  document.documentElement.classList.remove('no-js');
  document.documentElement.classList.add('js');

  const routeList = document.querySelector('[data-testid="route-list"]');
  const difficultyFilter = document.querySelector('[data-testid="difficulty-filter"]');
  const groupNeedsInputs = Array.from(document.querySelectorAll('input[name="groupNeeds"]'));
  const planForm = document.getElementById('plan-form');
  const summaryContent = document.getElementById('plan-summary-content');
  const statusNode = document.getElementById('plan-status');
  const printButton = document.getElementById('print-plan');

  if (
    !routeList ||
    !difficultyFilter ||
    groupNeedsInputs.length === 0 ||
    !planForm ||
    !summaryContent ||
    !statusNode
  ) {
    return;
  }

  statusNode.setAttribute('role', 'status');
  statusNode.setAttribute('aria-atomic', 'true');
  statusNode.setAttribute('tabindex', '-1');

  const detailNodes = {
    kicker: document.getElementById('selected-route-kicker'),
    status: document.getElementById('selected-route-status'),
    name: document.getElementById('selected-route-name'),
    summary: document.getElementById('selected-route-summary'),
    fit: document.getElementById('selected-route-fit'),
    planNote: document.getElementById('selected-route-plan-note'),
    weather: document.getElementById('selected-route-weather'),
    terrain: document.getElementById('selected-route-terrain'),
    signal: document.getElementById('selected-route-signal'),
    why: document.getElementById('selected-route-why'),
    facts: document.getElementById('route-facts'),
  };

  const formFields = {
    groupSize: document.getElementById('group-size'),
    departureTime: document.getElementById('departure-time'),
    meetingPoint: document.getElementById('meeting-point'),
    turnaroundTime: document.getElementById('turnaround-time'),
    groupNotes: document.getElementById('group-notes'),
  };

  let routes = [];
  let groupNeeds = 'mixed';
  let reviewedRouteId = 'rowan-loop';
  let plannedRouteId = 'rowan-loop';
  let visibleRouteIds = new Set();

  const getRouteById = (routeId) => routes.find((route) => route.id === routeId) || null;
  const getReviewedRoute = () => getRouteById(reviewedRouteId);
  const getPlannedRoute = () => getRouteById(plannedRouteId);
  const getCheckedEssentials = () =>
    Array.from(planForm.querySelectorAll('input[name="essentials"]:checked')).map(
      (input) => input.value
    );

  const focusStatus = () => {
    statusNode.focus();
  };

  const setStatus = (message, state, options = {}) => {
    statusNode.textContent = message;

    if (state) {
      statusNode.dataset.state = state;
    } else {
      delete statusNode.dataset.state;
    }

    if (options.focus) {
      focusStatus();
    }
  };

  const renderRouteButtons = () => {
    routeList.querySelectorAll('[data-route-id]').forEach((button) => {
      const route = getRouteById(button.dataset.routeId);
      if (!route) {
        return;
      }

      const suitability = CAIRN.getSuitability(route, groupNeeds);
      const statusChip = button.querySelector('.status-chip');
      const fitNode = button.querySelector('.route-choice-fit');

      button.dataset.routeStatus = route.status;
      button.setAttribute('aria-pressed', String(route.id === reviewedRouteId));
      button.classList.toggle('is-compare-only', route.status === 'closed');
      button.hidden = !visibleRouteIds.has(route.id);

      if (statusChip) {
        statusChip.textContent = CAIRN.formatStatus(route.status);
        statusChip.className = `status-chip ${
          route.status === 'closed' ? 'status-chip-closed' : 'status-chip-open'
        }`;
      }

      if (fitNode) {
        fitNode.textContent = `${CAIRN.groupLabels[groupNeeds]}: ${suitability}`;
      }
    });
  };

  const renderRouteDetails = () => {
    const reviewedRoute = getReviewedRoute();
    const plannedRoute = getPlannedRoute();

    if (!reviewedRoute) {
      return;
    }

    detailNodes.kicker.textContent = CAIRN.getRouteTone(reviewedRoute, groupNeeds);
    detailNodes.status.textContent = CAIRN.formatStatus(reviewedRoute.status);
    detailNodes.name.textContent = reviewedRoute.name;
    detailNodes.summary.textContent = CAIRN.getRouteSummary(reviewedRoute, groupNeeds);
    detailNodes.fit.textContent = `${CAIRN.groupLabels[groupNeeds]}: ${CAIRN.getSuitability(
      reviewedRoute,
      groupNeeds
    )}`;
    detailNodes.planNote.textContent =
      reviewedRoute.status === 'closed'
        ? `Compare only today. Active plan remains ${plannedRoute?.name || 'unset'}.`
        : reviewedRoute.id === plannedRoute?.id
          ? 'Available for planning today'
          : `Available, but the active plan remains ${plannedRoute?.name || reviewedRoute.name}.`;
    detailNodes.weather.textContent = reviewedRoute.weather;
    detailNodes.terrain.textContent = reviewedRoute.terrain;
    detailNodes.signal.textContent = reviewedRoute.signal;
    detailNodes.why.textContent = reviewedRoute.why;
    detailNodes.facts.innerHTML = `
      <div>
        <dt>Difficulty</dt>
        <dd>${CAIRN.formatDifficulty(reviewedRoute.difficulty)}</dd>
      </div>
      <div>
        <dt>Distance</dt>
        <dd>${reviewedRoute.distance_km} km</dd>
      </div>
      <div>
        <dt>Duration</dt>
        <dd>${reviewedRoute.duration}</dd>
      </div>
      <div>
        <dt>Ascent</dt>
        <dd>${reviewedRoute.ascent_m} m</dd>
      </div>
    `;
  };

  const refreshSummary = () => {
    summaryContent.textContent = CAIRN.buildSummary({
      plannedRoute: getPlannedRoute(),
      reviewedRoute: getReviewedRoute(),
      groupNeeds,
      groupSize: formFields.groupSize.value || '0',
      departureTime: formFields.departureTime.value || 'unspecified time',
      turnaroundTime: formFields.turnaroundTime.value || 'an unspecified turnaround',
      meetingPoint: formFields.meetingPoint.value.trim() || 'an agreed meeting point',
      notes: formFields.groupNotes.value.trim(),
      essentialsCount: getCheckedEssentials().length,
    });
  };

  const refreshView = () => {
    renderRouteButtons();
    renderRouteDetails();
    refreshSummary();
  };

  const applyContextChange = () => {
    const nextState = CAIRN.resolveContextChange({
      routes,
      plannedRouteId,
      reviewedRouteId,
      groupNeeds,
      difficultyFilter: difficultyFilter.value,
    });

    plannedRouteId = nextState.plannedRouteId;
    reviewedRouteId = nextState.reviewedRouteId;
    visibleRouteIds = new Set(nextState.visibleRouteIds);
    refreshView();

    return nextState;
  };

  const handleRouteReview = (routeId) => {
    const nextState = CAIRN.reviewRoute({
      routes,
      routeId,
      plannedRouteId,
    });

    reviewedRouteId = nextState.reviewedRouteId;
    plannedRouteId = nextState.plannedRouteId;
    visibleRouteIds.add(reviewedRouteId);
    visibleRouteIds.add(plannedRouteId);
    setStatus(nextState.message, '');
    refreshView();
  };

  routeList.addEventListener('click', (event) => {
    const button = event.target.closest('[data-route-id]');
    if (!button) {
      return;
    }

    handleRouteReview(button.dataset.routeId);
  });

  routeList.addEventListener('keydown', (event) => {
    if (
      event.key !== 'ArrowDown' &&
      event.key !== 'ArrowRight' &&
      event.key !== 'ArrowUp' &&
      event.key !== 'ArrowLeft'
    ) {
      return;
    }

    event.preventDefault();

    const focusedButton = event.target.closest('[data-route-id]');
    const direction =
      event.key === 'ArrowUp' || event.key === 'ArrowLeft' ? 'previous' : 'next';
    const nextRouteId = CAIRN.getNavigableRouteId({
      routes,
      currentRouteId: focusedButton?.dataset.routeId || reviewedRouteId,
      visibleRouteIds: Array.from(visibleRouteIds),
      direction,
    });

    if (!nextRouteId) {
      return;
    }

    routeList.querySelector(`[data-route-id="${nextRouteId}"]`)?.focus();
    handleRouteReview(nextRouteId);
  });

  difficultyFilter.addEventListener('change', () => {
    const nextState = applyContextChange();
    const filterLabel =
      difficultyFilter.value === 'all'
        ? 'Showing all routes.'
        : `Showing ${difficultyFilter.value} routes.`;

    setStatus(
      nextState.message ||
        `${filterLabel} Active plan: ${getPlannedRoute()?.name || 'none available'}.`,
      ''
    );
  });

  groupNeedsInputs.forEach((input) => {
    input.addEventListener('change', () => {
      if (!input.checked) {
        return;
      }

      groupNeeds = input.value;
      const nextState = applyContextChange();

      setStatus(
        nextState.message ||
          `Guidance updated for a ${CAIRN.groupLabels[groupNeeds]}. Active plan: ${getPlannedRoute()?.name || 'none available'}.`,
        ''
      );
    });
  });

  planForm.addEventListener('input', refreshSummary);

  planForm.addEventListener('submit', (event) => {
    event.preventDefault();

    const plannedRoute = getPlannedRoute();
    const checkedEssentials = getCheckedEssentials();
    const issues = CAIRN.validatePlan({
      plannedRoute,
      groupSize: formFields.groupSize.value,
      departureTime: formFields.departureTime.value,
      turnaroundTime: formFields.turnaroundTime.value,
      meetingPoint: formFields.meetingPoint.value,
      checkedEssentials,
    });

    refreshSummary();

    if (issues.length > 0) {
      setStatus(issues.join(' '), '', { focus: true });
      return;
    }

    setStatus(
      `Field plan confirmed: ${plannedRoute.name} for a ${CAIRN.groupLabels[groupNeeds]} of ${formFields.groupSize.value} walkers. Meet at ${formFields.meetingPoint.value.trim()} by ${formFields.departureTime.value} and turn back by ${formFields.turnaroundTime.value}.`,
      'success',
      { focus: true }
    );
  });

  if (printButton) {
    printButton.addEventListener('click', () => {
      window.print();
    });
  }

  const initialize = async () => {
    routes = CAIRN.readStaticRoutes(routeList);

    try {
      const response = await fetch('data/routes.json', { cache: 'no-store' });
      if (!response.ok) {
        throw new Error(`Failed to load routes: ${response.status}`);
      }
      const payload = await response.json();
      routes = payload.map(CAIRN.normalizeRoute);
    } catch (error) {
      setStatus(
        'Using built-in route notes because the route data could not be refreshed.',
        ''
      );
    }

    visibleRouteIds = new Set(routes.map((route) => route.id));
    const recommended = CAIRN.chooseContextRoute(routes, groupNeeds, difficultyFilter.value);
    plannedRouteId = recommended?.id || plannedRouteId;

    if (!getRouteById(reviewedRouteId)) {
      reviewedRouteId = plannedRouteId;
    }

    applyContextChange();
  };

  initialize();
})();
