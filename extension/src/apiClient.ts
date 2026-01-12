import axios from 'axios';
import * as vscode from 'vscode';

export interface ErrorAnalysisResponse {
    summary: string;
    category: string;
    root_causes: { cause: string; confidence: number }[];
    suggested_steps: string[];
    uncertainty_statement?: string | null;
}

export class ApiClient {
    private backendUrl: string;

    constructor() {
        // Read configuration
        const config = vscode.workspace.getConfiguration('errorExplainer');
        this.backendUrl = config.get<string>('backendUrl') || 'http://127.0.0.1:8000';
    }

    public async analyzeError(rawError: string, language?: string): Promise<ErrorAnalysisResponse> {
        const config = vscode.workspace.getConfiguration('errorExplainer');
        const enableHistory = config.get<boolean>('enableHistory') || false;

        try {
            const response = await axios.post(`${this.backendUrl}/analyze`, {
                raw_error: rawError,
                language: language,
                save_analysis: enableHistory
            });
            return response.data;
        } catch (error: any) {
            console.error(error);
            throw new Error(`Failed to analyze error: ${error.message || 'Unknown error'}`);
        }
    }

    public async getHistory(): Promise<any[]> {
        try {
            const response = await axios.get(`${this.backendUrl}/history`);
            return response.data;
        } catch (error: any) {
            console.error(error);
            throw new Error(`Failed to fetch history: ${error.message}`);
        }
    }

    public async clearHistory(): Promise<void> {
        try {
            await axios.delete(`${this.backendUrl}/history`);
        } catch (error: any) {
            console.error(error);
            throw new Error(`Failed to clear history: ${error.message}`);
        }
    }
}

