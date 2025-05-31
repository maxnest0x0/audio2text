import { createApp } from 'https://cdn.jsdelivr.net/npm/vue@3/dist/vue.esm-browser.js';

const IDLE = 0;
const TRANSCRIBING = 1;
const PENDING = 2;
const RECORDING = 3;

createApp({
    data() {
        return {
            state: IDLE,
            transcription: [],
            recorder: null,
        };
    },
    computed: {
        isIdle() {
            return this.state === IDLE;
        },
        isTranscribing() {
            return this.state === TRANSCRIBING;
        },
        isPending() {
            return this.state === PENDING;
        },
        isRecording() {
            return this.state === RECORDING;
        },
    },
    methods: {
        async transcribeAudio(audio) {
            this.state = TRANSCRIBING;
            this.transcription = [];
            const data = new FormData();
            data.append('audio', audio);
            const response = await fetch('/api/transcribe', { method: 'POST', body: data });
            if (!response.ok) {
                console.error(`HTTP Error ${response.status}`);
                alert('Произошла ошибка сервера');
                this.state = IDLE;
                return;
            }
            const result = await response.json();
            this.transcription = result.transcription;
            this.state = IDLE;
        },
        handleFileChange(event) {
            const file = event.target.files[0];
            if (file) this.transcribeAudio(file);
        },
        handleFileButtonClick() {
            if (this.state !== IDLE) return;
            document.querySelector('#audioFileInput').click();
        },
        handleRecordStartClick() {
            if (this.state !== IDLE) return;
            this.state = PENDING;
            navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
                this.state = RECORDING;
                const recorder = this.recorder = new MediaRecorder(stream);
                const chunks = [];
                recorder.start();
                recorder.ondataavailable = event => chunks.push(event.data);
                recorder.onstop = () => {
                    const blob = new Blob(chunks);
                    this.transcribeAudio(blob);
                };
                recorder.onerror = event => {
                    console.error(event.error);
                    alert('Произошла ошибка при записи звука');
                    this.state = IDLE;
                };
            }).catch(error => {
                console.error(error);
                alert('Не удалось получить доступ к микрофону');
                this.state = IDLE;
            });
        },
        handleRecordStopClick() {
            if (this.recorder) this.recorder.stop();
        },
        openDocs() {
            window.open('/docs');
        },
        openRepo() {
            window.open('https://github.com/maxnest0x0/audio2text');
        },
    },
    mounted() {
        document.fonts.ready.finally(() => {
            document.body.classList.remove('hidden');
        });
    },
}).mount('.container');
