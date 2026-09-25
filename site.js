const tabs = [...document.querySelectorAll('.navigation [data-view]')];
const views = [...document.querySelectorAll('.view')];
function selectView(id) {
  const target = tabs.find(tab => tab.dataset.view === id) || tabs[0];
  for (const tab of tabs) {
    const selected = tab === target;
    tab.setAttribute('aria-selected', String(selected));
    tab.tabIndex = selected ? 0 : -1;
  }
  document.documentElement.dataset.view = target.dataset.view;
  for (const view of views) view.hidden = view.id !== `panel-${target.dataset.view}`;
}
function fromHash() { selectView(location.hash.slice(1)); }
function navigate(id) {
  if (location.hash !== `#${id}`) history.pushState(null, '', `#${id}`);
  selectView(id);
}
for (const tab of tabs) tab.addEventListener('click', () => navigate(tab.dataset.view));
document.querySelector('.identity').addEventListener('click', event => {
  event.preventDefault(); navigate('documents');
});
document.querySelector('.navigation').addEventListener('keydown', event => {
  const index = tabs.indexOf(event.target);
  if (index < 0) return;
  let next;
  if (event.key === 'ArrowDown' || event.key === 'ArrowRight') next = (index + 1) % tabs.length;
  else if (event.key === 'ArrowUp' || event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
  else if (event.key === 'Home') next = 0;
  else if (event.key === 'End') next = tabs.length - 1;
  else return;
  event.preventDefault(); tabs[next].focus(); tabs[next].click();
});
addEventListener('hashchange', fromHash);
addEventListener('popstate', fromHash);
fromHash();
const mobileNavigation = matchMedia('(max-width: 800px)');
function orientTabs() { document.querySelector('.navigation').setAttribute('aria-orientation', mobileNavigation.matches ? 'horizontal' : 'vertical'); }
mobileNavigation.addEventListener('change', orientTabs); orientTabs();
