// The Trail's layout: an Area's Topics as stepping stones down one stretch of path, swaying left and
// right, and the dotted path's curve through them. x is a percentage of the stretch's width, so the
// sway narrows with the screen; y is in px, so stones keep their spacing.

export const STEP = 132; // px between neighbouring stones, top to bottom
const END = 70; // px of path above the first stone and below the last

export interface Stone {
  x: number; // % of the stretch's width
  y: number; // px from the stretch's top
}

export interface TrailLayout {
  stones: Stone[]; // in Topic order
  height: number; // px
  path: string; // SVG path data in a viewBox of 100 × height
}

/** The stretch for an Area's `topics` Topics; `area` is the Area's place on the Trail, which varies
 * where its sway starts, so neighbouring stretches don't look stamped out. */
export function trailLayout(topics: number, area: number): TrailLayout {
  const stones = Array.from({ length: topics }, (_, j) => ({
    x: round(50 + 30 * Math.sin(j * 1.15 + area * 2)),
    y: END + j * STEP,
  }));
  const height = 2 * END + Math.max(0, topics - 1) * STEP;
  return { stones, height, path: curve(stones, height) };
}

// A smooth vertical S-curve from the stretch's top, through every stone, to its bottom: each leg is a
// cubic Bézier whose control points sit at the leg's middle height, so the path leaves and enters
// every stone heading straight down.
function curve(stones: Stone[], height: number): string {
  if (stones.length === 0) return "";
  const first = stones[0];
  const last = stones[stones.length - 1];
  const points = [{ x: first.x, y: 0 }, ...stones, { x: last.x, y: height }];
  let d = `M ${points[0].x} ${points[0].y}`;
  for (let k = 1; k < points.length; k++) {
    const p = points[k - 1];
    const q = points[k];
    const mid = (p.y + q.y) / 2;
    d += ` C ${p.x} ${mid}, ${q.x} ${mid}, ${q.x} ${q.y}`;
  }
  return d;
}

/** Each Topic's number on the Trail: its place among the Area's stops (non-planned Topics, which Previous /
 * Next stop walks in this order), or null for a planned Topic, which has no number. */
export function stopNumbers(topics: { planned: boolean }[]): (number | null)[] {
  let stop = 0;
  return topics.map((topic) => (topic.planned ? null : ++stop));
}

const round = (n: number) => Number(n.toFixed(1));
