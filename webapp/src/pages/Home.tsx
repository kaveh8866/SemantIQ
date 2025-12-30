import { ArrowRight, Activity, Users, Eye } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div className="space-y-12">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-extrabold text-slate-900 tracking-tight">
          Unified Multimodal Benchmarking
        </h1>
        <p className="text-lg text-slate-600 max-w-2xl mx-auto">
          Explore and analyze performance across Text (SMF), Human-AI (HACS), and Vision (T2I) domains.
          Transparent, reproducible, and research-focused.
        </p>
        <div className="pt-4">
          <Link
            to="/runs"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700"
          >
            View Benchmark Runs
            <ArrowRight className="ml-2 w-5 h-5" />
          </Link>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <DomainCard
          title="SMF (Text)"
          description="Semantic Alignment & Safety benchmarks for Large Language Models."
          icon={Activity}
          color="bg-blue-50 text-blue-700"
        />
        <DomainCard
          title="HACS (Human-AI)"
          description="Human-in-the-loop evaluation for collaboration and interaction quality."
          icon={Users}
          color="bg-purple-50 text-purple-700"
        />
        <DomainCard
          title="Vision (T2I)"
          description="Deterministic rendering and semantic scoring for Text-to-Image models."
          icon={Eye}
          color="bg-pink-50 text-pink-700"
        />
      </div>

      <div className="bg-amber-50 border border-amber-200 rounded-lg p-6 text-sm text-amber-800">
        <h3 className="font-semibold mb-2">Research Disclaimer</h3>
        <p>
          This platform provides evaluation metrics based on specific, predefined benchmarks. 
          High scores indicate adherence to these specific tests, not general intelligence or consciousness. 
          We do not endorse "leaderboards" or competitive rankings without context.
        </p>
      </div>
    </div>
  );
}

function DomainCard({ title, description, icon: Icon, color }: any) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg border border-slate-100 p-6 hover:shadow-md transition-shadow">
      <div className={`inline-flex items-center justify-center p-3 rounded-lg ${color} mb-4`}>
        <Icon className="w-6 h-6" />
      </div>
      <h3 className="text-lg font-medium text-slate-900">{title}</h3>
      <p className="mt-2 text-slate-500">{description}</p>
    </div>
  );
}
