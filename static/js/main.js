console.log("Portfolio JS loaded");

// Fade in the main heading
window.addEventListener('DOMContentLoaded', () => {
    const h1 = document.querySelector('h1');
    if (h1) {
        h1.style.opacity = 0;
        h1.style.transition = 'opacity 1.2s cubic-bezier(.4,0,.2,1)';
        setTimeout(() => {
            h1.style.opacity = 1;
        }, 200);
    }

    // Font color controls for test-fonts page
    const colorControls = document.querySelector('.color-controls');
    if (colorControls) {
        const sample = document.querySelector('.font-sample');
        colorControls.addEventListener('input', (e) => {
            if (!sample) return;
            if (e.target.matches('[data-css-var]')) {
                const cssVar = e.target.getAttribute('data-css-var');
                sample.style.setProperty(cssVar, e.target.value);
            }
        });
    }

    // For all font samples, allow color controls to work
    const allColorControls = document.querySelectorAll('.color-controls');
    allColorControls.forEach(ctrl => {
        const sample = ctrl.nextElementSibling;
        if (!sample) return;
        ctrl.addEventListener('input', (e) => {
            if (e.target.matches('[data-css-var]')) {
                const cssVar = e.target.getAttribute('data-css-var');
                sample.style.setProperty(cssVar, e.target.value);
            }
        });
    });
});