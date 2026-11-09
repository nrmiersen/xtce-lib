function expandApiAnchor(hash = location.hash) {
    if (!hash) return;
    let target;
    try {
        target = document.getElementById(decodeURIComponent(hash.slice(1)));
    } catch {
        return;
    }
    if (!target) return;
    let current = target;
    while (current) {
        if (current.matches("details.api-class-disclosure")) current.open = true;
        current = current.parentElement;
    }
}

function prepareApiToc() {
    if (!document.querySelector(".doc.doc-object")) return;
    document.querySelectorAll(".md-nav--secondary .md-nav__item").forEach((item, index) => {
        const link = item.querySelector(":scope > a.md-nav__link");
        const children = item.querySelector(":scope > nav.md-nav");
        if (!link || !children || item.querySelector(":scope > .api-toc-toggle")) return;

        const button = document.createElement("button");
        const label = link.textContent.trim();
        button.type = "button";
        button.className = "api-toc-toggle";
        button.setAttribute("aria-label", `Toggle ${label} subsections`);
        button.setAttribute("aria-expanded", "false");
        button.title = `Toggle ${label} subsections`;
        children.id = `api-toc-children-${index}`;
        children.classList.add("api-toc-children");
        children.hidden = true;
        button.setAttribute("aria-controls", children.id);
        button.addEventListener("click", () => {
            children.hidden = !children.hidden;
            button.setAttribute("aria-expanded", String(!children.hidden));
        });
        item.classList.add("api-toc-item");
        item.insertBefore(button, children);
    });
}

function prepareApiClasses() {
    document.querySelectorAll(".doc.doc-object.doc-class").forEach((object) => {
        const heading = object.querySelector(":scope > .doc-heading[id]");
        if (!heading || !heading.id.startsWith("xtce_lib.xtce.")) return;

        const disclosure = document.createElement("details");
        disclosure.className = "api-class-disclosure";
        const summary = document.createElement("summary");
        const contents = object.querySelector(":scope > .doc-contents");
        const description = contents?.querySelector(":scope > p:not(.doc-class-bases)");

        object.insertBefore(disclosure, heading);
        disclosure.appendChild(summary);
        summary.appendChild(heading);
        if (description && !description.querySelector(".doc-section-title")) {
            description.classList.add("api-class-description");
            summary.appendChild(description);
        }
        while (disclosure.nextSibling) disclosure.appendChild(disclosure.nextSibling);
    });
    prepareApiToc();
    expandApiAnchor();
}

document.addEventListener("click", (event) => {
    const link = event.target.closest("a[href]");
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (url.origin === location.origin && url.pathname === location.pathname) {
        expandApiAnchor(url.hash);
    }
});
window.addEventListener("hashchange", () => expandApiAnchor());
if (typeof document$ !== "undefined") {
    document$.subscribe(prepareApiClasses);
} else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", prepareApiClasses);
} else {
    prepareApiClasses();
}