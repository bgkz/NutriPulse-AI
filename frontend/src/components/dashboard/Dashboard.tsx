import type { User } from "../../types/user";

export default function Dashboard({ id, username }: User) {
  async function handleFileUpload(file: File) {
    alert(file.name + " wird hochgeladen");
  }
  return (
    <div className="flex flex-col md:flex-row items-center justify-center gap-6 min-h-screen w-full bg-gradient-to-br from-slate-50 via-white to-violet-100 p-4 dark:from-slate-950 dark:via-slate-900 dark:to-violet-950">
      <span>
        Hello {username} --- ID: {id}
      </span>

      <div className="flex flex-col items-center justify-center gap-2 p-4 bg-white/50 dark:bg-slate-900/50 rounded-xl shadow-sm">
        <span>Meine Dokumente (0)</span>
      </div>

      {/* Das Label verknüpft den Text mit dem unsichtbaren Input */}
      <label
        htmlFor="file-upload"
        className="cursor-pointer px-4 py-2 bg-violet-600 hover:bg-violet-700 text-white rounded-lg transition-colors font-medium shadow"
      >
        Trainingsdaten importieren
      </label>

      {/* Das eigentliche Input bleibt versteckt */}
      <input
        id="file-upload"
        type="file"
        accept="application/pdf"
        className="hidden"
        onChange={(e) => {
          const file = e.target.files?.[0];

          if (file) {
            handleFileUpload(file);
          }
        }}
      />
    </div>
  );
}
