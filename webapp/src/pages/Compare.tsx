import { useEffect, useState } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { fetchRunDetail } from '../api/client';
import { RunSummary } from '../api/types';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip, Legend } from 'recharts';
import { ArrowLeft, AlertTriangle } from 'lucide-react';

const COLORS = ['#4f46e5', '#db2777', '#059669']; // Indigo, Pink, Emerald

export default function Compare() {
  const [searchParams] = useSearchParams();
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const runIds = searchParams.get('ids')?.split(',').filter(Boolean) || [];

  useEffect(() => {
    if (runIds.length === 0) {
      setLoading(false);
      return;
    }

    Promise.all(runIds.map(id => fetchRunDetail(id)))
      .then(results => {
        setRuns(results);
      })
      .catch(err => {
        console.error(err);
        setError("Failed to load one or more runs.");
      })
      .finally(() => setLoading(false));
  }, [searchParams]);

  if (loading) return <div className="text-center py-12">Loading comparisons...</div>;
  if (error) return <div className="text-center py-12 text-red-600">Error: {error}</div>;
  
  if (runIds.length === 0) {
    return (
      <div className="text-center py-12">
        <h2 className="text-xl font-bold text-slate-900">No runs selected</h2>
        <Link to="/runs" className="text-indigo-600 hover:text-indigo-900 mt-4 inline-block">
          Go to Runs List
        </Link>
      </div>
    );
  }

  // Check for mixed domains
  const domains = new Set(runs.map(r => r.domain));
  const hasMixedDomains = domains.size > 1;

  // Prepare Chart Data
  // We need to union all categories
  const allCategories = new Set<string>();
  runs.forEach(r => r.categories.forEach(c => allCategories.add(c.categoryId)));
  
  const chartData = Array.from(allCategories).map(catId => {
    const dataPoint: any = { subject: catId.toUpperCase(), fullMark: 1.0 };
    runs.forEach((r, idx) => {
        const cat = r.categories.find(c => c.categoryId === catId);
        dataPoint[`run_${idx}`] = cat ? cat.score : 0;
    });
    return dataPoint;
  });

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-slate-900">Compare Runs</h1>
        <Link to="/runs" className="flex items-center text-sm text-slate-500 hover:text-slate-900">
          <ArrowLeft className="h-4 w-4 mr-1" /> Back to List
        </Link>
      </div>

      {hasMixedDomains && (
        <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
          <div className="flex">
            <div className="flex-shrink-0">
              <AlertTriangle className="h-5 w-5 text-yellow-400" aria-hidden="true" />
            </div>
            <div className="ml-3">
              <p className="text-sm text-yellow-700">
                You are comparing runs from different domains ({Array.from(domains).join(', ')}). 
                Scores may not be directly comparable.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Comparison Chart */}
      <div className="bg-white shadow rounded-lg p-6 border border-slate-200">
        <h3 className="text-lg font-medium text-slate-900 mb-4">Profile Comparison</h3>
        <div className="h-96 w-full">
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={chartData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" />
              <PolarRadiusAxis angle={30} domain={[0, 1]} />
              {runs.map((run, idx) => (
                <Radar
                  key={run.runId}
                  name={run.subject}
                  dataKey={`run_${idx}`}
                  stroke={COLORS[idx % COLORS.length]}
                  fill={COLORS[idx % COLORS.length]}
                  fillOpacity={0.3}
                />
              ))}
              <Legend />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Comparison Table */}
      <div className="bg-white shadow overflow-hidden rounded-lg border border-slate-200">
        <table className="min-w-full divide-y divide-slate-200">
          <thead className="bg-slate-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Metric</th>
              {runs.map((run, idx) => (
                <th key={run.runId} className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider" style={{ color: COLORS[idx % COLORS.length] }}>
                  {run.subject} <br/>
                  <span className="font-normal text-slate-400">{run.metadata.model}</span>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-slate-200">
            {/* Overall Score Row */}
            <tr className="bg-slate-50 font-bold">
              <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">Overall Score</td>
              {runs.map(run => (
                <td key={run.runId} className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                  {run.overallScore?.toFixed(2)}
                </td>
              ))}
            </tr>
            {/* Category Rows */}
            {Array.from(allCategories).map(catId => (
              <tr key={catId} className="hover:bg-slate-50">
                <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-slate-900">
                  {catId.toUpperCase()}
                </td>
                {runs.map(run => {
                   const cat = run.categories.find(c => c.categoryId === catId);
                   return (
                     <td key={run.runId} className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                       {cat ? cat.score.toFixed(2) : '-'}
                     </td>
                   );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
