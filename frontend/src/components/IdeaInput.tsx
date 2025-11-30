import { useState } from 'react';

interface Props {
    onSubmit: (text: string) => void;
    isLoading: boolean;
}

export const IdeaInput: React.FC<Props> = ({ onSubmit, isLoading }) => {
    const [text, setText] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (text.trim()) {
            onSubmit(text);
        }
    };

    return (
        <div className="card mb-8">
            <h3 className="text-lg font-semibold mb-2">Describe your startup idea or update</h3>
            <p className="text-sm text-slate-500 mb-4">
                Be specific about who you are targeting, what problem you solve, and how you plan to grow.
            </p>
            <form onSubmit={handleSubmit}>
                <textarea
                    className="w-full h-32 p-3 border rounded-md border-slate-300 focus:ring-primary focus:border-primary"
                    placeholder="e.g. We are building a CRM for freelance graphic designers..."
                    value={text}
                    onChange={(e) => setText(e.target.value)}
                    disabled={isLoading}
                />
                <div className="mt-4 flex justify-end">
                    <button
                        type="submit"
                        className="btn btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
                        disabled={isLoading || !text.trim()}
                    >
                        {isLoading ? 'Analyzing...' : 'Run Reality Check'}
                    </button>
                </div>
            </form>
        </div>
    );
};
