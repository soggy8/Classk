// API helper functions

const API = {
    // Base URL for API endpoints
    baseURL: '',

    // Make a GET request
    get: async function(url) {
        try {
            const response = await fetch(this.baseURL + url);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('GET request failed:', error);
            throw error;
        }
    },

    // Make a POST request
    post: async function(url, data) {
        try {
            const response = await fetch(this.baseURL + url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('POST request failed:', error);
            throw error;
        }
    },

    // Make a form POST request (for file uploads)
    postForm: async function(url, formData) {
        try {
            const response = await fetch(this.baseURL + url, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('POST form request failed:', error);
            throw error;
        }
    }
};

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}
