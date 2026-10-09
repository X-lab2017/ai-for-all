(() => {
  'use strict';
  const $ = s => document.querySelector(s), $$ = s => [...document.querySelectorAll(s)];
  const scenes = $$('.scene'), reduced = matchMedia('(prefers-reduced-motion: reduce)');
  let current = 0, paused = reduced.matches, tour = false, elapsed = 0, clock = 0, last = null, lastPulse = -1, inspecting = false;
  const details = {
    practice: ['成长 / 01', '实践贡献', '从真实问题开始，贡献代码、文档、数据、工具或使用反馈。公共品的采用，也会带来新的问题与下一轮实践。'],
    visible: ['成长 / 02', '贡献可见', '借助数据与评价识别多样贡献，提供可追溯的证据；不把单一排名等同于一个人的全部价值。'],
    growth: ['成长 / 03', '人才成长', '在实践、反馈与协作中积累能力，让学习者与开发者获得继续创造的机会。'],
    goods: ['成长 / 04', '公共品与应用', '把能力转化为可共享、可维护的成果。经过采用与本地化，回应真实需要，并将反馈带回实践。'],
    resources: ['投入 / 01', '资源投入', '汇聚算力、资金、导师时间、工具与场景等支持，为有价值的实践提供条件。'],
    match: ['投入 / 02', '匹配支持', '依据公开条件、实际需要与实践证据匹配资源。基础参与无需既有贡献分数。'],
    value: ['投入 / 03', '价值实现', '资源支持开发者成长、公共品维护和场景应用；价值是否实现，需要从实际采用与受益中判断。'],
    verify: ['投入 / 04', '效果验证', '检查资源是否回应需要、成果是否产生帮助。公开结果与局限，为下一轮投入提供依据。'],
    core: ['共同内核', '数据与评价', '两个飞轮的共同依据：实践证据汇入，评价依据反馈。它支持识别贡献、匹配资源、核验效果，是支撑循环的内核，不是第三个飞轮。']
  };
  const mapDetails = {
    goal: ['一个目标：用得起，更用得好。', '技术可获得只是起点；持续使用、学习和创造的能力，决定机会能否成为实际帮助。'],
    forces: ['两股力量：开源 × 开发者。', '开源降低门槛，开发者把能力转化为工具和应用。两股力量相互促进，共同支持公共品创造。'],
    core: ['一个内核：数据与评价。', '来自实践的证据支持识别贡献、匹配资源与核验效果；评价依据再反馈到两个飞轮。'],
    cycles: ['两个飞轮：成长与投入。', '成长创造公共品与应用价值，投入支持持续实践。效果证据为下一轮支持提供依据。'],
    benefits: ['三重普惠：互补的受益视角。', '开发者、大众、全球南方不是互斥人群，也不是先后阶段；它们帮助我们看见不同需要并检验受益。']
  };
  function setDetail(key) {
    const item = details[key]; if (!item) return;
    $$('#flywheels [data-detail]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.detail === key)));
    $('#cycle-detail .detail-number').textContent = item[0];
    $('#cycle-detail h2').textContent = item[1]; $('#cycle-detail p').textContent = item[2];
  }
  function setMap(key) {
    if (!mapDetails[key]) return;
    $$('[data-map]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.map === key)));
    $('#map-detail h2').textContent = mapDetails[key][0]; $('#map-detail p').textContent = mapDetails[key][1];
  }
  function updateControls() {
    $('#previous').disabled = current === 0; $('#next').disabled = current === scenes.length - 1;
    $('.chapter[aria-current]')?.removeAttribute('aria-current');
    $(`.chapter[data-go="${current}"]`).setAttribute('aria-current', 'step');
    $('#status').textContent = `${tour ? '自动导览 · 无声' : '自由探索'} · 0${current + 1} / 03`;
    $('#autoplay').textContent = tour ? 'Ⅱ 暂停导览' : elapsed >= 90000 ? '↺ 重播导览' : elapsed > 0 ? '▷ 继续导览' : '▷ 90 秒导览';
    $('#autoplay').setAttribute('aria-pressed', String(tour));
  }
  function show(index, manual = false) {
    index = Math.max(0, Math.min(scenes.length - 1, index));
    if (manual) { tour = false; elapsed = 0; $('#tour-progress').style.width = '0%'; document.body.classList.remove('tour'); }
    current = index; inspecting = false; lastPulse = -1;
    scenes.forEach((s, i) => { s.hidden = i !== index; });
    history.replaceState(null, '', '#' + scenes[index].id);
    updateControls();
    if (manual) { window.scrollTo({ top: 0, behavior: 'instant' }); $('#stage').focus({ preventScroll: true }); }
    applyMotion();
  }
  function applyMotion() {
    document.body.classList.toggle('paused', paused);
    $('#motion').textContent = paused ? '开启动效' : '暂停动效';
    $('#motion').setAttribute('aria-pressed', String(paused));
    $$('svg').forEach(svg => {
      if (typeof svg.pauseAnimations !== 'function') return;
      if (paused || document.hidden || svg.closest('.scene')?.hidden) svg.pauseAnimations(); else svg.unpauseAnimations();
    });
  }
  function toggleTour() {
    tour = !tour;
    if (tour && (elapsed === 0 || elapsed >= 90000)) { elapsed = 0; show(0); window.scrollTo({ top: 0, behavior: 'instant' }); }
    document.body.classList.toggle('tour', tour); updateControls();
  }
  async function toggleFullscreen() {
    try {
      if (document.fullscreenElement) await document.exitFullscreen();
      else if (document.documentElement.requestFullscreen) await document.documentElement.requestFullscreen();
    } catch { $('#status').textContent = '当前浏览器未允许全屏，可继续浏览演示'; }
  }
  $$('[data-go]').forEach(b => b.addEventListener('click', () => show(Number(b.dataset.go), true)));
  $$('[data-detail]').forEach(b => { b.setAttribute('aria-pressed', 'false'); b.addEventListener('click', () => { inspecting = true; $$('.pulse').forEach(n => n.classList.remove('pulse')); setDetail(b.dataset.detail); }); });
  $$('[data-map]').forEach(b => { b.setAttribute('aria-pressed', 'false'); b.addEventListener('click', () => { inspecting = true; setMap(b.dataset.map); }); });
  $('#motion').addEventListener('click', () => { paused = !paused; applyMotion(); });
  reduced.addEventListener('change', e => { paused = e.matches; applyMotion(); });
  $('#autoplay').addEventListener('click', toggleTour);
  $('#previous').addEventListener('click', () => show(current - 1, true));
  $('#next').addEventListener('click', () => show(current + 1, true));
  $('#fullscreen').addEventListener('click', toggleFullscreen);
  document.addEventListener('fullscreenchange', () => { $('#fullscreen').textContent = document.fullscreenElement ? '退出全屏 ↙' : '全屏演讲 ↗'; });
  $('#sources-open').addEventListener('click', () => { if (tour) toggleTour(); $('#sources').showModal(); });
  $('#sources-close').addEventListener('click', () => $('#sources').close());
  document.addEventListener('keydown', e => {
    if ($('#sources').open || e.altKey || e.ctrlKey || e.metaKey || /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)) return;
    if (e.key === 'ArrowRight') { e.preventDefault(); show(current + 1, true); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); show(current - 1, true); }
    else if (e.code === 'Space' && !e.target.closest('button,a')) { e.preventDefault(); toggleTour(); }
    else if (e.key.toLowerCase() === 'f' && !e.target.closest('button,a')) { e.preventDefault(); toggleFullscreen(); }
  });
  document.addEventListener('visibilitychange', () => { last = null; applyMotion(); });
  window.addEventListener('hashchange', () => { const n = scenes.findIndex(s => '#' + s.id === location.hash); if (n >= 0) show(n, true); });
  function tick(now) {
    const delta = last === null ? 0 : Math.min(now - last, 100); last = now;
    if (!document.hidden) {
      if (!paused) clock += delta;
      if (tour) {
        elapsed = Math.min(90000, elapsed + delta);
        const next = Math.min(2, Math.floor(elapsed / 30000));
        if (next !== current) { show(next); window.scrollTo({ top: 0, behavior: 'instant' }); }
        $('#tour-progress').style.width = `${elapsed / 900}%`;
        if (current === 2 && !inspecting) {
          const k = Math.floor((elapsed - 60000) / 4000);
          if (k < 5) { const key = ['goal', 'forces', 'core', 'cycles', 'benefits'][k]; if (!$(`[data-map="${key}"]`).matches('[aria-pressed=true]')) setMap(key); }
          else { $$('[data-map]').forEach(b => b.setAttribute('aria-pressed', 'false')); $('#map-detail h2').textContent = '从一个真实问题开始。'; $('#map-detail p').textContent = '分享需要、贡献工具与案例，或提供资源和应用场景。'; }
        }
        if (elapsed >= 90000) { tour = false; document.body.classList.remove('tour'); updateControls(); }
      }
      const pulse = Math.floor(clock / 2000) % 4;
      if (!paused && current === 1 && !inspecting && pulse !== lastPulse) {
        lastPulse = pulse; $$('.node').forEach((b, i) => b.classList.toggle('pulse', i % 4 === pulse));
      }
    }
    requestAnimationFrame(tick);
  }
  const start = scenes.findIndex(s => '#' + s.id === location.hash);
  show(start >= 0 ? start : 0); requestAnimationFrame(tick);
})();
