// YouTube Boost - background service worker
// Initializes default storage on install and provides a small message API
// so the content script / popup / dashboard can share state through
// chrome.storage.local (works across extension pages and content scripts,
// unlike page-scoped window.localStorage).

const DEFAULT_SETTINGS = {
  filterEnabled: true,
  blockedKeywords: [],
  blockedChannels: [],
  adsEnabled: true,
  adFrequencyPerSession: 2
};

const DEFAULT_ADS = [
  {
    id: "sample-ad-1",
    title: "Beispiel-Anzeige",
    text: "Dein Werbetext erscheint hier.",
    imageUrl: "",
    targetUrl: "https://example.com",
    cpm: 5,
    active: true,
    impressions: 0,
    clicks: 0,
    createdAt: Date.now()
  }
];

async function initStorage() {
  const data = await chrome.storage.local.get([
    "settings",
    "ads",
    "playlists",
    "watchTime",
    "adSessionState"
  ]);

  const patch = {};
  if (!data.settings) patch.settings = DEFAULT_SETTINGS;
  if (!data.ads) patch.ads = DEFAULT_ADS;
  if (!data.playlists) patch.playlists = [];
  if (!data.watchTime) patch.watchTime = {}; // { "YYYY-MM-DD": seconds }
  if (!data.adSessionState) patch.adSessionState = {}; // { tabId: count }

  if (Object.keys(patch).length) {
    await chrome.storage.local.set(patch);
  }
}

chrome.runtime.onInstalled.addListener(() => {
  initStorage();
});

chrome.runtime.onStartup.addListener(() => {
  initStorage();
});

// Central message handler: keeps ad impression/click counting and
// watch-time accumulation atomic even if multiple tabs write at once.
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (!message || !message.type) return;

  switch (message.type) {
    case "AD_IMPRESSION": {
      recordAdEvent(message.adId, "impressions").then(() => sendResponse({ ok: true }));
      return true;
    }
    case "AD_CLICK": {
      recordAdEvent(message.adId, "clicks").then(() => sendResponse({ ok: true }));
      return true;
    }
    case "ADD_WATCH_TIME": {
      addWatchTime(message.seconds).then(() => sendResponse({ ok: true }));
      return true;
    }
    default:
      return;
  }
});

async function recordAdEvent(adId, field) {
  const { ads = [] } = await chrome.storage.local.get("ads");
  const next = ads.map((ad) =>
    ad.id === adId ? { ...ad, [field]: (ad[field] || 0) + 1 } : ad
  );
  await chrome.storage.local.set({ ads: next });
}

async function addWatchTime(seconds) {
  if (!seconds || seconds <= 0) return;
  const today = new Date().toISOString().slice(0, 10);
  const { watchTime = {} } = await chrome.storage.local.get("watchTime");
  watchTime[today] = (watchTime[today] || 0) + seconds;
  await chrome.storage.local.set({ watchTime });
}
