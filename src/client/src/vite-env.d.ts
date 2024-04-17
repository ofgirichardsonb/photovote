/// <reference types="vite/client" />
declare global {
    interface ImportMetaEnv {
        readonly VITE_API_BASE_URL: string;
        readonly VITE_WS_URL: string;
        readonly VITE_CLIENT_ID: string;
        readonly VITE_BASE_URL: string;
    }

    interface ImportMeta {
        readonly env: ImportMetaEnv
    }
}