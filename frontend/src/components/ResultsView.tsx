import React from 'react';
import type { AnalysisResponse } from '../api/client';

interface Props {
    data: AnalysisResponse;
}

const SeverityBadge: React.FC<{ severity: string }> = ({ severity }) => {
    const colors = {
        blocker: 'bg-red-100 text-red-800',
        major: 'bg-orange-100 text-orange-800',
        minor: 'bg-yellow-100 text-yellow-800',
        ok: 'bg-green-100 text-green-800',
    };
    return (
        <span className={`px-2 py-1 rounded-full text-xs font-bold uppercase ${colors[severity as keyof typeof colors] || 'bg-gray-100'}`}>
            {severity}
        </span>
    );
};

export const ResultsView: React.FC<Props> = ({ data }) => {
    const { snapshot, dimension_reviews, experiments, drift, status } = data;

    return (
        <div className="space-y-8">
            {/* Header Status */}
            <div className={`p-4 rounded-lg border flex justify-between items-center ${status === 'BLOCKED' ? 'bg-red-50 border-red-200' : 'bg-green-50 border-green-200'}`}>
                <div>
                    <h2 className={`text-xl font-bold ${status === 'BLOCKED' ? 'text-red-700' : 'text-green-700'}`}>
                        Status: {status}
                    </h2>
                    <p className="text-sm text-slate-600">Version {snapshot.version} • {new Date(snapshot.timestamp).toLocaleString()}</p>
                </div>
            </div>

            {/* Drift Section */}
            {drift.length > 0 && (
                <div className="card border-l-4 border-l-purple-500">
                    <h3 className="text-lg font-bold mb-4 text-purple-900">🚨 Detected Drift</h3>
                    <div className="space-y-4">
                        {drift.map((item, idx) => (
                            <div key={idx} className="bg-slate-50 p-3 rounded border">
                                <div className="flex justify-between mb-1">
                                    <span className="font-semibold capitalize">{item.field.replace('_', ' ')}</span>
                                    <span className={`text-xs px-2 py-0.5 rounded ${item.classification === 'major_change' ? 'bg-red-100 text-red-700' : 'bg-blue-100 text-blue-700'}`}>
                                        {item.classification.replace('_', ' ')}
                                    </span>
                                </div>
                                <div className="grid grid-cols-2 gap-4 text-sm">
                                    <div className="text-red-600 line-through opacity-70">{item.before || '(empty)'}</div>
                                    <div className="text-green-600">{item.after}</div>
                                </div>
                                {item.comment && <p className="text-xs text-slate-500 mt-2 italic">{item.comment}</p>}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Dimension Reviews */}
            <div className="grid md:grid-cols-2 gap-6">
                {dimension_reviews.map((review, idx) => (
                    <div key={idx} className="card">
                        <div className="flex justify-between items-start mb-3">
                            <h4 className="font-bold text-lg">{review.dimension}</h4>
                            <SeverityBadge severity={review.severity} />
                        </div>
                        {review.issue && (
                            <div className="mb-3">
                                <p className="text-sm font-semibold text-red-600">Issue:</p>
                                <p className="text-sm text-slate-700">{review.issue}</p>
                            </div>
                        )}
                        {review.recommendation && (
                            <div>
                                <p className="text-sm font-semibold text-blue-600">Recommendation:</p>
                                <p className="text-sm text-slate-700">{review.recommendation}</p>
                            </div>
                        )}
                        {!review.issue && <p className="text-sm text-green-600 italic">No issues detected.</p>}
                    </div>
                ))}
            </div>

            {/* Snapshot Summary */}
            <div className="card bg-slate-50">
                <h3 className="text-lg font-bold mb-4">Current Snapshot</h3>
                <div className="grid md:grid-cols-2 gap-6 text-sm">
                    <div>
                        <p className="font-semibold text-slate-500 uppercase text-xs">Target User</p>
                        <p className="mb-3">{snapshot.target_user || 'N/A'}</p>

                        <p className="font-semibold text-slate-500 uppercase text-xs">Problem</p>
                        <p className="mb-3">{snapshot.problem || 'N/A'}</p>
                    </div>
                    <div>
                        <p className="font-semibold text-slate-500 uppercase text-xs">Hypothesis</p>
                        <p className="mb-3">{snapshot.hypothesis || 'N/A'}</p>

                        <p className="font-semibold text-slate-500 uppercase text-xs">Primary Channel</p>
                        <p className="mb-3">
                            <span className="font-medium">{snapshot.primary_channel_type}</span>: {snapshot.primary_channel_description}
                        </p>
                    </div>
                </div>
            </div>

            {/* Experiments */}
            {experiments.length > 0 && (
                <div>
                    <h3 className="text-xl font-bold mb-4">🧪 Proposed Experiments</h3>
                    <div className="grid gap-4">
                        {experiments.map((exp, idx) => (
                            <div key={idx} className="card border-l-4 border-l-blue-500">
                                <h4 className="font-bold text-lg mb-2">{exp.title}</h4>
                                <div className="flex gap-4 text-sm text-slate-500 mb-4">
                                    <span>⏱ {exp.time_cost}</span>
                                    <span>📢 {exp.channel_type}</span>
                                </div>
                                <div className="mb-3">
                                    <p className="font-semibold text-sm mb-1">Steps:</p>
                                    <ul className="list-disc list-inside text-sm space-y-1 text-slate-700">
                                        {exp.steps.map((step, sIdx) => (
                                            <li key={sIdx}>{step}</li>
                                        ))}
                                    </ul>
                                </div>
                                <div>
                                    <p className="font-semibold text-sm mb-1">Success Criteria:</p>
                                    <p className="text-sm text-slate-700">{exp.success_criteria}</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};
