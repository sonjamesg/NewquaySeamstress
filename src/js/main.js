// Entry point, bundled and minified by build.py (esbuild) into /assets/js/site.<hash>.js
import { initNav, initCallBar } from './nav.js';
import { initReveal } from './reveal.js';
import { initForm } from './form.js';
import { initSeam } from './seam.js';

// Switch on the non-critical stylesheet (loaded with media="print" so it never blocks rendering).
var lazyCss = document.getElementById('lazy-css'); if (lazyCss) lazyCss.media = 'all';

initNav();
initCallBar();
initReveal();
initForm();
initSeam();
