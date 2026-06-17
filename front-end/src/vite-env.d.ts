/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_SHOW_CFPB_HEADER: string // Cast to string since Vite delivers it as a string
  readonly VITE_ADMIN_EMAIL: string
  readonly VITE_DOWNLOAD_ACKNOWLEDGMENT_TEXT: string
  readonly VITE_PII_WARNING_TEXT: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}
