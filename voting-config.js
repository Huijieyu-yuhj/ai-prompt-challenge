// ===== Voting System Configuration =====
const VOTING_CONFIG = {
    SUPABASE_URL: 'https://pkdqjaxkkmkmntvyifau.supabase.co',
    SUPABASE_ANON_KEY: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBrZHFqYXhra21rbW50dnlpZmF1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzkyNzQxNTEsImV4cCI6MjA5NDg1MDE1MX0.PQHSrL9C3CSPOIdFukZglcuVR-IGTlz_1jH34aiLJ2A',
    VOTING_PAGE_URL: 'https://huijieyu-yuhj.github.io/ai-prompt-challenge/vote.html',
    ADMIN_PASSWORD: 'admin123',
    VOTING_TIME_LIMIT_SECONDS: 120,
    VOTES_PER_AWARD: 2,
    AWARDS: [
        { id: 'bestCreative', name: 'Best Creative', icon: 'fa-palette' },
        { id: 'promptMaster', name: 'Prompt Master', icon: 'fa-wand-magic-sparkles' }
    ]
};

// ===== Supabase REST API Helper =====
const SupabaseAPI = {
    getHeaders() {
        return {
            'apikey': VOTING_CONFIG.SUPABASE_ANON_KEY,
            'Authorization': `Bearer ${VOTING_CONFIG.SUPABASE_ANON_KEY}`,
            'Content-Type': 'application/json',
            'Prefer': 'return=representation'
        };
    },

    async query(table, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = `${VOTING_CONFIG.SUPABASE_URL}/rest/v1/${table}?${queryString}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error(`Query failed: ${response.status} ${response.statusText}`);
        return response.json();
    },

    async create(table, data) {
        const url = `${VOTING_CONFIG.SUPABASE_URL}/rest/v1/${table}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`Create failed: ${response.status} ${response.statusText}`);
        return response.json();
    },

    async update(table, column, value, data) {
        const url = `${VOTING_CONFIG.SUPABASE_URL}/rest/v1/${table}?${column}=eq.${value}`;
        const response = await fetch(url, {
            method: 'PATCH',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`Update failed: ${response.status} ${response.statusText}`);
        return response.json();
    },

    async delete(table, column, value) {
        const url = `${VOTING_CONFIG.SUPABASE_URL}/rest/v1/${table}?${column}=eq.${value}`;
        const response = await fetch(url, {
            method: 'DELETE',
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error(`Delete failed: ${response.status} ${response.statusText}`);
        return response.json();
    },

    async checkVoted(sessionId) {
        const result = await this.query('votes', `voter_session_id=eq.${sessionId}&limit=1`);
        return result && result.length > 0;
    },

    async getVotingSession() {
        const result = await this.query('voting_session', 'order=created_at.desc&limit=1');
        return result && result.length > 0 ? result[0] : null;
    },

    async getAllVotes() {
        return this.query('votes', 'order=created_at.desc');
    },

    async deleteAllVotes() {
        const url = `${VOTING_CONFIG.SUPABASE_URL}/rest/v1/votes?id=not.is.null`;
        const response = await fetch(url, {
            method: 'DELETE',
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error(`Delete all failed: ${response.status} ${response.statusText}`);
        return response.json();
    }
};

// ===== Session Management =====
const SessionManager = {
    STORAGE_KEY: 'voter_session_id',

    getSessionId() {
        let sessionId = localStorage.getItem(this.STORAGE_KEY);
        if (!sessionId) {
            sessionId = this.generateId();
            localStorage.setItem(this.STORAGE_KEY, sessionId);
        }
        return sessionId;
    },

    generateId() {
        return 'vs_' + Date.now() + '_' + Math.random().toString(36).substring(2, 15);
    },

    hasVoted() {
        return sessionStorage.getItem('has_voted') === 'true';
    },

    markAsVoted() {
        sessionStorage.setItem('has_voted', 'true');
    }
};
