(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const landing = $("landing");
  const solicitation = $("solicitation");
  const comeBack = $("comeBack");
  const modeLabel = $("modeLabel");
  const landingKicker = $("landingKicker");
  const landingTitle = $("landingTitle");
  const landingQuestion = $("landingQuestion");
  const bootstrapActions = $("bootstrapActions");
  const challengeAudio = $("challengeAudio");
  const recordButton = $("recordButton");
  const stopButton = $("stopButton");
  const discardButton = $("discardButton");
  const submitButton = $("submitButton");
  const preview = $("preview");
  const status = $("submissionStatus");
  const timer = $("timer");
  const recordingState = $("recordingState");
  const meterState = $("meterState");
  const canvas = $("meter");
  const context = canvas.getContext("2d");

  let stream = null;
  let recorder = null;
  let chunks = [];
  let blob = null;
  let objectUrl = null;
  let startedAt = 0;
  let recordingDurationMs = 0;
  let timerHandle = null;
  let audioContext = null;
  let analyser = null;
  let animationHandle = null;

  function show(section) {
    [landing, solicitation, comeBack].forEach((node) => { node.hidden = node !== section; });
    section.querySelector("button:not([disabled])")?.focus();
  }

  function renderPledgeState(body) {
    const mode = body.mode || "bootstrap";
    challengeAudio.pause();
    challengeAudio.removeAttribute("src");
    challengeAudio.hidden = true;
    bootstrapActions.hidden = false;

    if (mode === "normal" && body.challenge?.audio_url) {
      modeLabel.textContent = "BORROWED VOICE MODE";
      landingKicker.textContent = "Pledge speaks with a borrowed voice.";
      landingTitle.textContent = "Who are you?";
      landingQuestion.textContent = "Listen to Pledge's borrowed challenge.";
      challengeAudio.src = body.challenge.audio_url;
      challengeAudio.hidden = false;
      bootstrapActions.hidden = true;
      $("landingStatus").textContent = "";
      return;
    }

    if (mode === "sulk") {
      modeLabel.textContent = "SULK MODE";
      landingKicker.textContent = "Pledge once had a voice.";
      landingTitle.textContent = "Now Pledge has none.";
      landingQuestion.textContent = "May Pledge borrow yours?";
      return;
    }

    modeLabel.textContent = "BOOTSTRAP MODE";
    landingKicker.textContent = "Pledge begins mute.";
    landingTitle.textContent = "Pledge has no voice of its own.";
    landingQuestion.textContent = "Can Pledge borrow your voice?";
  }

  async function loadPledgeState() {
    const apiUrl = String(window.PLEDGE_CONFIG?.API_URL || "").replace(/\/$/, "");
    if (!apiUrl) return;
    $("landingStatus").textContent = "Checking Pledge's voice catalogue…";
    try {
      const result = await fetch(`${apiUrl}/state`, { cache: "no-store" });
      const body = await result.json().catch(() => ({}));
      if (!result.ok) throw new Error(body.error || `State request failed (${result.status}).`);
      renderPledgeState(body);
    } catch (error) {
      $("landingStatus").textContent = error?.message || "Pledge could not determine its state.";
    }
  }

  function formatTime(ms) {
    const seconds = Math.max(0, Math.floor(ms / 1000));
    return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, "0")}`;
  }

  function drawIdle() {
    context.fillStyle = "#020302";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.strokeStyle = "#314038";
    context.lineWidth = 2;
    context.beginPath();
    context.moveTo(0, canvas.height / 2);
    context.lineTo(canvas.width, canvas.height / 2);
    context.stroke();
  }

  function drawMeter() {
    if (!analyser) return;
    const values = new Uint8Array(analyser.frequencyBinCount);
    analyser.getByteTimeDomainData(values);
    context.fillStyle = "#020302";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.strokeStyle = "#d6ff3f";
    context.lineWidth = 3;
    context.beginPath();
    values.forEach((value, index) => {
      const x = index * canvas.width / (values.length - 1);
      const y = value / 255 * canvas.height;
      index ? context.lineTo(x, y) : context.moveTo(x, y);
    });
    context.stroke();
    animationHandle = requestAnimationFrame(drawMeter);
  }

  async function releaseMicrophone() {
    clearInterval(timerHandle);
    timerHandle = null;
    cancelAnimationFrame(animationHandle);
    animationHandle = null;
    stream?.getTracks().forEach((track) => track.stop());
    stream = null;
    analyser = null;
    if (audioContext) await audioContext.close().catch(() => {});
    audioContext = null;
    meterState.textContent = "READY";
    drawIdle();
  }

  function discard() {
    if (objectUrl) URL.revokeObjectURL(objectUrl);
    objectUrl = null;
    blob = null;
    chunks = [];
    recordingDurationMs = 0;
    preview.removeAttribute("src");
    preview.hidden = true;
    discardButton.disabled = true;
    submitButton.disabled = true;
    timer.textContent = "0:00";
    recordingState.textContent = "Ready";
    status.textContent = "";
  }

  async function startRecording() {
    discard();
    status.textContent = "";
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const preferred = ["audio/webm;codecs=opus", "audio/webm", "audio/mp4"]
        .find((type) => window.MediaRecorder?.isTypeSupported(type));
      recorder = preferred ? new MediaRecorder(stream, { mimeType: preferred }) : new MediaRecorder(stream);
      chunks = [];
      recorder.addEventListener("dataavailable", (event) => {
        if (event.data.size) chunks.push(event.data);
      });
      recorder.addEventListener("stop", finishRecording, { once: true });

      audioContext = new AudioContext();
      analyser = audioContext.createAnalyser();
      analyser.fftSize = 1024;
      audioContext.createMediaStreamSource(stream).connect(analyser);
      drawMeter();

      recorder.start(250);
      startedAt = Date.now();
      timerHandle = setInterval(() => { timer.textContent = formatTime(Date.now() - startedAt); }, 200);
      recordingState.textContent = "Recording";
      meterState.textContent = "LISTENING";
      recordButton.disabled = true;
      stopButton.disabled = false;
    } catch (error) {
      status.textContent = error?.name === "NotAllowedError"
        ? "Microphone permission was not granted."
        : "Pledge could not start the microphone.";
      await releaseMicrophone();
    }
  }

  async function finishRecording() {
    const duration = Date.now() - startedAt;
    recordingDurationMs = duration;
    await releaseMicrophone();
    recordButton.disabled = false;
    stopButton.disabled = true;

    blob = new Blob(chunks, { type: recorder.mimeType || "audio/webm" });
    const valid = blob.size > 1000 && duration >= 750 && duration <= 30000;
    if (!valid) {
      recordingState.textContent = "Envelope rejected";
      status.textContent = duration > 30000
        ? "The recording is longer than 30 seconds."
        : "The recording is too short or contains no usable audio object.";
      discardButton.disabled = false;
      return;
    }

    objectUrl = URL.createObjectURL(blob);
    preview.src = objectUrl;
    preview.hidden = false;
    discardButton.disabled = false;
    submitButton.disabled = false;
    recordingState.textContent = "Recorded";
    timer.textContent = formatTime(duration);
    status.textContent = "Local envelope checks passed. Listen before submitting.";
  }

  function stopRecording() {
    if (recorder?.state === "recording") recorder.stop();
  }

  function blobToBase64(value) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.addEventListener("load", () => resolve(String(reader.result).split(",", 2)[1]));
      reader.addEventListener("error", () => reject(reader.error));
      reader.readAsDataURL(value);
    });
  }

  async function submitRecording() {
    if (!blob) return;
    const apiUrl = String(window.PLEDGE_CONFIG?.API_URL || "").replace(/\/$/, "");
    if (!apiUrl) {
      status.textContent = "Pledge intake is not configured. Add the deployed ApiUrl to config.js.";
      return;
    }

    submitButton.disabled = true;
    discardButton.disabled = true;
    status.textContent = "Making the recording durable…";

    try {
      const audioBase64 = await blobToBase64(blob);
      const borrowingTerm = document.querySelector('input[name="term"]:checked')?.value;
      const result = await fetch(`${apiUrl}/submissions`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          audio_base64: audioBase64,
          media_type: blob.type,
          duration_ms: Math.round(recordingDurationMs),
          borrowing_term: borrowingTerm
        })
      });
      const body = await result.json().catch(() => ({}));
      if (!result.ok) throw new Error(body.error || `Submission failed (${result.status}).`);
      comeBack.dataset.submissionId = body.submission_id;
      show(comeBack);
    } catch (error) {
      status.textContent = error?.message || "Pledge could not accept the recording.";
      submitButton.disabled = false;
      discardButton.disabled = false;
    }
  }

  $("agreeButton").addEventListener("click", () => show(solicitation));
  $("declineButton").addEventListener("click", () => {
    $("landingStatus").textContent = "Pledge remains mute.";
  });
  $("cancelButton").addEventListener("click", async () => {
    if (recorder?.state === "recording") recorder.stop();
    await releaseMicrophone();
    discard();
    show(landing);
  });
  $("returnButton").addEventListener("click", async () => {
    discard();
    show(landing);
    await loadPledgeState();
  });
  recordButton.addEventListener("click", startRecording);
  stopButton.addEventListener("click", stopRecording);
  discardButton.addEventListener("click", discard);
  submitButton.addEventListener("click", submitRecording);

  window.addEventListener("beforeunload", () => {
    stream?.getTracks().forEach((track) => track.stop());
    if (objectUrl) URL.revokeObjectURL(objectUrl);
  });

  drawIdle();
  loadPledgeState();
})();
