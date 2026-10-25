// The Map's ring layout: an Area's Topics as bubbles on rings around the island's centre, with the
// island sized from the outermost ring, so every bubble fits however many Topics the Area has.
// All lengths are in px at full scale; the Map scales them down together on narrow screens.

export const BUBBLE = 116; // a Topic's bubble diameter
export const PLANNED_BUBBLE = 78; // in an Area whose Topics are all planned
const GAP = 16; // between neighbouring bubbles
const PAD = 30; // between the outermost bubbles and the island's edge

export interface Point {
  x: number;
  y: number;
}

export interface RingLayout {
  points: Point[]; // bubble centres, relative to the island's centre, in Topic order
  size: number; // the island's diameter
}

// `count` points on a circle, clockwise from the top (screen y grows downwards), turned by `phase`.
function ring(count: number, radius: number, phase = 0): Point[] {
  return Array.from({ length: count }, (_, k) => {
    const angle = -Math.PI / 2 + phase + (k / count) * 2 * Math.PI;
    return { x: radius * Math.cos(angle), y: radius * Math.sin(angle) };
  });
}

export function ringLayout(topics: number, bubble: number): RingLayout {
  const step = bubble + GAP; // centre-to-centre distance of neighbouring bubbles
  // The radius at which `count` bubbles on one ring sit `step` apart.
  const fit = (count: number) => (count < 2 ? 0 : step / (2 * Math.sin(Math.PI / count)));
  const centre = { x: 0, y: 0 };

  let points: Point[];
  if (topics < 5) {
    // Two side by side read left to right; one sits in the centre.
    points = ring(topics, fit(topics), topics === 2 ? -Math.PI / 2 : 0);
  } else if (topics <= 13) {
    points = [centre, ...ring(topics - 1, Math.max(step, fit(topics - 1)))];
  } else {
    // A second ring beyond the first six, turned half a slot so its bubbles sit between the spokes.
    const outer = topics - 7;
    points = [centre, ...ring(6, step), ...ring(outer, Math.max(2 * step, fit(outer)), Math.PI / outer)];
  }

  const reach = Math.max(0, ...points.map(({ x, y }) => Math.hypot(x, y)));
  return { points, size: 2 * (reach + bubble / 2 + PAD) };
}
