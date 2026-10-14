import { useState } from "react";
import api from "../services/api";

const statusLabels = [
  "Uploading Video",
  "Extracting Frames",
  "Detecting Faces",
  "Spatial Analysis",
  "Temporal Analysis",
  "Generating Result",
];

function Home() {
  const [video, setVideo] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [videoMeta, setVideoMeta] = useState({ duration: null, width: null, height: null });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [statusSteps, setStatusSteps] = useState(
    statusLabels.map((label, index) => ({
      id: index + 1,
      label,
      done: false,
      active: false,
    }))
  );

  const formatScore = (value) => {
    if (value === null || value === undefined) return "N/A";
    return Number(value).toFixed(4);
  };

  const formatPercent = (value) => {
    if (value === null || value === undefined) return "N/A";
    return `${Number(value).toFixed(2)}%`;
  };

  const setProgressState = (activeIndex) => {
    setStatusSteps((current) =>
      current.map((step, index) => ({
        ...step,
        done: index < activeIndex,
        active: index === activeIndex,
      }))
    );
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0] || null;
    setVideo(selectedFile);
    setResult(null);
    setVideoMeta({ duration: null, width: null, height: null });

    if (selectedFile) {
      const nextPreviewUrl = URL.createObjectURL(selectedFile);
      setPreviewUrl(nextPreviewUrl);
    } else {
      setPreviewUrl(null);
    }
  };

  const handleUpload = async () => {
    if (!video) {
      alert("Please select a video.");
      return;
    }

    const formData = new FormData();
    formData.append("video", video);

    setLoading(true);
    setResult(null);
    setProgressState(0);

    const delay = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

    try {
      const progressPromise = (async () => {
        for (let index = 1; index < statusLabels.length; index += 1) {
          await delay(500);
          setProgressState(index);
        }
      })();

      const response = await Promise.all([api.post("/predict/", formData), progressPromise]);
      setResult(response[0].data);
      setProgressState(statusLabels.length - 1);
      setStatusSteps((current) =>
        current.map((step, index) => ({
          ...step,
          done: index <= statusLabels.length - 1,
          active: false,
        }))
      );
    } catch (error) {
      console.error(error);
      alert(error.response?.data?.detail || "Prediction failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 px-4 py-8 text-slate-100">
      <div className="mx-auto max-w-6xl space-y-6">
        <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-8 shadow-2xl">
          <h1 className="text-4xl font-semibold">Deepfake Video Detection</h1>
          <p className="mt-2 text-slate-400">Upload a video and inspect the prediction workflow through a professional dashboard.</p>
        </div>

        <div className="grid gap-6 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl">
            <h2 className="text-2xl font-semibold">Video Preview</h2>
            <div className="mt-4 overflow-hidden rounded-2xl border border-slate-800 bg-slate-950">
              {previewUrl ? (
                <video
                  key={previewUrl}
                  src={previewUrl}
                  controls
                  preload="metadata"
                  className="w-full max-h-[320px] object-contain"
                  onLoadedMetadata={(event) => {
                    const videoElement = event.currentTarget;
                    setVideoMeta({
                      duration: videoElement.duration,
                      width: videoElement.videoWidth,
                      height: videoElement.videoHeight,
                    });
                  }}
                />
              ) : (
                <div className="flex h-60 items-center justify-center text-slate-500">Select a video to preview it here.</div>
              )}
            </div>

            {video && (
              <div className="mt-4 space-y-2 text-sm text-slate-300">
                <div><span className="font-semibold text-slate-100">Filename:</span> {video.name}</div>
                <div><span className="font-semibold text-slate-100">File size:</span> {(video.size / (1024 * 1024)).toFixed(2)} MB</div>
                <div><span className="font-semibold text-slate-100">Duration:</span> {videoMeta.duration ? `${videoMeta.duration.toFixed(2)}s` : "Not available"}</div>
                <div><span className="font-semibold text-slate-100">Resolution:</span> {videoMeta.width && videoMeta.height ? `${videoMeta.width} × ${videoMeta.height}` : "Not available"}</div>
              </div>
            )}

            <input
              type="file"
              accept="video/*"
              className="mt-6 w-full rounded-xl border border-slate-700 bg-slate-950 p-3 text-sm"
              onChange={handleFileChange}
            />

            <button
              disabled={loading}
              onClick={handleUpload}
              className="mt-4 w-full rounded-xl bg-blue-600 px-4 py-3 font-semibold transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
            >
              {loading ? "Analyzing..." : "Analyze Video"}
            </button>
          </div>

          <div className="space-y-6">
            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl">
              <h2 className="text-2xl font-semibold">Processing Status</h2>
              <div className="mt-4 space-y-3">
                {statusSteps.map((step) => (
                  <div key={step.id} className="flex items-center rounded-xl border border-slate-800 bg-slate-950/70 px-4 py-3">
                    <div className={`mr-3 h-3 w-3 rounded-full ${step.done ? "bg-emerald-500" : step.active ? "bg-amber-500" : "bg-slate-600"}`} />
                    <span className={step.active ? "text-amber-400" : step.done ? "text-emerald-400" : "text-slate-300"}>{step.label}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="rounded-3xl border border-slate-800 bg-slate-900/80 p-6 shadow-2xl">
              <h2 className="text-2xl font-semibold">Analysis Result</h2>
              {!result ? (
                <div className="mt-4 text-slate-400">No analysis has been run yet.</div>
              ) : (
                <div className="mt-4 space-y-5">
                  <div className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                    <div className="text-sm uppercase tracking-[0.2em] text-slate-400">Prediction</div>
                    <div className={`mt-2 text-3xl font-semibold ${result.prediction === "FAKE" ? "text-rose-400" : "text-emerald-400"}`}>{result.prediction}</div>
                    <div className="mt-3 text-sm text-slate-400">Confidence: {result.confidence}%</div>
                  </div>

                  <div className="space-y-3">
                    {[
                      { label: "Spatial Score", value: result.spatial_score },
                      { label: "Temporal Score", value: result.temporal_score },
                      { label: "Fusion Score", value: result.final_score },
                    ].map((item) => (
                      <div key={item.label} className="rounded-2xl border border-slate-800 bg-slate-950/70 p-4">
                        <div className="flex items-center justify-between text-sm text-slate-400">
                          <span>{item.label}</span>
                          <span>{formatScore(item.value)}</span>
                        </div>
                        <div className="mt-3 h-2 rounded-full bg-slate-800">
                          <div className="h-2 rounded-full bg-blue-500" style={{ width: `${Math.max(0, Math.min(100, Number(item.value) * 100))}%` }} />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;