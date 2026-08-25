### Phase 9 Bug Fix: Chart Axes & Visibility

**Copy and paste this into Open Code to fix the chart:**

***

The height of the chart is much better now, but the actual graph is unreadable because the X-axis (the time parameters at the bottom) is missing or cut off! 

Please fix the `Recharts` component with the following adjustments:
1. Ensure the `<XAxis />` and `<YAxis />` components are explicitly included and their `stroke` or `tick` colors are set to a visible light gray/white (e.g., `#9ca3af`) so they don't blend into the dark background.
2. Add a `margin={{ top: 10, right: 30, left: 0, bottom: 30 }}` to the main `<AreaChart>` or `<LineChart>` component to ensure the bottom labels aren't clipped off the screen.
3. Make sure the `dataKey` for the X-axis is correctly mapped to the `hour` field from the API so the times actually display on the bottom of the chart!
4. Ensure the Line/Area stroke color stands out (e.g., a bright red `#ef4444`).
