function setStatus(message, type = "info") {
  const status = document.getElementById("status");
  if (!message) {
    status.hidden = true;
    status.textContent = "";
    status.dataset.type = "";
    return;
  }

  status.hidden = false;
  status.textContent = message;
  status.dataset.type = type;
}

async function fetchText(path) {
  const res = await fetch(path, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`Fetch failed: ${res.status} ${res.statusText}`);
  }
  return await res.text();
}

async function getMarked() {
  // Prefer global UMD build if present
  if (globalThis.marked && typeof globalThis.marked.parse === "function") {
    return globalThis.marked;
  }

  throw new Error(
    "Markdown 解析器 marked 未加载（请检查 index.html 是否成功加载 ./vendor/marked.min.js）。"
  );
}

function parseMarkdown(markedLib, markdown) {
  const options = {
    gfm: true,
    breaks: true,
    headerIds: true,
    mangle: false,
  };

  if (markedLib && typeof markedLib.parse === "function") {
    return markedLib.parse(markdown, options);
  }
  if (typeof markedLib === "function") {
    return markedLib(markdown, options);
  }

  throw new Error("marked 已加载但未暴露 parse()。");
}

function applyVibeAnimations(contentEl) {
  const children = contentEl.children;
  for (let i = 0; i < children.length; i++) {
    // 强制重绘以重新触发动画
    children[i].style.animation = 'none';
    children[i].style.opacity = '0';
    setTimeout(() => {
      // 交错动画延迟 (比如每个元素间隔 0.15s，最多封顶 3s)
      const delay = Math.min(i * 0.15, 3);
      children[i].style.animation = `fadeInLine 0.5s ease forwards ${delay}s`;
    }, 10);
  }
}

function removeVibeAnimations(contentEl) {
  const children = contentEl.children;
  for (let i = 0; i < children.length; i++) {
    children[i].style.animation = 'none';
    children[i].style.opacity = '1';
  }
}

async function renderMarkdown(markdown) {
  const markedLib = await getMarked();
  const html = parseMarkdown(markedLib, markdown);

  const purifier = globalThis.DOMPurify;
  if (!purifier || typeof purifier.sanitize !== "function") {
    throw new Error("HTML 清洗器 DOMPurify 未加载。");
  }

  const clean = purifier.sanitize(html, {
    USE_PROFILES: { html: true },
  });

  const content = document.getElementById("content");
  content.innerHTML = clean;
  
  if (document.body.classList.contains('vibe-theme')) {
    applyVibeAnimations(content);
  }
}

async function loadReport(reportPath) {
  setStatus(`正在加载：${reportPath}`);

  try {
    const markdown = await fetchText(reportPath);
    await renderMarkdown(markdown);
    setStatus(`已加载：${reportPath}`);
  } catch (err) {
    console.error(err);
    setStatus(`加载失败：${reportPath}。${err?.message || err}`, "error");

    const content = document.getElementById("content");
    content.innerHTML = "";
  }
}

function setupThemeToggle() {
  const toggleBtn = document.getElementById('theme-toggle');
  if (toggleBtn) {
    toggleBtn.addEventListener('click', () => {
      document.body.classList.toggle('vibe-theme');
      const isVibe = document.body.classList.contains('vibe-theme');
      toggleBtn.textContent = isVibe ? '🔥 Normal Mode' : '✨ Vibe Mode';
      
      const content = document.getElementById('content');
      if (isVibe) {
        applyVibeAnimations(content);
      } else {
        removeVibeAnimations(content);
      }
    });
  }
}

function wireUi() {
  setupThemeToggle();
  loadReport("report.md");
}

wireUi();
