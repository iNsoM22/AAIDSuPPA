window.uploadAnswers = async function uploadAnswers() {
  const input = document.getElementById('csvFile');
  if (!input.files.length) {
    alert('Please choose a CSV file first.');
    return;
  }

  const formData = new FormData();
  formData.append('file', input.files[0]);

  const res = await fetch('/upload/answers', {
    method: 'POST',
    body: formData
  });

  const payload = await res.json();
  if (!res.ok) {
    alert(payload.error || 'Upload failed');
    return;
  }

  window.currentUploadId = payload.upload_id;
  document.getElementById('uploadSummary').textContent =
    `Upload ${payload.upload_id} · Students: ${payload.n_students} · Questions: ${payload.n_questions}`;
};
