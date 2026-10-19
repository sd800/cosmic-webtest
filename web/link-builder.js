(() => {
  'use strict';
  const form = document.querySelector('#link-builder');
  if (!form) return;
  const field = name => form.elements.namedItem(name);
  const encode = value => encodeURIComponent(value.toWellFormed());

  function addresses(value) {
    if (!value.trim()) return [];
    const items = value.split(/[,;]/).map(item => item.trim());
    return items.every(item => /^[^\s@<>"?&#:,;]+@[^\s@<>/?#&:,;]+\.[^\s@<>/?#&:,;.]+$/u.test(item)) ? items : null;
  }

  function setLink(kind, uri, label) {
    const link = document.querySelector(`#builder-${kind}-link`);
    const code = document.querySelector(`#builder-${kind}-uri`);
    link.replaceChildren(document.createTextNode(label));
    if (uri) {
      const arrow = document.createElement('span');
      arrow.setAttribute('aria-hidden', 'true');
      arrow.textContent = '↗';
      link.append(arrow);
      link.setAttribute('href', uri);
      link.removeAttribute('aria-disabled');
      link.removeAttribute('tabindex');
    } else {
      link.removeAttribute('href');
      link.setAttribute('aria-disabled', 'true');
      link.tabIndex = -1;
    }
    code.textContent = uri || '—';
  }

  function update() {
    const rawPhone = field('phone').value.trim();
    const phone = rawPhone.replace(/[\s().-]/g, '');
    const phoneValid = /^\+?\d{3,15}$/.test(phone);
    const phoneInvalid = Boolean(rawPhone) && !phoneValid;
    field('phone').setAttribute('aria-invalid', String(phoneInvalid));
    document.querySelector('#builder-phone-error').hidden = !phoneInvalid;
    const phoneLabel = rawPhone || '等待输入电话号码';
    setLink('tel', phoneValid ? `tel:${phone}` : '', phoneLabel);
    const smsBody = field('smsBody').value;
    setLink('sms', phoneValid ? `sms:${phone}${smsBody ? `?body=${encode(smsBody)}` : ''}` : '', phoneLabel);

    const to = addresses(field('email').value);
    const cc = addresses(field('cc').value);
    const bcc = addresses(field('bcc').value);
    for (const [name, values] of [['email', to], ['cc', cc], ['bcc', bcc]]) {
      field(name).setAttribute('aria-invalid', String(values === null));
    }
    document.querySelector('#builder-email-error').hidden = to !== null && cc !== null && bcc !== null;
    let mailUri = '';
    if (to?.length && cc && bcc) {
      const query = [];
      for (const [key, value] of [['cc', cc.join(',')], ['bcc', bcc.join(',')], ['subject', field('subject').value], ['body', field('mailBody').value]]) {
        if (value) query.push(`${key}=${encode(value)}`);
      }
      mailUri = `mailto:${to.map(address => encode(address).replace(/%40/gi, '@')).join(',')}${query.length ? `?${query.join('&')}` : ''}`;
    }
    setLink('mailto', mailUri, field('email').value.trim() || '等待输入邮箱地址');
  }

  form.addEventListener('input', update);
  form.addEventListener('submit', event => event.preventDefault());
  document.querySelector('#builder-reset').addEventListener('click', () => {
    form.reset();
    update();
  });
  update();
})();
