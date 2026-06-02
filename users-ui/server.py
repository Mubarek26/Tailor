import http.server
import socketserver
import os
import urllib.parse

PORT = 8082

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tailor Shop - User Management Terminal</title>
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
            --primary: #8b5cf6;
            --primary-glow: rgba(139, 92, 246, 0.15);
            --primary-gradient: linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%);
            --success: #10b981;
            --success-bg: rgba(16, 185, 129, 0.1);
            --warning: #f59e0b;
            --warning-bg: rgba(245, 158, 11, 0.1);
            --danger: #ef4444;
            --danger-bg: rgba(239, 68, 68, 0.1);
            --font-main: 'Outfit', sans-serif;
            --shadow-lg: 0 20px 25px -5px rgb(0 0 0 / 0.5), 0 8px 10px -6px rgb(0 0 0 / 0.5);
            --shadow-glow: 0 0 30px rgba(139, 92, 246, 0.2);
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
                radial-gradient(at 0% 0%, rgba(139, 92, 246, 0.12) 0px, transparent 50%),
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
            border-bottom: 1px solid var(--border-color);
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
            box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
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
            background: rgba(139, 92, 246, 0.15);
            border: 1px solid rgba(139, 92, 246, 0.3);
            color: #d8b4fe;
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

        .summary-card.total-users::before {
            background: linear-gradient(90deg, #8b5cf6, #d8b4fe);
        }

        .summary-card.pending-owners::before {
            background: linear-gradient(90deg, #f59e0b, #3b82f6);
        }

        .summary-card.active-tailors::before {
            background: linear-gradient(90deg, #10b981, #06b6d4);
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

        /* Controls row with filters and search */
        .controls-row {
            display: flex;
            gap: 0.75rem;
            align-items: center;
            width: 100%;
            flex-wrap: wrap;
        }

        @media (min-width: 640px) {
            .controls-row {
                width: auto;
                max-width: 500px;
                flex-wrap: nowrap;
            }
        }

        .filter-select {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.6rem 2rem 0.6rem 1rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-family: var(--font-main);
            cursor: pointer;
            appearance: none;
            -webkit-appearance: none;
            background-image: url("data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3E%3Cpath stroke='%2394a3b8' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3E%3C/svg%3E");
            background-repeat: no-repeat;
            background-position: right 0.75rem center;
            background-size: 1.25rem;
            transition: all 0.2s ease;
        }

        .filter-select:focus {
            outline: none;
            border-color: var(--primary);
        }

        .filter-select option {
            background-color: #121424;
            color: var(--text-primary);
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

        /* Users Table */
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
            background-color: rgba(139, 92, 246, 0.08);
        }

        .user-identity {
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .avatar-initial {
            width: 2.25rem;
            height: 2.25rem;
            border-radius: 50%;
            background: rgba(139, 92, 246, 0.15);
            color: var(--primary);
            font-weight: 700;
            font-size: 0.95rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(139, 92, 246, 0.2);
        }

        .user-details-mini {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
            max-width: 180px;
        }

        .user-name-cell {
            font-weight: 600;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .user-email-cell {
            font-size: 0.75rem;
            color: var(--text-secondary);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .role-badge {
            display: inline-flex;
            padding: 0.2rem 0.5rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: capitalize;
        }

        .role-badge.superadmin {
            background-color: rgba(139, 92, 246, 0.15);
            color: #c084fc;
            border: 1px solid rgba(139, 92, 246, 0.2);
        }

        .role-badge.owner {
            background-color: rgba(59, 130, 246, 0.1);
            color: #60a5fa;
            border: 1px solid rgba(59, 130, 246, 0.2);
        }

        .role-badge.tailor {
            background-color: rgba(16, 185, 129, 0.1);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.2);
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

        .status-badge.approved, .status-badge.active {
            background-color: var(--success-bg);
            color: var(--success);
            border: 1px solid rgba(16, 185, 129, 0.2);
        }

        .status-badge.rejected {
            background-color: var(--danger-bg);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.2);
        }

        .badge-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background-color: currentColor;
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
            box-shadow: 0 4px 10px rgba(139, 92, 246, 0.2);
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
            background: rgba(139, 92, 246, 0.08);
            border: 1px solid rgba(139, 92, 246, 0.2);
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
            grid-template-columns: 1fr;
            gap: 0.75rem;
        }

        .meta-item {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
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

        /* Approval Actions panel */
        .approval-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.75rem;
            background: rgba(245, 158, 11, 0.03);
            border: 1px solid rgba(245, 158, 11, 0.2);
            border-radius: 1rem;
            padding: 1rem;
        }

        .approval-header {
            grid-column: span 2;
            font-size: 0.8rem;
            font-weight: 700;
            color: var(--warning);
            text-transform: uppercase;
            text-align: center;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }

        .btn-approve {
            background: var(--success);
            border: none;
            color: white;
            padding: 0.6rem;
            border-radius: 0.5rem;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }

        .btn-approve:hover {
            opacity: 0.9;
        }

        .btn-reject {
            background: var(--danger);
            border: none;
            color: white;
            padding: 0.6rem;
            border-radius: 0.5rem;
            font-weight: 700;
            font-size: 0.85rem;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }

        .btn-reject:hover {
            opacity: 0.9;
        }

        /* Profile Editing Form */
        .profile-form {
            display: flex;
            flex-direction: column;
            gap: 1rem;
            background: rgba(139, 92, 246, 0.03);
            border: 1px solid rgba(139, 92, 246, 0.15);
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

        .input-text {
            width: 100%;
            background: rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-family: var(--font-main);
            transition: all 0.2s ease;
        }

        .input-text:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .select-field {
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

        .select-field:focus {
            outline: none;
            border-color: var(--primary);
            box-shadow: 0 0 0 2px var(--primary-glow);
        }

        .select-field option {
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
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        }

        .btn-submit:hover:not(:disabled) {
            opacity: 0.95;
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(139, 92, 246, 0.4);
        }

        .btn-submit:active:not(:disabled) {
            transform: translateY(0);
        }

        .btn-submit:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            box-shadow: none;
        }

        /* Account Deletion Panel */
        .danger-panel {
            background: rgba(239, 68, 68, 0.03);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-radius: 1.25rem;
            padding: 1.25rem;
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .danger-title {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--danger);
        }

        .danger-desc {
            font-size: 0.75rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .btn-delete {
            background: rgba(239, 68, 68, 0.15);
            border: 1px solid rgba(239, 68, 68, 0.3);
            color: #fca5a5;
            padding: 0.75rem;
            border-radius: 0.75rem;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.2s ease;
            text-align: center;
        }

        .btn-delete:hover {
            background: var(--danger);
            border-color: transparent;
            color: white;
            box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
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
            box-shadow: 0 8px 20px rgba(139, 92, 246, 0.3);
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
            box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3);
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-login:hover {
            opacity: 0.95;
            box-shadow: 0 6px 20px rgba(139, 92, 246, 0.45);
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
                    <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                    <circle cx="9" cy="7" r="4"></circle>
                    <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                    <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                </svg>
            </div>
            <span class="logo-text">Tailor Pro</span>
            <span class="terminal-badge">User Registry</span>
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
                <div class="summary-card total-users">
                    <span class="summary-label">Total Accounts</span>
                    <span class="summary-value" id="stat-total-users">0</span>
                </div>
                <div class="summary-card pending-owners">
                    <span class="summary-label">Pending Owners</span>
                    <span class="summary-value" id="stat-pending-owners" style="color: var(--warning);">0</span>
                </div>
                <div class="summary-card active-tailors">
                    <span class="summary-label">Active Shop Tailors</span>
                    <span class="summary-value" id="stat-active-tailors" style="color: var(--success);">0</span>
                </div>
            </div>

            <!-- Users Table Panel -->
            <div class="panel">
                <div class="panel-header">
                    <div class="panel-title-container">
                        <h2 class="panel-title">User Directory</h2>
                        <span class="panel-subtitle">Review, edit, and approve shop accounts</span>
                    </div>
                    <div class="controls-row">
                        <select class="filter-select" id="role-filter">
                            <option value="all">All Roles</option>
                            <option value="owner">Owners</option>
                            <option value="tailor">Tailors</option>
                            <option value="superadmin">Superadmins</option>
                        </select>
                        <div class="search-wrapper">
                            <span class="search-icon">
                                <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                    <circle cx="11" cy="11" r="8"></circle>
                                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                                </svg>
                            </span>
                            <input type="text" class="search-input" id="search-bar" placeholder="Search by name, email, phone...">
                        </div>
                    </div>
                </div>

                <div class="table-container">
                    <table id="users-table">
                        <thead>
                            <tr>
                                <th>User</th>
                                <th>Role</th>
                                <th>Phone Number</th>
                                <th>Status</th>
                                <th style="text-align: right;">Action</th>
                            </tr>
                        </thead>
                        <tbody id="table-body">
                            <tr>
                                <td colspan="5" class="empty-table loading-shimmer" style="height: 15rem;"></td>
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
        <div class="panel sidebar" id="users-sidebar">
            <div class="sidebar-placeholder" id="sidebar-placeholder">
                <div class="placeholder-icon">
                    <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                    </svg>
                </div>
                <h3 class="placeholder-title">Select User Account</h3>
                <p class="placeholder-text">Click on any user row or select "Manage" to view details, update their status, modify credentials, or delete records.</p>
            </div>

            <div class="sidebar-content" id="sidebar-content" style="display: none;">
                <div>
                    <h3 class="panel-title" id="side-user-title" style="margin-bottom: 0.25rem;">User Profile</h3>
                    <span class="panel-subtitle" id="side-user-subtitle">Administrative profile controls</span>
                </div>

                <!-- Owner Account Approval Box -->
                <div id="side-approval-container" style="display: none;">
                    <div class="approval-actions">
                        <div class="approval-header">Pending Owner Application</div>
                        <button class="btn-approve" onclick="handleStatusUpdate('approved')">Approve Account</button>
                        <button class="btn-reject" onclick="handleStatusUpdate('rejected')">Reject Account</button>
                    </div>
                </div>

                <!-- Account Metadata Details -->
                <div>
                    <h4 class="sidebar-section-title">Registration Meta</h4>
                    <div class="meta-grid">
                        <div class="meta-item">
                            <span class="meta-label">Unique Database ID</span>
                            <span class="meta-value" id="side-meta-id" style="font-family: monospace; font-size: 0.8rem; word-break: break-all;">--</span>
                        </div>
                        <div class="meta-item" style="margin-top: 0.5rem;">
                            <span class="meta-label">Joined Date</span>
                            <span class="meta-value" id="side-meta-date">--</span>
                        </div>
                    </div>
                </div>

                <!-- Profile Editing Form -->
                <div>
                    <h4 class="sidebar-section-title">Modify Credentials</h4>
                    <form class="profile-form" id="edit-profile-form" onsubmit="handleProfileSubmit(event)">
                        <div class="form-group">
                            <label class="form-label" for="edit-name">Full Name</label>
                            <input type="text" id="edit-name" class="input-text" required placeholder="User name">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="edit-email">Email Address</label>
                            <input type="email" id="edit-email" class="input-text" required placeholder="name@example.com">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="edit-phone">Phone Number</label>
                            <input type="text" id="edit-phone" class="input-text" required placeholder="0912...">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="edit-address">Home Address</label>
                            <input type="text" id="edit-address" class="input-text" placeholder="Addis Ababa, Ethiopia">
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="edit-role-select">Access Role</label>
                            <select id="edit-role-select" class="select-field" required>
                                <option value="owner">Owner / Shop Manager</option>
                                <option value="tailor">Tailor / Workshop Staff</option>
                                <option value="superadmin">Superadmin / System Auditor</option>
                            </select>
                        </div>

                        <div class="form-group">
                            <label class="form-label" for="edit-status-select">Account Status</label>
                            <select id="edit-status-select" class="select-field" required>
                                <option value="pending">Pending Review</option>
                                <option value="approved">Approved / Active</option>
                                <option value="rejected">Rejected / Disabled</option>
                            </select>
                        </div>

                        <button type="submit" class="btn-submit" id="submit-profile-btn">
                            <svg class="spinner" viewBox="0 0 50 50" id="form-spinner">
                                <circle cx="25" cy="25" r="20" stroke="currentColor" fill="none"></circle>
                            </svg>
                            <span id="submit-btn-text">Save Profile Changes</span>
                        </button>
                    </form>
                </div>

                <!-- Danger Zone Delete Box -->
                <div>
                    <h4 class="sidebar-section-title" style="color: var(--danger); border-color: rgba(239,68,68,0.2);">Danger Zone</h4>
                    <div class="danger-panel">
                        <span class="danger-title">Delete Account Permanent</span>
                        <p class="danger-desc">This action removes all database records associated with this user. It is irreversible.</p>
                        <button class="btn-delete" onclick="handleDeleteUser()">Delete User Account</button>
                    </div>
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
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                        <circle cx="9" cy="7" r="4"></circle>
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                        <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
                    </svg>
                </div>
                <h2 class="modal-title">Identity Verification</h2>
                <p class="modal-subtitle">Sign in with system administrator credentials to access the user registry terminal</p>
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
        let selectedUserId = null;
        let allUsers = [];
        let totalPagesCount = 1;
        let activeSearchQuery = "";
        let activeRoleFilter = "all";

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
            selectedUserId = null;
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

                if (response.status === 204) {
                    return null;
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

        // Fetch User Statistics
        async function loadUserStats() {
            try {
                // Fetch stats by roles and statuses
                const res = await fetchAPI("/users?limit=1000");
                const list = res.data?.users ?? res.users ?? [];
                
                const total = list.length;
                const pending = list.filter(u => u.role === "owner" && u.status === "pending").length;
                const activeTailors = list.filter(u => u.role === "tailor").length;

                document.getElementById("stat-total-users").textContent = total;
                document.getElementById("stat-pending-owners").textContent = pending;
                document.getElementById("stat-active-tailors").textContent = activeTailors;
            } catch (e) {
                console.error("Failed loading summary statistics", e);
            }
        }

        // Load users registry list
        async function loadUsersDirectory(page = 1) {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = `
                <tr>
                    <td colspan="5" class="empty-table loading-shimmer" style="height: 15rem;"></td>
                </tr>
            `;

            try {
                const limit = 10;
                let endpoint = `/users?page=${page}&limit=${limit}`;
                if (activeRoleFilter !== "all") {
                    endpoint += `&role=${activeRoleFilter}`;
                }
                
                const res = await fetchAPI(endpoint);
                const usersData = res.data ?? res;
                
                allUsers = Array.isArray(usersData) ? usersData : usersData.users ?? [];
                totalPagesCount = usersData.pagination?.totalPages ?? 1;
                currentPage = page;

                renderUsersTable();
                updatePaginationControls();
            } catch (e) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="12" cy="12" r="10"></circle>
                                <line x1="12" y1="8" x2="12" y2="12"></line>
                                <line x1="12" y1="16" x2="12.01" y2="16"></line>
                            </svg>
                            <p>Failed to load users directory.</p>
                        </td>
                    </tr>
                `;
                console.error("Failed loading user database", e);
            }
        }

        // Render table
        function renderUsersTable() {
            const tableBody = document.getElementById("table-body");
            tableBody.innerHTML = "";

            // Filter in-memory by search queries
            const filteredUsers = allUsers.filter(u => {
                const name = (u.fullName || "").toLowerCase();
                const email = (u.email || "").toLowerCase();
                const phone = (u.phoneNumber || "").toLowerCase();
                const query = activeSearchQuery.toLowerCase();
                return name.includes(query) || email.includes(query) || phone.includes(query);
            });

            if (filteredUsers.length === 0) {
                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5" class="empty-table">
                            <svg viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                                <circle cx="11" cy="11" r="8"></circle>
                                <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                            </svg>
                            <p>No matching user profiles found.</p>
                        </td>
                    </tr>
                `;
                return;
            }

            filteredUsers.forEach(u => {
                const name = u.fullName || "—";
                const email = u.email || "No email";
                const phone = u.phoneNumber || "—";
                const initial = name[0]?.toUpperCase() || "?";
                
                const isSelected = u._id === selectedUserId;
                const rowClass = isSelected ? 'table-row selected' : 'table-row';
                
                const status = u.status || "active";
                
                const tr = document.createElement("tr");
                tr.className = rowClass;
                tr.onclick = () => selectUser(u._id);
                
                tr.innerHTML = `
                    <td>
                        <div class="user-identity">
                            <div class="avatar-initial">${initial}</div>
                            <div class="user-details-mini">
                                <span class="user-name-cell">${name}</span>
                                <span class="user-email-cell">${email}</span>
                            </div>
                        </div>
                    </td>
                    <td>
                        <span class="role-badge ${u.role}">${u.role}</span>
                    </td>
                    <td style="color: var(--text-secondary); font-weight: 500;">${phone}</td>
                    <td>
                        <span class="status-badge ${status}">
                            <span class="badge-dot"></span>
                            ${status}
                        </span>
                    </td>
                    <td style="text-align: right;">
                        <button class="btn-manage" onclick="event.stopPropagation(); selectUser('${u._id}')">Manage</button>
                    </td>
                `;
                tableBody.appendChild(tr);
            });
        }

        // Pagination updates
        function updatePaginationControls() {
            document.getElementById("pagination-info").textContent = `Showing Page ${currentPage} of ${totalPagesCount}`;
            document.getElementById("prev-page-btn").disabled = currentPage <= 1;
            document.getElementById("next-page-btn").disabled = currentPage >= totalPagesCount;
        }

        // Select user row
        async function selectUser(userId) {
            selectedUserId = userId;
            renderUsersTable();

            const placeholder = document.getElementById("sidebar-placeholder");
            const content = document.getElementById("sidebar-content");
            
            placeholder.style.display = "none";
            content.style.display = "block";

            // Reset values
            document.getElementById("side-user-title").textContent = "Loading User details...";
            document.getElementById("side-meta-id").textContent = "--";
            document.getElementById("side-meta-date").textContent = "--";
            document.getElementById("side-approval-container").style.display = "none";
            
            try {
                const res = await fetchAPI(`/users/${userId}`);
                const user = res.data?.user ?? res.user ?? res.data ?? res;

                document.getElementById("side-user-title").textContent = user.fullName;
                document.getElementById("side-meta-id").textContent = user._id;
                document.getElementById("side-meta-date").textContent = user.createdAt ? new Date(user.createdAt).toLocaleDateString("en-US", { month: 'short', day: 'numeric', year: 'numeric' }) : "—";
                
                // Form setup
                document.getElementById("edit-name").value = user.fullName || "";
                document.getElementById("edit-email").value = user.email || "";
                document.getElementById("edit-phone").value = user.phoneNumber || "";
                document.getElementById("edit-address").value = user.address || "";
                document.getElementById("edit-role-select").value = user.role || "owner";
                document.getElementById("edit-status-select").value = user.status || "approved";

                // Show approval buttons if owner and pending
                if (user.role === "owner" && user.status === "pending") {
                    document.getElementById("side-approval-container").style.display = "block";
                }

            } catch (err) {
                console.error("Failed loading selected user details", err);
                placeholder.style.display = "flex";
                content.style.display = "none";
                showToast("Could not load administrative details for this account. Ensure you have Superadmin access.", "error");
            }
        }

        // Handle Admin Login
        async function handleLoginSubmit(event) {
            event.preventDefault();
            
            const identifier = document.getElementById("login-identifier").value.trim();
            const password = document.getElementById("login-password").value;
            
            const spinner = document.getElementById("login-spinner");
            const btnText = document.getElementById("login-btn-text");
            const submitBtn = document.getElementById("login-btn-submit");

            spinner.style.display = "inline-block";
            btnText.textContent = "Verifying...";
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
                
                // Check if user is Superadmin
                const userObj = resData.data?.user ?? resData.user ?? {};
                if (userObj.role !== "superadmin") {
                    throw new Error("Access Denied: Only Superadmin auditors can access this registry terminal.");
                }

                const token = resData.token;
                setToken(token);
                showToast("Identity verified! Loading administrative terminal.");
                hideAuthModal();
                
                // Refresh list
                loadUserStats();
                loadUsersDirectory(1);

            } catch (e) {
                showToast(e.message || "Authentication credentials incorrect.", "error");
                console.error("Login verification failed:", e);
            } finally {
                spinner.style.display = "none";
                btnText.textContent = "Sign In & Connect";
                submitBtn.disabled = false;
            }
        }

        // Handle Owner Status Approval / Rejection
        async function handleStatusUpdate(newStatus) {
            if (!selectedUserId) return;
            
            try {
                await fetchAPI(`/users/${selectedUserId}/status`, {
                    method: "PATCH",
                    body: JSON.stringify({ status: newStatus })
                });
                
                showToast(`Owner status updated to ${newStatus}!`);
                
                // Reload list
                await loadUserStats();
                await loadUsersDirectory(currentPage);
                await selectUser(selectedUserId);
            } catch (err) {
                console.error("Failed updating user status", err);
                showToast(err.message || "Failed to update owner status.", "error");
            }
        }

        // Handle Profile Edit Submission
        async function handleProfileSubmit(event) {
            event.preventDefault();
            
            if (!selectedUserId) return;

            const fullName = document.getElementById("edit-name").value.trim();
            const email = document.getElementById("edit-email").value.trim();
            const phoneNumber = document.getElementById("edit-phone").value.trim();
            const address = document.getElementById("edit-address").value.trim();
            const role = document.getElementById("edit-role-select").value;
            const status = document.getElementById("edit-status-select").value;

            const spinner = document.getElementById("form-spinner");
            const btnText = document.getElementById("submit-btn-text");
            const submitBtn = document.getElementById("submit-profile-btn");

            spinner.style.display = "inline-block";
            btnText.textContent = "Updating...";
            submitBtn.disabled = true;

            try {
                await fetchAPI(`/users/${selectedUserId}`, {
                    method: "PUT",
                    body: JSON.stringify({
                        fullName,
                        email,
                        phoneNumber,
                        address,
                        role,
                        status
                    })
                });

                showToast("Account credentials updated successfully!");
                
                await loadUserStats();
                await loadUsersDirectory(currentPage);
                await selectUser(selectedUserId);
            } catch (err) {
                console.error("Failed updating profile", err);
                showToast(err.message || "Failed to update account details.", "error");
            } finally {
                spinner.style.display = "none";
                btnText.textContent = "Save Profile Changes";
                submitBtn.disabled = false;
            }
        }

        // Handle User Account Deletion
        async function handleDeleteUser() {
            if (!selectedUserId) return;
            
            const confirmed = confirm("Are you sure you want to permanently delete this user account? All associated records will be destroyed.");
            if (!confirmed) return;

            try {
                await fetchAPI(`/users/${selectedUserId}`, {
                    method: "DELETE"
                });

                showToast("User account successfully deleted.");
                
                selectedUserId = null;
                document.getElementById("sidebar-content").style.display = "none";
                document.getElementById("sidebar-placeholder").style.display = "flex";

                await loadUserStats();
                await loadUsersDirectory(1);
            } catch (err) {
                console.error("Failed deleting user account", err);
                showToast(err.message || "Failed to delete user profile.", "error");
            }
        }

        // Setup Event Handlers
        document.getElementById("prev-page-btn").onclick = () => {
            if (currentPage > 1) {
                loadUsersDirectory(currentPage - 1);
            }
        };

        document.getElementById("next-page-btn").onclick = () => {
            if (currentPage < totalPagesCount) {
                loadUsersDirectory(currentPage + 1);
            }
        };

        document.getElementById("search-bar").oninput = (e) => {
            activeSearchQuery = e.target.value;
            renderUsersTable();
        };

        document.getElementById("role-filter").onchange = (e) => {
            activeRoleFilter = e.target.value;
            loadUsersDirectory(1);
        };

        document.getElementById("logout-btn").onclick = () => {
            clearToken();
            showToast("Logged out of administrative terminal.");
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
                loadUserStats();
                loadUsersDirectory(1);
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
        
        # Standardize routing for user directory portal
        if path in ('/', '/users', '/users/', '/index.html'):
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
        print(f"Users UI Server running at http://localhost:{PORT}/users")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nShutting down server...")
