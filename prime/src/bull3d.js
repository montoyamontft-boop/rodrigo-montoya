// Karnes del Norte Prime — the logo's bull as a lit, faceted sculpture (three.js).
// The facets come from bull.json (traced from the logo by site/trace_logo.py); each one is extruded on its own,
// tipped a few degrees like a folded plane, so the light breaks on it the way it does on an origami bull.
//
//   const bull = Bull3D.mount(el, { data, onHover(cut, x, y), onSelect(cut), interactive: true, view: { y: -0.4 } })
//   bull.focus('ribeye' | null)   lift one cut toward the light, ember-lit
//   bull.explode(0..1)            separate the cuts in depth and outward
//   bull.view({ y, x, zoom })     turn the sculpture (eased)
//   bull.supported                false when WebGL is unavailable (the page keeps its SVG bull)
import {
  ACESFilmicToneMapping, AmbientLight, Color, DirectionalLight, ExtrudeGeometry, Group, Mesh, MeshStandardMaterial,
  PCFSoftShadowMap, PerspectiveCamera, PlaneGeometry, Raycaster, Scene, Shape, ShadowMaterial, SpotLight,
  SRGBColorSpace, Vector2, Vector3, WebGLRenderer,
} from 'three';

const BONE = new Color('#ece6dc');
const EMBER = new Color('#c9a45c');
const DIM = new Color('#8f8a83');

function webgl() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl2') || c.getContext('webgl')));
  } catch { return false; }
}

function parse(data) {
  const [x0, y0, w, h] = data.viewBox.split(/\s+/).map(Number);
  const cx = x0 + w / 2, cy = y0 + h / 2, s = 10 / Math.max(w, h);
  const toPts = (str) => str.trim().split(/\s+/).map((p) => { const [x, y] = p.split(',').map(Number); return new Vector2((x - cx) * s, -(y - cy) * s); });
  const facets = [];
  for (const [cut, polys] of Object.entries(data.cuts)) polys.forEach((p) => facets.push({ cut, pts: toPts(p) }));
  data.chamberete.forEach((p) => facets.push({ cut: 'chamberete', pts: toPts(p) }));
  data.rest.forEach((p) => facets.push({ cut: null, pts: toPts(p) }));
  return facets;
}

// a small deterministic random, so the sculpture is the same on every visit
const rnd = (i) => { const x = Math.sin(i * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

export function mount(el, opts = {}) {
  const api = { supported: webgl(), focus() {}, explode() {}, view() {}, dispose() {} };
  if (!api.supported) return api;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  const renderer = new WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = SRGBColorSpace;
  renderer.toneMapping = ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = PCFSoftShadowMap;
  renderer.domElement.className = 'bull3d-canvas';
  renderer.domElement.setAttribute('aria-hidden', 'true');
  el.appendChild(renderer.domElement);
  el.classList.add('is-3d');

  const scene = new Scene();
  const camera = new PerspectiveCamera(30, 1, 0.1, 100);
  camera.position.set(0, 0.6, 24);

  // light: one warm key from above-left, an ember rim from behind, almost no fill — a lit thing in a dark room
  scene.add(new AmbientLight('#ffffff', 0.07));
  const key = new SpotLight('#ffe3c4', 760, 60, 0.4, 0.6, 1.6);
  key.position.set(-13, 12, 10);
  key.castShadow = true;
  key.shadow.mapSize.set(1024, 1024);
  key.shadow.bias = -0.0004;
  scene.add(key, key.target);
  const rim = new DirectionalLight('#ff8a4c', 3.4);
  rim.position.set(9, 4, -10);
  scene.add(rim);
  const fill = new DirectionalLight('#c9d2ff', 0.25);
  fill.position.set(8, -2, 10);
  scene.add(fill);

  const floor = new Mesh(new PlaneGeometry(60, 60), new ShadowMaterial({ opacity: 0.38 }));
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -5.15;
  floor.receiveShadow = true;
  scene.add(floor);

  const bull = new Group();
  scene.add(bull);
  const meshes = [];
  parse(opts.data).forEach((f, i) => {
    const shape = new Shape(f.pts);
    const depth = f.cut ? 0.55 + rnd(i) * 0.5 : 0.5 + rnd(i) * 0.2;
    const geo = new ExtrudeGeometry(shape, { depth, bevelEnabled: true, bevelThickness: 0.09, bevelSize: 0.05, bevelSegments: 1, curveSegments: 2 });
    geo.computeBoundingBox();
    const c = new Vector3(); geo.boundingBox.getCenter(c);
    geo.translate(-c.x, -c.y, -depth / 2);
    const mat = new MeshStandardMaterial({ color: BONE.clone(), roughness: 0.52, metalness: 0.04, flatShading: true, emissive: new Color('#000000') });
    const m = new Mesh(geo, mat);
    m.position.set(c.x, c.y, (rnd(i + 7) - 0.5) * 0.5);
    // tip each facet a few degrees, like a folded plane
    m.rotation.set((rnd(i + 3) - 0.5) * 0.16, (rnd(i + 5) - 0.5) * 0.2, 0);
    m.castShadow = true;
    m.receiveShadow = true;
    m.userData = { cut: f.cut, home: m.position.clone(), dir: new Vector3(c.x, c.y, 0).normalize(), lift: 0, glow: 0, i };
    bull.add(m);
    meshes.push(m);
  });

  // state, eased every frame
  const st = { ry: opts.view?.y ?? -0.38, rx: opts.view?.x ?? 0.04, zoom: opts.view?.zoom ?? 1, explode: 0, focus: null, px: 0, py: 0, hover: null };
  const cur = { ry: st.ry, rx: st.rx, zoom: st.zoom, explode: 0, px: 0, py: 0 };

  const size = () => {
    const r = el.getBoundingClientRect();
    const w = Math.max(1, r.width), h = Math.max(1, r.height);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // keep the whole bull in frame on tall and wide boxes alike
    camera.position.z = (w / h < 0.9 ? 30 : 24) / cur.zoom;
    camera.updateProjectionMatrix();
  };
  const ro = new ResizeObserver(size);
  ro.observe(el);
  size();

  // pointer: the bull turns a little toward it; facets answer the pointer
  const ray = new Raycaster(), ndc = new Vector2();
  const pick = (e) => {
    const r = renderer.domElement.getBoundingClientRect();
    ndc.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    ray.setFromCamera(ndc, camera);
    const hit = ray.intersectObjects(meshes, false)[0];
    return hit && hit.object.userData.cut ? hit.object.userData.cut : null;
  };
  if (opts.interactive) {
    const host = opts.pointerHost || el;
    host.addEventListener('pointermove', (e) => {
      if (e.pointerType === 'touch') return;
      const r = host.getBoundingClientRect();
      st.px = ((e.clientX - r.left) / r.width) * 2 - 1;
      st.py = ((e.clientY - r.top) / r.height) * 2 - 1;
      const cut = pick(e);
      if (cut !== st.hover) { st.hover = cut; el.style.cursor = cut ? 'pointer' : ''; }
      opts.onHover && opts.onHover(cut, e.clientX, e.clientY);
      wake();
    });
    host.addEventListener('pointerleave', () => { st.px = st.py = 0; st.hover = null; opts.onHover && opts.onHover(null); wake(); });
    renderer.domElement.addEventListener('click', (e) => { const cut = pick(e); if (cut && opts.onSelect) opts.onSelect(cut); });
  }

  let raf = 0, visible = true, t0 = performance.now();
  const ease = (a, b, k) => a + (b - a) * k;
  const frame = (now) => {
    raf = 0;
    const t = (now - t0) / 1000, k = reduce ? 1 : 0.075;
    cur.ry = ease(cur.ry, st.ry + st.px * 0.32, k);
    cur.rx = ease(cur.rx, st.rx + st.py * 0.1, k);
    cur.explode = ease(cur.explode, st.explode, reduce ? 1 : 0.09);
    if (Math.abs(cur.zoom - st.zoom) > 0.001) { cur.zoom = ease(cur.zoom, st.zoom, k); size(); }
    bull.rotation.y = cur.ry + (reduce ? 0 : Math.sin(t * 0.45) * 0.05);
    bull.rotation.x = cur.rx;
    bull.position.y = reduce ? 0 : Math.sin(t * 0.8) * 0.06;
    let moving = !reduce;
    for (const m of meshes) {
      const u = m.userData;
      const on = u.cut && (u.cut === st.focus || u.cut === st.hover);
      u.lift = ease(u.lift, on ? 1 : 0, reduce ? 1 : 0.12);
      u.glow = ease(u.glow, on ? 1 : 0, reduce ? 1 : 0.12);
      const e = cur.explode, out = 1.5 * e, z = (rnd(u.i + 11) - 0.35) * 2.2 * e + u.lift * 1.4;
      m.position.set(u.home.x + u.dir.x * out, u.home.y + u.dir.y * out, u.home.z + z);
      const dim = st.focus && !on ? 0.55 : 0;
      m.material.color.copy(BONE).lerp(DIM, dim).lerp(EMBER, u.glow * 0.85);
      m.material.emissive.copy(EMBER).multiplyScalar(u.glow * 0.18);
      if (Math.abs(u.lift - (on ? 1 : 0)) > 0.002) moving = true;
    }
    if (Math.abs(cur.ry - (st.ry + st.px * 0.32)) > 0.0005 || Math.abs(cur.explode - st.explode) > 0.0005) moving = true;
    renderer.render(scene, camera);
    if (moving && visible && !document.hidden) raf = requestAnimationFrame(frame);
  };
  const wake = () => { if (!raf && visible) raf = requestAnimationFrame(frame); };
  new IntersectionObserver((es) => { visible = es[0].isIntersecting; if (visible) wake(); }, { rootMargin: '120px' }).observe(el);
  document.addEventListener('visibilitychange', wake);
  wake();

  api.focus = (cut) => { st.focus = cut || null; wake(); };
  api.explode = (v) => { st.explode = Math.max(0, Math.min(1, v)); wake(); };
  api.view = (v = {}) => { if (v.y != null) st.ry = v.y; if (v.x != null) st.rx = v.x; if (v.zoom != null) st.zoom = v.zoom; wake(); };
  api.dispose = () => { cancelAnimationFrame(raf); ro.disconnect(); renderer.dispose(); };
  return api;
}

window.Bull3D = { mount };
