import { useEffect, useState } from 'react';
import { fetchRuns } from '../api/client';
import { RunSummary, BenchmarkDomain } from '../api/types';
import { Link } from 'react-router-dom';
import { Search, Filter, GitCompare } from 'lucide-react';
import clsx from 'clsx';

export default function Runs() {
  const [runs, setRuns] = useState<RunSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [filterDomain, setFilterDomain] = useState<BenchmarkDomain | 'ALL'>('ALL');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedRuns, setSelectedRuns] = useState<Set<string>>(new Set());

  useEffect(() => {
    fetchRuns()
      .then(setRuns)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const toggleRunSelection = (runId: string) => {
    const newSelected = new Set(selectedRuns);
    if (newSelected.has(runId)) {
      newSelected.delete(runId);
    } else {
      if (newSelected.size >= 3) {
        alert("You can compare up to 3 runs at a time.");
        return;
      }
      newSelected.add(runId);
    }
    setSelectedRuns(newSelected);
  };

  const filteredRuns = runs.filter(run => {
    const matchesDomain = filterDomain === 'ALL' || run.domain === filterDomain;
    const matchesSearch = run.subject.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          run.runId.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesDomain && matchesSearch;
  });

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-2xl font-bold text-slate-900">Benchmark Runs</h2>
        
        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <div className="relative rounded-md shadow-sm">
            <div className="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3">
              <Search className="h-4 w-4 text-slate-400" />
            </div>
            <input
              type="text"
              className="block w-full rounded-md border-slate-300 pl-10 focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm py-2 border"
              placeholder="Search model or ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex items-center gap-2">
            <Filter className="h-4 w-4 text-slate-500" />
            <select
              className="block w-full rounded-md border-slate-300 py-2 pl-3 pr-10 text-base focus:border-indigo-500 focus:outline-none focus:ring-indigo-500 sm:text-sm border"
              value={filterDomain}
              onChange={(e) => setFilterDomain(e.target.value as any)}
            >
              <option value="ALL">All Domains</option>
              <option value="SMF">SMF (Text)</option>
              <option value="HACS">HACS (Human)</option>
              <option value="VISION">Vision (T2I)</option>
            </select>
          </div>
        </div>
      </div>

      {selectedRuns.size > 0 && (
        <div className="bg-indigo-50 border border-indigo-200 rounded-md p-4 flex items-center justify-between">
           <div className="text-indigo-900 text-sm">
             <span className="font-bold">{selectedRuns.size}</span> runs selected for comparison.
           </div>
           <Link 
             to={`/compare?ids=${Array.from(selectedRuns).join(',')}`}
             className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
           >
             <GitCompare className="mr-2 h-4 w-4" />
             Compare Selected
           </Link>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12 text-slate-500">Loading runs...</div>
      ) : (
        <div className="bg-white shadow overflow-hidden rounded-lg border border-slate-200">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider w-10">
                  Select
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Run ID</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Subject / Model</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Domain</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Score</th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider">Date</th>
                <th className="px-6 py-3 text-right text-xs font-medium text-slate-500 uppercase tracking-wider">Action</th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {filteredRuns.map((run) => (
                <tr key={run.runId} className="hover:bg-slate-50">
                  <td className="px-6 py-4 whitespace-nowrap">
                    <input
                      type="checkbox"
                      className="h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-slate-300 rounded"
                      checked={selectedRuns.has(run.runId)}
                      onChange={() => toggleRunSelection(run.runId)}
                    />
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-indigo-600 font-mono">
                    {run.runId.substring(0, 16)}...
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900">
                    {run.subject}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm">
                    <span className={clsx(
                      "px-2 inline-flex text-xs leading-5 font-semibold rounded-full",
                      run.domain === 'SMF' && "bg-blue-100 text-blue-800",
                      run.domain === 'HACS' && "bg-purple-100 text-purple-800",
                      run.domain === 'VISION' && "bg-pink-100 text-pink-800"
                    )}>
                      {run.domain}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-900 font-bold">
                    {run.overallScore?.toFixed(2) ?? "N/A"}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                    {new Date(run.metadata.timestamp).toLocaleDateString()}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <Link to={`/runs/${run.runId}`} className="text-indigo-600 hover:text-indigo-900">
                      View
                    </Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredRuns.length === 0 && (
             <div className="text-center py-12 text-slate-500">No runs found matching your filters.</div>
          )}
        </div>
      )}
    </div>
  );
}
