// ===== Voting System Configuration =====
const VOTING_CONFIG = {
    BMOB_APP_ID: '518ebf4f1f9f0c10b45a559ca0dd13e8',
    BMOB_REST_API_KEY: '972e52f296e6d8a848fe229727a4ea6c',
    BMOB_SECRET_KEY: '69de25ef4d2a84b6',
    VOTING_PAGE_URL: 'https://huijieyu-yuhj.github.io/ai-prompt-challenge/vote.html',
    ADMIN_PASSWORD: 'admin123',
    VOTING_TIME_LIMIT_SECONDS: 120,
    VOTES_PER_AWARD: 2,
    AWARDS: [
        { id: 'bestCreative', name: 'Best Creative', icon: 'fa-palette' },
        { id: 'promptMaster', name: 'Prompt Master', icon: 'fa-wand-magic-sparkles' }
    ]
};

// ===== Bmob REST API Helper =====
const BmobAPI = {
    BASE_URL: 'https://api2.bmob.cn/1',

    getHeaders() {
        return {
            'X-Bmob-Application-Id': VOTING_CONFIG.BMOB_APP_ID,
            'X-Bmob-REST-API-Key': VOTING_CONFIG.BMOB_REST_API_KEY,
            'Content-Type': 'application/json'
        };
    },

    async query(className, params = {}) {
        const queryString = new URLSearchParams(params).toString();
        const url = `${this.BASE_URL}/classes/${className}?${queryString}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: this.getHeaders(),
            mode: 'cors'
        });
        if (!response.ok) throw new Error(`Query failed: ${response.status} ${response.statusText}`);
        return response.json();
    },

    async create(className, data) {
        const url = `${this.BASE_URL}/classes/${className}`;
        const response = await fetch(url, {
            method: 'POST',
            headers: this.getHeaders(),
            body: JSON.stringify(data),
            mode: 'cors'
        });
        if (!response.ok) throw new Error(`Create failed: ${response.status} ${response.statusText}`);
        return response.json();
    },

    async update(className, objectId, data) {
        const url = `${this.BASE_URL}/classes/${className}/${objectId}`;
        const response = await fetch(url, {
            method: 'PUT',
            headers: this.getHeaders(),
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`Update failed: ${response.statusText}`);
        return response.json();
    },

    async delete(className, objectId) {
        const url = `${this.BASE_URL}/classes/${className}/${objectId}`;
        const response = await fetch(url, {
            method: 'DELETE',
            headers: this.getHeaders()
        });
        if (!response.ok) throw new Error(`Delete failed: ${response.statusText}`);
        return response.json();
    },

    async checkVoted(sessionId) {
        const result = await this.query('Vote', { where: JSON.stringify({ voterSessionId: sessionId }) });
        return result.results && result.results.length > 0;
    },

    async getVotingSession() {
        const result = await this.query('VotingSession', { order: '-createdAt', limit: 1 });
        return result.results && result.results.length > 0 ? result.results[0] : null;
    },

    async getAllVotes() {
        return this.query('Vote');
    },

    async deleteAllVotes() {
        const votes = await this.getAllVotes();
        if (votes.results && votes.results.length > 0) {
            const deletePromises = votes.results.map(v => this.delete('Vote', v.objectId));
            await Promise.all(deletePromises);
        }
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
