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
 quoteForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const formData = new FormData(quoteForm);
  const data = Object.fromEntries(formData);
  
  // Build mailto link as fallback
  const subject = encodeURIComponent(`Quote Request: ${data.product || 'E-Z UP Products'}`);
  const body = encodeURIComponent(
   `Name: ${data.name}\nEmail: ${data.email}\nPhone: ${data.phone || 'N/A'}\nProduct Interest: ${data.product || 'N/A'}\n\nMessage:\n${data.message || 'N/A'}`
  );
  
  // Show success message
  const btn = quoteForm.querySelector('button[type="submit"]');
  const originalText = btn.textContent;
  btn.textContent = ' Request Sent!';
  btn.style.background = '#22c55e';
  
  setTimeout(() => {
   window.location.href = `mailto:info@giantpro.com?subject=${subject}&body=${body}`;
   btn.textContent = originalText;
   btn.style.background = '';
   quoteForm.reset();
  }, 1000);
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
