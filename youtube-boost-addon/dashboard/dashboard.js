// YouTube Boost - admin dashboard logic

document.addEventListener("DOMContentLoaded", async () => {
  await renderAds();
  setupDialog();
  setupExport();

  chrome.storage.onChanged.addListener((changes, area) => {
    if (area === "local" && changes.ads) renderAds();
  });
});

function euro(value) {
  return value.toLocaleString("de-DE", { minimumFractionDigits: 2, maximumFractionDigits: 2 }) + " €";
}

function revenueFor(ad) {
  return ((ad.impressions || 0) / 1000) * (ad.cpm || 0);
}

function ctrFor(ad) {
  if (!ad.impressions) return 0;
  return ((ad.clicks || 0) / ad.impressions) * 100;
}

async function getAds() {
  const { ads = [] } = await chrome.storage.local.get("ads");
  return ads;
}

async function setAds(ads) {
  await chrome.storage.local.set({ ads });
}

async function renderAds() {
  const ads = await getAds();
  const body = document.getElementById("ads-table-body");
  const empty = document.getElementById("ads-empty");
  body.innerHTML = "";

  if (!ads.length) {
    empty.classList.remove("yb-hidden");
  } else {
    empty.classList.add("yb-hidden");
  }

  let totalImpressions = 0;
  let totalClicks = 0;
  let totalRevenue = 0;

  ads.forEach((ad) => {
    totalImpressions += ad.impressions || 0;
    totalClicks += ad.clicks || 0;
    totalRevenue += revenueFor(ad);

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td><span class="${ad.active ? "status-active" : "status-inactive"}">${ad.active ? "Aktiv" : "Pausiert"}</span></td>
      <td>${escapeHtml(ad.title)}</td>
      <td>${escapeHtml(ad.targetUrl)}</td>
      <td>${(ad.cpm || 0).toFixed(2)}</td>
      <td>${ad.impressions || 0}</td>
      <td>${ad.clicks || 0}</td>
      <td>${ctrFor(ad).toFixed(2)}%</td>
      <td>${euro(revenueFor(ad))}</td>
      <td></td>
    `;

    const actionsCell = tr.lastElementChild;

    const toggleBtn = document.createElement("button");
    toggleBtn.className = "db-mini-btn";
    toggleBtn.textContent = ad.active ? "Pausieren" : "Aktivieren";
    toggleBtn.addEventListener("click", () => toggleAd(ad.id));
    actionsCell.appendChild(toggleBtn);

    const editBtn = document.createElement("button");
    editBtn.className = "db-mini-btn";
    editBtn.textContent = "Bearbeiten";
    editBtn.addEventListener("click", () => openDialog(ad));
    actionsCell.appendChild(editBtn);

    const delBtn = document.createElement("button");
    delBtn.className = "db-mini-btn";
    delBtn.textContent = "Löschen";
    delBtn.addEventListener("click", () => deleteAd(ad.id));
    actionsCell.appendChild(delBtn);

    body.appendChild(tr);
  });

  document.getElementById("sum-impressions").textContent = totalImpressions.toLocaleString("de-DE");
  document.getElementById("sum-clicks").textContent = totalClicks.toLocaleString("de-DE");
  document.getElementById("sum-ctr").textContent =
    (totalImpressions ? ((totalClicks / totalImpressions) * 100).toFixed(2) : "0.00") + "%";
  document.getElementById("sum-revenue").textContent = euro(totalRevenue);
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str || "";
  return div.innerHTML;
}

async function toggleAd(id) {
  const ads = await getAds();
  const updated = ads.map((ad) => (ad.id === id ? { ...ad, active: !ad.active } : ad));
  await setAds(updated);
}

async function deleteAd(id) {
  if (!confirm("Diese Anzeige wirklich löschen?")) return;
  const ads = await getAds();
  await setAds(ads.filter((ad) => ad.id !== id));
}

// ---------- Dialog (add / edit) ----------

function setupDialog() {
  const dialog = document.getElementById("ad-dialog");
  const form = document.getElementById("ad-form");

  document.getElementById("add-ad").addEventListener("click", () => openDialog(null));
  document.getElementById("ad-cancel").addEventListener("click", () => dialog.close());

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    await saveAdFromForm();
    dialog.close();
  });
}

function openDialog(ad) {
  const dialog = document.getElementById("ad-dialog");
  document.getElementById("ad-dialog-title").textContent = ad ? "Anzeige bearbeiten" : "Neue Anzeige";
  document.getElementById("ad-id").value = ad ? ad.id : "";
  document.getElementById("ad-title").value = ad ? ad.title : "";
  document.getElementById("ad-text").value = ad ? ad.text || "" : "";
  document.getElementById("ad-image").value = ad ? ad.imageUrl || "" : "";
  document.getElementById("ad-url").value = ad ? ad.targetUrl : "";
  document.getElementById("ad-cpm").value = ad ? ad.cpm : 5;
  document.getElementById("ad-active").checked = ad ? !!ad.active : true;
  dialog.showModal();
}

async function saveAdFromForm() {
  const id = document.getElementById("ad-id").value;
  const ads = await getAds();

  const fields = {
    title: document.getElementById("ad-title").value.trim(),
    text: document.getElementById("ad-text").value.trim(),
    imageUrl: document.getElementById("ad-image").value.trim(),
    targetUrl: document.getElementById("ad-url").value.trim(),
    cpm: parseFloat(document.getElementById("ad-cpm").value) || 0,
    active: document.getElementById("ad-active").checked
  };

  if (id) {
    await setAds(ads.map((ad) => (ad.id === id ? { ...ad, ...fields } : ad)));
  } else {
    ads.push({
      id: `ad-${Date.now()}`,
      impressions: 0,
      clicks: 0,
      createdAt: Date.now(),
      ...fields
    });
    await setAds(ads);
  }
}

// ---------- CSV export ----------

function setupExport() {
  document.getElementById("export-csv").addEventListener("click", async () => {
    const ads = await getAds();
    const header = ["Titel", "Ziel-URL", "Aktiv", "CPM (€)", "Impressionen", "Klicks", "CTR (%)", "Einnahmen (€)"];
    const rows = ads.map((ad) => [
      ad.title,
      ad.targetUrl,
      ad.active ? "Ja" : "Nein",
      (ad.cpm || 0).toFixed(2),
      ad.impressions || 0,
      ad.clicks || 0,
      ctrFor(ad).toFixed(2),
      revenueFor(ad).toFixed(2)
    ]);

    const csv = [header, ...rows]
      .map((row) => row.map(csvEscape).join(";"))
      .join("\r\n");

    const blob = new Blob(["﻿" + csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `youtube-boost-ads-${new Date().toISOString().slice(0, 10)}.csv`;
    document.body.appendChild(a);
    a.click();
    a.remove();
    URL.revokeObjectURL(url);
  });
}

function csvEscape(value) {
  const str = String(value ?? "");
  if (/[;"\n]/.test(str)) {
    return `"${str.replace(/"/g, '""')}"`;
  }
  return str;
}
