(() => {
  "use strict";

  /* Mobile menu */
  const menuBtn = document.querySelector(".menu-btn");
  const menu = document.getElementById("menu");
  if (menuBtn && menu) {
    const setOpen = (open) => {
      menuBtn.setAttribute("aria-expanded", String(open));
      menu.hidden = !open;
    };
    menuBtn.addEventListener("click", () => setOpen(menuBtn.getAttribute("aria-expanded") !== "true"));
    menu.addEventListener("click", (ev) => {
      if (ev.target.closest("a")) setOpen(false);
    });
    document.addEventListener("keydown", (ev) => {
      if (ev.key === "Escape" && !menu.hidden) {
        setOpen(false);
        menuBtn.focus();
      }
    });
    matchMedia("(min-width: 981px)").addEventListener("change", (ev) => {
      if (ev.matches) setOpen(false);
    });
  }

  /* Home hero: the four banners are exits on one overhead sign */
  const hero = document.querySelector("[data-hero]");
  if (hero) {
    const tabs = [...hero.querySelectorAll(".exit")];
    const slides = [...hero.querySelectorAll("[data-slide]")];
    const sign = hero.querySelector(".sign");
    const rig = hero.querySelector(".rig");
    const pauseBtn = hero.querySelector(".exits__pause");
    const INTERVAL = 7000;
    let current = 0;
    let timer = null;
    let paused = matchMedia("(prefers-reduced-motion: reduce)").matches;
    let held = false;

    const show = (index, moveFocus) => {
      current = (index + tabs.length) % tabs.length;
      tabs.forEach((tab, i) => {
        tab.setAttribute("aria-selected", String(i === current));
        tab.tabIndex = i === current ? 0 : -1;
      });
      slides.forEach((el) => el.classList.toggle("is-active", Number(el.dataset.slide) === current));
      sign.classList.remove("is-swept");
      void sign.offsetWidth; // restart the headlight sweep
      sign.classList.add("is-swept");
      if (moveFocus) tabs[current].focus();
    };

    const stop = () => {
      clearInterval(timer);
      timer = null;
    };
    const start = () => {
      stop();
      if (!paused && !held && !document.hidden) timer = setInterval(() => show(current + 1), INTERVAL);
    };
    const syncPause = () => {
      pauseBtn.setAttribute("aria-pressed", String(paused));
      pauseBtn.setAttribute("aria-label", paused ? "Resume rotation" : "Pause rotation");
    };

    tabs.forEach((tab, i) => {
      tab.addEventListener("click", () => {
        show(i);
        start();
      });
      tab.addEventListener("keydown", (ev) => {
        const step = { ArrowRight: 1, ArrowLeft: -1 }[ev.key];
        if (step) {
          ev.preventDefault();
          show(current + step, true);
        } else if (ev.key === "Home" || ev.key === "End") {
          ev.preventDefault();
          show(ev.key === "Home" ? 0 : tabs.length - 1, true);
        }
      });
    });

    pauseBtn.addEventListener("click", () => {
      paused = !paused;
      syncPause();
      start();
    });

    const hold = (value) => () => {
      held = value;
      start();
    };
    rig.addEventListener("pointerenter", hold(true));
    rig.addEventListener("pointerleave", hold(false));
    hero.addEventListener("focusin", hold(true));
    hero.addEventListener("focusout", hold(false));
    document.addEventListener("visibilitychange", start);

    syncPause();
    start();
  }

  /* Contact form: field errors, then sending -> sent or not sent.
     data-endpoint is empty until the API is agreed with the developer; while it is
     empty the form runs in preview mode and sends nothing. In preview, adding
     ?form=error to the page address shows the "not sent" state. */
  const form = document.querySelector("[data-contact-form]");
  if (form) {
    const alertBox = form.querySelector("[data-form-alert]");
    const submit = form.querySelector("[data-form-submit]");
    const done = document.querySelector("[data-form-done]");
    const endpoint = form.dataset.endpoint;
    const idleLabel = submit.textContent;
    let sending = false;

    const rules = {
      first_name: (v) => (v ? "" : "Enter your first name."),
      last_name: (v) => (v ? "" : "Enter your last name."),
      phone: (v) => {
        if (!v) return "Enter your phone number.";
        let d = v.replace(/\D/g, "");
        if (d.length === 11 && d[0] === "1") d = d.slice(1);
        return /^[2-9]\d{9}$/.test(d) ? "" : "Enter a 10-digit US phone number, like (636) 442-1334.";
      },
      email: (v) => {
        if (!v) return "Enter your email address.";
        return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v) ? "" : "Enter an email address like name@example.com.";
      },
      zip: (v) => (!v || /^\d{5}(-\d{4})?$/.test(v) ? "" : "Enter a 5-digit ZIP code, like 63043."),
    };

    const check = (name) => {
      const input = form.elements[name];
      const message = rules[name](input.value.trim());
      const field = input.closest(".field");
      const error = field.querySelector(".field__error");
      field.toggleAttribute("data-invalid", Boolean(message));
      input.setAttribute("aria-invalid", String(Boolean(message)));
      error.textContent = message;
      error.hidden = !message;
      return message ? { input, message } : null;
    };

    const el = (tag, text) => {
      const node = document.createElement(tag);
      if (text) node.textContent = text;
      return node;
    };

    const showProblems = (problems) => {
      const list = el("ul");
      problems.forEach(({ input, message }) => {
        const link = el("a", message);
        link.href = "#" + input.id;
        link.addEventListener("click", (ev) => {
          ev.preventDefault();
          input.focus();
        });
        const item = el("li");
        item.append(link);
        list.append(item);
      });
      const n = problems.length;
      alertBox.replaceChildren(el("strong", `Fix ${n} ${n === 1 ? "field" : "fields"} to send your message`), list);
      alertBox.hidden = false;
    };

    const showNotSent = () => {
      const call = el("a", form.dataset.phone);
      call.href = form.dataset.tel;
      const text = el("p", "Check your connection and try again, or call ");
      text.append(call, ".");
      alertBox.replaceChildren(el("strong", "Message not sent"), text);
      alertBox.hidden = false;
      alertBox.focus();
    };

    const setSending = (on) => {
      sending = on;
      submit.disabled = on;
      submit.textContent = on ? "Sending…" : idleLabel;
      form.setAttribute("aria-busy", String(on));
    };

    const send = async (data) => {
      if (!endpoint) {
        await new Promise((resolve) => setTimeout(resolve, 900));
        if (new URLSearchParams(location.search).get("form") === "error") throw new Error("preview");
        return;
      }
      const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(Object.fromEntries(data)),
      });
      if (!response.ok) throw new Error(String(response.status));
    };

    Object.keys(rules).forEach((name) => {
      form.elements[name].addEventListener("input", () => {
        if (form.elements[name].closest(".field").hasAttribute("data-invalid")) check(name);
      });
    });

    form.addEventListener("submit", async (ev) => {
      ev.preventDefault();
      if (sending) return;
      const problems = Object.keys(rules).map(check).filter(Boolean);
      if (problems.length) {
        showProblems(problems);
        problems[0].input.focus();
        return;
      }
      alertBox.hidden = true;
      setSending(true);
      try {
        await send(new FormData(form));
        form.hidden = true;
        done.querySelector("[data-form-preview]").hidden = Boolean(endpoint);
        done.hidden = false;
        done.focus();
      } catch (err) {
        showNotSent();
      } finally {
        setSending(false);
      }
    });

    done.querySelector("[data-form-again]").addEventListener("click", () => {
      form.reset();
      Object.keys(rules).forEach((name) => {
        const field = form.elements[name].closest(".field");
        field.removeAttribute("data-invalid");
        field.querySelector(".field__error").hidden = true;
        form.elements[name].removeAttribute("aria-invalid");
      });
      alertBox.hidden = true;
      done.hidden = true;
      form.hidden = false;
      form.elements.first_name.focus();
    });
  }

  /* Reviews page filter */
  const reviews = document.querySelector("[data-reviews]");
  if (reviews) {
    const chips = [...reviews.querySelectorAll("[data-filter]")];
    const items = [...reviews.querySelectorAll(".quote")];
    const count = reviews.querySelector("[data-count]");
    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const filter = chip.dataset.filter;
        let shown = 0;
        chips.forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
        items.forEach((item) => {
          const on = filter === "all" || item.dataset.cat === filter;
          item.hidden = !on;
          if (on) shown += 1;
        });
        count.textContent = shown;
      });
    });
  }
})();
