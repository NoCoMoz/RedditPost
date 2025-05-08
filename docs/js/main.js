document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation Toggle
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                if (navLinks.classList.contains('active')) {
                    navLinks.classList.remove('active');
                    hamburger.classList.remove('active');
                }
            }
        });
    });
    
    // Template Tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button
            this.classList.add('active');
            
            // Show corresponding tab pane
            const tabId = this.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Add mobile nav styles dynamically
    if (navLinks) {
        const style = document.createElement('style');
        style.textContent = `
            @media (max-width: 768px) {
                .nav-links.active {
                    display: flex;
                    flex-direction: column;
                    position: absolute;
                    top: 80px;
                    left: 0;
                    right: 0;
                    background-color: #3a5a80;
                    padding: 20px;
                    z-index: 100;
                    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
                }
                
                .nav-links.active li {
                    margin: 10px 0;
                }
                
                .hamburger.active span:nth-child(1) {
                    transform: rotate(45deg) translate(5px, 5px);
                }
                
                .hamburger.active span:nth-child(2) {
                    opacity: 0;
                }
                
                .hamburger.active span:nth-child(3) {
                    transform: rotate(-45deg) translate(7px, -6px);
                }
                
                .hamburger span {
                    transition: all 0.3s ease;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Highlight code blocks
    document.querySelectorAll('pre code').forEach(block => {
        highlightSyntax(block);
    });
    
    // Simple syntax highlighting function
    function highlightSyntax(codeBlock) {
        let html = codeBlock.innerHTML;
        
        // Comments
        html = html.replace(/(#.*$)/gm, '<span style="color: #6a9955;">$1</span>');
        
        // Strings
        html = html.replace(/(".*?")/g, '<span style="color: #ce9178;">$1</span>');
        html = html.replace(/('.*?')/g, '<span style="color: #ce9178;">$1</span>');
        
        // Keywords
        const keywords = ['import', 'from', 'def', 'for', 'in', 'if', 'else', 'return', 'class', 'try', 'except', 'with', 'as', 'and', 'or', 'not', 'None', 'True', 'False'];
        keywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'g');
            html = html.replace(regex, `<span style="color: #569cd6;">${keyword}</span>`);
        });
        
        // Function calls
        html = html.replace(/(\w+)(\()/g, '<span style="color: #dcdcaa;">$1</span>$2');
        
        codeBlock.innerHTML = html;
    }
    
    // Add animation on scroll
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.feature-card, .step, .docs-card');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 100) {
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }
        });
    };
    
    // Set initial styles for animation
    document.querySelectorAll('.feature-card, .step, .docs-card').forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    
    // Run animation on load and scroll
    window.addEventListener('load', animateOnScroll);
    window.addEventListener('scroll', animateOnScroll);
});
