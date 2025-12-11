// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="title.html">BARGE Rulebook</a></span></li><li class="chapter-item expanded "><li class="spacer"></li></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="preface.html">Preface</a></span></li><li class="chapter-item expanded "><li class="spacer"></li></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="common-rules-and-variations.html"><strong aria-hidden="true">1.</strong> Common Rules and Variations</a></span><ol class="section"><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="limit.html"><strong aria-hidden="true">1.1.</strong> Limit</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="no-limit.html"><strong aria-hidden="true">1.2.</strong> No Limit</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="pot-limit.html"><strong aria-hidden="true">1.3.</strong> Pot Limit</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="ties-odd-chips.html"><strong aria-hidden="true">1.4.</strong> Ties &amp; Odd Chips</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="big-blind-ante.html"><strong aria-hidden="true">1.5.</strong> Big Blind Ante</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="bomb-pot.html"><strong aria-hidden="true">1.6.</strong> Bomb Pot</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="bounty.html"><strong aria-hidden="true">1.7.</strong> Bounty</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="jam-or-fold.html"><strong aria-hidden="true">1.8.</strong> Jam-or-Fold</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="lammers.html"><strong aria-hidden="true">1.9.</strong> Lammers</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="shootout.html"><strong aria-hidden="true">1.10.</strong> Shootout</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="short-deck.html"><strong aria-hidden="true">1.11.</strong> Short Deck</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="win-the-button.html"><strong aria-hidden="true">1.12.</strong> Win the Button</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="dice-procedures.html"><strong aria-hidden="true">1.13.</strong> Dice Procedures</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="stud-procedures.html"><strong aria-hidden="true">1.14.</strong> Stud Procedures</a></span></li></ol><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="variants.html"><strong aria-hidden="true">2.</strong> Poker Variants</a></span><ol class="section"><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="ace-to-5-triple-draw.html"><strong aria-hidden="true">2.1.</strong> Ace-to-5 Triple Draw</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="action-razz.html"><strong aria-hidden="true">2.2.</strong> Action Razz</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="action-razzdugi.html"><strong aria-hidden="true">2.3.</strong> Action Razzdugi</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="archie.html"><strong aria-hidden="true">2.4.</strong> Archie</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="badacey.html"><strong aria-hidden="true">2.5.</strong> Badacey</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="badeucy.html"><strong aria-hidden="true">2.6.</strong> Badeucy</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="badugi.html"><strong aria-hidden="true">2.7.</strong> Badugi</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="bidirectional-chowaha.html"><strong aria-hidden="true">2.8.</strong> Bidirectional Chowaha High/Low</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="big-o.html"><strong aria-hidden="true">2.9.</strong> Big O</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="binglaha.html"><strong aria-hidden="true">2.10.</strong> Binglaha</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="california-lowball.html"><strong aria-hidden="true">2.11.</strong> California Lowball</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="chowaha.html"><strong aria-hidden="true">2.12.</strong> Chowaha</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="courchevel.html"><strong aria-hidden="true">2.13.</strong> Courchevel (High Only)</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="crazy-pineapple-high-low.html"><strong aria-hidden="true">2.14.</strong> Crazy Pineapple High/Low</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="deuce-to-seven-lowball.html"><strong aria-hidden="true">2.15.</strong> Deuce-to-Seven Lowball</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="deuce-to-seven-razz.html"><strong aria-hidden="true">2.16.</strong> Deuce-to-Seven Razz</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="deuce-to-seven-triple-draw.html"><strong aria-hidden="true">2.17.</strong> Deuce-to-Seven Triple Draw</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="dramadugi.html"><strong aria-hidden="true">2.18.</strong> Dramadugi</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="dramaha.html"><strong aria-hidden="true">2.19.</strong> Dramaha</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="dramaha-49.html"><strong aria-hidden="true">2.20.</strong> Dramaha 49</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="duck-flush.html"><strong aria-hidden="true">2.21.</strong> Duck Flush</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="five-card-draw.html"><strong aria-hidden="true">2.22.</strong> Five Card Draw</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="five-card-omaha.html"><strong aria-hidden="true">2.23.</strong> Five Card Omaha</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="five-card-stud.html"><strong aria-hidden="true">2.24.</strong> Five Card Stud</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="four-card-chowaha.html"><strong aria-hidden="true">2.25.</strong> Four Card Chowaha High/Low</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="irish.html"><strong aria-hidden="true">2.26.</strong> Irish</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="korean.html"><strong aria-hidden="true">2.27.</strong> Korean</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="lazy-pineapple-high-only.html"><strong aria-hidden="true">2.28.</strong> Lazy Pineapple (High Only)</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="lazy-pineapple-high-low-eight-or-better.html"><strong aria-hidden="true">2.29.</strong> Lazy Pineapple High/Low</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="london-lowball.html"><strong aria-hidden="true">2.30.</strong> London Lowball</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="mexican-poker.html"><strong aria-hidden="true">2.31.</strong> Mexican Poker</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="mississippi-stud-and-variants.html"><strong aria-hidden="true">2.32.</strong> Mississippi Stud and Variants</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="murder.html"><strong aria-hidden="true">2.33.</strong> Murder</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="oklahoma.html"><strong aria-hidden="true">2.34.</strong> Oklahoma</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="omaha-high-only.html"><strong aria-hidden="true">2.35.</strong> Omaha (High Only)</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="omaha-high-low-eight-or-better.html"><strong aria-hidden="true">2.36.</strong> Omaha High/Low</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="omaha-x-or-better.html"><strong aria-hidden="true">2.37.</strong> Omaha X or Better</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="paradise-road-pickem.html"><strong aria-hidden="true">2.38.</strong> Paradise Road Pick&#39;em</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="quick-quads.html"><strong aria-hidden="true">2.39.</strong> Quick Quads</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="razz.html"><strong aria-hidden="true">2.40.</strong> Razz</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="razzdugi.html"><strong aria-hidden="true">2.41.</strong> Razzdugi</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="rio-bravo.html"><strong aria-hidden="true">2.42.</strong> Rio Bravo</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="scrotum.html"><strong aria-hidden="true">2.43.</strong> Scrotum</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="short-deck-omaha.html"><strong aria-hidden="true">2.44.</strong> Short Deck Omaha</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="short-deck-texas-holdem.html"><strong aria-hidden="true">2.45.</strong> Short Deck Texas Hold&#39;em</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="sohe-simultaneous-omaha-holdem.html"><strong aria-hidden="true">2.46.</strong> Sohe (Simultaneous Omaha/Hold’em)</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="stud.html"><strong aria-hidden="true">2.47.</strong> Stud</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="stud-high-low-eight-or-better.html"><strong aria-hidden="true">2.48.</strong> Stud High/Low</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="stud-high-low-no-qualifier.html"><strong aria-hidden="true">2.49.</strong> Stud High/Low No Qualifier</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="super-stud.html"><strong aria-hidden="true">2.50.</strong> Super Stud</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="texas-holdem.html"><strong aria-hidden="true">2.51.</strong> Texas Hold&#39;em</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="texas-holdem-high-low-eight-or-better.html"><strong aria-hidden="true">2.52.</strong> Texas Hold&#39;em High/Low</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="triple-draw-dramaha.html"><strong aria-hidden="true">2.53.</strong> Triple Draw Dramaha</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="two-or-five-omaha-8-or-better.html"><strong aria-hidden="true">2.54.</strong> Two-or-Five Omaha Eight-or-Better</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="wonky-donkey.html"><strong aria-hidden="true">2.55.</strong> Wonky Donkey</a></span></li></ol><li class="chapter-item expanded "><li class="spacer"></li></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="lowball-scales.html">Appendix A: Lowball Scales</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="lowball-hand-numbers.html">Appendix A.1: Lowball Hand Numbers</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="sevens-rule.html">Appendix B: The Sevens Rule</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="what-beats-what.html">Appendix C: What Beats What</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="killer-cards.html">Appendix D: Killer Cards Revisited (Abridged)</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="killer-cards-holdem.html">Appendix D.1: Killer Cards table for Hold&#39;em</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="killer-cards-omaha.html">Appendix D.2: Killer Cards table for Omaha</a></span></li><li class="chapter-item expanded "><span class="chapter-link-wrapper"><a href="colophon.html">Colophon</a></span></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split('#')[0].split('?')[0];
        if (current_page.endsWith('/')) {
            current_page += 'index.html';
        }
        const links = Array.prototype.slice.call(this.querySelectorAll('a'));
        const l = links.length;
        for (let i = 0; i < l; ++i) {
            const link = links[i];
            const href = link.getAttribute('href');
            if (href && !href.startsWith('#') && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The 'index' page is supposed to alias the first chapter in the book.
            if (link.href === current_page
                || i === 0
                && path_to_root === ''
                && current_page.endsWith('/index.html')) {
                link.classList.add('active');
                let parent = link.parentElement;
                while (parent) {
                    if (parent.tagName === 'LI' && parent.classList.contains('chapter-item')) {
                        parent.classList.add('expanded');
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', e => {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        const sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via
            // 'next/previous chapter' buttons
            const activeSection = document.querySelector('#mdbook-sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        const sidebarAnchorToggles = document.querySelectorAll('.chapter-fold-toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(el => {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define('mdbook-sidebar-scrollbox', MDBookSidebarScrollbox);


// ---------------------------------------------------------------------------
// Support for dynamically adding headers to the sidebar.

(function() {
    // This is used to detect which direction the page has scrolled since the
    // last scroll event.
    let lastKnownScrollPosition = 0;
    // This is the threshold in px from the top of the screen where it will
    // consider a header the "current" header when scrolling down.
    const defaultDownThreshold = 150;
    // Same as defaultDownThreshold, except when scrolling up.
    const defaultUpThreshold = 300;
    // The threshold is a virtual horizontal line on the screen where it
    // considers the "current" header to be above the line. The threshold is
    // modified dynamically to handle headers that are near the bottom of the
    // screen, and to slightly offset the behavior when scrolling up vs down.
    let threshold = defaultDownThreshold;
    // This is used to disable updates while scrolling. This is needed when
    // clicking the header in the sidebar, which triggers a scroll event. It
    // is somewhat finicky to detect when the scroll has finished, so this
    // uses a relatively dumb system of disabling scroll updates for a short
    // time after the click.
    let disableScroll = false;
    // Array of header elements on the page.
    let headers;
    // Array of li elements that are initially collapsed headers in the sidebar.
    // I'm not sure why eslint seems to have a false positive here.
    // eslint-disable-next-line prefer-const
    let headerToggles = [];
    // This is a debugging tool for the threshold which you can enable in the console.
    let thresholdDebug = false;

    // Updates the threshold based on the scroll position.
    function updateThreshold() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const windowHeight = window.innerHeight;
        const documentHeight = document.documentElement.scrollHeight;

        // The number of pixels below the viewport, at most documentHeight.
        // This is used to push the threshold down to the bottom of the page
        // as the user scrolls towards the bottom.
        const pixelsBelow = Math.max(0, documentHeight - (scrollTop + windowHeight));
        // The number of pixels above the viewport, at least defaultDownThreshold.
        // Similar to pixelsBelow, this is used to push the threshold back towards
        // the top when reaching the top of the page.
        const pixelsAbove = Math.max(0, defaultDownThreshold - scrollTop);
        // How much the threshold should be offset once it gets close to the
        // bottom of the page.
        const bottomAdd = Math.max(0, windowHeight - pixelsBelow - defaultDownThreshold);
        let adjustedBottomAdd = bottomAdd;

        // Adjusts bottomAdd for a small document. The calculation above
        // assumes the document is at least twice the windowheight in size. If
        // it is less than that, then bottomAdd needs to be shrunk
        // proportional to the difference in size.
        if (documentHeight < windowHeight * 2) {
            const maxPixelsBelow = documentHeight - windowHeight;
            const t = 1 - pixelsBelow / Math.max(1, maxPixelsBelow);
            const clamp = Math.max(0, Math.min(1, t));
            adjustedBottomAdd *= clamp;
        }

        let scrollingDown = true;
        if (scrollTop < lastKnownScrollPosition) {
            scrollingDown = false;
        }

        if (scrollingDown) {
            // When scrolling down, move the threshold up towards the default
            // downwards threshold position. If near the bottom of the page,
            // adjustedBottomAdd will offset the threshold towards the bottom
            // of the page.
            const amountScrolledDown = scrollTop - lastKnownScrollPosition;
            const adjustedDefault = defaultDownThreshold + adjustedBottomAdd;
            threshold = Math.max(adjustedDefault, threshold - amountScrolledDown);
        } else {
            // When scrolling up, move the threshold down towards the default
            // upwards threshold position. If near the bottom of the page,
            // quickly transition the threshold back up where it normally
            // belongs.
            const amountScrolledUp = lastKnownScrollPosition - scrollTop;
            const adjustedDefault = defaultUpThreshold - pixelsAbove
                + Math.max(0, adjustedBottomAdd - defaultDownThreshold);
            threshold = Math.min(adjustedDefault, threshold + amountScrolledUp);
        }

        if (documentHeight <= windowHeight) {
            threshold = 0;
        }

        if (thresholdDebug) {
            const id = 'mdbook-threshold-debug-data';
            let data = document.getElementById(id);
            if (data === null) {
                data = document.createElement('div');
                data.id = id;
                data.style.cssText = `
                    position: fixed;
                    top: 50px;
                    right: 10px;
                    background-color: 0xeeeeee;
                    z-index: 9999;
                    pointer-events: none;
                `;
                document.body.appendChild(data);
            }
            data.innerHTML = `
                <table>
                  <tr><td>documentHeight</td><td>${documentHeight.toFixed(1)}</td></tr>
                  <tr><td>windowHeight</td><td>${windowHeight.toFixed(1)}</td></tr>
                  <tr><td>scrollTop</td><td>${scrollTop.toFixed(1)}</td></tr>
                  <tr><td>pixelsAbove</td><td>${pixelsAbove.toFixed(1)}</td></tr>
                  <tr><td>pixelsBelow</td><td>${pixelsBelow.toFixed(1)}</td></tr>
                  <tr><td>bottomAdd</td><td>${bottomAdd.toFixed(1)}</td></tr>
                  <tr><td>adjustedBottomAdd</td><td>${adjustedBottomAdd.toFixed(1)}</td></tr>
                  <tr><td>scrollingDown</td><td>${scrollingDown}</td></tr>
                  <tr><td>threshold</td><td>${threshold.toFixed(1)}</td></tr>
                </table>
            `;
            drawDebugLine();
        }

        lastKnownScrollPosition = scrollTop;
    }

    function drawDebugLine() {
        if (!document.body) {
            return;
        }
        const id = 'mdbook-threshold-debug-line';
        const existingLine = document.getElementById(id);
        if (existingLine) {
            existingLine.remove();
        }
        const line = document.createElement('div');
        line.id = id;
        line.style.cssText = `
            position: fixed;
            top: ${threshold}px;
            left: 0;
            width: 100vw;
            height: 2px;
            background-color: red;
            z-index: 9999;
            pointer-events: none;
        `;
        document.body.appendChild(line);
    }

    function mdbookEnableThresholdDebug() {
        thresholdDebug = true;
        updateThreshold();
        drawDebugLine();
    }

    window.mdbookEnableThresholdDebug = mdbookEnableThresholdDebug;

    // Updates which headers in the sidebar should be expanded. If the current
    // header is inside a collapsed group, then it, and all its parents should
    // be expanded.
    function updateHeaderExpanded(currentA) {
        // Add expanded to all header-item li ancestors.
        let current = currentA.parentElement;
        while (current) {
            if (current.tagName === 'LI' && current.classList.contains('header-item')) {
                current.classList.add('expanded');
            }
            current = current.parentElement;
        }
    }

    // Updates which header is marked as the "current" header in the sidebar.
    // This is done with a virtual Y threshold, where headers at or below
    // that line will be considered the current one.
    function updateCurrentHeader() {
        if (!headers || !headers.length) {
            return;
        }

        // Reset the classes, which will be rebuilt below.
        const els = document.getElementsByClassName('current-header');
        for (const el of els) {
            el.classList.remove('current-header');
        }
        for (const toggle of headerToggles) {
            toggle.classList.remove('expanded');
        }

        // Find the last header that is above the threshold.
        let lastHeader = null;
        for (const header of headers) {
            const rect = header.getBoundingClientRect();
            if (rect.top <= threshold) {
                lastHeader = header;
            } else {
                break;
            }
        }
        if (lastHeader === null) {
            lastHeader = headers[0];
            const rect = lastHeader.getBoundingClientRect();
            const windowHeight = window.innerHeight;
            if (rect.top >= windowHeight) {
                return;
            }
        }

        // Get the anchor in the summary.
        const href = '#' + lastHeader.id;
        const a = [...document.querySelectorAll('.header-in-summary')]
            .find(element => element.getAttribute('href') === href);
        if (!a) {
            return;
        }

        a.classList.add('current-header');

        updateHeaderExpanded(a);
    }

    // Updates which header is "current" based on the threshold line.
    function reloadCurrentHeader() {
        if (disableScroll) {
            return;
        }
        updateThreshold();
        updateCurrentHeader();
    }


    // When clicking on a header in the sidebar, this adjusts the threshold so
    // that it is located next to the header. This is so that header becomes
    // "current".
    function headerThresholdClick(event) {
        // See disableScroll description why this is done.
        disableScroll = true;
        setTimeout(() => {
            disableScroll = false;
        }, 100);
        // requestAnimationFrame is used to delay the update of the "current"
        // header until after the scroll is done, and the header is in the new
        // position.
        requestAnimationFrame(() => {
            requestAnimationFrame(() => {
                // Closest is needed because if it has child elements like <code>.
                const a = event.target.closest('a');
                const href = a.getAttribute('href');
                const targetId = href.substring(1);
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    threshold = targetElement.getBoundingClientRect().bottom;
                    updateCurrentHeader();
                }
            });
        });
    }

    // Takes the nodes from the given head and copies them over to the
    // destination, along with some filtering.
    function filterHeader(source, dest) {
        const clone = source.cloneNode(true);
        clone.querySelectorAll('mark').forEach(mark => {
            mark.replaceWith(...mark.childNodes);
        });
        dest.append(...clone.childNodes);
    }

    // Scans page for headers and adds them to the sidebar.
    document.addEventListener('DOMContentLoaded', function() {
        const activeSection = document.querySelector('#mdbook-sidebar .active');
        if (activeSection === null) {
            return;
        }

        const main = document.getElementsByTagName('main')[0];
        headers = Array.from(main.querySelectorAll('h2, h3, h4, h5, h6'))
            .filter(h => h.id !== '' && h.children.length && h.children[0].tagName === 'A');

        if (headers.length === 0) {
            return;
        }

        // Build a tree of headers in the sidebar.

        const stack = [];

        const firstLevel = parseInt(headers[0].tagName.charAt(1));
        for (let i = 1; i < firstLevel; i++) {
            const ol = document.createElement('ol');
            ol.classList.add('section');
            if (stack.length > 0) {
                stack[stack.length - 1].ol.appendChild(ol);
            }
            stack.push({level: i + 1, ol: ol});
        }

        // The level where it will start folding deeply nested headers.
        const foldLevel = 3;

        for (let i = 0; i < headers.length; i++) {
            const header = headers[i];
            const level = parseInt(header.tagName.charAt(1));

            const currentLevel = stack[stack.length - 1].level;
            if (level > currentLevel) {
                // Begin nesting to this level.
                for (let nextLevel = currentLevel + 1; nextLevel <= level; nextLevel++) {
                    const ol = document.createElement('ol');
                    ol.classList.add('section');
                    const last = stack[stack.length - 1];
                    const lastChild = last.ol.lastChild;
                    // Handle the case where jumping more than one nesting
                    // level, which doesn't have a list item to place this new
                    // list inside of.
                    if (lastChild) {
                        lastChild.appendChild(ol);
                    } else {
                        last.ol.appendChild(ol);
                    }
                    stack.push({level: nextLevel, ol: ol});
                }
            } else if (level < currentLevel) {
                while (stack.length > 1 && stack[stack.length - 1].level > level) {
                    stack.pop();
                }
            }

            const li = document.createElement('li');
            li.classList.add('header-item');
            li.classList.add('expanded');
            if (level < foldLevel) {
                li.classList.add('expanded');
            }
            const span = document.createElement('span');
            span.classList.add('chapter-link-wrapper');
            const a = document.createElement('a');
            span.appendChild(a);
            a.href = '#' + header.id;
            a.classList.add('header-in-summary');
            filterHeader(header.children[0], a);
            a.addEventListener('click', headerThresholdClick);
            const nextHeader = headers[i + 1];
            if (nextHeader !== undefined) {
                const nextLevel = parseInt(nextHeader.tagName.charAt(1));
                if (nextLevel > level && level >= foldLevel) {
                    const toggle = document.createElement('a');
                    toggle.classList.add('chapter-fold-toggle');
                    toggle.classList.add('header-toggle');
                    toggle.addEventListener('click', () => {
                        li.classList.toggle('expanded');
                    });
                    const toggleDiv = document.createElement('div');
                    toggleDiv.textContent = '❱';
                    toggle.appendChild(toggleDiv);
                    span.appendChild(toggle);
                    headerToggles.push(li);
                }
            }
            li.appendChild(span);

            const currentParent = stack[stack.length - 1];
            currentParent.ol.appendChild(li);
        }

        const onThisPage = document.createElement('div');
        onThisPage.classList.add('on-this-page');
        onThisPage.append(stack[0].ol);
        const activeItemSpan = activeSection.parentElement;
        activeItemSpan.after(onThisPage);
    });

    document.addEventListener('DOMContentLoaded', reloadCurrentHeader);
    document.addEventListener('scroll', reloadCurrentHeader, { passive: true });
})();

