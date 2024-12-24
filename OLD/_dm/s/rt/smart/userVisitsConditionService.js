function isReachedTotalVisits(expectedVisits) {
    const userVisitsCookie = getCookie('dm_total_visits');
    let userVisits = 0;
    if (userVisitsCookie) {
        userVisits = parseInt(userVisitsCookie);
    } else {
        // if cookie hasn't been set, yet it will be null
        const lastView = getCookie('dm_this_page_view'); // data & time of last visit in site
        if (!lastView) {
            userVisits++;
        } else {
            const now = new Date();
            const visitLength = window.visitLength || 0;
            if (now.getTime() - lastView > window.visitLength) {
                userVisits++; // this counts as a new visit
            }
        }

    }
    return userVisits === expectedVisits;
}

function shouldShowRuleObjectForUserVisit(ruleObjName, settings, actionType) {
    const expectedTotalVisits = parseInt(settings.user_visits_number);

    if (expectedTotalVisits) {
        const cookieName = getSmartRuleCookieName(ruleObjName, actionType);
        return (
            isReachedTotalVisits(expectedTotalVisits) && // all the times after the first one you go to the site after the condition was applied
            // but the configured period of time didn't meet, the action shouldn't be applied
            getCookie(cookieName) === null &&
            // there is no cookie of the same action type - site visitor already saw this action
            !hasCookieOfType(actionType)
        );
    }

    //if there is no user_visits_number in settings it means
    // that the condition is not user_visits, and we need to disregard this conditions
    return true;
}

