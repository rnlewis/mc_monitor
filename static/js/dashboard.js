function copySeed(el) {
  navigator.clipboard.writeText(el.textContent);

  // Temporarily swap tooltip text
  el.classList.add('show-tooltip');
  setTimeout(() => el.classList.remove('show-tooltip'), 1500);
}