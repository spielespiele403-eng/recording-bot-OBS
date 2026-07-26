// YouTube Boost - popup logic

document.addEventListener("DOMContentLoaded", async () => {
  setupTabs();
  await renderStats();
  await renderPlaylists();
  await renderFilterSettings();
  setupPlaylistForm();
  setupFilterForm();
  setupDashboardButton();
});

function setupTabs() {
  const tabs = document.querySelectorAll(".yb-tab");
  const panels = document.querySelectorAll(".yb-panel");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      panels.forEach((p) => p.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(`tab-${tab.dataset.tab}`).classList.add("active");
    });
  });
}

// ---------- Watch-time stats ----------

function formatMinutes(seconds) {
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return `${minutes}m`;
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  return `${hours}h ${rest}m`;
}

function isoDate(d) {
  return d.toISOString().slice(0, 10);
}

async function renderStats() {
  const { watchTime = {} } = await chrome.storage.local.get("watchTime");
  const today = isoDate(new Date());

  let weekSeconds = 0;
  let totalSeconds = 0;
  const now = new Date();

  for (const [dateStr, seconds] of Object.entries(watchTime)) {
    totalSeconds += seconds;
    const d = new Date(dateStr);
    const diffDays = (now - d) / (1000 * 60 * 60 * 24);
    if (diffDays <= 7) weekSeconds += seconds;
  }

  document.getElementById("stat-today").textContent = formatMinutes(watchTime[today] || 0);
  document.getElementById("stat-week").textContent = formatMinutes(weekSeconds);
  document.getElementById("stat-total").textContent = formatMinutes(totalSeconds);

  const list = document.getElementById("stat-daily-list");
  list.innerHTML = "";
  const sortedDates = Object.keys(watchTime).sort().reverse().slice(0, 10);
  for (const dateStr of sortedDates) {
    const li = document.createElement("li");
    li.innerHTML = `<span>${dateStr}</span><span>${formatMinutes(watchTime[dateStr])}</span>`;
    list.appendChild(li);
  }
}

// ---------- Playlists ----------

async function getActiveYouTubeVideo() {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (!tab || !tab.url || !tab.url.includes("youtube.com/watch")) return null;
  try {
    const url = new URL(tab.url);
    const videoId = url.searchParams.get("v");
    if (!videoId) return null;
    const title = (tab.title || videoId).replace(/ - YouTube$/, "");
    return { videoId, title, url: tab.url };
  } catch {
    return null;
  }
}

async function renderPlaylists() {
  const { playlists = [] } = await chrome.storage.local.get("playlists");
  const list = document.getElementById("playlist-list");
  list.innerHTML = "";

  const current = await getActiveYouTubeVideo();

  playlists.forEach((playlist) => {
    const li = document.createElement("li");

    const header = document.createElement("div");
    header.className = "yb-list-header";

    const name = document.createElement("span");
    name.textContent = `${playlist.name} (${playlist.videos.length})`;
    header.appendChild(name);

    const actions = document.createElement("span");

    if (current) {
      const addBtn = document.createElement("button");
      addBtn.className = "yb-mini-btn";
      addBtn.textContent = "＋ Video";
      addBtn.title = "Aktuelles Video hinzufügen";
      addBtn.addEventListener("click", () => addVideoToPlaylist(playlist.id, current));
      actions.appendChild(addBtn);
    }

    const delBtn = document.createElement("button");
    delBtn.className = "yb-mini-btn";
    delBtn.textContent = "🗑";
    delBtn.title = "Playlist löschen";
    delBtn.addEventListener("click", () => deletePlaylist(playlist.id));
    actions.appendChild(delBtn);

    header.appendChild(actions);
    li.appendChild(header);

    if (playlist.videos.length) {
      const videoList = document.createElement("ul");
      videoList.className = "yb-list-videos";
      playlist.videos.forEach((video) => {
        const vLi = document.createElement("li");
        const link = document.createElement("a");
        link.href = video.url;
        link.target = "_blank";
        link.textContent = video.title;
        link.style.color = "inherit";
        link.style.textDecoration = "none";
        link.style.overflow = "hidden";
        link.style.textOverflow = "ellipsis";
        link.style.whiteSpace = "nowrap";
        link.style.maxWidth = "220px";
        vLi.appendChild(link);

        const removeBtn = document.createElement("button");
        removeBtn.className = "yb-mini-btn";
        removeBtn.textContent = "×";
        removeBtn.addEventListener("click", () => removeVideoFromPlaylist(playlist.id, video.videoId));
        vLi.appendChild(removeBtn);

        videoList.appendChild(vLi);
      });
      li.appendChild(videoList);
    }

    list.appendChild(li);
  });
}

function setupPlaylistForm() {
  document.getElementById("playlist-add").addEventListener("click", async () => {
    const input = document.getElementById("playlist-name");
    const name = input.value.trim();
    if (!name) return;
    const { playlists = [] } = await chrome.storage.local.get("playlists");
    playlists.push({ id: `pl-${Date.now()}`, name, videos: [] });
    await chrome.storage.local.set({ playlists });
    input.value = "";
    renderPlaylists();
  });
}

async function addVideoToPlaylist(playlistId, video) {
  const { playlists = [] } = await chrome.storage.local.get("playlists");
  const updated = playlists.map((p) => {
    if (p.id !== playlistId) return p;
    if (p.videos.some((v) => v.videoId === video.videoId)) return p;
    return { ...p, videos: [...p.videos, video] };
  });
  await chrome.storage.local.set({ playlists: updated });
  renderPlaylists();
}

async function removeVideoFromPlaylist(playlistId, videoId) {
  const { playlists = [] } = await chrome.storage.local.get("playlists");
  const updated = playlists.map((p) =>
    p.id === playlistId ? { ...p, videos: p.videos.filter((v) => v.videoId !== videoId) } : p
  );
  await chrome.storage.local.set({ playlists: updated });
  renderPlaylists();
}

async function deletePlaylist(playlistId) {
  const { playlists = [] } = await chrome.storage.local.get("playlists");
  await chrome.storage.local.set({ playlists: playlists.filter((p) => p.id !== playlistId) });
  renderPlaylists();
}

// ---------- Filter settings ----------

async function renderFilterSettings() {
  const { settings } = await chrome.storage.local.get("settings");
  if (!settings) return;
  document.getElementById("filter-enabled").checked = !!settings.filterEnabled;
  document.getElementById("filter-keywords").value = (settings.blockedKeywords || []).join(", ");
  document.getElementById("filter-channels").value = (settings.blockedChannels || []).join(", ");
  document.getElementById("ads-enabled").checked = !!settings.adsEnabled;
}

function setupFilterForm() {
  document.getElementById("filter-save").addEventListener("click", async () => {
    const { settings = {} } = await chrome.storage.local.get("settings");
    const updated = {
      ...settings,
      filterEnabled: document.getElementById("filter-enabled").checked,
      adsEnabled: document.getElementById("ads-enabled").checked,
      blockedKeywords: document.getElementById("filter-keywords").value
        .split(",").map((s) => s.trim()).filter(Boolean),
      blockedChannels: document.getElementById("filter-channels").value
        .split(",").map((s) => s.trim()).filter(Boolean)
    };
    await chrome.storage.local.set({ settings: updated });

    const saved = document.getElementById("filter-saved");
    saved.classList.remove("yb-hidden");
    setTimeout(() => saved.classList.add("yb-hidden"), 1500);
  });
}

// ---------- Dashboard ----------

function setupDashboardButton() {
  document.getElementById("open-dashboard").addEventListener("click", () => {
    chrome.runtime.openOptionsPage();
  });
}
