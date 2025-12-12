export default function SettingsPage() {
  return (
    <div className="space-y-4">
      <div className="text-xl font-semibold">Settings</div>
      <div className="text-sm text-gray-400">Environment and API settings are configured via environment variables.</div>
      <div className="rounded-lg border border-gray-800 p-4">
        <div className="text-sm">NEXT_PUBLIC_API_URL</div>
        <div className="text-xs text-gray-500">Backend FastAPI URL (default http://localhost:8000)</div>
      </div>
      <div className="rounded-lg border border-gray-800 p-4">
        <div className="text-sm">NEXT_PUBLIC_API_KEY</div>
        <div className="text-xs text-gray-500">x-api-key header for backend authentication (default dev-key)</div>
      </div>
    </div>
  );
}
