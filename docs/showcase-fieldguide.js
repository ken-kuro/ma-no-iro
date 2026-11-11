const enc = x => { const v = x <= 0.0031308 ? 12.92 * x : 1.055 * x ** (1 / 2.4) - 0.055; return Math.round(Math.min(Math.max(v, 0), 1) * 255).toString(16).padStart(2, "0"); };
const linToHex = c => "#" + c.map(enc).join("");
const CONES = /* Stockman and Sharpe (2000) 2-degree cone fundamentals, energy, peak 1: [nm, L, M, S] */ [[390, 0.0004, 0.0004, 0.0095], [395, 0.0011, 0.001, 0.0238], [400, 0.0024, 0.0023, 0.0566], [405, 0.0048, 0.0047, 0.1225], [410, 0.0087, 0.0088, 0.233], [415, 0.0134, 0.0145, 0.3814], [420, 0.0184, 0.0217, 0.5436], [425, 0.0229, 0.0296, 0.6745], [430, 0.0282, 0.0395, 0.8026], [435, 0.0341, 0.0518, 0.9036], [440, 0.0403, 0.0648, 0.991], [445, 0.0449, 0.0759, 0.9915], [450, 0.0499, 0.0871, 0.9554], [455, 0.0553, 0.0982, 0.8602], [460, 0.0647, 0.1163, 0.7867], [465, 0.0807, 0.1445, 0.7383], [470, 0.0995, 0.1759, 0.6464], [475, 0.1188, 0.2054, 0.5164], [480, 0.1401, 0.2358, 0.3903], [485, 0.164, 0.2681, 0.2903], [490, 0.1916, 0.3036, 0.2119], [495, 0.2329, 0.3571, 0.1605], [500, 0.289, 0.4278, 0.1228], [505, 0.3597, 0.5156, 0.0889], [510, 0.4437, 0.6155, 0.0608], [515, 0.5365, 0.7192, 0.0428], [520, 0.6286, 0.8166, 0.0292], [525, 0.7047, 0.8855, 0.0194], [530, 0.7706, 0.9357, 0.0126], [535, 0.8257, 0.9689, 0.0081], [540, 0.881, 0.9952, 0.0051], [545, 0.9191, 0.9972, 0.0032], [550, 0.9402, 0.9772, 0.002], [555, 0.9657, 0.9566, 0.0012], [560, 0.9814, 0.9178, 0.0007], [565, 0.9945, 0.8732, 0.0005], [570, 1.0, 0.8135, 0.0003], [575, 0.9923, 0.7403, 0.0002], [580, 0.9694, 0.6533, 0.0001], [585, 0.9556, 0.5726, 0.0001], [590, 0.9277, 0.4926, 0.0], [595, 0.886, 0.4112, 0.0], [600, 0.834, 0.3344, 0.0], [605, 0.7751, 0.2649, 0.0], [610, 0.7057, 0.2053, 0.0], [615, 0.6308, 0.1562, 0.0], [620, 0.5542, 0.1166, 0.0], [625, 0.4799, 0.0856, 0.0], [630, 0.4007, 0.0621, 0.0], [635, 0.3279, 0.0445, 0.0], [640, 0.2658, 0.0314, 0.0], [645, 0.2133, 0.0218, 0.0], [650, 0.1651, 0.0154, 0.0], [655, 0.1247, 0.0107, 0.0], [660, 0.093, 0.0073, 0.0], [665, 0.0685, 0.005, 0.0], [670, 0.0499, 0.0034, 0.0], [675, 0.0358, 0.0024, 0.0], [680, 0.0254, 0.0016, 0.0], [685, 0.0177, 0.0011, 0.0], [690, 0.0122, 0.0008, 0.0], [695, 0.0085, 0.0005, 0.0], [700, 0.0059, 0.0004, 0.0], [705, 0.0041, 0.0003, 0.0], [710, 0.0028, 0.0002, 0.0], [715, 0.0019, 0.0001, 0.0], [720, 0.0013, 0.0001, 0.0]];
function drawEye() {
  const W = 560, H = 300, pl = 14, pr = 14, pt = 22, pb = 34;
  const x = l => pl + (W - pl - pr) * (l - 390) / 330, y = v => H - pb - (H - pt - pb) * v;
  const path = k => CONES.map((r, i) => (i ? "L" : "M") + x(r[0]).toFixed(1) + " " + y(r[k]).toFixed(1)).join(" ");
  let v = ""; for (let l = 390; l <= 720; l += 2) v += (v ? " L " : "M ") + x(l).toFixed(1) + " " + y(cmf(l)[1]).toFixed(1);
  const a = F.kuromurasaki.ansi.normal;
  const lbl = (l, val, t, c) => `<text x="${x(l)}" y="${y(val) - 8}" text-anchor="middle" font-size="14" font-weight="500" fill="${c}" font-family="IBM Plex Sans, sans-serif">${t}</text>`;
  const ticks = [400, 500, 600, 700].map(l => `<line x1="${x(l)}" y1="${y(0)}" x2="${x(l)}" y2="${y(0) + 5}" stroke="${K.dim.hex}"/><text x="${x(l)}" y="${H - 10}" font-size="12" text-anchor="middle" fill="${K.muted.hex}" font-family="IBM Plex Mono, monospace">${l}</text>`).join("");
  document.getElementById("fig-eye").innerHTML = `<svg viewBox="0 0 ${W} ${H}" aria-hidden="true">
    <line x1="${x(390)}" y1="${y(0)}" x2="${x(720)}" y2="${y(0)}" stroke="${K.dim.hex}"/>${ticks}
    <path d="${path(3)}" fill="none" stroke="${a.blue.hex}" stroke-width="2.5"/>
    <path d="${path(2)}" fill="none" stroke="${a.green.hex}" stroke-width="2.5"/>
    <path d="${path(1)}" fill="none" stroke="${a.red.hex}" stroke-width="2.5"/>
    <path d="${v}" fill="none" stroke="${K.text.hex}" stroke-width="1.5" stroke-dasharray="4 4"/>
    <line x1="${x(555)}" y1="${y(0)}" x2="${x(555)}" y2="${y(1)}" stroke="${K.function.hex}" stroke-width="1"/>
    ${lbl(445, 1, "short", a.blue.hex)}${lbl(530, 1.0, "medium", a.green.hex)}${lbl(600, 0.93, "long", a.red.hex)}
    <text x="${x(555) + 6}" y="${y(0.08)}" font-size="13" fill="${K.function.hex}" font-family="IBM Plex Sans, sans-serif">555 nm</text></svg>`;
}
function drawMix(colors = K) {
  const pairs = [["purple", colors.keyword.hex, "green", colors.function.hex], ["blue", colors.blue.hex, "yellow", colors.yellow.hex], ["red", colors.red.hex, "cyan", colors.cyan.hex]];
  document.getElementById("fig-mix").innerHTML = pairs.map(([an, a, bn, b]) => {
    const A = hexToLin(a), B = hexToLin(b), at = t => A.map((v, k) => v + (B[k] - v) * t);
    const stops = Array.from({ length: 33 }, (_, i) => `${linToHex(at(i / 32))} ${(i / 32 * 100).toFixed(2)}%`).join(", ");
    let grey = 0, least = Infinity;   // the point where the three lights are most nearly equal
    for (let i = 0; i <= 1000; i++) { const c = at(i / 1000), m = (c[0] + c[1] + c[2]) / 3, v = c.reduce((s, x) => s + (x - m) ** 2, 0); if (v < least) { least = v; grey = i / 1000; } }
    return `<div><div class="ends"><span>${an}</span><span>${bn}</span></div><div class="strip" style="background:linear-gradient(90deg, ${stops})"><i class="tick" style="left:${(grey * 100).toFixed(1)}%"></i></div></div>`;
  }).join("");
}

