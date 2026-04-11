# Apple Health XML Schema

The `export.xml` file follows a specific structure for different health data types.

## Record Types

`Record` elements represent a single data point (e.g., heart rate reading, step count).

- **`type`**: The identifier for the health metric (e.g., `HKQuantityTypeIdentifierStepCount`).
- **`sourceName`**: The device or app that recorded the data.
- **`unit`**: The unit of measurement (e.g., `count`, `km`, `kcal`).
- **`creationDate`**: When the record was created.
- **`startDate` / `endDate`**: The time period the record covers.
- **`value`**: The actual measurement value.

## Workout Types

`Workout` elements represent a specific exercise session.

- **`workoutActivityType`**: The type of workout (e.g., `HKWorkoutActivityTypeRunning`).
- **`duration`**: Duration in minutes.
- **`totalDistance`**: Distance covered.
- **`totalEnergyBurned`**: Calories burned.

## ActivitySummary

`ActivitySummary` elements provide daily totals for Apple's activity rings.

- **`dateComponents`**: The date for the summary.
- **`activeEnergyBurned`**: Total active calories.
- **`activeEnergyBurnedGoal`**: The user's calorie goal.
- **`appleExerciseTime`**: Minutes spent exercising.
- **`appleStandHours`**: Number of hours with at least one minute of standing.
