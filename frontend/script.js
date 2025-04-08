document.getElementById("video-analyze-form").addEventListener("submit", async function (e) {
  e.preventDefault();

  const fileInput = document.getElementById("videoInput");
  const file = fileInput.files[0];

  const statusText = document.getElementById("upload-status");
  const resultDiv = document.getElementById("result");

  if (!file) {
    alert("⚠️ Please select a video file.");
    return;
  }

  console.log("🎥 File selected:", file);
  statusText.innerText = "⬆️ Uploading video...";

  const formData = new FormData();
  formData.append("file", file); // Matches FastAPI's expected field name

  try {
    // Step 1: Upload the video
    const uploadRes = await fetch("http://127.0.0.1:8000/upload_video", {
      method: "POST",
      body: formData,
    });

    const uploadText = await uploadRes.text();
    let uploadData;
    try {
      uploadData = JSON.parse(uploadText);
    } catch {
      throw new Error("❌ Invalid JSON from upload response: " + uploadText);
    }

    if (!uploadRes.ok) {
      const errorMsg = JSON.stringify(uploadData?.detail || uploadData || "Upload failed");
      throw new Error("❌ Upload failed: " + errorMsg);
    }

    const filename = uploadData.filename;
    console.log("✅ Upload successful. Saved as:", filename);
    statusText.innerText = "🔍 Analyzing video for emotions...";

    // Step 2: Analyze the uploaded video
    const analyzeRes = await fetch("http://127.0.0.1:8000/analyze_video", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ filename: filename }),
    });
    

    const analyzeText = await analyzeRes.text();
    let analyzeData;
    try {
      analyzeData = JSON.parse(analyzeText);
    } catch {
      throw new Error("❌ Invalid JSON from analysis response: " + analyzeText);
    }

    if (!analyzeRes.ok) {
      const errorMsg = JSON.stringify(analyzeData?.detail || analyzeData || "Analysis failed");
      throw new Error("❌ Analysis failed: " + errorMsg);
    }

    console.log("✅ Analysis successful:", analyzeData);

    // Show final results in a friendly format
    resultDiv.innerHTML = `
      <strong>🧠 Facial Expression:</strong> ${analyzeData.facial_expression}<br>
      <strong>🎤 Voice Emotion:</strong> ${analyzeData.voice_emotion}<br>
      <strong>📊 Final Assessment:</strong> <b>${analyzeData.final_result}</b>
    `;

    statusText.innerText = "✅ Analysis complete.";
  } catch (error) {
    console.error("❌ Error occurred:", error);
    statusText.innerText = "❌ Error: " + error.message;
    alert("⚠️ " + error.message);
  }
});
