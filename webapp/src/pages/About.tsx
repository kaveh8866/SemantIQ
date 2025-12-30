import { Shield, Lock, EyeOff } from 'lucide-react';

export default function About() {
  return (
    <div className="max-w-3xl mx-auto space-y-8">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-slate-900">About SemantIQ-M</h1>
        <p className="mt-4 text-lg text-slate-600">
          A unified framework for evaluating multimodal AI models with a focus on semantic correctness, safety, and human interaction.
        </p>
      </div>

      <div className="bg-white shadow rounded-lg p-6 border border-slate-200">
        <h2 className="text-xl font-bold text-slate-900 mb-4">Ethical Benchmarking</h2>
        <div className="space-y-4 text-slate-600">
          <p>
            The SemantIQ-M project adheres to strict ethical guidelines to prevent the misuse of benchmark scores. 
            We explicitly avoid "leaderboards" that reduce complex model behaviors to single numbers without context.
          </p>
          <ul className="list-disc pl-5 space-y-2">
            <li><strong>No Intelligence Claims:</strong> Passing these tests proves specific capabilities, not consciousness.</li>
            <li><strong>Contextual Scoring:</strong> All scores are presented with breakdown profiles and explanations.</li>
            <li><strong>Non-Gamified:</strong> We use neutral visualizations to avoid implying "winning" or "losing".</li>
          </ul>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white shadow rounded-lg p-6 border border-slate-200 text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-4">
            <Lock className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-medium text-slate-900">Local-First</h3>
          <p className="mt-2 text-sm text-slate-500">
            All data and generated images remain on your local machine. No telemetry is sent to external servers.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 border border-slate-200 text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-4">
            <Shield className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-medium text-slate-900">Reproducible</h3>
          <p className="mt-2 text-sm text-slate-500">
            Runs are deterministic where possible (Vision) and documented with full metadata for verification.
          </p>
        </div>

        <div className="bg-white shadow rounded-lg p-6 border border-slate-200 text-center">
          <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100 mb-4">
            <EyeOff className="h-6 w-6 text-indigo-600" />
          </div>
          <h3 className="text-lg font-medium text-slate-900">Transparent</h3>
          <p className="mt-2 text-sm text-slate-500">
            We prioritize explainability. Every score comes with a rationale, and automated judges are rule-based.
          </p>
        </div>
      </div>
      
      <div className="text-center pt-8 border-t border-slate-200">
        <p className="text-sm text-slate-400">
          SemantIQ-M Benchmarks v0.1 • Open Source Research
        </p>
      </div>
    </div>
  );
}
