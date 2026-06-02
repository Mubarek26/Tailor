import http.server
import socketserver
import os
import urllib.parse

PORT = 8081

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailor Shop - Payment Terminal</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #07080e;
            --bg-surface: rgba(16, 18, 35, 0.65);
            --bg-card: rgba(22, 25, 49, 0.5);
            --border-color: rgba(255, 255, 255, 0.08);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --primary: #6366f1;
            --primary-glow: rgba(99, 102, 241, 0.15);
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.1);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.1);
            --danger: #ef4444;
            --danger-bg: rgba(239, 68, 68, 0.1);
            --font-main: 'Outfit', sans-serif;
            --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.5);
            --shadow-glow: 0 0 30px rgba(99, 102, 241, 0.2);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-main);
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.12) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(239, 68, 68, 0.05) 0px, transparent 50%),
                radial-gradient(at 50% 0%, rgba(16, 185, 129, 0.03) 0px, transparent 50%);
            background-attachment: fixed;
            color: var(--text-primary);
            min-height: 100vh;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
        }

        /* Scrollbars */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
        }
        ::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.15);
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.25);
        }

        /* Header Bar */
        header {
            background: rgba(10, 11, 20, 0.6);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-b: 1px solid var(--border-color);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo-container {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .logo-icon {
            background: var(--primary-gradient);
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 0.75rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
        }

        .logo-icon svg {
            width: 1.25rem;
            height: 1.25rem;
            stroke: white;
            fill: none;
        }

        .logo-text {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #ffffff, #94a3b8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .terminal-badge {
            background: rgba(99, 102, 241, 0.15);
            border: 1px solid rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
        }

        .user-menu {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .api-status {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.8rem;
            font-weight: 500;
            color: var(--text-secondary);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--success);
            box-shadow: 0 0 10px var(--success);
        }

        .status-dot.disconnected {
            background-color: var(--danger);
            box-shadow: 0 0 10px var(--danger);
        }

        .btn-logout {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.5rem 1rem;
            border-radius: 0.75rem;
            font-size: 0.85rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-logout:hover {
            background: rgba(239, 68, 68, 0.1);
            color: var(--danger);
            border-color: rgba(239, 68, 68, 0.2);
        }

        /* Layout Grid */
        .container {
            max-width: 1600px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 1fr;
            gap: 2rem;
            flex-grow: 1;
        }

        @media (min-width: 1024px) {
            .container {
                grid-template-columns: 1.8fr 1.2fr;
            }
        }

        /* Left Side: Summary and Table */
        .main-content {
            display: flex;
            flex-direction: column;
            gap: 2rem;
        }

        /* Summary Cards */
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(1, 1fr);
            gap: 1rem;
        }

        @media (min-width: 640px) {
            .summary-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }

        .summary-card {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 1.25rem;
            padding: 1.25rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            position: relative;
            overflow: hidden;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }

        .summary-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: transparent;
        }

        .summary-card.revenue::before {
            background: linear-gradient(90deg, #6366f1, #a855f7);
        }

        .summary-card.deposits::before {
            background: linear-gradient(90deg, #10b981, #3b82f6);
        }

        .summary-card.outstanding::before {
            background: linear-gradient(90deg, #f59e0b, #ef4444);
        }

        .summary-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }

        .summary-value {
            font-size: 1.75rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: var(--text-primary);
        }

        .summary-value.outstanding-value {
            color: #fca5a5;
        }

        /* Dashboard Panel */
        .panel {
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 1.5rem;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            box-shadow: var(--shadow-lg);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .panel-header {
            padding: 1.5rem;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }

        @media (min-width: 640px) {
            .panel-header {
                flex-direction: row;
                justify-content: space-between;
                align-items: center;
            }
        }

        .panel-title-container {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .panel-title {
            font-size: 1.25rem;
            font-weight: 800;
            letter-spacing: -0.015em;
        }

        .panel-subtitle {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        /* Search and Filters */
        .controls-row {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            width: 100%;
        }

        @media (min-width: 640px) {
            .controls-row {
                width: auto;
                max-width: 320px;
            }
        }

        .search-wrapper {
            position: relative;
            flex-grow: 1;
            display: flex;
            align-items: center;
        }

        .search-input {
            width: 100%;
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.6rem 1rem 0.6rem 2.25rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-family: var(--font-main);
            transition: all 0.2s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .search-icon {
            position: absolute;
            left: 0.75rem;
            color: var(--text-muted);
            pointer-events: none;
        }

        .search-icon svg {
            width: 1rem;
            height: 1rem;
            stroke: currentColor;
            fill: none;
        }

        /* Orders Table */
        .table-container {
            overflow-x: auto;
            flex-grow: 1;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 0.9rem;
        }

        th {
            background: rgba(0, 0, 0, 0.1);
            color: var(--text-secondary);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }

        td {
            padding: 1rem 1.5rem;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
            vertical-align: middle;
        }

        tr:last-child td {
            border-bottom: none;
        }

        tr.table-row {
            cursor: pointer;
            transition: background-color 0.15s ease;
        }

        tr.table-row:hover {
            background-color: rgba(255, 255, 255, 0.02);
        }

        tr.table-row.selected {
            background-color: rgba(99, 102, 241, 0.08);
        }

        .order-code {
            font-family: monospace;
            font-size: 0.95rem;
            font-weight: 800;
            color: var(--primary);
        }

        .customer-name {
            font-weight: 600;
        }

        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.2rem 0.6rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }

        .status-badge.pending {
            background-color: var(--warning-bg);
            color: var(--warning);
            border: 1px solid rgba(245, 158, 11, 0.2);
        }

        .status-badge.in_progress {
            background-color: rgba(59, 130, 246, 0.1);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .status-badge.completed {
            background-color: var(--success-bg);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: currentColor;
        }

        .remaining-amount {
            font-weight: 700;
        }

        .remaining-amount.has-balance {
            color: #ef4444;
        }

        .remaining-amount.no-balance {
            color: var(--success);
        }

        .btn-manage {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.35rem 0.75rem;
            border-radius: 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-manage:hover {
            background: var(--primary-gradient);
            border-color: transparent;
            box-shadow: 0 4px 10px rgba(99, 102, 241, 0.2);
        }

        tr.selected .btn-manage {
            background: var(--primary-gradient);
            border-color: transparent;
        }

        /* Pagination */
        .pagination-container {
            padding: 1.25rem 1.5rem;
            border-top: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: rgba(0, 0, 0, 0.05);
        }

        .pagination-text {
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        .pagination-actions {
            display: flex;
            gap: 0.5rem;
        }

        .btn-page {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.4rem 0.8rem;
            border-radius: 0.5rem;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .btn-page:hover:not(:disabled) {
            background: rgba(255, 255, 255, 0.1);
        }

        .btn-page:disabled {
            opacity: 0.4;
            cursor: not-allowed;
        }

        /* Right Side: Sidebar */
        .sidebar {
            display: flex;
            flex-direction: column;
            height: fit-content;
            position: sticky;
            top: 5.5rem;
        }

        .sidebar-placeholder {
            padding: 4rem 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            gap: 1.5rem;
            color: var(--text-secondary);
        }

        .placeholder-icon {
            width: 4rem;
            height: 4rem;
            background: rgba(99, 102, 241, 0.08);
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-radius: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            box-shadow: var(--shadow-glow);
        }

        .placeholder-icon svg {
            width: 2rem;
            height: 2rem;
            stroke: currentColor;
            fill: none;
        }

        .placeholder-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: var(--text-primary);
        }

        .placeholder-text {
            font-size: 0.85rem;
            max-width: 260px;
            line-height: 1.5;
        }

        /* Sidebar Content Loaded */
        .sidebar-content {
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .sidebar-section-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.5rem;
            margin-bottom: 0.75rem;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        .meta-item {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .meta-label {
            font-size: 0.7rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.02em;
            color: var(--text-muted);
        }

        .meta-value {
            font-size: 0.9rem;
            font-weight: 600;
        }

        /* Ledger / Financial Overview Box */
        .ledger-box {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            padding: 1rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .ledger-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85rem;
        }

        .ledger-row.total {
            border-top: 1px dashed var(--border-color);
            padding-top: 0.75rem;
            margin-top: 0.25rem;
        }

        .ledger-row.remaining {
            background: rgba(239, 68, 68, 0.06);
            border: 1px solid rgba(239, 68, 68, 0.15);
            padding: 0.6rem 0.8rem;
            border-radius: 0.75rem;
            margin-top: 0.25rem;
        }

        .ledger-row.remaining.cleared {
            background: rgba(16, 185, 129, 0.06);
            border: 1px solid rgba(16, 185, 129, 0.15);
        }

        .ledger-label {
            color: var(--text-secondary);
        }

        .ledger-row.total .ledger-label {
            font-weight: 700;
            color: var(--text-primary);
        }

        .ledger-row.remaining .ledger-label {
            font-weight: 700;
            color: #fca5a5;
        }

        .ledger-row.remaining.cleared .ledger-label {
            color: #a7f3d0;
        }

        .ledger-val {
            font-weight: 700;
        }

        .ledger-row.total .ledger-val {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--primary);
        }

        .ledger-row.remaining .ledger-val {
            font-size: 1.1rem;
            font-weight: 900;
            color: #ef4444;
        }

        .ledger-row.remaining.cleared .ledger-val {
            color: var(--success);
        }

        /* Transaction History */
        .history-list {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 150px;
            overflow-y: auto;
            padding-right: 0.25rem;
        }

        .history-item {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--border-color);
            border-radius: 0.75rem;
            padding: 0.6rem 0.8rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
        }

        .history-info {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .history-type {
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.65rem;
            letter-spacing: 0.05em;
        }

        .history-type.deposit {
            color: #60a5fa;
        }

        .history-type.full {
            color: #a7f3d0;
        }

        .history-date {
            color: var(--text-muted);
            font-size: 0.7rem;
        }

        .history-amount {
            font-weight: 700;
            color: var(--text-primary);
        }

        .no-history {
            text-align: center;
            padding: 1.5rem;
            border: 1px dashed var(--border-color);
            border-radius: 0.75rem;
            font-size: 0.8rem;
            color: var(--text-muted);
            font-style: italic;
        }

        /* Payment Form */
        .payment-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            background: rgba(99, 102, 241, 0.03);
            border: 1px solid rgba(99, 102, 241, 0.15);
            border-radius: 1.25rem;
            padding: 1.25rem;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 0.4rem;
        }

        .form-label {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }

        .input-amount-wrapper {
            position: relative;
            display: flex;
            align-items: center;
        }

        .currency-prefix {
            position: absolute;
            left: 1rem;
            font-weight: 700;
            font-size: 0.9rem;
            color: var(--text-muted);
            pointer-events: none;
        }

        .input-amount {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1rem 0.75rem 3rem;
            border-radius: 0.75rem;
            font-size: 1.1rem;
            font-weight: 700;
            font-family: var(--font-main);
            transition: all 0.2s ease;
        }

        .input-amount:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .select-type {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-weight: 600;
            font-family: var(--font-main);
            appearance: none;
            -webkit-appearance: none;
            background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1.25rem;
            cursor: pointer;
            transition: all 0.2s ease;
        }

        .select-type:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .select-type option {
            background-color: #121424;
            color: var(--text-primary);
        }

        .btn-submit {
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 0.85rem;
            border-radius: 0.75rem;
            font-size: 0.95rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
        }

        .btn-submit:hover:not(:disabled) {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(99, 102, 241, 0.4);
        }

        .btn-submit:active:not(:disabled) {
            transform: translateY(0);
        }

        .btn-submit:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            box-shadow: none;
        }

        .spinner {
            animation: spin 1s linear infinite;
            width: 1.2rem;
            height: 1.2rem;
            display: none;
        }

        .spinner circle {
            stroke: currentColor;
            stroke-width: 4;
            fill: none;
            stroke-dasharray: 42;
            stroke-dashoffset: 14;
        }

        @keyframes spin {
            100% { transform: rotate(360deg); }
        }

        /* Login Modal overlay */
        .modal-overlay {
            position: fixed;
            inset: 0;
            background: rgba(4, 5, 10, 0.8);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
        }

        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }

        .modal {
            background: rgba(20, 22, 42, 0.9);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 2rem;
            width: 90%;
            max-width: 440px;
            padding: 2.5rem;
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), var(--shadow-glow);
            transform: scale(0.95);
            transition: transform 0.3s ease;
        }

        .modal-overlay.active .modal {
            transform: scale(1);
        }

        .modal-header {
            text-align: center;
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.75rem;
        }

        .modal-logo {
            width: 3.5rem;
            height: 3.5rem;
            background: var(--primary-gradient);
            border-radius: 1.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 8px 20px rgba(99, 102, 241, 0.3);
        }

        .modal-logo svg {
            width: 1.75rem;
            height: 1.75rem;
            stroke: white;
            fill: none;
        }

        .modal-title {
            font-size: 1.75rem;
            font-weight: 900;
            letter-spacing: -0.025em;
        }

        .modal-subtitle {
            font-size: 0.9rem;
            color: var(--text-secondary);
            max-width: 280px;
        }

        .modal-form {
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .input-field {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.85rem 1.2rem;
            border-radius: 0.85rem;
            font-size: 0.95rem;
            font-family: var(--font-main);
            transition: all 0.2s ease;
        }

        .input-field:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .btn-login {
            background: var(--primary-gradient);
            border: none;
            color: white;
            padding: 0.9rem;
            border-radius: 0.85rem;
            font-size: 1rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-login:hover {
            opacity: 0.95;
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.45);
        }

        /* Toast Container */
        #toast-container {
            position: fixed;
            top: 2rem;
            right: 2rem;
            z-index: 9999;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
            pointer-events: none;
        }

        .toast {
            background: rgba(18, 20, 38, 0.9);
            border: 1px solid var(--border-color);
            border-radius: 1rem;
            padding: 1rem 1.5rem;
            color: var(--text-primary);
            font-size: 0.9rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            transform: translateX(120%);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            pointer-events: auto;
            backdrop-filter: blur(12px);
        }

        .toast.show {
            transform: translateX(0);
        }

        .toast-icon {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 1.5rem;
            height: 1.5rem;
            border-radius: 50%;
        }

        .toast.success {
            border-left: 4px solid var(--success);
        }

        .toast.success .toast-icon {
            background-color: var(--success-bg);
            color: var(--success);
        }

        .toast.error {
            border-left: 4px solid var(--danger);
        }

        .toast.error .toast-icon {
            background-color: var(--danger-bg);
            color: var(--danger);
        }

        /* Loading Shimmers */
        .loading-shimmer {
            background: linear-gradient(
                90deg,
                rgba(255, 255, 255, 0.03) 25%,
                rgba(255, 255, 255, 0.08) 50%,
                rgba(255, 255, 255, 0.03) 75%
            );
            background-size: 200% 100%;
            animation: shimmer 1.5s infinite;
        }

        @keyframes shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }

        /* Empty state styles */
        .empty-table {
            text-align: center;
            padding: 3rem;
            color: var(--text-secondary);
        }

        .empty-table svg {
            width: 2.5rem;
            height: 2.5rem;
            margin-bottom: 1rem;
            stroke: var(--text-muted);
            fill: none;
        }
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="logo-container">
            <div class="logo-icon">
                <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <circle cx="6" cy="6" r="3"></circle>
                    <circle cx="6" cy="18" r="3"></circle>
                    <line x1="20" y1="4" x2="8.12" y2="15.88"></line>
                    <line x1="14.47" y1="14.48" x2="20" y2="20"></line>
                    <line x1="8.12" y1="8.12" x2="12" y2="12"></line>
                </svg>
            </div>
            <span class="logo-text">Tailor Pro</span>
            <span class="terminal-badge">Payment Gateway</span>
        </div>
        <div class="user-menu">
            <div class="api-status">
                <div class="status-dot" id="status-dot"></div>
                <span id="status-text">Connecting...</span>
            </div>
            <button class="btn-logout" id="logout-btn">Sign Out</button>
        </div>
    </header>

    <!-- Main Workspace Container -->
    <main class="container">
        
        <!-- Left Side Dashboard -->
        <div class="main-content">
            
            <!-- Summary stats row -->
            <div class="summary-grid">
                <div class="summary-card revenue">
                    <span class="summary-label">Total Revenue</span>
                    <span class="summary-value" id="stat-revenue">ETB 0</span>
                </div>
                <div class="summary-card deposits">
                    <span class="summary-label">Total Deposits</span>
                    <span class="summary-value" id="stat-deposits">ETB 0</span>
                </div>
                <div class="summary-card outstanding">
                    <span class="summary-label">Outstanding Balance</span>
                    <span class="summary-value outstanding-value" id="stat-outstanding">ETB 0</span>
                </div>
            </div>

            <!-- Orders Table Panel -->
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title-container">
                        <h2 class="panel-title">Order Ledger</h2>
                        <span class="panel-subtitle">Select an order from the directory to review transactions</span>
                    </div>
                    <div class="controls-row">
                        <div class="search-wrapper">
                            <span class="search-icon">
                                <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                            </span>
                            <input type="text" class="search-input" id="search-bar" placeholder="Filter by Name or Unique Code...">
                        </div>
                    </div>
                </div>

                <div class="table-container">
                    <table id="orders-table">
                        <thead>
                            <tr>
                                <th>Code</th>
                                <th>Customer</th>
                                <th>Total</th>
                                <th>Deposit</th>
                                <th>Outstanding</th>
                                <th>Status</th>
                                <th style="text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">
                            <!-- Table rows will be populated dynamically -->
                            <tr>
                                <td colspan="7" class="empty-table loading-shimmer" style="height: 15rem;"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Table Pagination -->
                <div class="pagination-container">
                    <span class="pagination-text" id="pagination-info">Showing Page -- of --</span>
                    <div class="pagination-actions">
                        <button class="btn-page" id="prev-page-btn" disabled>Previous</button>
                        <button class="btn-page" id="next-page-btn" disabled>Next</button>
                    </div>
                </div>
            </div>

        </div>

        <!-- Right Side: Sidebar Panel -->
        <div class="panel sidebar" id="payments-sidebar">
            <div class="sidebar-placeholder" id="sidebar-placeholder">
                <div class="placeholder-icon">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <rect x="2" y="4" width="20" height="16" rx="2"></rect>
                        <line x1="12" y1="10" x2="12" y2="10"></line>
                        <line x1="2" y1="10" x2="22" y2="10"></line>
                    </svg>
                </div>
                <h3 class="placeholder-title">Select Order Reference</h3>
                <p class="placeholder-text">Click on any order row or select "Manage" to load its transaction history ledger and record payments.</p>
            </div>

            <div class="sidebar-content" id="sidebar-content" style="display: none;">
                <div>
                    <h3 class="panel-title" id="side-order-title" style="margin-bottom: 0.25rem;">Order Details</h3>
                    <span class="panel-subtitle" id="side-order-subtitle">Transaction audit and payment registry</span>
                </div>

                <!-- Customer Details Meta -->
                <div>
                    <h4 class="sidebar-section-title">Customer details</h4>
                    <div class="meta-grid">
                        <div class="meta-item">
                            <span class="meta-label">Full Name</span>
                            <span class="meta-value" id="side-cust-name">--</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Phone Number</span>
                            <span class="meta-value" id="side-cust-phone">--</span>
                        </div>
                    </div>
                </div>

                <!-- Financial Balance Ledger -->
                <div>
                    <h4 class="sidebar-section-title">Ledger Balance</h4>
                    <div class="ledger-box">
                        <div class="ledger-row">
                            <span class="ledger-label">Total Price</span>
                            <span class="ledger-val" id="side-ledger-total">ETB 0</span>
                        </div>
                        <div class="ledger-row">
                            <span class="ledger-label">Total Paid (Deposit)</span>
                            <span class="ledger-val" id="side-ledger-paid" style="color: #60a5fa;">ETB 0</span>
                        </div>
                        <div class="ledger-row remaining" id="side-ledger-remaining-row">
                            <span class="ledger-label" id="side-ledger-remaining-label">Outstanding Balance</span>
                            <span class="ledger-val" id="side-ledger-remaining">ETB 0</span>
                        </div>
                    </div>
                </div>

                <!-- Payments Ledger History -->
                <div>
                    <h4 class="sidebar-section-title">Payment History</h4>
                    <div class="history-list" id="side-payment-history">
                        <!-- Loaded transactions list -->
                    </div>
                </div>

                <!-- Record Payment Form Box -->
                <div>
                    <h4 class="sidebar-section-title">Register Payment</h4>
                    <form class="payment-form" id="register-payment-form" onsubmit="handlePaymentSubmit(event)">
                        <div class="form-group">
                            <label class="form-label" for="amount-input">Amount (ETB)</label>
                            <div class="input-amount-wrapper">
                                <span class="currency-prefix">ETB</span>
                                <input type="number" id="amount-input" class="input-amount" step="0.01" min="0.01" required placeholder="0.00">
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="payment-type-select">Payment Type</label>
                            <select id="payment-type-select" class="select-type" required>
                                <option value="deposit">Deposit / Partial Payment</option>
                                <option value="full">Full / Remaining Payment</option>
                            </select>
                        </div>

                        <button type="submit" class="btn-submit" id="submit-payment-btn">
                            <svg class="spinner" viewBox="0 0 50 50" id="form-spinner">
                                <circle cx="25" cy="25" r="20" stroke="currentColor" fill="none"></circle>
                            </svg>
                            <span id="submit-btn-text">Record Payment</span>
                        </button>
                    </form>
                </div>
            </div>
        </div>

    </main>

    <!-- Authentication Overlay Modal -->
    <div class="modal-overlay" id="auth-modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <div class="modal-logo">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <circle cx="6" cy="6" r="3"></circle>
                        <circle cx="6" cy="18" r="3"></circle>
                        <line x1="20" y1="4" x2="8.12" y2="15.88"></line>
                        <line x1="14.47" y1="14.48" x2="20" y2="20"></line>
                        <line x1="8.12" y1="8.12" x2="12" y2="12"></line>
                    </svg>
                </div>
                <h2 class="modal-title">Terminal Access</h2>
                <p class="modal-subtitle">Authenticate with your shop credentials to open the payment registry dashboard</p>
            </div>
            
            <form class="modal-form" onsubmit="handleLoginSubmit(event)">
                <input type="text" id="login-identifier" class="input-field" placeholder="Email or Phone Number" required autocomplete="username">
                <input type="password" id="login-password" class="input-field" placeholder="Access Password" required autocomplete="current-password">
                <button type="submit" class="btn-login" id="login-btn-submit">
                    <svg class="spinner" viewBox="0 0 50 50" id="login-spinner">
                        <circle cx="25" cy="25" r="20" stroke="currentColor" fill="none"></circle>
                    </svg>
                    <span id="login-btn-text">Sign In & Connect</span>
                </button>
            </form>
        </div>
    </div>

    <!-- Toast Notifications Area -->
    <div id="toast-container"></div>

    <!-- Page Logic & API Client integration -->
    <script>
        const API_BASE = "http://localhost:5000/api";
        const TOKEN_KEY = "tsms_token";
        
        let currentPage = 1;
        let selectedOrderId = null;
        let allOrders = [];
        let totalPagesCount = 1;
        let activeSearchQuery = "";

        // Toast Helper
        function showToast(message, type = "success") {
            const container = document.getElementById("toast-container");
            const toast = document.createElement("div");
            toast.className = `toast ${type}`;
            
            const icon = type === "success" 
                ? `<div class="toast-icon">✓</div>` 
                : `<div class="toast-icon">✗</div>`;
                
            toast.innerHTML = `
                ${icon}
                <span>${message}</span>
            `;
            
            container.appendChild(toast);
            
            // Trigger animation
            setTimeout(() => toast.classList.add("show"), 10);
            
            // Auto dismiss
            setTimeout(() => {
                toast.classList.remove("show");
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        // Token Management
        function getToken() {
            return localStorage.getItem(TOKEN_KEY);
        }

        function setToken(token) {
            localStorage.setItem(TOKEN_KEY, token);
        }

        function clearToken() {
            localStorage.removeItem(TOKEN_KEY);
            selectedOrderId = null;
            document.getElementById("sidebar-content").style.display = "none";
            document.getElementById("sidebar-placeholder").style.display = "flex";
        }

        // Authenticated API request wrapper
        async function fetchAPI(endpoint, options = {}) {
            const token = getToken();
            const headers = {
                "Content-Type": "application/json",
                ...options.headers
            };
            
            if (token) {
                headers["Authorization"] = `Bearer ${token}`;
            }

            try {
                const response = await fetch(`${API_BASE}${endpoint}`, {
                    ...options,
                    headers
                });

                if (response.status === 401) {
                    clearToken();
                    updateStatusDisplay(false, "Session Expired");
                    showAuthModal();
                    throw new Error("Unauthorized - JWT token expired or invalid");
                }

                if (!response.ok) {
                    const errorDetails = await response.json().catch(() => ({}));
                    throw new Error(errorDetails.message || `API error - status: ${response.status}`);
                }

                updateStatusDisplay(true, "Connected");
                return await response.json();
            } catch (err) {
                console.error("API Call failure:", err);
                if (err.message.includes("Failed to fetch") || err.message.includes("NetworkError")) {
                    updateStatusDisplay(false, "Server Offline");
                    showToast("Cannot connect to backend API server. Verify it is running.", "error");
                }
                throw err;
            }
        }

        // Update top status indicator
        function updateStatusDisplay(connected, text) {
            const dot = document.getElementById("status-dot");
            const label = document.getElementById("status-text");
            if (connected) {
                dot.classList.remove("disconnected");
                label.textContent = text;
            } else {
                dot.classList.add("disconnected");
                label.textContent = text;
            }
        }

        // Modal triggers
        function showAuthModal() {
            document.getElementById("auth-modal-overlay").classList.add("active");
        }

        function hideAuthModal() {
            document.getElementById("auth-modal-overlay").classList.remove("active");
        }

        // Format Currency utility
        function formatETB(value) {
            const num = Number(value || 0);
            return `ETB ${num.toLocaleString("en-US", { maximumFractionDigits: 0 })}`;
        }

        // Fetch dashboard statistics summary
        async function loadSummaryStats() {
            try {
                const res = await fetchAPI("/analytics/summary");
                const summary = res.data ?? res;
                
                document.getElementById("stat-revenue").textContent = formatETB(summary.total_revenue || 0);
                document.getElementById("stat-deposits").textContent = formatETB(summary.total_deposit || 0);
                document.getElementById("stat-outstanding").textContent = formatETB(summary.total_remaining || 0);
            } catch (e) {
                console.error("Failed to load statistics summary", e);
            }
        }

        // Load active orders list
        async function loadOrdersDirectory(page = 1) {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = `
                <tr>
                    <td colspan="7" class="empty-table loading-shimmer" style="height: 15rem;"></td>
                </tr>
            `;

            try {
                const limit = 10;
                const endpoint = `/orders?page=${page}&limit=${limit}`;
                const res = await fetchAPI(endpoint);
                const orderData = res.data ?? res;
                
                allOrders = Array.isArray(orderData) ? orderData : orderData.orders ?? [];
                totalPagesCount = orderData.pagination?.totalPages ?? 1;
                currentPage = page;

                renderOrdersTable();
                updatePaginationControls();
            } catch (e) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="7" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            <p>Failed to load orders repository.</p>
                        </td>
                    </tr>
                `;
                console.error("Failed loading order registry details", e);
            }
        }

        // Filter and render table
        function renderOrdersTable() {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = "";

            // Filter orders in-memory by search input if search query exists
            const filteredOrders = allOrders.filter(order => {
                const customer = order.customer_id || {};
                const name = (customer.name || "").toLowerCase();
                const code = (customer.unique_code || "").toString().toLowerCase();
                const query = activeSearchQuery.toLowerCase();
                return name.includes(query) || code.includes(query);
            });

            if (filteredOrders.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="7" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"></circle>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                            </svg>
                            <p>No matching orders found.</p>
                        </td>
                    </tr>
                `;
                return;
            }

            filteredOrders.forEach(o => {
                const cust = o.customer_id || {};
                const name = cust.name || "—";
                const code = cust.unique_code ? `#${cust.unique_code}` : "—";
                
                const isSelected = o._id === selectedOrderId;
                const rowClass = isSelected ? 'table-row selected' : 'table-row';
                
                const remaining = o.remaining_price || 0;
                const isCleared = remaining <= 0;
                const remClass = isCleared ? 'remaining-amount no-balance' : 'remaining-amount has-balance';
                
                const tr = document.createElement("tr");
                tr.className = rowClass;
                tr.onclick = () => selectOrder(o._id);
                
                tr.innerHTML = `
                    <td class="order-code">${code}</td>
                    <td class="customer-name">${name}</td>
                    <td>${formatETB(o.total_price)}</td>
                    <td style="color: var(--text-secondary);">${formatETB(o.deposit)}</td>
                    <td class="${remClass}">${formatETB(remaining)}</td>
                    <td>
                        <span class="status-badge ${o.status}">
                            <span class="badge-dot"></span>
                            ${o.status.replace('_', ' ')}
                        </span>
                    </td>
                    <td style="text-align: right;">
                        <button class="btn-manage" onclick="event.stopPropagation(); selectOrder('${o._id}')">Manage</button>
                    </td>
                `;
                tableBody.appendChild(tr);
            });
        }

        // Pagination buttons status
        function updatePaginationControls() {
            document.getElementById("pagination-info").textContent = `Showing Page ${currentPage} of ${totalPagesCount}`;
            document.getElementById("prev-page-btn").disabled = currentPage <= 1;
            document.getElementById("next-page-btn").disabled = currentPage >= totalPagesCount;
        }

        // Click order row
        async function selectOrder(orderId) {
            selectedOrderId = orderId;
            
            // Re-render table rows to update highlights
            renderOrdersTable();

            const placeholder = document.getElementById("sidebar-placeholder");
            const content = document.getElementById("sidebar-content");
            
            placeholder.style.display = "none";
            content.style.display = "block";

            // Clear values while loading
            document.getElementById("side-order-title").textContent = "Loading Order details...";
            document.getElementById("side-cust-name").textContent = "--";
            document.getElementById("side-cust-phone").textContent = "--";
            document.getElementById("side-ledger-total").textContent = "ETB --";
            document.getElementById("side-ledger-paid").textContent = "ETB --";
            document.getElementById("side-ledger-remaining").textContent = "ETB --";
            document.getElementById("side-payment-history").innerHTML = `<div class="no-history">Querying ledger balance...</div>`;
            document.getElementById("amount-input").value = "";

            try {
                // Fetch direct order details and payment history concurrently
                const [orderRes, paymentRes] = await Promise.all([
                    fetchAPI(`/orders/${orderId}`),
                    fetchAPI(`/payments/${orderId}`)
                ]);

                const order = orderRes.data?.order ?? orderRes.order ?? orderRes.data ?? orderRes;
                const paymentObj = paymentRes.data ?? paymentRes;
                const history = paymentObj.history || paymentObj.payments || [];

                const cust = order.customer_id || {};
                const name = cust.name || "—";
                const phone = cust.phone || "—";
                const code = cust.unique_code ? `#${cust.unique_code}` : order._id.slice(-6).toUpperCase();

                document.getElementById("side-order-title").textContent = `Order ${code}`;
                document.getElementById("side-cust-name").textContent = name;
                document.getElementById("side-cust-phone").textContent = phone;
                
                const total = order.total_price || 0;
                const deposit = order.deposit || 0;
                const remaining = order.remaining_price || 0;

                document.getElementById("side-ledger-total").textContent = formatETB(total);
                document.getElementById("side-ledger-paid").textContent = formatETB(deposit);
                document.getElementById("side-ledger-remaining").textContent = formatETB(remaining);

                const remainingRow = document.getElementById("side-ledger-remaining-row");
                const remainingLabel = document.getElementById("side-ledger-remaining-label");
                if (remaining <= 0) {
                    remainingRow.className = "ledger-row remaining cleared";
                    remainingLabel.textContent = "Balance Cleared";
                } else {
                    remainingRow.className = "ledger-row remaining";
                    remainingLabel.textContent = "Outstanding Balance";
                }

                // Render ledger transaction history
                const historyContainer = document.getElementById("side-payment-history");
                historyContainer.innerHTML = "";

                if (history.length === 0) {
                    historyContainer.innerHTML = `<div class="no-history">No transaction history found for this order.</div>`;
                } else {
                    // Sort descending date
                    const sortedHistory = [...history].sort((a,b) => new Date(b.payment_date || 0) - new Date(a.payment_date || 0));
                    sortedHistory.forEach(tx => {
                        const dateStr = tx.payment_date ? new Date(tx.payment_date).toLocaleDateString("en-US", { month: 'short', day: 'numeric', year: 'numeric' }) : "—";
                        const div = document.createElement("div");
                        div.className = "history-item";
                        div.innerHTML = `
                            <div class="history-info">
                                <span class="history-type ${tx.payment_type}">${tx.payment_type}</span>
                                <span class="history-date">${dateStr}</span>
                            </div>
                            <span class="history-amount">${formatETB(tx.amount)}</span>
                        `;
                        historyContainer.appendChild(div);
                    });
                }

                // Focus amount input
                document.getElementById("amount-input").placeholder = `${remaining}`;

            } catch (err) {
                console.error("Failed loading selected order details sidebar", err);
                placeholder.style.display = "flex";
                content.style.display = "none";
                showToast("Could not load details for the selected order.", "error");
            }
        }

        // Handle Login Submission
        async function handleLoginSubmit(event) {
            event.preventDefault();
            
            const identifier = document.getElementById("login-identifier").value.trim();
            const password = document.getElementById("login-password").value;
            
            const spinner = document.getElementById("login-spinner");
            const btnText = document.getElementById("login-btn-text");
            const submitBtn = document.getElementById("login-btn-submit");

            spinner.style.display = "inline-block";
            btnText.textContent = "Validating...";
            submitBtn.disabled = true;

            try {
                const response = await fetch(`${API_BASE}/auth/login`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ identifier, password })
                });

                if (!response.ok) {
                    const err = await response.json().catch(() => ({}));
                    throw new Error(err.message || "Failed to authenticate.");
                }

                const resData = await response.json();
                const token = resData.token;

                if (!token) {
                    throw new Error("No token returned by identity provider.");
                }

                setToken(token);
                showToast("Authentication successful! Welcome to Gateway.");
                hideAuthModal();
                
                // Load all dashboard components
                loadSummaryStats();
                loadOrdersDirectory(1);

            } catch (e) {
                showToast(e.message || "Access credentials incorrect. Retry.", "error");
                console.error("Login verification failed:", e);
            } finally {
                spinner.style.display = "none";
                btnText.textContent = "Sign In & Connect";
                submitBtn.disabled = false;
            }
        }

        // Handle Recording a New Payment
        async function handlePaymentSubmit(event) {
            event.preventDefault();
            
            if (!selectedOrderId) {
                showToast("No active order reference selected.", "error");
                return;
            }

            const amountVal = parseFloat(document.getElementById("amount-input").value);
            const paymentType = document.getElementById("payment-type-select").value;

            if (isNaN(amountVal) || amountVal <= 0) {
                showToast("Please register a valid payment amount.", "error");
                return;
            }

            const spinner = document.getElementById("form-spinner");
            const btnText = document.getElementById("submit-btn-text");
            const submitBtn = document.getElementById("submit-payment-btn");

            spinner.style.display = "inline-block";
            btnText.textContent = "Registering...";
            submitBtn.disabled = true;

            try {
                const res = await fetchAPI("/payments", {
                    method: "POST",
                    body: JSON.stringify({
                        order_id: selectedOrderId,
                        amount: amountVal,
                        payment_type: paymentType
                    })
                });

                showToast("Transaction registered successfully!");
                
                // Refresh data
                await loadSummaryStats();
                await loadOrdersDirectory(currentPage);
                await selectOrder(selectedOrderId);

            } catch (err) {
                console.error("Failed recording payment", err);
                showToast(err.message || "Failed to register transaction.", "error");
            } finally {
                spinner.style.display = "none";
                btnText.textContent = "Record Payment";
                submitBtn.disabled = false;
            }
        }

        // Setup Event Handlers
        document.getElementById("prev-page-btn").onclick = () => {
            if (currentPage > 1) {
                loadOrdersDirectory(currentPage - 1);
            }
        };

        document.getElementById("next-page-btn").onclick = () => {
            if (currentPage < totalPagesCount) {
                loadOrdersDirectory(currentPage + 1);
            }
        };

        document.getElementById("search-bar").oninput = (e) => {
            activeSearchQuery = e.target.value;
            renderOrdersTable();
        };

        document.getElementById("logout-btn").onclick = () => {
            clearToken();
            showToast("Logged out of Payment Gateway.");
            showAuthModal();
        };

        // Initialize App
        window.addEventListener("DOMContentLoaded", () => {
            const token = getToken();
            if (!token) {
                updateStatusDisplay(false, "Offline");
                showAuthModal();
            } else {
                updateStatusDisplay(true, "Connected");
                loadSummaryStats();
                loadOrdersDirectory(1);
            }
        });
    </script>
</body>
</html>
"""

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        
        # Standardize routing for payments gateway
        if path in ('/', '/payments', '/payments/', '/index.html'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - Path Not Found")

if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Payments UI Server running at http://localhost:{PORT}/payments")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nShutting down server...")
