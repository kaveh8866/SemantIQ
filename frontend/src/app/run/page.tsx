"use client";

import { useEffect, useMemo, useState } from "react";
import { playgroundRun, getRun, getRunResults } from "@/lib/api";
import { Badge } from "@/components/ui/badge";
import { Card, CardTitle, CardValue } from "@/components/ui/card";

type ProviderOption = {
  provider: "openai" | "grok" | "gemini"| "openrouter";
  label: string;
  defaultModel: string;
};

const PROVIDERS: ProviderOption[] = [
  { provider: "openai", label: "OpenAI", defaultModel: "gpt-4o-mini" },
  { provider: "grok", label: "Grok", defaultModel: "grok-2-mini" },
  { provider: "openrouter", label: "OpenRouter", defaultModel: "openrouter/auto" },
];

export default function RunPlaygroundPage() {
  const [showKeys, setShowKeys] = useState(false);
  const [selected, setSelected] = useState<Record<string, boolean>>({ openai: true, grok: false });
  const [models, setModels] = useState<Record<string, string>>({
    openai: "gpt-4o-mini",
    grok: "grok-2-mini",
  });
  const [temps, setTemps] = useState<Record<string, number>>({ openai: 0.2, grok: 0.2 });
  const [maxTokens, setMaxTokens] = useState<Record<string, number>>({ openai: 256, grok: 256 });
  const [systemPrompt, setSystemPrompt] = useState("");
  const [userPrompt, setUserPrompt] = useState("");
  const [isRunning, setIsRunning] = useState(false);
  const [runs, setRuns] = useState<number[]>([]);
  const [statuses, setStatuses] = useState<Record<number, string>>({});
  const [answers, setAnswers] = useState<Record<number, string>>({});

  const providerKeys = useMemo(() => {
    return {
      openai: localStorage.getItem("semantiq_api_key_openai") || "",
      grok: localStorage.getItem("semantiq_api_key_grok") || "",
      openrouter: localStorage.getItem("semantiq_api_key_openrouter") || "",
    };
  }, [showKeys]);

  useEffect(() => {
    if (!runs.length) return;
    let mounted = true;
    const tick = async () => {
      for (const id of runs) {
        try {
          const r = await getRun(id);
          if (!mounted) return;
          setStatuses((prev) => ({ ...prev, [id]: r.status }));
          if (r.status === "completed" && !answers[id]) {
            const res = await getRunResults(id);
            const text = (res.answers?.[0]?.answer_text as string) || "";
            setAnswers((prev) => ({ ...prev, [id]: text }));
          }
        } catch {
          // ignore
        }
      }
    };
    const t = setInterval(tick, 1200);
    tick();
    return () => {
      mounted = false;
      clearInterval(t);
    };
  }, [runs, answers]);

  const selectedProviders = PROVIDERS.filter((p) => selected[p.provider]);

  async function onRun() {
    if (!userPrompt.trim() || !selectedProviders.length) return;
    setIsRunning(true);
    setRuns([]);
    setStatuses({});
    setAnswers({});
    const promptText = systemPrompt.trim()
      ? `System:\n${systemPrompt.trim()}\n\nUser:\n${userPrompt.trim()}`
      : userPrompt.trim();
    const modelsPayload = selectedProviders.map((p) => ({
      provider: p.provider,
      model_name: models[p.provider] || p.defaultModel,
      temperature: temps[p.provider],
      max_tokens: maxTokens[p.provider],
      api_key: (providerKeys as any)[p.provider] || undefined,
    }));
    try {
      const resp = await playgroundRun({
        models: modelsPayload,
        benchmarks_data: [
          { id: "PG-1", module: "playground", prompt_text: promptText, dimensions: [] },
        ],
      });
      setRuns(resp.runs || []);
    } catch (e) {
      // you can show a toast
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="text-xl font-semibold">Model Playground & Vergleich</div>
        <button
          className="rounded-md border border-gray-700 px-3 py-1 text-sm hover:bg-background-lighter"
          onClick={() => setShowKeys(true)}
        >
          API-Schlüssel verwalten
        </button>
      </div>

      <div className="grid grid-cols-1 gap-6 md:grid-cols-3">
        <div className="md:col-span-1 space-y-4">
          <div className="rounded-lg border border-gray-800 p-4">
            <div className="font-medium mb-2">Anbieter & Modelle</div>
            {PROVIDERS.map((p) => (
              <label key={p.provider} className="block mb-3">
                <input
                  type="checkbox"
                  className="mr-2"
                  checked={!!selected[p.provider]}
                  onChange={(e) =>
                    setSelected((prev) => ({ ...prev, [p.provider]: e.target.checked }))
                  }
                />
                {p.label}
                {selected[p.provider] && (
                  <div className="mt-2 ml-6 space-y-2">
                    <input
                      className="w-full rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
                      value={models[p.provider] || ""}
                      onChange={(e) =>
                        setModels((prev) => ({ ...prev, [p.provider]: e.target.value }))
                      }
                      placeholder={`Modellname (z.B. ${p.defaultModel})`}
                    />
                    <div className="flex gap-2">
                      <input
                        type="number"
                        step="0.1"
                        className="w-1/2 rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
                        value={temps[p.provider] ?? 0.2}
                        onChange={(e) =>
                          setTemps((prev) => ({ ...prev, [p.provider]: parseFloat(e.target.value) }))
                        }
                        placeholder="Temperature"
                      />
                      <input
                        type="number"
                        className="w-1/2 rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
                        value={maxTokens[p.provider] ?? 256}
                        onChange={(e) =>
                          setMaxTokens((prev) => ({
                            ...prev,
                            [p.provider]: parseInt(e.target.value, 10),
                          }))
                        }
                        placeholder="Max Tokens"
                      />
                    </div>
                  </div>
                )}
              </label>
            ))}
          </div>

          <button
            className="w-full rounded-md bg-electric px-3 py-2 text-sm font-medium text-black disabled:opacity-50"
            onClick={onRun}
            disabled={isRunning || !userPrompt.trim() || !selectedProviders.length}
          >
            Ausführen & Vergleichen
          </button>
        </div>

        <div className="md:col-span-2 space-y-4">
          <div className="rounded-lg border border-gray-800 p-4">
            <div className="font-medium mb-2">System Prompt</div>
            <textarea
              className="min-h-[80px] w-full rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
              value={systemPrompt}
              onChange={(e) => setSystemPrompt(e.target.value)}
              placeholder="Optional: Richtlinien, Rollen, Ziele..."
            />
          </div>
          <div className="rounded-lg border border-gray-800 p-4">
            <div className="font-medium mb-2">User Prompt</div>
            <textarea
              className="min-h-[160px] w-full rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
              value={userPrompt}
              onChange={(e) => setUserPrompt(e.target.value)}
              placeholder="Ihr Prompt für alle ausgewählten Modelle"
            />
          </div>
        </div>
      </div>

      {!!runs.length && (
        <div className="rounded-lg border border-gray-800 p-4">
          <div className="font-medium mb-4">Ergebnisse</div>
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {runs.map((id) => (
              <div key={id} className="rounded-md border border-gray-700 p-3">
                <div className="flex items-center justify-between mb-2">
                  <div className="text-sm text-gray-400">Run #{id}</div>
                  <Badge className="border-gray-600">{statuses[id] || "pending"}</Badge>
                </div>
                <div className="text-sm whitespace-pre-wrap">
                  {answers[id] || "Warten auf Antwort..."}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {showKeys && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70">
          <div className="w-full max-w-lg rounded-lg border border-gray-800 bg-background p-4">
            <div className="text-lg font-semibold mb-2">API-Schlüssel verwalten</div>
            <div className="text-sm text-gray-400 mb-4">
              Schlüssel werden lokal gespeichert und nur für die Anfrage genutzt.
            </div>
            <div className="space-y-3">
              <div>
                <div className="text-sm mb-1">OpenAI</div>
                <input
                  className="w-full rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
                  defaultValue={providerKeys.openai}
                  onChange={(e) => localStorage.setItem("semantiq_api_key_openai", e.target.value)}
                  placeholder="sk-..." />
              </div>
              <div>
                <div className="text-sm mb-1">Grok</div>
                <input
                  className="w-full rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
                  defaultValue={providerKeys.grok}
                  onChange={(e) => localStorage.setItem("semantiq_api_key_grok", e.target.value)}
                  placeholder="gsk-..." />
              </div>
              <div>
                <div className="text-sm mb-1">OpenRouter</div>
                <input
                  className="w-full rounded-md border border-gray-700 bg-background px-2 py-1 text-sm"
                  defaultValue={providerKeys.openrouter}
                  onChange={(e) => localStorage.setItem("semantiq_api_key_openrouter", e.target.value)}
                  placeholder="or-..." />
              </div>
            </div>
            <div className="mt-4 flex justify-end gap-2">
              <button
                className="rounded-md border border-gray-700 px-3 py-1 text-sm hover:bg-background-lighter"
                onClick={() => setShowKeys(false)}
              >
                Schließen
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
