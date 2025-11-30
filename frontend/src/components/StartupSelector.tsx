import { useState } from 'react';

interface Props {
    onSelect: (startupId: string) => void;
}

export const StartupSelector: React.FC<Props> = ({ onSelect }) => {
    const [startupId, setStartupId] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (startupId.trim()) {
            onSelect(startupId.trim());
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-[50vh]">
            <div className="card w-full max-w-md">
                <h2 className="text-2xl font-bold mb-4 text-center">Founder Reality-Check</h2>
                <p className="text-slate-500 mb-6 text-center">Enter a Startup ID to begin or resume a session.</p>
                <form onSubmit={handleSubmit} className="space-y-4">
                    <div>
                        <label htmlFor="startupId" className="block text-sm font-medium text-slate-700">Startup ID</label>
                        <input
                            type="text"
                            id="startupId"
                            className="mt-1 block w-full rounded-md border-slate-300 shadow-sm focus:border-primary focus:ring-primary sm:text-sm p-2 border"
                            placeholder="e.g. my-awesome-saas"
                            value={startupId}
                            onChange={(e) => setStartupId(e.target.value)}
                            required
                        />
                    </div>
                    <button type="submit" className="btn btn-primary w-full">
                        Start Session
                    </button>
                </form>
            </div>
        </div>
    );
};
