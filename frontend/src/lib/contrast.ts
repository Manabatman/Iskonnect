/** Parse `hsl(H S% L%)` or `hsl(H S% L% / a)` into linear RGB 0–1. */
function hslToRgb(hsl: string): [number, number, number] {
  const match = hsl.match(/hsl\(\s*([\d.]+)\s+([\d.]+)%\s+([\d.]+)%/i);
  if (!match) throw new Error(`Invalid HSL: ${hsl}`);
  const h = Number(match[1]) / 360;
  const s = Number(match[2]) / 100;
  const l = Number(match[3]) / 100;

  const hue2rgb = (p: number, q: number, t: number) => {
    let tt = t;
    if (tt < 0) tt += 1;
    if (tt > 1) tt -= 1;
    if (tt < 1 / 6) return p + (q - p) * 6 * tt;
    if (tt < 1 / 2) return q;
    if (tt < 2 / 3) return p + (q - p) * (2 / 3 - tt) * 6;
    return p;
  };

  let r: number;
  let g: number;
  let b: number;
  if (s === 0) {
    r = g = b = l;
  } else {
    const q = l < 0.5 ? l * (1 + s) : l + s - l * s;
    const p = 2 * l - q;
    r = hue2rgb(p, q, h + 1 / 3);
    g = hue2rgb(p, q, h);
    b = hue2rgb(p, q, h - 1 / 3);
  }
  return [r, g, b];
}

function relativeLuminance([r, g, b]: [number, number, number]): number {
  const transform = (c: number) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4);
  return 0.2126 * transform(r) + 0.7152 * transform(g) + 0.0722 * transform(b);
}

export function contrastRatio(fgHsl: string, bgHsl: string): number {
  const l1 = relativeLuminance(hslToRgb(fgHsl));
  const l2 = relativeLuminance(hslToRgb(bgHsl));
  const lighter = Math.max(l1, l2);
  const darker = Math.min(l1, l2);
  return (lighter + 0.05) / (darker + 0.05);
}

export interface ContrastPair {
  name: string;
  foreground: string;
  background: string;
  minRatio: number;
}

export function assertContrastPairs(pairs: ContrastPair[]): void {
  for (const pair of pairs) {
    const ratio = contrastRatio(pair.foreground, pair.background);
    if (ratio < pair.minRatio) {
      throw new Error(`${pair.name}: contrast ${ratio.toFixed(2)} < ${pair.minRatio}`);
    }
  }
}
