import * as vscode from 'vscode';
import { ErrorAnalysisResponse } from '../apiClient';

export class AnalysisPanel {
    public static currentPanel: AnalysisPanel | undefined;
    private readonly _panel: vscode.WebviewPanel;
    private _disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel, extensionUri: vscode.Uri) {
        this._panel = panel;
        this._panel.onDidDispose(() => this.dispose(), null, this._disposables);
    }

    public static createOrShow(extensionUri: vscode.Uri, analysis: ErrorAnalysisResponse) {
        const column = vscode.window.activeTextEditor
            ? vscode.window.activeTextEditor.viewColumn
            : undefined;

        // If we already have a panel, show it.
        if (AnalysisPanel.currentPanel) {
            AnalysisPanel.currentPanel._panel.reveal(column);
            AnalysisPanel.currentPanel._update(analysis);
            return;
        }

        // Otherwise, create a new panel.
        const panel = vscode.window.createWebviewPanel(
            'errorExplainer',
            'AI Error Explanation',
            column || vscode.ViewColumn.One,
            {
                enableScripts: true,
                localResourceRoots: [vscode.Uri.joinPath(extensionUri, 'media')]
            }
        );

        AnalysisPanel.currentPanel = new AnalysisPanel(panel, extensionUri);
        AnalysisPanel.currentPanel._update(analysis);
    }

    private _update(analysis: ErrorAnalysisResponse) {
        this._panel.webview.html = this._getHtmlForWebview(analysis);
    }

    public dispose() {
        AnalysisPanel.currentPanel = undefined;
        this._panel.dispose();
        while (this._disposables.length) {
            const x = this._disposables.pop();
            if (x) {
                x.dispose();
            }
        }
    }

    private _getHtmlForWebview(analysis: ErrorAnalysisResponse) {
        const causesHtml = analysis.root_causes.map(rc =>
            `<div class="card cause">
                <div class="header">
                    <strong>${rc.cause}</strong>
                    <span class="confidence">${(rc.confidence * 100).toFixed(0)}% Confidence</span>
                </div>
            </div>`
        ).join('');

        const stepsHtml = analysis.suggested_steps.map(step =>
            `<li>${step}</li>`
        ).join('');

        return `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Error Analysis</title>
            <style>
                body { font-family: sans-serif; padding: 20px; color: var(--vscode-editor-foreground); background-color: var(--vscode-editor-background); }
                h1 { font-size: 1.5rem; border-bottom: 1px solid var(--vscode-panel-border); padding-bottom: 10px; }
                h2 { font-size: 1.2rem; margin-top: 20px; }
                .summary { font-size: 1.1rem; margin-bottom: 20px; padding: 10px; background-color: var(--vscode-textBlockQuote-background); border-left: 4px solid var(--vscode-textBlockQuote-border); }
                .card { background-color: var(--vscode-editorClient-activeBackground); padding: 10px; margin-bottom: 5px; border-radius: 4px; }
                .confidence { float: right; font-size: 0.8rem; opacity: 0.8; }
                ul { padding-left: 20px; }
                li { margin-bottom: 5px; }
                .badge { display: inline-block; padding: 2px 6px; border-radius: 4px; background-color: var(--vscode-badge-background); color: var(--vscode-badge-foreground); font-size: 0.8rem; }
            </style>
        </head>
        <body>
            <h1>Error Analysis</h1>
            <div>
                <span class="badge">${analysis.category}</span>
            </div>
            
            <div class="summary">
                ${analysis.summary}
            </div>

            <h2>Root Cause Hypotheses</h2>
            ${causesHtml}

            <h2>Suggested Fixes</h2>
            <ul>
                ${stepsHtml}
            </ul>

            ${analysis.uncertainty_statement ? `<p><em>Note: ${analysis.uncertainty_statement}</em></p>` : ''}
        </body>
        </html>`;
    }
}
