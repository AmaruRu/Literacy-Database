/**
 * Read Mississippi - Main JavaScript
 * Handles navigation, smooth scrolling, and basic interactivity
 */

// Smooth scrolling for internal links
document.addEventListener('DOMContentLoaded', function() {
  // Add smooth scrolling to all links
  const links = document.querySelectorAll('a[href^="#"]');
  
  links.forEach(link => {
    link.addEventListener('click', function(e) {
      e.preventDefault();
      
      const targetId = this.getAttribute('href').substring(1);
      const targetElement = document.getElementById(targetId);
      
      if (targetElement) {
        targetElement.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
  
  // Add fade-in animation to sections on scroll
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
  };
  
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
      }
    });
  }, observerOptions);
  
  // Observe all major sections
  const sections = document.querySelectorAll('section');
  sections.forEach(section => {
    observer.observe(section);
  });
  
  // Add active class to current page navigation
  highlightCurrentPage();
});

// Function to scroll to a section (used by onclick handlers)
function scrollToSection(sectionId) {
  const element = document.getElementById(sectionId);
  if (element) {
    element.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  }
}

// Highlight current page in navigation
function highlightCurrentPage() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('nav a');
  
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    const button = link.querySelector('button');
    
    if (button) {
      if (href === currentPage || 
          (currentPage === '' && href === 'index.html') ||
          (currentPage === '/' && href === 'index.html')) {
        button.classList.add('active');
      } else {
        button.classList.remove('active');
      }
    }
  });
}

// Add scroll-to-top button functionality
function scrollToTop() {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  });
}

// Show/hide scroll-to-top button based on scroll position
window.addEventListener('scroll', function() {
  const scrollBtn = document.getElementById('scroll-to-top');
  if (scrollBtn) {
    if (window.pageYOffset > 300) {
      scrollBtn.style.display = 'block';
    } else {
      scrollBtn.style.display = 'none';
    }
  }
});

// Add loading animation
window.addEventListener('load', function() {
  document.body.classList.add('loaded');
});

// Handle form submissions (if any forms are added later)
function handleFormSubmit(event) {
  event.preventDefault();
  // Add form handling logic here
  console.log('Form submitted');
}

// Mobile menu toggle (if hamburger menu is added)
function toggleMobileMenu() {
  const nav = document.querySelector('nav ul');
  if (nav) {
    nav.classList.toggle('mobile-active');
  }
}

// Console message
console.log('📚 Read Mississippi - Every Page Matters');
console.log('Built with ❤️ by Team Read');
