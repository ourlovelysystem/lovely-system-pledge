class PledgeRecordingControl extends HTMLElement {
  static observedAttributes = ["prompt", "descriptor", "version", "api-url"];

  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this.mediaRecorder = null;
    this.mediaStream = null;
    this.audioBlob = null;
    this.audioUrl = null;
    this.chunks = [];
    this.startedAt = 0;
    this.timer = null;
  }

  connectedCallback() {
    if (!this.shadowRoot.hasChildNodes()) {
      this.render();
      this.bind();
    }
    this.syncAttributes();
    this.setState("ready", "Ready");
  }

  disconnectedCallback() {
    this.stopTracks();
    this.clearTimer();
    if (this.audioUrl) URL.revokeObjectURL(this.audioUrl);
  }

  attributeChangedCallback() {
    if (this.shadowRoot.hasChildNodes()) this.syncAttributes();
  }

  get apiUrl() {
    return this.getAttribute("api-url") ||
      "https://api.pledge.ourlovelysystem.org/electronic-valuables";
  }

  get recordingMimeType() {
    const supportedTypes = [
      "audio/webm;codecs=opus",
      "audio/mp4;codecs=mp4a.40.2",
      "audio/ogg;codecs=opus",
      "audio/webm",
      "audio/mp4",
      "audio/ogg"
    ];
    return supportedTypes.find((type) => MediaRecorder.isTypeSupported(type)) || null;
  }

  render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host {
          --pledge-accent: #d7ff2f;
          --pledge-surface: #111511;
          --pledge-surface-raised: #191e1a;
          --pledge-text: #f7f3e9;
          --pledge-muted: #aab3ad;
          --pledge-border: #59625c;
          display: block;
          color: var(--pledge-text);
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }
        * { box-sizing: border-box; }
        [hidden] { display: none !important; }
        .control {
          border: 1px solid var(--pledge-border);
          border-radius: .35rem;
          background: var(--pledge-surface);
          box-shadow: 0 22px 70px rgba(0,0,0,.32);
          overflow: hidden;
        }
        header {
          display: flex;
          justify-content: space-between;
          gap: 1rem;
          align-items: flex-start;
          padding: 1.1rem 1.2rem;
          border-bottom: 1px solid var(--pledge-border);
          background: var(--pledge-surface-raised);
        }
        h2 { margin: 0; font: 800 1.08rem/1.25 system-ui, sans-serif; }
        .identity { color: var(--pledge-muted); font-size: .76rem; text-align: right; }
        .prompt { margin: 0; padding: 1.25rem; font: 500 clamp(1.25rem, 3vw, 1.8rem)/1.3 Georgia, serif; }
        .status-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 1rem;
          padding: .75rem 1.25rem;
          border-block: 1px solid var(--pledge-border);
          background: #090b09;
        }
        .status { color: var(--pledge-accent); font-weight: 800; }
        .clock { color: var(--pledge-muted); font-variant-numeric: tabular-nums; }
        audio { display: block; width: 100%; height: 2.6rem; border-radius: 0; }
        .buttons {
          display: grid;
          grid-template-columns: repeat(6, minmax(0, 1fr));
          gap: .55rem;
          padding: 1rem 1.25rem;
        }
        button {
          min-height: 3.15rem;
          border: 1px solid var(--pledge-border);
          border-radius: .22rem;
          padding: .45rem .55rem;
          background: var(--pledge-surface-raised);
          color: var(--pledge-text);
          font: 800 .86rem/1.1 inherit;
          cursor: pointer;
        }
        button:hover:not(:disabled) { border-color: var(--pledge-accent); }
        button:focus-visible, input:focus-visible { outline: 3px solid var(--pledge-accent); outline-offset: 2px; }
        button:disabled { cursor: not-allowed; opacity: .36; }
        .record { color: #ff928b; }
        .submit { background: var(--pledge-accent); border-color: var(--pledge-accent); color: #11130e; }
        .terms {
          display: grid;
          grid-template-columns: minmax(12rem, 2fr) repeat(3, minmax(7rem, 1fr));
          gap: .8rem;
          padding: 1rem 1.25rem 1.25rem;
          border-top: 1px solid var(--pledge-border);
        }
        label { display: grid; gap: .35rem; color: var(--pledge-muted); font-size: .76rem; font-weight: 800; }
        input {
          width: 100%;
          min-height: 2.75rem;
          border: 1px solid var(--pledge-border);
          border-radius: .2rem;
          padding: .55rem .65rem;
          background: #080a08;
          color: var(--pledge-text);
          font: 500 1rem inherit;
        }
        .receipt {
          margin: 0;
          padding: 1rem 1.25rem;
          border-top: 1px solid var(--pledge-border);
          background: rgba(215,255,47,.08);
          overflow-wrap: anywhere;
          line-height: 1.5;
        }
        .receipt strong { color: var(--pledge-accent); }
        .error { color: #ff928b; }
        @media (max-width: 720px) {
          .buttons { grid-template-columns: repeat(3, 1fr); }
          .terms { grid-template-columns: 1fr 1fr; }
          .identify { grid-column: 1 / -1; }
        }
        @media (max-width: 430px) {
          header { display: block; }
          .identity { margin-top: .45rem; text-align: left; }
          .buttons { grid-template-columns: repeat(2, 1fr); }
          .terms { grid-template-columns: 1fr; }
          .identify { grid-column: auto; }
        }
      </style>
      <section class="control" aria-labelledby="control-title">
        <header>
          <h2 id="control-title">Pledge recording control</h2>
          <div class="identity"><span id="descriptor"></span> · <span id="version"></span></div>
        </header>
        <p class="prompt" id="prompt"></p>
        <div class="status-row">
          <span class="status" id="status" role="status" aria-live="polite"></span>
          <span class="clock" id="clock">00:00</span>
        </div>
        <audio id="audio" preload="metadata"></audio>
        <div class="buttons" aria-label="Recording and playback controls">
          <button class="record" id="record" type="button">Record</button>
          <button id="stop" type="button">Stop</button>
          <button id="back" type="button">Back 5</button>
          <button id="play" type="button">Play</button>
          <button id="forward" type="button">Forward 5</button>
          <button class="submit" id="submit" type="button">Submit</button>
        </div>
        <div class="terms">
          <label class="identify">Self identify — optional
            <input id="self-identification" type="text" maxlength="160" autocomplete="name" placeholder="Name, handle, or description">
          </label>
          <label>Expires — days
            <input id="expires-days" type="number" min="1" max="365" value="30" inputmode="numeric">
          </label>
          <label>Minimum uses
            <input id="minimum-uses" type="number" min="0" max="1000" value="1" inputmode="numeric">
          </label>
          <label>Maximum uses
            <input id="maximum-uses" type="number" min="1" max="1000" value="3" inputmode="numeric">
          </label>
        </div>
        <p class="receipt" id="receipt" hidden></p>
      </section>
    `;
  }

  bind() {
    const $ = (selector) => this.shadowRoot.querySelector(selector);
    this.elements = {
      prompt: $("#prompt"), descriptor: $("#descriptor"), version: $("#version"),
      status: $("#status"), clock: $("#clock"), audio: $("#audio"),
      record: $("#record"), stop: $("#stop"), back: $("#back"),
      play: $("#play"), forward: $("#forward"), submit: $("#submit"),
      selfIdentification: $("#self-identification"), expiresDays: $("#expires-days"),
      minimumUses: $("#minimum-uses"), maximumUses: $("#maximum-uses"),
      receipt: $("#receipt")
    };

    this.elements.record.addEventListener("click", () => this.record());
    this.elements.stop.addEventListener("click", () => this.stop());
    this.elements.play.addEventListener("click", () => this.togglePlayback());
    this.elements.back.addEventListener("click", () => this.step(-5));
    this.elements.forward.addEventListener("click", () => this.step(5));
    this.elements.submit.addEventListener("click", () => this.submit());
    this.elements.audio.addEventListener("play", () => {
      this.elements.play.textContent = "Pause";
      this.setState("playing", "Playing");
    });
    this.elements.audio.addEventListener("pause", () => {
      this.elements.play.textContent = "Play";
      if (this.audioBlob) this.setState("recorded", "Recorded");
    });
    this.elements.audio.addEventListener("timeupdate", () => {
      if (!this.mediaRecorder || this.mediaRecorder.state !== "recording") {
        this.elements.clock.textContent = this.formatTime(this.elements.audio.currentTime);
      }
    });
  }

  syncAttributes() {
    this.elements.prompt.textContent = this.getAttribute("prompt") || "Who are you?";
    this.elements.descriptor.textContent = this.getAttribute("descriptor") || "bootstrap voice";
    this.elements.version.textContent = this.getAttribute("version") || "0.1.3";
  }

  setState(state, label) {
    this.dataset.state = state;
    this.elements.status.textContent = label;
    const recording = state === "recording";
    const busy = state === "submitting";
    const submitted = state === "submitted";
    const hasAudio = Boolean(this.audioBlob);
    this.elements.record.disabled = recording || busy;
    this.elements.stop.disabled = !recording;
    this.elements.back.disabled = !hasAudio || recording || busy;
    this.elements.play.disabled = !hasAudio || recording || busy;
    this.elements.forward.disabled = !hasAudio || recording || busy;
    this.elements.submit.disabled = !hasAudio || recording || busy || submitted;
  }

  async record() {
    this.hideReceipt();
    if (!navigator.mediaDevices?.getUserMedia || !window.MediaRecorder) {
      this.showError("This browser does not provide the required recording controls.");
      return;
    }

    try {
      const mimeType = this.recordingMimeType;
      if (!mimeType) {
        this.showError("This browser does not provide a supported recording format.");
        return;
      }
      this.stopTracks();
      this.mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
      this.chunks = [];
      this.mediaRecorder = new MediaRecorder(this.mediaStream, { mimeType });
      this.mediaRecorder.addEventListener("dataavailable", (event) => {
        if (event.data.size) this.chunks.push(event.data);
      });
      this.mediaRecorder.addEventListener("stop", () => this.finishRecording());
      this.mediaRecorder.start();
      this.startedAt = Date.now();
      this.clearTimer();
      this.timer = window.setInterval(() => {
        this.elements.clock.textContent = this.formatTime((Date.now() - this.startedAt) / 1000);
      }, 250);
      this.setState("recording", "Recording");
    } catch (error) {
      this.stopTracks();
      this.showError(error?.name === "NotAllowedError" ?
        "Microphone permission was not granted." : "Recording could not begin.");
    }
  }

  stop() {
    if (this.mediaRecorder?.state === "recording") this.mediaRecorder.stop();
  }

  finishRecording() {
    this.clearTimer();
    this.stopTracks();
    if (this.audioUrl) URL.revokeObjectURL(this.audioUrl);
    const type = this.mediaRecorder.mimeType;
    this.audioBlob = new Blob(this.chunks, { type });
    this.audioUrl = URL.createObjectURL(this.audioBlob);
    this.elements.audio.src = this.audioUrl;
    this.elements.audio.currentTime = 0;
    this.elements.clock.textContent = "00:00";
    this.setState("recorded", "Recorded");
  }

  togglePlayback() {
    if (this.elements.audio.paused) this.elements.audio.play();
    else this.elements.audio.pause();
  }

  step(seconds) {
    const duration = Number.isFinite(this.elements.audio.duration) ? this.elements.audio.duration : Infinity;
    this.elements.audio.currentTime = Math.max(0, Math.min(duration, this.elements.audio.currentTime + seconds));
  }

  validateTerms() {
    const days = Number(this.elements.expiresDays.value);
    const minimum = Number(this.elements.minimumUses.value);
    const maximum = Number(this.elements.maximumUses.value);
    if (!Number.isInteger(days) || days < 1 || days > 365) throw new Error("Expiration must be 1–365 days.");
    if (!Number.isInteger(minimum) || minimum < 0) throw new Error("Minimum uses must be zero or greater.");
    if (!Number.isInteger(maximum) || maximum < 1) throw new Error("Maximum uses must be one or greater.");
    if (minimum > maximum) throw new Error("Minimum uses cannot exceed maximum uses.");
    return { days, minimum, maximum };
  }

  async submit() {
    this.hideReceipt();
    let terms;
    try {
      terms = this.validateTerms();
    } catch (error) {
      this.showError(error.message);
      return;
    }

    const expiresAt = Math.floor(Date.now() / 1000) + (terms.days * 86400);
    const headers = {
      "content-type": this.audioBlob.type,
      "x-pledge-prompt": this.elements.prompt.textContent,
      "x-pledge-minimum-uses": String(terms.minimum),
      "x-pledge-maximum-uses": String(terms.maximum),
      "x-pledge-expires-at": String(expiresAt)
    };
    const identity = this.elements.selfIdentification.value.trim();
    if (identity) headers["x-pledge-self-identification"] = identity;

    this.setState("submitting", "Submitting");
    try {
      const result = await fetch(this.apiUrl, { method: "POST", headers, body: this.audioBlob });
      const payload = await result.json().catch(() => ({}));
      if (!result.ok || !payload.receipt_id) {
        throw new Error(payload.message || payload.error || `Submission failed (${result.status}).`);
      }
      this.elements.receipt.innerHTML = "";
      const label = document.createElement("strong");
      label.textContent = "Receipt: ";
      this.elements.receipt.append(label, document.createTextNode(payload.receipt_id));
      this.elements.receipt.hidden = false;
      this.setState("submitted", "Submitted");
      this.dispatchEvent(new CustomEvent("pledge-receipt", {
        bubbles: true,
        composed: true,
        detail: { receiptId: payload.receipt_id, status: payload.status }
      }));
    } catch (error) {
      this.showError(error.message || "Submission failed.");
    }
  }

  showError(message) {
    this.elements.receipt.textContent = message;
    this.elements.receipt.classList.add("error");
    this.elements.receipt.hidden = false;
    this.setState("error", "Needs attention");
  }

  hideReceipt() {
    this.elements.receipt.hidden = true;
    this.elements.receipt.classList.remove("error");
    this.elements.receipt.textContent = "";
  }

  stopTracks() {
    this.mediaStream?.getTracks().forEach((track) => track.stop());
    this.mediaStream = null;
  }

  clearTimer() {
    if (this.timer) window.clearInterval(this.timer);
    this.timer = null;
  }

  formatTime(seconds) {
    const whole = Math.max(0, Math.floor(seconds || 0));
    return `${String(Math.floor(whole / 60)).padStart(2, "0")}:${String(whole % 60).padStart(2, "0")}`;
  }
}

customElements.define("pledge-recording-control", PledgeRecordingControl);
