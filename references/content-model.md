# Content model and invariants

Use this reference when creating or refactoring the guide's data layer.

## Core records

### Trip

- `id`, `title`, `subtitle`
- `startDate`, `endDate`, `timezone`
- `origin`, `destinations`, `partySize`
- `currency`, `budgetTarget`
- `routeSummary`, `phaseIds`
- `fixedFacts`, `lastContentReview`

### Phase

- `id`, `name`, `dateRange`, `regionKey`
- `summary`, `dayIds`, `accent`

### Day

- `id`, `date`, `dayNumber`, `phaseId`
- `location`, `title`, `summary`
- `intensity`: `rest | light | moderate | high | transfer`
- `hotelChange`, `overnightLocation`
- `transportSegmentIds`, `scheduleNodeIds`
- `optional`, `weatherDependent`, `recheckItems`

### Schedule node

- `id`, `dayId`, `startTime`, `endTime`
- `placeId`, `title`, `description`
- `arrivalMethod`, `duration`, `costRange`
- `bookingStatus`, `fallback`, `notes`

### Place

- `id`, `name`, `localName`, `regionKey`
- `coordinates`, `category`, `summary`
- `imageId`, `recommendedDuration`
- `officialUrl`, `sourceIds`, `verifiedAt`

### Transport segment

- `id`, `from`, `to`, `mode`, `date`
- `departureTime`, `arrivalTime`, `operator`, `serviceNumber`
- `status`: `booked | planned | candidate | unknown`
- `sourceIds`, `verifiedAt`, `needsRecheck`, `uncertaintyNote`
- `bookingDeadline`, `fallbackOptions`

### Recommendation

For stays and food, include `id`, `city`, `area`, `name`, `type`, `priceBand`, `whyItFits`, `bookingAdvice`, `sourceIds`, and `verifiedAt`. Avoid unsupported ratings.

### Source

- `id`, `title`, `url`, `publisher`
- `sourceType`: `official | operator | property | reputable_secondary | user_supplied`
- `checkedAt`, `supports`, `notes`

### Image

- `id`, `localPath`, `alt`, `subjectPlaceId`
- `sourceUrl`, `creator`, `license`, `retrievedAt`

### Budget item

- `id`, `category`, `label`, `amount`, `currency`
- `basis`: `paid | quoted | observed | estimated`
- `scope`: `per_person | per_room | per_group`
- `partySizeAssumption`, `lowerBound`, `upperBound`, `sourceIds`

## Invariants

- Every referenced ID resolves exactly once.
- Dates fall inside the trip range and day numbers are monotonic.
- A booked segment is never overwritten by a planning candidate.
- Map points, itinerary cards, and guide pages share the same place IDs.
- Budget totals are derived, not copied into several files.
- Each visible dynamic fact can be traced to a source and review date.
- Each place image has a unique subject and meaningful alt text.
- Optional and weather-dependent items never appear as guaranteed.
- Changing a destination or date cannot leave retired labels in navigation, manifest, calendar export, or service-worker cache names.
