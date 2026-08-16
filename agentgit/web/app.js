/* AgentGit dashboard — frontend logic */
"use strict";

const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => Array.from(document.querySelectorAll(sel));

let snapshots = [];
let selected = null;

const esc = (s) =>
  String(s == null ? "" : s).replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );

function toast(msg, isError = false) {
  const t = $("#toast");
  t.textContent = msg;
  t.classList.toggle("error", isError);
  t.hidden = false;
  clearTimeout(t._timer);
  t._timer = setTimeout(() => { t.hidden = true; }, 2600);
}

async function api(path, opts = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...opts,
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || `Request failed (${res.status})`);
  return data;
}

/* ---------------- status & stats ---------------- */
async function loadStatus() {
  try {
    const st = await api("/api/status");
    $("#statSnapshots").textContent = snapshots.length;
    $("#statFiles").textContent = st.tracked_files ?? 0;
    const clean = st.clean;
    const dot = $("#statClean");
    dot.className = "stat-dot " + (clean ? "clean" : "dirty");
    $("#statCleanLabel").textContent = clean ? "Clean" : "Changes pending";
    $("#snapCount").textContent = `${snapshots.length} total`;
  } catch (e) {
    toast(e.message, true);
  }
}

/* ---------------- timeline ---------------- */
function renderTimeline() {
  const tl = $("#timeline");
  const empty = $("#timelineEmpty");
  if (!snapshots.length) {
    tl.innerHTML = '<div class="empty">No snapshots yet. Create one to begin tracking.</div>';
    return;
  }
  const list = [...snapshots].reverse();
  tl.innerHTML = list
    .map(
      (s) => `
      <div class="tl-item ${selected === s.id ? "active" : ""}" data-id="${esc(s.id)}">
        <div class="tl-top">
          <span class="tl-id">${esc(s.id)}</span>
          <span class="tl-time">${esc(s.created_at.replace("T", " ").slice(0, 19))}</span>
        </div>
        <div class="tl-msg">${esc(s.message || "(no message)")}</div>
        <div class="tl-meta">
          <span class="tag">${esc(s.agent || "unknown")}</span>
          <span class="tag files">${s.file_count} files</span>
        </div>
      </div>`
    )
    .join("");
  $$(".tl-item").forEach((el) =>
    el.addEventListener("click", () => {
      selected = el.dataset.id;
      renderTimeline();
      loadDiff(selected);
    })
  );
}

/* ---------------- diff ---------------- */
async function loadDiff(id) {
  const view = $("#diffView");
  view.innerHTML = '<div class="empty">Loading…</div>';
  try {
    const d = await api(`/api/diff?id=${encodeURIComponent(id)}`);
    $("#diffMeta").textContent = `${d.changed_count} changed`;
    if (d.changed_count === 0) {
      view.innerHTML = '<div class="empty">No changes since this snapshot.</div>';
      return;
    }
    const chips = `
      <div class="diff-summary">
        <span class="chip add">+ ${d.added.length} added</span>
        <span class="chip mod">~ ${d.modified.length} modified</span>
        <span class="chip del">− ${d.deleted.length} deleted</span>
      </div>`;
    let groups = "";
    const renderGroup = (files, state, label) => {
      files.forEach((f) => {
        groups += `
          <div class="file-group">
            <div class="file-head"><span>${esc(f)}</span><span class="fstate ${state}">${label}</span></div>
            <div class="file-body" data-snap="${esc(id)}" data-path="${esc(f)}" data-state="${state}">loading…</div>
          </div>`;
      });
    };
    d.added.forEach((f) => renderGroup([f], "add", "ADDED"));
    d.modified.forEach((f) => renderGroup([f], "mod", "MODIFIED"));
    d.deleted.forEach((f) => renderGroup([f], "del", "DELETED"));
    view.innerHTML = chips + groups;
    loadFileBodies(id, d);
  } catch (e) {
    view.innerHTML = `<div class="empty">${esc(e.message)}</div>`;
  }
}

async function loadFileBodies(snapId, d) {
  const bodies = $$(".file-body");
  await Promise.all(
    bodies.map(async (el) => {
      const path = el.dataset.path;
      const state = el.dataset.state;
      try {
        const snapFile = await api(`/api/file?id=${encodeURIComponent(snapId)}&path=${encodeURIComponent(path)}`);
        const current = await api(`/api/current?path=${encodeURIComponent(path)}`);
        const snapLines = (snapFile.content || "").split("\n");
        const curLines = (current.content || "").split("\n");
        let html = "";
        if (state === "add") {
          curLines.forEach((ln, i) => { html += `<span class="ln">${i + 1}</span>${esc(ln)}\n`; });
        } else if (state === "del") {
          snapLines.forEach((ln, i) => { html += `<span class="ln">${i + 1}</span>${esc(ln)}\n`; });
        } else {
          const max = Math.max(snapLines.length, curLines.length);
          for (let i = 0; i < max; i++) {
            const a = snapLines[i] || "";
            const b = curLines[i] || "";
            const mark = a !== b ? "▸ " : "  ";
            html += `<span class="ln">${i + 1}</span>${mark}${esc(b)}\n`;
          }
        }
        el.textContent = "";
        el.innerHTML = html;
      } catch {
        el.textContent = "(unable to load)";
      }
    })
  );
}

/* ---------------- agents ---------------- */
async function loadAgents() {
  try {
    const data = await api("/api/agents");
    const agents = Object.entries(data.agents || {});
    $("#statAgents").textContent = agents.length;
    const view = $("#agentsView");
    if (!agents.length) {
      view.innerHTML = '<div class="empty">No AI coding agents detected.</div>';
      return;
    }
    view.innerHTML = agents
      .map(
        ([name, info]) => `
        <div class="agent-card">
          <span class="agent-dot ${esc(info.status)}"></span>
          <div>
            <div class="agent-name">${esc(name)}</div>
            <div class="agent-state">${esc(info.status)}</div>
          </div>
        </div>`
      )
      .join("");
  } catch (e) {
    $("#agentsView").innerHTML = `<div class="empty">${esc(e.message)}</div>`;
  }
}

/* ---------------- actions ---------------- */
function openModal(backdrop) {
  backdrop.hidden = false;
}
function closeModal(backdrop) {
  backdrop.hidden = true;
}

async function createSnapshot(agent, message) {
  try {
    const m = await api("/api/snapshot", {
      method: "POST",
      body: JSON.stringify({ agent: agent || null, message: message || null }),
    });
    toast(`Snapshot ${m.id} created`);
    await refresh();
    selected = m.id;
    renderTimeline();
    loadDiff(m.id);
  } catch (e) {
    toast(e.message, true);
  }
}

async function revertSnapshot(id) {
  try {
    const r = await api("/api/revert", { method: "POST", body: JSON.stringify({ id }) });
    toast(`Reverted: ${r.restored.length} restored, ${r.removed.length} removed`);
    await refresh();
  } catch (e) {
    toast(e.message, true);
  }
}

async function refresh() {
  const [snaps] = await Promise.all([api("/api/snapshots"), loadStatus()]);
  snapshots = snaps.snapshots || [];
  renderTimeline();
  loadAgents();
}

/* ---------------- init ---------------- */
function init() {
  const backdrop = $("#modalBackdrop");
  const revertBackdrop = $("#revertBackdrop");

  $("#btnSnapshot").addEventListener("click", () => {
    $("#snapAgent").value = "";
    $("#snapMessage").value = "";
    openModal(backdrop);
  });
  $("#btnCancel").addEventListener("click", () => closeModal(backdrop));
  backdrop.addEventListener("click", (e) => { if (e.target === backdrop) closeModal(backdrop); });
  $("#btnConfirm").addEventListener("click", async () => {
    closeModal(backdrop);
    await createSnapshot($("#snapAgent").value.trim(), $("#snapMessage").value.trim());
  });

  $("#btnAgents").addEventListener("click", () => {
    $("#agentsView").scrollIntoView({ behavior: "smooth", block: "center" });
  });

  $("#btnRevertCancel").addEventListener("click", () => closeModal(revertBackdrop));
  revertBackdrop.addEventListener("click", (e) => { if (e.target === revertBackdrop) closeModal(revertBackdrop); });
  $("#btnRevertConfirm").addEventListener("click", async () => {
    closeModal(revertBackdrop);
    if (selected) await revertSnapshot(selected);
  });

  // long-press / context menu on a timeline item offers revert
  document.addEventListener("click", (e) => {
    const item = e.target.closest(".tl-item");
    if (!item) return;
    if (e.ctrlKey || e.metaKey) {
      e.preventDefault();
      selected = item.dataset.id;
      $("#revertBody").textContent = `Restore working tree to snapshot ${selected}? (Ctrl/Cmd-click to revert)`;
      openModal(revertBackdrop);
    }
  });

  // populate datalist with detected agents
  api("/api/agents").then((data) => {
    const dl = $("#agentList");
    dl.innerHTML = Object.keys(data.agents || {})
      .map((a) => `<option value="${esc(a)}"></option>`)
      .join("");
  }).catch(() => {});

  refresh();
  setInterval(refresh, 4000);
}

document.addEventListener("DOMContentLoaded", init);
