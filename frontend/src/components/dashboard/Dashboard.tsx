import { useState } from "react";
type DashboardProps = {
  token: string;
};

type JobProps = {
  job_id: string;
  status: string;
};

type JobResultProps = {
  status: string;
  result: any;
};

export default function Dashboard({ token }: DashboardProps) {
  const [url, setUrl] = useState("");
  const [jobId, setJobId] = useState<any>(null);
  const [result, setResult] = useState<any>(null);

  async function getJobStatus() {
    try {
      const response = await fetch(
        `http://localhost:8000/documents/jobs/${jobId}`,
        {
          method: "GET",
        },
      );

      const data: JobResultProps = await response.json();

      if (response.ok) {
        if (data.status === "finished") {
          setResult(data.result);
          alert(JSON.stringify(data.result));
        }

        if (data.status === "failed") {
          alert("Job failed");
        }
        if (data.status === "started") {
          alert("Job stated, no results yet for ID: " + jobId);
        }
      }
    } catch (error) {
      alert("Error: " + error);
    }
  }

  async function handleUrlImport(url: string) {
    try {
      const response = await fetch("http://localhost:8000/documents/", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data: JobProps = await response.json();

      if (response.ok) {
        alert("Response was successful: " + data.job_id);
        setJobId(data.job_id);
      } else {
        alert("Response was not successful: ");
      }
    } catch (error) {
      alert("Error: " + error);
    }
  }

  return (
    <div className="flex flex-col md:flex-row items-center justify-center gap-6 min-h-screen w-full bg-gradient-to-br from-slate-50 via-white to-violet-100 p-4 dark:from-slate-950 dark:via-slate-900 dark:to-violet-950">
      <span>Hello {token} ---</span>

      <div className="flex flex-col items-center justify-center gap-2 p-4 bg-white/50 dark:bg-slate-900/50 rounded-xl shadow-sm">
        <span>Meine Dokumente (0)</span>
      </div>

      <div>
        <label>URL</label>
        <input
          type="url"
          placeholder="https://example.com"
          value={url}
          onChange={(event) => setUrl(event.target.value)}
        />
      </div>
      <button
        onClick={() => handleUrlImport(url)}
        className="cursor-pointer rounded-xl bg-violet-600 px-4 py-3 font-semibold text-white shadow-lg shadow-violet-600/20 transition hover:-translate-y-0.5 hover:bg-violet-700 focus:ring-4 focus:ring-violet-500/25 focus:outline-none"
      >
        Submit
      </button>
      <button
        onClick={() => getJobStatus()}
        className="cursor-pointer rounded-xl bg-violet-600 px-4 py-3 font-semibold text-white shadow-lg shadow-violet-600/20 transition hover:-translate-y-0.5 hover:bg-violet-700 focus:ring-4 focus:ring-violet-500/25 focus:outline-none"
      >
        See Job Statuus
      </button>
    </div>
  );
}
