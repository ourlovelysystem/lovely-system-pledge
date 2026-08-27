(() => {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const landing = $("landing");
  const solicitation = $("solicitation");
  const comeBack = $("comeBack");
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
  let timerHandle = null;
  let audioContext = null;
  let analyser = null;
  let animationHandle = null;

  function show(section) {
    [landing, solicitation, comeBack].forEach((node) => { node.hidden = node !== section; });
    section.querySelector("button:not([disabled])")?.focus();
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
  $("returnButton").addEventListener("click", () => {
    discard();
    show(landing);
  });
  recordButton.addEventListener("click", startRecording);
  stopButton.addEventListener("click", stopRecording);
  discardButton.addEventListener("click", discard);
  submitButton.addEventListener("click", () => {
    if (!blob) return;
    show(comeBack);
  });

  window.addEventListener("beforeunload", () => {
    stream?.getTracks().forEach((track) => track.stop());
    if (objectUrl) URL.revokeObjectURL(objectUrl);
  });

  drawIdle();
})();