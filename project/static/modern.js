/**
 * Read Mississippi V3 - Modern Interactions
 * Smooth navigation, animations, and mobile menu
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileMenu();
    initSmoothNav();
    initCounters();
    initNewsletterForm();
    initScrollAnimations();
  });
  
  // Mobile Menu Toggle
  function initMobileMenu() {
    const toggle = document.getElementById('mobile-menu-toggle');
    const nav = document.getElementById('side-nav');
    
    if (!toggle || !nav) return;
    
    toggle.addEventListener('click', function() {
      this.classList.toggle('active');
      nav.classList.toggle('active');
      document.body.style.overflow = nav.classList.contains('active') ? 'hidden' : '';
    });
    
    // Close menu when clicking a link
    const navLinks = nav.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
      link.addEventListener('click', function() {
        if (window.innerWidth <= 1024) {
          toggle.classList.remove('active');
          nav.classList.remove('active');
          document.body.style.overflow = '';
        }
      });
    });
  }
  
  // Smooth Navigation with Active States
  function initSmoothNav() {
    const navLinks = document.querySelectorAll('.nav-link[data-section]');
    
    // Smooth scroll
    navLinks.forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const target = document.querySelector(targetId);
        
        if (target) {
          const offset = 80;
          const targetPosition = target.offsetTop - offset;
          
          window.scrollTo({
            top: targetPosition,
            behavior: 'smooth'
          });
        }
      });
    });
    
    // Update active state on scroll
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', () => {
      let current = '';
      
      sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.clientHeight;
        
        if (window.pageYOffset >= sectionTop && window.pageYOffset < sectionTop + sectionHeight) {
          current = section.getAttribute('id');
        }
      });
      
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('data-section') === current) {
          link.classList.add('active');
        }
      });
    });
  }
  
  // Animated Counters
  function initCounters() {
    const counters = document.querySelectorAll('.stat-value[data-count]');
    
    const observerOptions = {
      threshold: 0.5,
      rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
          animateCounter(entry.target);
          entry.target.classList.add('counted');
        }
      });
    }, observerOptions);
    
    counters.forEach(counter => observer.observe(counter));
  }
  
  function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-count'));
    const duration = 2000;
    const increment = target / (duration / 16);
    let current = 0;
    
    const timer = setInterval(() => {
      current += increment;
      
      if (current >= target) {
        element.textContent = formatNumber(target);
        clearInterval(timer);
      } else {
        element.textContent = formatNumber(Math.floor(current));
      }
    }, 16);
  }
  
  function formatNumber(num) {
    if (num >= 1000) {
      return Math.floor(num / 1000) + 'K';
    }
    return num;
  }
  
  // Newsletter Form
  function initNewsletterForm() {
    const form = document.getElementById('newsletter-form');
    
    if (!form) return;
    
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const email = this.querySelector('input[type="email"]').value;
      
      if (validateEmail(email)) {
        showNotification('Thank you for subscribing! 🎉', 'success');
        this.reset();
      } else {
        showNotification('Please enter a valid email address', 'error');
      }
    });
  }
  
  function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  }
  
  function showNotification(message, type = 'success') {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
      <div class="notification-content">
        <span class="notification-icon">${type === 'success' ? '✓' : '✗'}</span>
        <span class="notification-message">${message}</span>
      </div>
    `;
    
    // Styles
    const styles = `
      position: fixed;
      top: 24px;
      right: 24px;
      padding: 16px 24px;
      background: ${type === 'success' ? 'linear-gradient(135deg, #28a745 0%, #20894a 100%)' : '#dc3545'};
      color: white;
      border-radius: 12px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.2);
      z-index: 10000;
      animation: slideInRight 0.3s ease;
      font-family: 'Inter', sans-serif;
    `;
    
    notification.style.cssText = styles;
    document.body.appendChild(notification);
    
    setTimeout(() => {
      notification.style.animation = 'slideOutRight 0.3s ease';
      setTimeout(() => notification.remove(), 300);
    }, 4000);
  }
  
  // Add notification styles
  const notificationStyles = document.createElement('style');
  notificationStyles.textContent = `
    @keyframes slideInRight {
      from {
        transform: translateX(400px);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
    
    @keyframes slideOutRight {
      from {
        transform: translateX(0);
        opacity: 1;
      }
      to {
        transform: translateX(400px);
        opacity: 0;
      }
    }
    
    .notification-content {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    
    .notification-icon {
      font-size: 1.2rem;
      font-weight: bold;
    }
    
    .notification-message {
      font-size: 0.95rem;
      font-weight: 500;
    }
  `;
  document.head.appendChild(notificationStyles);
  
  // Scroll Animations
  function initScrollAnimations() {
    const animatedElements = document.querySelectorAll('[data-animate]');
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    });
    
    animatedElements.forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      observer.observe(el);
    });
  }
  
  // Smooth scroll helper
  function smoothScroll(target) {
    const element = document.querySelector(target);
    if (element) {
      const offset = 80;
      const targetPosition = element.offsetTop - offset;
      
      window.scrollTo({
        top: targetPosition,
        behavior: 'smooth'
      });
    }
  }
  
  // Make smoothScroll globally available
  window.smoothScroll = smoothScroll;
  
  // Parallax effect on hero
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero-section');
    
    if (hero && scrolled < window.innerHeight) {
      const circles = hero.querySelectorAll('.circle');
      circles.forEach((circle, index) => {
        const speed = 0.1 * (index + 1);
        circle.style.transform = `translateY(${scrolled * speed}px)`;
      });
    }
  });
  
  // Console message
  console.log('✨ Read Mississippi V3 - Modern Design Loaded');
  console.log('📚 Every Page Matters');