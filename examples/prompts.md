# Example prompts

## Add an item

```text
Use $grocery-shopping-agent-skill to add rolled oats as a recurring item.
I want enough for seven breakfasts each week, substitutions are allowed, and the substitute must remain unsweetened.
Do not research prices yet.
```

## Edit or skip an item

```text
Use $grocery-shopping-agent-skill to skip frozen vegetables this week and change pasta to a biweekly cadence.
Preserve the existing price history.
```

## Weekly review

```text
Use $grocery-shopping-agent-skill to review the next seven days.
Refresh public prices, coupons, mandatory fees, and availability.
Compare a complete basket with any meaningfully cheaper split order.
Show substitutions separately and stop at the approval queue.
```

## Deal-only check

```text
Use $grocery-shopping-agent-skill to refresh deals for active items only.
Do not change quantities or preferred specifications.
Flag membership-only or checkout-only claims as unverified.
```

## Mark a purchase

```text
Use $grocery-shopping-agent-skill to record that the approved rice and frozen vegetables were purchased today.
Keep their history and calculate the next review date from the saved cadence.
```
