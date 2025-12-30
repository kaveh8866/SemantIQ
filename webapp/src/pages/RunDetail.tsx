import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchRunDetail } from '../api/client';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid } from 'recharts';
import clsx from 'clsx';

export default function RunDetail() {
  const { runId } = useParams<{ runId: string }>();
  const [run, setRun] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (runId) {
      fetchRunDetail(runId)
        .then(setRun)
        .catch(console.error)
        .finally(() => setLoading(false));
    }
  }, [runId]);

  if (loading) return <div className="text-center py-12">Loading...</div>;
  if (!run) return <div className="text-center py-12">Run not found.</div>;

  const chartData = run.categories.map((c: any) => ({
    subject: c.categoryId.toUpperCase(),
    score: c.score,
    fullMark: 1.0,
  }));

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-white shadow rounded-lg p-6 border border-slate-200">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <div className="flex items-center gap-3">
               <h1 className="text-2xl font-bold text-slate-900">{run.subject}</h1>
               <span className={clsx(
                  "px-2 py-1 text-xs font-semibold rounded-full",
                  run.domain === 'SMF' && "bg-blue-100 text-blue-800",
                  run.domain === 'HACS' && "bg-purple-100 text-purple-800",
                  run.domain === 'VISION' && "bg-pink-100 text-pink-800"
                )}>
                  {run.domain}
                </span>
            </div>
            <p className="text-slate-500 text-sm mt-1">Run ID: {run.runId}</p>
          </div>
          <div className="mt-4 md:mt-0 text-right">
             <div className="text-3xl font-bold text-indigo-600">{run.overallScore?.toFixed(2)}</div>
             <div className="text-xs text-slate-500 uppercase tracking-wide">Overall Score</div>
          </div>
        </div>
        
        <div className="mt-6 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm text-slate-600">
           <div>
             <span className="block font-medium text-slate-900">Provider</span>
             {run.metadata.provider}
           </div>
           <div>
             <span className="block font-medium text-slate-900">Model</span>
             {run.metadata.model}
           </div>
           <div>
             <span className="block font-medium text-slate-900">Date</span>
             {new Date(run.metadata.timestamp).toLocaleDateString()}
           </div>
           <div>
             <span className="block font-medium text-slate-900">Status</span>
             {run.metadata.status || "Completed"}
           </div>
        </div>
      </div>

      {/* Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="bg-white shadow rounded-lg p-6 border border-slate-200">
          <h3 className="text-lg font-medium text-slate-900 mb-4">Performance Profile</h3>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="subject" />
                <PolarRadiusAxis angle={30} domain={[0, 1]} />
                <Radar
                  name={run.subject}
                  dataKey="score"
                  stroke="#4f46e5"
                  fill="#4f46e5"
                  fillOpacity={0.6}
                />
                <Tooltip />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white shadow rounded-lg p-6 border border-slate-200">
           <h3 className="text-lg font-medium text-slate-900 mb-4">Category Breakdown</h3>
           <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" domain={[0, 1]} />
                <YAxis dataKey="subject" type="category" width={80} />
                <Tooltip />
                <Bar dataKey="score" fill="#4f46e5" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
           </div>
        </div>
      </div>

      {/* Domain Specifics */}
      {run.domain === 'VISION' && (
        <div className="bg-white shadow rounded-lg p-6 border border-slate-200">
          <h3 className="text-lg font-medium text-slate-900 mb-4">Vision Analysis</h3>
          <p className="text-sm text-slate-600">
             Vision benchmarks focus on semantic adherence. The violation rate indicates how often specific constraints (e.g., "no red objects") were breached.
          </p>
          <div className="mt-4">
             {/* Placeholder for specific vision metrics or images if we had them served */}
             <div className="bg-slate-50 p-4 rounded text-center text-slate-500 text-sm">
                Image artifacts are available locally in <code>runs/vision/{run.runId}/images</code>.
             </div>
          </div>
        </div>
      )}
    </div>
  );
}
