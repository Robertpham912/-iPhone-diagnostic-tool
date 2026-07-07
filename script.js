(function () {
  "use strict";

  const state = {
    category: null,
    problemId: null,
    tree: null,
    current: null,
    path: [],
    autoTestResults: null,
  };

  const screens = document.querySelectorAll(".screen");
  function showScreen(id) {
    screens.forEach((s) => s.dataset.active = (s.id === id) ? "true" : "false");
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  document.querySelectorAll("[data-back]").forEach((btn) => {
    btn.addEventListener("click", () => {
      stopAllMedia();
      showScreen(btn.dataset.back);
    });
  });

  // ---------- HOME ----------
  document.querySelectorAll(".category-card").forEach((card) => {
    card.addEventListener("click", () => {
      state.category = card.dataset.category;
      loadProblems(state.category);
    });
  });

  function loadProblems(category) {
    fetch("/api/problems")
      .then((r) => r.json())
      .then((data) => {
        const list = data[category] || [];
        const grid = document.getElementById("problem-grid");
        grid.innerHTML = "";
        document.getElementById("problems-title").textContent =
          category === "hardware" ? "Phần cứng" : "Phần mềm";
        list.forEach((p) => {
          const btn = document.createElement("button");
          btn.className = "problem-card";
          btn.innerHTML = `<span>${p.name}</span><span class="problem-card__arrow">→</span>`;
          btn.addEventListener("click", () => selectProblem(p.id));
          grid.appendChild(btn);
        });
        showScreen("screen-problems");
      });
  }

  function selectProblem(problemId) {
    state.problemId = problemId;
    state.path = [];
    fetch(`/api/tree/${problemId}`)
      .then((r) => r.json())
      .then((data) => {
        state.tree = data;
        state.current = data.tree;
        if (data.auto_test) {
          renderAutoTest(data.auto_test, data.name);
          showScreen("screen-test");
        } else {
          renderTreeNode();
          showScreen("screen-tree");
        }
      });
  }

  document.getElementById("btn-continue-tree").addEventListener("click", () => {
    stopAllMedia();
    renderTreeNode();
    showScreen("screen-tree");
  });

  // ---------- DECISION TREE ----------
  function renderTrail() {
    const trail = document.getElementById("trail");
    trail.innerHTML = "";
    state.path.forEach((step) => {
      const chip = document.createElement("span");
      chip.className = "trail__chip";
      chip.textContent = step;
      trail.appendChild(chip);
    });
  }

  function renderTreeNode() {
    renderTrail();
    const node = state.current;
    if (node.diagnosis) {
      renderReport(node.diagnosis);
      showScreen("screen-report");
      return;
    }
    document.getElementById("question-text").textContent = node.question;
    const list = document.getElementById("option-list");
    list.innerHTML = "";
    node.options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.className = "option-btn";
      btn.textContent = opt.label;
      btn.addEventListener("click", () => {
        state.path.push(opt.label);
        state.current = opt.next;
        renderTreeNode();
      });
      list.appendChild(btn);
    });
  }

  function renderReport(diagnosis) {
    const badge = document.getElementById("report-severity");
    badge.textContent =
      diagnosis.severity === "ok" ? "BÌNH THƯỜNG" :
      diagnosis.severity === "warning" ? "CẦN CHÚ Ý" : "NGHIÊM TRỌNG";
    badge.className = "report-card__badge report-card__badge--" + diagnosis.severity;
    document.getElementById("report-title").textContent = diagnosis.title;
    document.getElementById("report-explanation").textContent = diagnosis.explanation;
    const steps = document.getElementById("report-steps");
    steps.innerHTML = "";
    diagnosis.steps.forEach((s) => {
      const li = document.createElement("li");
      li.textContent = s;
      steps.appendChild(li);
    });
    document.getElementById("report-service").hidden = !diagnosis.service;

    fetch("/api/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        problem_id: state.problemId,
        path: state.path,
        diagnosis: diagnosis,
      }),
    }).catch(() => {});
  }

  // ---------- AUTO TESTS ----------
  let mediaStream = null;
  let audioCtx = null;

  function stopAllMedia() {
    if (mediaStream) {
      mediaStream.getTracks().forEach((t) => t.stop());
      mediaStream = null;
    }
    if (audioCtx) {
      audioCtx.close().catch(() => {});
      audioCtx = null;
    }
  }

  function testRow(label, valueHtml) {
    return `<div class="test-row"><span>${label}</span><span class="test-row__value">${valueHtml}</span></div>`;
  }

  function renderAutoTest(type, problemName) {
    document.getElementById("test-title").textContent = problemName;
    const panel = document.getElementById("test-panel");
    panel.innerHTML = "";

    if (type === "battery") return testBattery(panel);
    if (type === "touch") return testTouch(panel);
    if (type === "audio") return testAudio(panel);
    if (type === "camera") return testCamera(panel);
    if (type === "storage") return testStorage(panel);
    if (type === "network") return testNetwork(panel);

    panel.innerHTML = `<p class="test-note">Không có kiểm tra tự động cho mục này, bấm "Tiếp tục" để trả lời câu hỏi.</p>`;
  }

  function testBattery(panel) {
    panel.innerHTML = `<div id="battery-rows"><p class="test-note">Đang đọc dữ liệu pin…</p></div>`;
    if (!navigator.getBattery) {
      document.getElementById("battery-rows").innerHTML =
        `<p class="test-note">Trình duyệt này không cho phép web đọc trực tiếp thông tin pin (Safari trên iOS chặn API này vì lý do riêng tư). Hãy kiểm tra thủ công tại Cài đặt > Pin > Tình trạng pin & sạc, rồi tiếp tục trả lời câu hỏi bên dưới.</p>`;
      return;
    }
    navigator.getBattery().then((battery) => {
      const rows = document.getElementById("battery-rows");
      function render() {
        rows.innerHTML =
          testRow("Mức pin", Math.round(battery.level * 100) + "%") +
          testRow("Đang sạc", battery.charging ? "Có" : "Không") +
          `<p class="test-note">Dữ liệu đọc trực tiếp từ trình duyệt. Trả lời thêm vài câu hỏi để chẩn đoán chính xác hơn.</p>`;
      }
      render();
      battery.addEventListener("levelchange", render);
      battery.addEventListener("chargingchange", render);
    });
  }

  function testTouch(panel) {
    panel.innerHTML = `
      <p class="test-note">Chạm và di chuyển ngón tay trong khung dưới đây để kiểm tra độ nhạy cảm ứng.</p>
      <div class="touch-pad" id="touch-pad">Chạm vào đây</div>
      <div id="touch-count" class="test-note">Số điểm chạm ghi nhận: 0</div>
    `;
    const pad = document.getElementById("touch-pad");
    let count = 0;
    function handle(e) {
      const rect = pad.getBoundingClientRect();
      const points = e.touches ? Array.from(e.touches) : [e];
      pad.querySelectorAll(".touch-dot").forEach((d) => d.remove());
      points.forEach((p) => {
        const dot = document.createElement("div");
        dot.className = "touch-dot";
        dot.style.left = (p.clientX - rect.left) + "px";
        dot.style.top = (p.clientY - rect.top) + "px";
        pad.appendChild(dot);
      });
      count++;
      document.getElementById("touch-count").textContent = "Số điểm chạm ghi nhận: " + count;
    }
    pad.addEventListener("pointerdown", handle);
    pad.addEventListener("pointermove", (e) => { if (e.buttons) handle(e); });
  }

  function testAudio(panel) {
    panel.innerHTML = `
      <div class="test-row"><span>Test loa</span>
        <button class="btn btn--ghost btn--small" id="btn-tone">▶ Phát âm 440Hz</button>
      </div>
      <div class="test-row"><span>Test mic (mức âm thanh)</span></div>
      <div class="meter"><div class="meter__fill" id="mic-meter"></div></div>
      <p class="test-note" id="audio-note">Bấm nút để phát âm thanh kiểm tra loa. Nói/vỗ tay để kiểm tra thanh mức mic bên trên có phản ứng không (cần cho phép quyền micro).</p>
    `;
    document.getElementById("btn-tone").addEventListener("click", () => {
      if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = audioCtx.createOscillator();
      const gain = audioCtx.createGain();
      osc.frequency.value = 440;
      gain.gain.value = 0.2;
      osc.connect(gain).connect(audioCtx.destination);
      osc.start();
      osc.stop(audioCtx.currentTime + 1);
    });

    navigator.mediaDevices?.getUserMedia({ audio: true }).then((stream) => {
      mediaStream = stream;
      audioCtx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
      const source = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 256;
      source.connect(analyser);
      const data = new Uint8Array(analyser.frequencyBinCount);
      const meter = document.getElementById("mic-meter");
      function loop() {
        if (!mediaStream) return;
        analyser.getByteFrequencyData(data);
        const avg = data.reduce((a, b) => a + b, 0) / data.length;
        meter.style.width = Math.min(100, (avg / 128) * 100) + "%";
        requestAnimationFrame(loop);
      }
      loop();
    }).catch(() => {
      document.getElementById("audio-note").textContent =
        "Không thể truy cập micro (có thể do bạn chưa cấp quyền). Vẫn có thể tiếp tục trả lời câu hỏi bên dưới.";
    });
  }

  function testCamera(panel) {
    panel.innerHTML = `
      <p class="test-note">Xem hình ảnh trực tiếp từ camera để kiểm tra độ nét, đốm mờ hoặc màn hình đen.</p>
      <video class="cam-preview" id="cam-preview" autoplay playsinline muted></video>
    `;
    navigator.mediaDevices?.getUserMedia({ video: true }).then((stream) => {
      mediaStream = stream;
      document.getElementById("cam-preview").srcObject = stream;
    }).catch(() => {
      panel.innerHTML += `<p class="test-note">Không thể truy cập camera (chưa cấp quyền hoặc trình duyệt chặn). Vẫn có thể tiếp tục trả lời câu hỏi bên dưới.</p>`;
    });
  }

  function testStorage(panel) {
    panel.innerHTML = `<p class="test-note">Đang kiểm tra dung lượng…</p>`;
    if (navigator.storage?.estimate) {
      navigator.storage.estimate().then(({ usage, quota }) => {
        const usedGB = (usage / 1e9).toFixed(1);
        const quotaGB = (quota / 1e9).toFixed(1);
        const pct = quota ? Math.round((usage / quota) * 100) : 0;
        panel.innerHTML =
          testRow("Dữ liệu web đã dùng (ước tính)", usedGB + " GB") +
          testRow("Hạn mức trình duyệt cho phép", quotaGB + " GB") +
          testRow("Tỉ lệ đã dùng", pct + "%") +
          `<p class="test-note">Đây là dung lượng riêng của trình duyệt, không phải toàn bộ máy. Muốn xem dung lượng thật của iPhone, vào Cài đặt > Cài đặt chung > Dung lượng iPhone.</p>`;
      });
    } else {
      panel.innerHTML = `<p class="test-note">Trình duyệt không hỗ trợ đọc dung lượng. Vào Cài đặt > Cài đặt chung > Dung lượng iPhone để kiểm tra thủ công.</p>`;
    }
  }

  function testNetwork(panel) {
    const online = navigator.onLine;
    const conn = navigator.connection || navigator.webkitConnection;
    let html =
      testRow("Trạng thái mạng", online ? "Đang kết nối" : "Mất kết nối");
    if (conn) {
      html += testRow("Loại kết nối", conn.effectiveType || "không rõ");
      if (conn.downlink) html += testRow("Tốc độ ước tính", conn.downlink + " Mbps");
    }
    html += `<p class="test-note">Bluetooth và các chi tiết phần cứng mạng khác không thể đọc được từ trình duyệt vì lý do bảo mật của iOS — phần này sẽ được hỏi thêm ở bước tiếp theo.</p>`;
    panel.innerHTML = html;
  }

  // ---------- HISTORY ----------
  document.getElementById("btn-history").addEventListener("click", () => {
    fetch("/api/history")
      .then((r) => r.json())
      .then((rows) => {
        const el = document.getElementById("history-table");
        if (!rows.length) {
          el.innerHTML = `<p class="history-empty">Chưa có lần chẩn đoán nào được ghi lại.</p>`;
        } else {
          el.innerHTML = rows.map((r) => {
            const date = new Date(r.ts * 1000);
            const time = date.toLocaleString("vi-VN");
            return `<div class="history-row">
              <span>${r.problem_name}<br><span class="history-row__time">${r.diagnosis_title}</span></span>
              <span class="history-row__time">${time}</span>
            </div>`;
          }).join("");
        }
        showScreen("screen-history");
      });
  });

})();
