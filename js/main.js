// ===== EZUP Atlantic Main JS =====

// Sticky header scroll effect
const header = document.querySelector('.header');
if (header) {
 window.addEventListener('scroll', () => {
  header.classList.toggle('scrolled', window.scrollY > 50);
 });
}

// Mobile menu
const menuToggle = document.querySelector('.menu-toggle');
const mobileNav = document.querySelector('.mobile-nav');
const mobileNavClose = document.querySelector('.mobile-nav-close');

if (menuToggle && mobileNav) {
 menuToggle.addEventListener('click', () => { mobileNav.classList.add('active'); document.body.style.overflow = 'hidden'; });
 if (mobileNavClose) mobileNavClose.addEventListener('click', () => { mobileNav.classList.remove('active'); document.body.style.overflow = ''; });
 mobileNav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => { mobileNav.classList.remove('active'); document.body.style.overflow = ''; });
 });
}

// Scroll animations
const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
const observer = new IntersectionObserver((entries) => {
 entries.forEach(entry => {
  if (entry.isIntersecting) {
   entry.target.classList.add('animate-in');
   observer.unobserve(entry.target);
  }
 });
}, observerOptions);

document.querySelectorAll('.category-card, .product-card, .model-card, .trust-item, .size-pill').forEach(el => {
 el.style.opacity = '0';
 el.style.transform = 'translateY(30px)';
 observer.observe(el);
});

// Quote form submission
const quoteForm = document.getElementById('quote-form');
if (quoteForm) {
 quoteForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(quoteForm);
  const data = Object.fromEntries(formData);
  const btn = quoteForm.querySelector('button[type="submit"]');
  const originalHTML = btn.innerHTML;

  // Loading state
  btn.disabled = true;
  btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="animation:spin 1s linear infinite"><circle cx="12" cy="12" r="10"/></svg> Sending...';
  btn.style.opacity = '0.7';

  try {
   const res = await fetch('/api/quote-request', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(data)
   });
   const result = await res.json();

   if (res.ok && result.ok) {
    // Success
    btn.innerHTML = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> Request Sent!';
    btn.style.background = '#22c55e';
    btn.style.opacity = '1';
    quoteForm.reset();

    // Show success banner
    const banner = document.createElement('div');
    banner.style.cssText = 'background:#dcfce7;color:#166534;padding:16px 24px;border-radius:8px;margin-top:16px;font-weight:600;display:flex;align-items:center;gap:10px;';
    banner.innerHTML = `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg> ${result.message} <strong style="margin-left:auto;">Ref: ${result.quoteId}</strong>`;
    quoteForm.parentElement.appendChild(banner);

    setTimeout(() => {
     btn.innerHTML = originalHTML;
     btn.style.background = '';
     btn.disabled = false;
    }, 5000);
   } else {
    throw new Error(result.error || 'Submission failed');
   }
  } catch (err) {
   btn.innerHTML = 'Error — Try Again';
   btn.style.background = '#ef4444';
   btn.style.opacity = '1';
   setTimeout(() => {
    btn.innerHTML = originalHTML;
    btn.style.background = '';
    btn.style.opacity = '1';
    btn.disabled = false;
   }, 3000);
  }
 });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
 anchor.addEventListener('click', function(e) {
  e.preventDefault();
  const target = document.querySelector(this.getAttribute('href'));
  if (target) target.scrollIntoView({ behavior: 'smooth', block: 'start' });
 });
});
