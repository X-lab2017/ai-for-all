/* Progressive enhancement. No tracking, external services or automatic animation. */
document.querySelectorAll('.concept').forEach(figure => {
  const data = JSON.parse(figure.querySelector('.concept-data').textContent);
  const detail = figure.querySelector('.concept-detail');
  const buttons = figure.querySelectorAll('[data-select]');
  const select = id => {
    const selected = data.nodes[id];
    if (!selected) return;
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.select === id)));
    figure.querySelectorAll('.concept-node').forEach(node => node.classList.toggle('is-selected', node.dataset.node === id));
    figure.querySelectorAll('.concept-edge').forEach(edge => edge.classList.toggle('is-related', edge.dataset.from === id || edge.dataset.to === id));
    detail.querySelector('strong').textContent = selected.title;
    detail.querySelector('p').textContent = selected.detail;
  };
  figure.classList.add('is-interactive');
  buttons.forEach(button => button.addEventListener('click', () => select(button.dataset.select)));
  select(data.default);
  figure.querySelectorAll('[data-cycle]').forEach(button => button.addEventListener('click', () => {
    const group = button.dataset.cycle;
    figure.querySelectorAll('[data-cycle]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    figure.querySelectorAll('[data-group]').forEach(item => item.classList.toggle('is-muted', group !== 'all' && item.dataset.group && item.dataset.group !== group));
    select(group === 'growth' ? 'practice' : group === 'value' ? 'invest' : 'shared-core');
  }));
});
const sectionLinks = [...document.querySelectorAll('.contents a')];
if ('IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    entries.filter(entry => entry.isIntersecting).forEach(entry => {
      sectionLinks.forEach(link => {
        if (link.hash === '#' + entry.target.id) link.setAttribute('aria-current', 'location');
        else link.removeAttribute('aria-current');
      });
    });
  }, {rootMargin:'-5% 0px -65% 0px'});
  document.querySelectorAll('article h2[id]').forEach(heading => observer.observe(heading));
}
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
