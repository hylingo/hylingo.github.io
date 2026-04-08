// One-shot reorder of ja_articles.json by difficulty.
// - Bucket by JLPT level
// - Custom order inside N5 and N5–N3
// - Preserve relative order in other buckets
import fs from 'node:fs';

const path = 'public/data/ja_articles.json';
const data = JSON.parse(fs.readFileSync(path, 'utf8'));

const levelOrder = ['N5', 'N5–N4', 'N5–N3', 'N4–N3', 'N3', 'N3–N2', 'N2', 'N1'];

const n5Order = [
  'n5-self-intro-essay',
  'n5-my-family-essay',
  'n5-my-day-essay',
  'n5-my-room-essay',
  'n5-food-i-like-essay',
];

const n5n3Order = [
  'n4-summer-at-grandpas-dialogue',
  'n4-summer-at-grandpas-essay',
  'n4-new-year-relatives-dialogue',
  'n4-new-year-relatives-essay',
  'n3-moving-unpack-dialogue',
  'n3-closet-organize-dialogue',
  'n3-family-dinner-dialogue',
  'n3-tokyo-day-essay',
  'n3-tokyo-day-dialogue',
  'n3-siblings-childhood-dialogue',
  'n3-family-trip-hotel-dialogue',
];

function sortBucket(items, level) {
  if (level === 'N5') {
    const map = new Map(items.map(x => [x.id, x]));
    const out = n5Order.map(id => map.get(id)).filter(Boolean);
    if (out.length !== items.length) throw new Error('N5 id mismatch');
    return out;
  }
  if (level === 'N5–N3') {
    const map = new Map(items.map(x => [x.id, x]));
    const out = n5n3Order.map(id => map.get(id)).filter(Boolean);
    if (out.length !== items.length) throw new Error('N5–N3 id mismatch: ' + out.length + '/' + items.length);
    return out;
  }
  return items; // preserve relative order
}

const buckets = new Map(levelOrder.map(l => [l, []]));
for (const item of data.items) {
  if (!buckets.has(item.level)) throw new Error('Unknown level: ' + item.level);
  buckets.get(item.level).push(item);
}

const reordered = [];
for (const lvl of levelOrder) {
  reordered.push(...sortBucket(buckets.get(lvl), lvl));
}

if (reordered.length !== data.items.length) {
  throw new Error('Count mismatch: ' + reordered.length + ' vs ' + data.items.length);
}

data.items = reordered;
fs.writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
console.log('OK, reordered', reordered.length, 'items');
