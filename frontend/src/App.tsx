import { useState } from 'react';
import { StartupSelector } from './components/StartupSelector';
import { IdeaInput } from './components/IdeaInput';
import { ResultsView } from './components/ResultsView';
import { analyzeStartup } from './api/client';
import type { AnalysisResponse } from './api/client';

function App() {
  const [startupId, setStartupId] = useState<string | null>(null);
  const [analysisData, setAnalysisData] = useState<AnalysisResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSelectStartup = (id: string) => {
    setStartupId(id);
    setAnalysisData(null);
    setError(null);
  };

  const handleAnalyze = async (text: string) => {
    if (!startupId) return;

    setIsLoading(true);
    setError(null);
    try {
      const data = await analyzeStartup(startupId, text);
      setAnalysisData(data);
    } catch (err) {
      console.error(err);
      setError("Failed to analyze. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <header className="mb-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-slate-900">Founder Reality-Check Agent</h1>
          {startupId && (
            <button
              onClick={() => setStartupId(null)}
              className="text-sm text-slate-500 hover:text-slate-700 underline"
            >
              Switch Startup
            </button>
          )}
        </header>

        {!startupId ? (
          <StartupSelector onSelect={handleSelectStartup} />
        ) : (
          <div className="space-y-8">
            <div className="flex items-center justify-between">
              <span className="bg-blue-100 text-blue-800 text-sm font-medium px-3 py-1 rounded">
                Startup ID: {startupId}
              </span>
            </div>

            <IdeaInput onSubmit={handleAnalyze} isLoading={isLoading} />

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
                {error}
              </div>
            )}

            {analysisData && <ResultsView data={analysisData} />}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
