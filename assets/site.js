/* Renders project cards and writing lists from JSON files.
   Adding a project = add one entry to assets/projects.json. No HTML edits. */

async function loadJSON(path) {
  try { const r = await fetch(path); if (!r.ok) return null; return await r.json(); }
  catch (e) { return null; }
}

async function renderProjects(elId, prefix) {
  const el = document.getElementById(elId);
  const data = await loadJSON(prefix + 'assets/projects.json');
  if (!el || !data) return;
  el.replaceChildren();
  data.forEach(p => {
    const a = document.createElement('a');
    a.className = 'card'; a.href = prefix + p.url;
    const img = document.createElement('img');
    img.src = prefix + p.thumbnail; img.alt = p.title; img.loading = 'lazy';
    const body = document.createElement('div'); body.className = 'body';
    const h = document.createElement('h3'); h.textContent = p.title;
    const d = document.createElement('div'); d.className = 'desc'; d.textContent = p.description;
    const tags = document.createElement('div'); tags.className = 'tags';
    (p.tags || []).forEach(t => { const s = document.createElement('span'); s.className = 'tag'; s.textContent = t; tags.appendChild(s); });
    body.append(h, d, tags); a.append(img, body); el.appendChild(a);
  });
}

async function renderPosts(elId, jsonPath, limit) {
  const el = document.getElementById(elId);
  if (!el) return;
  const data = await loadJSON(jsonPath);
  el.replaceChildren();
  const posts = (data && data.posts) ? data.posts.slice(0, limit || 100) : [];
  if (!posts.length) {
    const d = document.createElement('div'); d.className = 'empty-state';
    d.textContent = 'New writing is on the way.';
    el.appendChild(d); return;
  }
  posts.forEach(p => {
    const a = document.createElement('a'); a.className = 'post' + (p.image ? ' has-thumb' : '');
    const prefix = jsonPath.startsWith('assets/') ? '' : '../';
    if (p.page) { a.href = prefix + p.page; }
    else { a.href = p.link; a.target = '_blank'; a.rel = 'noopener'; }
    if (p.image) {
      const img = document.createElement('img'); img.className = 'thumb';
      img.src = p.image; img.alt = ''; img.loading = 'lazy';
      a.appendChild(img);
    }
    const body = document.createElement('div'); body.className = 'pbody';
    const row = document.createElement('div'); row.className = 'prow';
    const h = document.createElement('h3'); h.textContent = p.title;
    const dt = document.createElement('span'); dt.className = 'date'; dt.textContent = p.date || '';
    row.append(h, dt); body.appendChild(row);
    if (p.excerpt) { const e = document.createElement('div'); e.className = 'excerpt'; e.textContent = p.excerpt; body.appendChild(e); }
    if (p.source) { const s = document.createElement('div'); s.className = 'src'; s.textContent = p.page ? p.source : p.source + ' ↗'; body.appendChild(s); }
    a.appendChild(body);
    el.appendChild(a);
  });
}
