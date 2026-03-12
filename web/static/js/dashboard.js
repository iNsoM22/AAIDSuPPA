const MAX_POLL_ATTEMPTS = 300;
const BASE_POLL_DELAY_MS = 1000;

async function pollStatus(jobId) {
  const progressEl = document.getElementById('progress');
  const statusEl = document.getElementById('runStatus');
  let attempts = 0;

  while (attempts < MAX_POLL_ATTEMPTS) {
    attempts += 1;
    const res = await fetch(`/run/status/${jobId}`);
    const payload = await res.json();

    if (!res.ok) {
      statusEl.textContent = payload.error || 'Unknown error';
      return;
    }

    progressEl.value = payload.progress;
    statusEl.textContent = `Status: ${payload.status} (${payload.progress}%)`;

    if (payload.status === 'done') {
      window.location.href = `/results/${jobId}`;
      return;
    }

    if (payload.status === 'error') {
      statusEl.textContent = `Error: ${payload.error || 'unknown'}`;
      return;
    }
    const delayMs = Math.min(BASE_POLL_DELAY_MS + attempts * 10, 3000);
    await new Promise((resolve) => setTimeout(resolve, delayMs));
  }

  statusEl.textContent = 'Status: timeout while waiting for job completion';
}

window.runAnalysis = async function runAnalysis() {
  if (!window.currentUploadId) {
    alert('Please upload a CSV first.');
    return;
  }

  const mode = document.getElementById('mode').value;
  const payload = {
    upload_id: window.currentUploadId,
    mode,
    threshold: Number(document.getElementById('threshold').value),
    num_threads: Number(document.getElementById('threads').value),
    schedule: document.getElementById('schedule').value,
    chunk_size: Number(document.getElementById('chunk').value)
  };

  const res = await fetch('/run/analyze', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });

  const body = await res.json();
  if (!res.ok) {
    alert(body.error || 'Failed to start analysis');
    return;
  }

  pollStatus(body.job_id);
};

document.addEventListener('DOMContentLoaded', () => {
  const modeEl = document.getElementById('mode');
  const ompPanel = document.getElementById('ompConfig');

  const updatePanel = () => {
    ompPanel.style.display = modeEl.value === 'omp' ? 'block' : 'none';
  };

  modeEl.addEventListener('change', updatePanel);
  updatePanel();
});
