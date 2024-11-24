function isInRange(
    originStartTime,
    originEndTime,
    allDayEnabled = false,
    settingsRrule,
    timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone
) {
    const now = new Date();
    const currentTime = timeZone
        ? new Date(now.toLocaleString('en-US', { timeZone }))
        : now;

    // Convert the times to the same timezone as the conditionTimezone
    let startTime = new Date(
        originStartTime.toLocaleString('en-US', { timeZone })
    );
    let endTime = new Date(originEndTime.toLocaleString('en-US', { timeZone }));

    // If all day is true, adjust the start and end times to be full day
    if (allDayEnabled) {
        startTime.setHours(0, 0, 0, 0);
        endTime.setHours(23, 59, 59, 999);
    }

    if (settingsRrule && rrule) {
        //rrule is a 3rd party library to parse rrule strings
        const recurringRule = rrule.rrulestr(settingsRrule);
        recurringRule.options = {
            ...recurringRule.options,
            tzid: timeZone,
            dtstart: startTime,
            until: getEndDate(
                endTime,
                recurringRule.options,
                currentTime,
                originStartTime,
                originEndTime,
                allDayEnabled
            ),
        };

        const betweenOccurrences = measureFunctionExecutionTime(() =>
            recurringRule.between(
                recurringRule.options.dtstart,
                recurringRule.options.until,
                true
            )
        );

        return betweenOccurrences.some((occurrence) => {
            if (!allDayEnabled) {
                setTimeFromAnotherDate(occurrence, originEndTime);
                return (
                    compareDates(currentTime, occurrence, true) &&
                    compareDatesIgnoringSeconds(currentTime, occurrence) <= 0
                );
            }
            return compareDates(currentTime, occurrence, allDayEnabled);
        });
    }

    return (
        compareDatesIgnoringSeconds(currentTime, startTime) >= 0 &&
        compareDatesIgnoringSeconds(currentTime, endTime) <= 0
    );
}

function shouldShowRuleObjectForDateTimeRange(
    ruleObjName,
    settings,
    actionType
) {
    const settingsStartTime = new Date(settings.start_time);
    const settingsEndTime = new Date(settings.end_time);
    const settingsAllDayEnabled = parseBoolean(settings.all_day_enabled);
    const settingsRrule = settings.rrule;
    const settingsTimeZone = settings.timezone;

    if (settingsStartTime && settingsEndTime) {
        const cookieName = getSmartRuleCookieName(ruleObjName, actionType);
        return (
            isInRange(
                settingsStartTime,
                settingsEndTime,
                settingsAllDayEnabled,
                settingsRrule,
                settingsTimeZone
            ) &&
            //if the rule was already shown we shouldn't show it again until the ttl time when cookie expires
            getCookie(cookieName) === null &&
            // there is no cookie of the same action type - site visitor already saw this action
            !hasCookieOfType(actionType)
        );
    }

    //if there is no start_time, end_time, all_day_enabled, timezone in settings it means
    // that the condition is not date time range, and we need to disregard this conditions
    return true;
}

function compareDates(date1, date2, allDay) {
    const d1 = new Date(date1);
    const d2 = new Date(date2);

    if (allDay) {
        const year1 = d1.getFullYear();
        const month1 = d1.getMonth();
        const day1 = d1.getDate();

        const year2 = d2.getFullYear();
        const month2 = d2.getMonth();
        const day2 = d2.getDate();

        return year1 === year2 && month1 === month2 && day1 === day2;
    } else {
        d1.setSeconds(0, 0);
        d2.setSeconds(0, 0);

        return d1.getTime() === d2.getTime();
    }
}

function compareDatesIgnoringSeconds(date1, date2) {
    let d1 = new Date(date1.getTime());
    let d2 = new Date(date2.getTime());

    d1.setSeconds(0, 0);
    d2.setSeconds(0, 0);

    if (d1.getTime() === d2.getTime()) {
        return 0;
    } else if (d1.getTime() < d2.getTime()) {
        return -1; //d1 is earlier than d2
    } else {
        return 1; //d1 is later than d2
    }
}

function getEndDate(
    endTime,
    options,
    currentTime,
    originStartTime,
    originEndTime,
    allDay
) {
    if (options.until) {
        if (allDay) {
            return options.until;
        }
        return setTimeFromAnotherDate(options.until, originEndTime);
    }
    const isOriginStartTimeEqualsToOriginEndTime = compareDates(
        originStartTime,
        originEndTime,
        true
    );
    if (!isOriginStartTimeEqualsToOriginEndTime) {
        // it means the user specify end time, rule should live until the end time
        return endTime;
    }
    const isEndTimeBeforeCurrentTime =
        compareDatesIgnoringSeconds(endTime, currentTime) < 0;
    if (isOriginStartTimeEqualsToOriginEndTime && isEndTimeBeforeCurrentTime) {
        // endTime === startTime - means the user didnt specify end time, the rule should live forever
        // we need to check if endTime < currentTime - in this case check until tmrw to not miss today
        const tmrw = new Date(currentTime);
        tmrw.setDate(currentTime.getDate() + 1);
        return tmrw;
    }
    return currentTime;
}

function setTimeFromAnotherDate(targetDate, sourceDate) {
    const hours = sourceDate.getHours();
    const minutes = sourceDate.getMinutes();
    const seconds = sourceDate.getSeconds();
    const milliseconds = sourceDate.getMilliseconds();

    targetDate.setHours(hours, minutes, seconds, milliseconds);

    return targetDate;
}

function measureFunctionExecutionTime(callback) {
    const startTime = performance.now();
    const res = callback();
    const endTime = performance.now();
    const duration = endTime - startTime;

    if (duration > 1000) {
        window.runtime.API.logService.warn(
            `The RRULE function took more than a second: ${duration.toFixed(
                3
            )} ms`
        );
    }
    return res;
}

//for testing purposes.
// unit tests are here: client/src/modules/runtime/src/code/services/tests/timeRangeConditionService.test.js
window.timeRangeConditionService = {
    isInRange,
};
