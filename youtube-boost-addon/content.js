// YouTube Boost - content script
// Runs on youtube.com pages. Three responsibilities:
//   1. Filter unwanted recommendation cards (keyword / channel blocklist)
//   2. Track watch time on video pages
//   3. Render a small, non-intrusive ad sidebar with impression/click tracking

(() => {
  "use strict";

  const RECOMMENDATION_SELECTORS = [
    "ytd-rich-item-renderer",      // home feed grid
    "ytd-compact-video-renderer",  // watch page "up next" sidebar
    "ytd-video-renderer"           // search results
  ].join(",");

  let settings = null;
  let ads = [];
  let adSessionKey = `session-${Math.random().toString(36).slice(2)}`;
  let adsShownThisSession = 0;

  async function loadState() {
    const data = await chrome.storage.local.get(["settings", "ads"]);
    settings = data.settings || { filterEnabled: true, blockedKeywords: [], blockedChannels: [], adsEnabled: true, adFrequencyPerSession: 2 };
    ads = data.ads || [];
  }

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area !== "local") return;
    if (changes.settings) settings = changes.settings.newValue;
    if (changes.ads) ads = changes.ads.newValue;
  });

  // ---------- 1. Recommendation filter ----------

  function textMatches(haystack, needles) {
    if (!haystack || !needles || !needles.length) return false;
    const lower = haystack.toLowerCase();
    return needles.some((n) => n && lower.includes(n.toLowerCase()));
  }

  function filterCard(card) {
    if (!settings || !settings.filterEnabled) {
      card.style.display = "";
      return;
    }
    const titleEl = card.querySelector("#video-title, #video-title-link, .title");
    const channelEl = card.querySelector("ytd-channel-name, #channel-name, .ytd-channel-name");
    const title = titleEl ? titleEl.textContent.trim() : "";
    const channel = channelEl ? channelEl.textContent.trim() : "";

    const blocked =
      textMatches(title, settings.blockedKeywords) ||
      textMatches(channel, settings.blockedChannels);

    card.style.display = blocked ? "none" : "";
    if (blocked) card.dataset.ybFiltered = "true";
  }

  function scanRecommendations(root = document) {
    root.querySelectorAll(RECOMMENDATION_SELECTORS).forEach(filterCard);
  }

  const feedObserver = new MutationObserver((mutations) => {
    for (const m of mutations) {
      if (m.addedNodes.length) {
        scanRecommendations(document);
        break;
      }
    }
  });

  function startFeedObserver() {
    feedObserver.observe(document.documentElement, { childList: true, subtree: true });
    scanRecommendations(document);
  }

  // ---------- 2. Watch-time tracker ----------

  let watchTimer = null;
  let accumulatedSeconds = 0;

  function flushWatchTime() {
    if (accumulatedSeconds <= 0) return;
    const seconds = accumulatedSeconds;
    accumulatedSeconds = 0;
    chrome.runtime.sendMessage({ type: "ADD_WATCH_TIME", seconds }).catch(() => {});
  }

  function attachVideoTracking() {
    const video = document.querySelector("video");
    if (!video || video.dataset.ybTracked) return;
    video.dataset.ybTracked = "true";

    if (watchTimer) clearInterval(watchTimer);
    watchTimer = setInterval(() => {
      if (!video.paused && !video.ended) {
        accumulatedSeconds += 1;
      }
      if (accumulatedSeconds >= 15) flushWatchTime();
    }, 1000);
  }

  window.addEventListener("beforeunload", flushWatchTime);
  document.addEventListener("visibilitychange", () => {
    if (document.visibilityState === "hidden") flushWatchTime();
  });
  setInterval(flushWatchTime, 30000);

  // ---------- 3. Ad sidebar ----------

  function pickAd() {
    const active = ads.filter((a) => a.active);
    if (!active.length) return null;
    return active[Math.floor(Math.random() * active.length)];
  }

  function buildAdCard(ad) {
    const card = document.createElement("div");
    card.className = "yb-ad-card";

    if (ad.imageUrl) {
      const img = document.createElement("img");
      img.src = ad.imageUrl;
      img.alt = ad.title || "Werbung";
      img.className = "yb-ad-image";
      card.appendChild(img);
    }

    const title = document.createElement("div");
    title.className = "yb-ad-title";
    title.textContent = ad.title || "Anzeige";
    card.appendChild(title);

    if (ad.text) {
      const text = document.createElement("div");
      text.className = "yb-ad-text";
      text.textContent = ad.text;
      card.appendChild(text);
    }

    card.addEventListener("click", () => {
      chrome.runtime.sendMessage({ type: "AD_CLICK", adId: ad.id }).catch(() => {});
      window.open(ad.targetUrl || "#", "_blank", "noopener,noreferrer");
    });

    return card;
  }

  function renderAdSidebar() {
    if (!settings || !settings.adsEnabled) return;
    if (document.getElementById("yb-ad-sidebar")) return;
    if (adsShownThisSession >= (settings.adFrequencyPerSession || 2)) return;

    const ad = pickAd();
    if (!ad) return;

    const container = document.createElement("div");
    container.id = "yb-ad-sidebar";
    container.className = "yb-ad-sidebar";

    const header = document.createElement("div");
    header.className = "yb-ad-header";
    header.innerHTML = `<span>Anzeige</span>`;

    const closeBtn = document.createElement("button");
    closeBtn.className = "yb-ad-close";
    closeBtn.setAttribute("aria-label", "Anzeige schließen");
    closeBtn.textContent = "×";
    closeBtn.addEventListener("click", () => container.remove());
    header.appendChild(closeBtn);

    container.appendChild(header);
    container.appendChild(buildAdCard(ad));
    document.body.appendChild(container);

    adsShownThisSession += 1;

    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          chrome.runtime.sendMessage({ type: "AD_IMPRESSION", adId: ad.id }).catch(() => {});
          io.disconnect();
        }
      });
    }, { threshold: 0.5 });
    io.observe(container);
  }

  // ---------- bootstrap ----------

  async function init() {
    await loadState();
    startFeedObserver();
    attachVideoTracking();
    renderAdSidebar();

    const pageObserver = new MutationObserver(() => {
      attachVideoTracking();
      renderAdSidebar();
    });
    pageObserver.observe(document.documentElement, { childList: true, subtree: true });
  }

  init();
})();
