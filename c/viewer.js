/**
 * viewer.js - renders a shared collection link (inthebinder.com/c/#v1/...).
 *
 * Lives in its own file (not inline) so the page can run under a strict
 * Content-Security-Policy: only scripts from this site run, never anything
 * that arrives inside a link.
 */
(function () {
  const S = window.HoloShare;
  const app = document.getElementById('app');
  // A card picture that fails to load becomes a plain placeholder with the
  // card id as TEXT (never markup). 'error' doesn't bubble, so listen in the
  // capture phase once for every <img> the page ever draws.
  app.addEventListener('error', (e) => {
    const img = e.target;
    if (!img || img.tagName !== 'IMG' || !img.dataset || img.dataset.fallback == null) return;
    const ph = document.createElement('div');
    ph.className = 'ph';
    ph.textContent = img.dataset.fallback;
    img.replaceWith(ph);
  }, true);
  const API = 'https://api.pokemontcg.io/v2/cards';
  const setCache = new Map();   // setId -> Promise<Map(cardId -> card)>
  const PRICE_KEY = {
    normal: ['normal', 'unlimited'], reverse: ['reverseHolofoil'], holo: ['holofoil', 'unlimitedHolofoil'],
    firstEdition: ['1stEditionNormal', '1stEdition'], firstEditionHolo: ['1stEditionHolofoil'],
    shadowless: ['unlimited', 'normal'], shadowlessHolo: ['unlimitedHolofoil', 'holofoil'],
  };
  const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const money = (v) => { const n = Number(v); return Number.isFinite(n) ? '$' + (n >= 100 ? n.toFixed(0) : n.toFixed(2)) : ''; };

  // Other games' ids carry the game: set 'op~3188', card 'op~712666' (the
  // TCGplayer product id). Their pictures come from TCGplayer's image server
  // and today's prices from the app's data repository.
  const GAMES = { op: 'One Piece', lorcana: 'Disney Lorcana', dbsfw: 'Dragon Ball Super Fusion World', mtg: 'Magic: The Gathering', ygo: 'Yu-Gi-Oh!' };
  const gameOf = (id) => { const i = String(id).indexOf('~'); const k = i > 0 ? String(id).slice(0, i) : ''; return GAMES[k] ? k : null; };
  const productOf = (id) => String(id).split('~')[1];
  const gamePriceCache = new Map();
  function loadGamePrices(game) {
    if (!gamePriceCache.has(game)) {
      gamePriceCache.set(game, fetch('https://raw.githubusercontent.com/h7k3r/inthebinder-data/data/' + game + '-prices.json')
        .then((r) => (r.ok ? r.json() : null)).then((j) => (j && j.prices) || {}).catch(() => ({})));
    }
    return gamePriceCache.get(game);
  }

  function loadSet(setId) {
    if (setCache.has(setId)) return setCache.get(setId);
    if (gameOf(setId)) { const empty = Promise.resolve(new Map()); setCache.set(setId, empty); return empty; }
    const p = (async () => {
      const map = new Map();
      for (let page = 1; page < 10; page++) {
        const q = `?q=set.id:${encodeURIComponent(setId)}&page=${page}&pageSize=250&select=id,name,number,images,tcgplayer,set`;
        let json = null;
        // The public card API is slow and drops requests under load: retry.
        for (let attempt = 0; attempt < 4 && !json; attempt++) {
          if (attempt) await new Promise((r) => setTimeout(r, 1500 * 2 ** (attempt - 1)));
          try {
            const res = await fetch(API + q);
            if (res.ok) json = await res.json();
          } catch (e) { json = null; }
        }
        if (!json) break;
        for (const c of json.data || []) map.set(c.id, c);
        if (!json.data || json.data.length < 250) break;
      }
      return map;
    })();
    setCache.set(setId, p);
    return p;
  }

  function priceOf(card, variant) {
    const prices = card && card.tcgplayer && card.tcgplayer.prices;
    if (!prices) return null;
    for (const k of PRICE_KEY[variant] || [variant]) {
      if (prices[k] && prices[k].market != null) return prices[k].market;
    }
    return null;
  }

  async function enrich(rows) {
    const sets = [...new Set(rows.map((r) => r.setId))];
    // Two sets at a time: gentler on the API than all at once.
    const maps = new Array(sets.length);
    let next = 0;
    await Promise.all([0, 1].map(async () => {
      while (next < sets.length) { const i = next++; maps[i] = await loadSet(sets[i]); }
    }));
    const bySet = new Map(sets.map((s, i) => [s, maps[i]]));
    const gamePrices = {};
    for (const g of new Set(rows.map((r) => gameOf(r.cardId)).filter(Boolean))) gamePrices[g] = await loadGamePrices(g);
    return rows.map((r) => {
      const g = gameOf(r.cardId);
      if (g) {
        const p = gamePrices[g][productOf(r.cardId) + '|' + (r.variant || 'normal')];
        return { ...r, card: null, game: g, price: p != null ? p : null };
      }
      const card = bySet.get(r.setId) && bySet.get(r.setId).get(r.cardId);
      return { ...r, card, price: priceOf(card, r.variant) };
    });
  }

  function cardTile(r, badge) {
    // Without details, the image server still has the picture at a known address.
    const num = r.cardId.startsWith(r.setId + '-') ? r.cardId.slice(r.setId.length + 1) : '';
    const src = r.game ? `https://tcgplayer-cdn.tcgplayer.com/product/${encodeURIComponent(productOf(r.cardId))}_400w.jpg`
      : r.card && r.card.images ? r.card.images.small : (num ? `https://images.pokemontcg.io/${encodeURIComponent(r.setId)}/${encodeURIComponent(num)}.png` : '');
    const label = r.game ? GAMES[r.game] + ' card' : (r.card ? r.card.name : r.cardId);
    // No inline onerror: an attribute's &#39; is decoded back to ' before the
    // handler runs, so a card id from the link could break out of it. The
    // fallback is swapped in by the 'error' listener on #app instead.
    const img = src ? `<img loading="lazy" src="${esc(src)}" alt="${esc(label)}" data-fallback="${esc(r.cardId)}">`
      : `<div class="ph">${esc(r.cardId)}</div>`;
    const variant = r.variant && r.variant !== 'normal' ? ` · ${esc(r.variant.replace(/([A-Z])/g, ' $1').toLowerCase())}` : '';
    return `<div class="card">${img}
      ${r.quantity > 1 ? `<span class="qty">×${r.quantity}</span>` : ''}
      ${badge ? `<span class="who" style="color:${badge[1]}">${esc(badge[0])}</span>` : ''}
      <div class="name" title="${esc(label)}">${esc(label)}</div>
      <div class="meta"><span>${r.game ? '' : '#' + esc(r.card ? r.card.number : num)}${variant}</span><b>${r.price != null ? money(r.price) : ''}</b></div>
    </div>`;
  }

  function renderSets(list, filter, badgeOf) {
    const f = (filter || '').trim().toLowerCase();
    const shown = f ? list.filter((r) => ((r.card && r.card.name) || r.cardId).toLowerCase().includes(f) || (r.card && r.card.set && r.card.set.name.toLowerCase().includes(f))) : list;
    if (!shown.length) return '<p class="empty">No cards match.</p>';
    const groups = new Map();
    for (const r of shown) {
      if (!groups.has(r.setId)) groups.set(r.setId, []);
      groups.get(r.setId).push(r);
    }
    const ordered = [...groups.entries()].sort((a, b) => {
      const da = (a[1][0].card && a[1][0].card.set && a[1][0].card.set.releaseDate) || '';
      const db = (b[1][0].card && b[1][0].card.set && b[1][0].card.set.releaseDate) || '';
      return db.localeCompare(da);
    });
    return ordered.map(([setId, cards]) => {
      const set = cards[0].card && cards[0].card.set;
      const value = cards.reduce((s, r) => s + (r.price || 0) * r.quantity, 0);
      cards.sort((a, b) => (parseInt(a.card && a.card.number, 10) || 0) - (parseInt(b.card && b.card.number, 10) || 0));
      return `<section class="set"><div class="sethead">
          ${set && set.images ? `<img src="${esc(set.images.logo)}" alt="">` : ''}
          <h2>${esc(set ? set.name : gameOf(setId) ? GAMES[gameOf(setId)] : setId)}</h2>
          <span>${cards.length}${set ? ' of ' + set.printedTotal : ''}${value ? ' · ' + money(value) : ''}</span>
        </div><div class="grid">${cards.map((r) => cardTile(r, badgeOf && badgeOf(r))).join('')}</div></section>`;
    }).join('');
  }

  function totals(list) {
    return {
      cards: list.reduce((s, r) => s + r.quantity, 0),
      value: list.reduce((s, r) => s + (r.price || 0) * r.quantity, 0),
      sets: new Set(list.map((r) => r.setId)).size,
    };
  }

  async function show() {
    const shared = S.parseShareLink(location.hash);
    if (!shared) {
      app.innerHTML = `<h1>Open a collection</h1>
        <p style="color:var(--dim)">In the In the Binder app, go to Collection and tap Share. Open that link here,
        or paste it below.</p>
        <div class="bar"><input id="paste" type="url" placeholder="Paste a In the Binder link"><button id="go">Open</button></div>`;
      document.getElementById('go').onclick = () => {
        const p = S.parseShareLink(document.getElementById('paste').value);
        if (p) { location.hash = document.getElementById('paste').value.split('#')[1]; }
      };
      return;
    }
    app.innerHTML = '<p class="loading">Loading card details…</p>';
    const mine = await enrich(shared.rows);
    const t = totals(mine);
    const title = shared.title || 'A In the Binder collection';
    document.title = `${title} · In the Binder`;

    let other = null;
    let tab = 'all';
    let filter = '';

    function draw() {
      let body;
      if (!other) {
        body = renderSets(mine, filter);
      } else {
        const key = (r) => `${r.cardId}::${r.variant}`;
        const theirs = new Map(other.list.map((r) => [key(r), r]));
        const ours = new Map(mine.map((r) => [key(r), r]));
        const both = mine.filter((r) => theirs.has(key(r)));
        const onlyA = mine.filter((r) => !theirs.has(key(r)));
        const onlyB = other.list.filter((r) => !ours.has(key(r)));
        const pick = { both, a: onlyA, b: onlyB }[tab] || both;
        const label = { both: 'In both', a: `Only in ${title}`, b: `Only in ${other.title}` };
        body = `<div class="tabs">
            ${['both', 'a', 'b'].map((k) => `<button class="tab ${tab === k ? 'on' : ''}" data-tab="${k}">${esc(label[k])} (${{ both, a: onlyA, b: onlyB }[k].length})</button>`).join('')}
          </div>` + renderSets(pick, filter);
      }
      app.innerHTML = `
        <h1>${esc(title)}</h1>
        <div class="stats">
          <div><strong>${t.cards.toLocaleString()}</strong>cards</div>
          <div><strong>${t.sets}</strong>sets</div>
          <div><strong>${t.value ? money(t.value) : '—'}</strong>market value</div>
          ${other ? `<div><strong>${esc(other.title)}</strong>${totals(other.list).cards.toLocaleString()} cards · ${money(totals(other.list).value)}</div>` : ''}
        </div>
        <div class="bar">
          <input id="filter" type="search" placeholder="Search cards or sets" value="${esc(filter)}">
          ${other ? '<button class="ghost" id="clear">Stop comparing</button>'
                  : '<input id="cmp" type="url" placeholder="Compare with another In the Binder link"><button id="cmpgo">Compare</button>'}
        </div>
        ${body}`;
      const fi = document.getElementById('filter');
      fi.oninput = () => { filter = fi.value; const pos = fi.selectionStart; draw(); const n = document.getElementById('filter'); n.focus(); n.setSelectionRange(pos, pos); };
      const go = document.getElementById('cmpgo');
      if (go) go.onclick = async () => {
        const p = S.parseShareLink(document.getElementById('cmp').value);
        if (!p) { alert('That is not a In the Binder link.'); return; }
        go.textContent = 'Loading…';
        other = { title: p.title || 'Other collection', list: await enrich(p.rows) };
        tab = 'both';
        draw();
      };
      const cl = document.getElementById('clear');
      if (cl) cl.onclick = () => { other = null; draw(); };
      app.querySelectorAll('[data-tab]').forEach((b) => { b.onclick = () => { tab = b.dataset.tab; draw(); }; });
    }
    draw();
  }

  window.addEventListener('hashchange', show);
  show();
})();
