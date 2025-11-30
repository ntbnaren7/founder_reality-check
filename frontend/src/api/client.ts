import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const apiClient = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

export interface StartupSnapshot {
    startup_id: string;
    version: number;
    timestamp: string;
    problem?: string;
    target_user?: string;
    job_to_be_done?: string;
    solution?: string;
    value_prop?: string;
    primary_channel_type?: string;
    primary_channel_description?: string;
    hypothesis?: string;
    metric?: string;
    timeframe?: string;
    tech_feasibility_notes?: string;
    top_risks?: string[];
    declared_next_steps?: string[];
}

export interface DimensionReview {
    dimension: string;
    severity: "blocker" | "major" | "minor" | "ok";
    issue?: string;
    evidence?: string;
    recommendation?: string;
}

export interface Experiment {
    title: string;
    channel_type: string;
    steps: string[];
    success_criteria: string;
    time_cost: string;
}

export interface DriftItem {
    field: string;
    before?: string;
    after?: string;
    classification: "major_change" | "minor_refinement";
    comment?: string;
}

export interface AnalysisResponse {
    snapshot: StartupSnapshot;
    dimension_reviews: DimensionReview[];
    experiments: Experiment[];
    drift: DriftItem[];
    status: "BLOCKED" | "OK";
}

export const analyzeStartup = async (startupId: string, inputText: string): Promise<AnalysisResponse> => {
    const response = await apiClient.post<AnalysisResponse>(`/startups/${startupId}/analyze`, {
        input_text: inputText,
    });
    return response.data;
};
