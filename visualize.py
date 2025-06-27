"""Generate an HTML visualization for a schedule."""

from __future__ import annotations

import json
from pathlib import Path
import argparse


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>RCPSP Schedule</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body { font-family: sans-serif; }
    table { border-collapse: collapse; }
    th, td { border: 1px solid #999; padding: 4px; text-align: center; }
    .task-cell { background-color: #cde; }
  </style>
</head>
<body>
  <div>
    <button id="zoom-in">Zoom In</button>
    <button id="zoom-out">Zoom Out</button>
  </div>
  <div id="table-container"></div>
  <script>
  const data = __DATA__;
  const tasks = data.tasks || [];
  const resources = data.resources || [];
  const scheduleMap = {};
  (data.schedule || []).forEach(d => scheduleMap[d.id] = d);

  const horizon = d3.max(data.schedule, d => d.end);
  const days = d3.range(horizon);
  const table = d3.select('#table-container').append('table');
  const header = table.append('tr');
  header.append('th').text('Resource');
  days.forEach(d => header.append('th').text(d));

  resources.forEach(res => {
    const row = table.append('tr');
    row.append('th').text(res.id);
    let day = 0;
    while (day < horizon) {
      const task = tasks.find(t => t.demands && t.demands[res.id] && scheduleMap[t.id].start <= day && scheduleMap[t.id].end > day);
      if (task) {
        const start = day;
        while (day < horizon && scheduleMap[task.id].start <= day && scheduleMap[task.id].end > day) {
          day++;
        }
        const cell = row.append('td')
          .attr('colspan', day - start)
          .attr('class', 'task-cell')
          .text(task.id);
        cell.append('title')
          .text(`${task.id}: ${scheduleMap[task.id].start} - ${scheduleMap[task.id].end} (${scheduleMap[task.id].end - scheduleMap[task.id].start} days)`);
      } else {
        row.append('td');
        day += 1;
      }
    }
  });

  let scale = 1;
  function updateZoom() {
    d3.selectAll('td,th')
      .style('font-size', (12 * scale) + 'px')
      .style('min-width', (40 * scale) + 'px');
  }
  d3.select('#zoom-in').on('click', () => { scale *= 1.25; updateZoom(); });
  d3.select('#zoom-out').on('click', () => { scale /= 1.25; updateZoom(); });
  updateZoom();
  </script>
</body>
</html>
"""


def visualize(json_path: Path, html_path: Path | None = None) -> None:
    """Generate an HTML file from a schedule JSON."""
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    html = HTML_TEMPLATE.replace("__DATA__", json.dumps(data))

    if html_path is None:
        html_path = json_path.with_suffix(".html")

    with open(html_path, "w", encoding="utf-8") as out:
        out.write(html)
    print(f"Wrote visualization to {html_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize RCPSP schedule")
    parser.add_argument("schedule", type=Path, help="Schedule JSON file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None, help="Output HTML file"
    )
    args = parser.parse_args()
    visualize(args.schedule, args.output)


if __name__ == "__main__":
    main()
