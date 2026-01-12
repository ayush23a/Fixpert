import * as vscode from 'vscode';
import { ApiClient } from './apiClient';
import { AnalysisPanel } from './panels/AnalysisPanel';

export function activate(context: vscode.ExtensionContext) {
    console.log('Extension "error-explainer" is now active!');

    const apiClient = new ApiClient();

    let disposable = vscode.commands.registerCommand('errorExplainer.analyzeError', async () => {
        let text = '';

        const editor = vscode.window.activeTextEditor;
        if (editor && !editor.selection.isEmpty) {
            text = editor.document.getText(editor.selection);
        } else {
            // Fallback: Try to get text from the terminal selection (via clipboard hack)
            await vscode.commands.executeCommand('workbench.action.terminal.copySelection');
            text = await vscode.env.clipboard.readText();
        }

        if (!text || text.trim().length === 0) {
            vscode.window.showWarningMessage('Please select the error text you want to analyze.');
            return;
        }

        vscode.window.withProgress({
            location: vscode.ProgressLocation.Notification,
            title: "Analyzing Error...",
            cancellable: false
        }, async (progress) => {
            try {
                const languageId = editor?.document.languageId;
                const analysis = await apiClient.analyzeError(text, languageId);
                AnalysisPanel.createOrShow(context.extensionUri, analysis);
            } catch (error: any) {
                vscode.window.showErrorMessage(`Analysis failed: ${error.message}`);
            }
        });
    });

    context.subscriptions.push(disposable);
}

export function deactivate() { }
