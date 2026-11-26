/* Five original research marks sampled as surfaces in three dimensions. */
(() => {
  'use strict';

  const tau = 2 * Math.PI;
  const sin = Math.sin;
  const cos = Math.cos;

  function surface(points, columns, rows, sample, { wrapRows = false } = {}) {
    for (let row = 0; row < rows; row++) {
      for (let column = 0; column < columns; column++) {
        const u = column / columns;
        const v = row / (wrapRows ? rows : rows - 1);
        points.push(sample(u, v));
      }
    }
  }

  // The feedback loop returns through each of three swollen nodes.
  function agentLoop(points) {
    surface(points, 94, 19, (u, v) => {
      const a = tau * u;
      const b = tau * v;
      const lobe = (.5 + .5 * cos(3 * a)) ** 3;
      const tube = .105 + .245 * lobe;
      const radius = .67 + tube * cos(b);
      return [radius * cos(a), .88 * radius * sin(a), tube * sin(b) + .21 * sin(3 * a)];
    }, { wrapRows: true });
  }

  // A sheet rolls over itself, opening into six outward-facing petals.
  function generationBloom(points) {
    surface(points, 104, 16, (u, v) => {
      const a = tau * u;
      const b = tau * v;
      const petal = (.5 + .5 * cos(6 * a)) ** .84;
      const radius = .49 + .265 * petal + .205 * cos(b);
      return [radius * cos(a), radius * sin(a), .245 * sin(b) + .15 * petal];
    }, { wrapRows: true });
  }

  // Offset token grids fold into three parallel attention planes.
  function attentionLayers(points) {
    for (let layer = -1; layer <= 1; layer++) {
      surface(points, 29, 17, (u, v) => {
        const x = (u * 29 / 28 - .5) * 1.74;
        const z = (v - .5) * .97;
        return [x, layer * .33 + .22 * sin(x * 3.2 + .7 * z), z];
      });
    }
  }

  // An almond-shaped aperture surrounds a separate, suspended pupil.
  function visionIris(points) {
    surface(points, 100, 13, (u, v) => {
      const a = tau * u;
      const b = tau * v;
      const radius = .09;
      return [(1 + radius * cos(b)) * cos(a),
        (.52 + radius * cos(b)) * sin(a) * (.58 + .42 * Math.abs(sin(a))),
        radius * sin(b) + .09 * cos(2 * a)];
    }, { wrapRows: true });
    surface(points, 35, 18, (u, v) => {
      const a = tau * u;
      const b = Math.PI * (v - .5);
      return [.29 * cos(b) * cos(a), .29 * sin(b), .29 * cos(b) * sin(a)];
    });
  }

  // Paired signals wind along a common axis and align at regular intervals.
  function pairedHelix(points) {
    const turns = tau * 1.24;
    for (const phase of [0, Math.PI]) {
      surface(points, 76, 14, (u, v) => {
        const a = u * turns + phase;
        const b = v * tau;
        const radius = .42 + .115 * cos(b);
        return [(u - .5) * 2.1 + .075 * sin(b), radius * cos(a), radius * sin(a)];
      }, { wrapRows: true });
    }
    for (let step = 0; step < 10; step++) {
      const u = .035 + step * .1;
      const a = u * turns;
      for (let index = 0; index < 12; index++) {
        const radius = (index / 11 - .5) * .85;
        points.push([(u - .5) * 2.1, radius * cos(a), radius * sin(a)]);
      }
    }
  }

  const subjects = {
    agents: { make: agentLoop, pitch: .62, yaw: -.18, roll: -.2 },
    genai: { make: generationBloom, pitch: .31, yaw: -.22, roll: .09 },
    llm: { make: attentionLayers, pitch: -.58, yaw: -.42, roll: -.04 },
    vision: { make: visionIris, pitch: .2, yaw: .05, roll: -.08 },
    biomedical: { make: pairedHelix, pitch: .2, yaw: .22, roll: -.42 },
  };

  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const visible = new Set();
  const byCanvas = new Map();
  let frame = 0;
  let lastPaint = 0;
  let phase = 0;

  function paint(mark) {
    const { canvas, context, points, subject, width, height, pixelRatio } = mark;
    if (!width || !height) return;
    const angle = phase + mark.offset;
    const pitch = subject.pitch + .15 * sin(angle * .75);
    const yaw = subject.yaw + .42 * sin(angle * .68);
    const roll = subject.roll + .06 * sin(angle * .87);
    const cx = cos(pitch), sx = sin(pitch), cy = cos(yaw), sy = sin(yaw), cz = cos(roll), sz = sin(roll);
    const scale = Math.min(width * .402, height * .43);
    const dot = Math.max(.57, scale * .022);
    context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    context.clearRect(0, 0, width, height);
    context.translate(width * .5, height * .5);
    context.fillStyle = getComputedStyle(canvas).color;

    // One fill call per mark. Near dots are heavier, so depth survives at small sizes.
    context.beginPath();
    for (const [x, y, z] of points) {
      const tx = x * cy + z * sy;
      const tz = z * cy - x * sy;
      const ty = y * cx - tz * sx;
      const depth = y * sx + tz * cx;
      const perspective = 1 / (1 - depth * .085);
      const px = (tx * cz - ty * sz) * scale * perspective;
      const py = (ty * cz + tx * sz) * scale * perspective;
      const size = Math.max(.35, dot * (1.04 + .69 * depth));
      context.moveTo(px + size, py);
      context.arc(px, py, size, 0, tau);
    }
    context.fill();
  }

  function resize(mark) {
    const width = mark.canvas.clientWidth;
    const height = mark.canvas.clientHeight;
    const pixelRatio = Math.min(devicePixelRatio || 1, 2);
    mark.canvas.width = Math.round(width * pixelRatio);
    mark.canvas.height = Math.round(height * pixelRatio);
    Object.assign(mark, { width, height, pixelRatio });
    paint(mark);
  }

  function tick(now) {
    if (now - lastPaint >= 40) {
      if (lastPaint) phase += Math.min(now - lastPaint, 90) * .0011;
      lastPaint = now;
      visible.forEach(paint);
    }
    frame = requestAnimationFrame(tick);
  }

  function syncPlayback() {
    const play = visible.size && !document.hidden && !preference.matches && !document.body.classList.contains('still');
    if (play && !frame) {
      lastPaint = 0;
      frame = requestAnimationFrame(tick);
    } else if (!play && frame) {
      cancelAnimationFrame(frame);
      frame = 0;
    }
  }

  const viewport = new IntersectionObserver(entries => {
    for (const entry of entries) {
      const mark = byCanvas.get(entry.target);
      if (entry.isIntersecting) {
        visible.add(mark);
        paint(mark);
      } else visible.delete(mark);
    }
    syncPlayback();
  });
  const sizeChanges = new ResizeObserver(entries => {
    for (const entry of entries) resize(byCanvas.get(entry.target));
  });

  for (const canvas of document.querySelectorAll('canvas[data-mark]')) {
    const subject = subjects[canvas.dataset.mark];
    const context = canvas.getContext('2d');
    if (!subject || !context) continue;
    const points = [];
    subject.make(points);
    const mark = { canvas, subject, points, context, offset: byCanvas.size * .41 };
    byCanvas.set(canvas, mark);
    resize(mark);
    sizeChanges.observe(canvas);
    viewport.observe(canvas);
  }
  new MutationObserver(syncPlayback).observe(document.body, { attributes: true, attributeFilter: ['class'] });
  preference.addEventListener('change', syncPlayback);
  document.addEventListener('visibilitychange', syncPlayback);
})();
