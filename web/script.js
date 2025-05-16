import { createApp } from 'https://cdn.jsdelivr.net/npm/vue@3/dist/vue.esm-browser.js';

createApp({
    data() {
        return {
            loading: false,
            transcription: [],
        };
    },
    methods: {
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) this.transcribeFile(file);
        },
        handleFileButtonClick() {
            if (!this.loading) document.querySelector('#audioFileInput').click();
        },
        async transcribeFile(file) {
            this.loading = true;
            this.transcription = [];
            const data = new FormData();
            data.append('audio', file);
            const response = await fetch('/api/transcribe', { method: 'POST', body: data });
            if (!response.ok)
                throw new Error(`HTTP Error ${response.status}`);
            const result = await response.json();
            this.transcription = result.transcription;
            this.loading = false;
        }
    },
}).mount('.container');
