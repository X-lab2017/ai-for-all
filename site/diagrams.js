/* Progressive enhancement: all static relationships remain visible without JS. */
document.querySelectorAll('.concept').forEach(figure => {
  const data = JSON.parse(figure.querySelector('.concept-data').textContent);
  const detail = figure.querySelector('.concept-detail');
  const buttons = figure.querySelectorAll('[data-select]');
  figure.classList.add('is-interactive');
  buttons.forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.select;
    const selected = data[id];
    if (!selected) return;
    buttons.forEach(item => item.setAttribute('aria-pressed', String(item.dataset.select === id)));
    figure.querySelectorAll('.concept-node').forEach(node => node.classList.toggle('is-selected', node.dataset.node === id));
    figure.querySelectorAll('.concept-edge').forEach(edge => edge.classList.toggle('is-related', edge.dataset.from === id || edge.dataset.to === id));
    detail.querySelector('strong').textContent = selected.title;
    detail.querySelector('p').textContent = selected.detail;
  }));
});
