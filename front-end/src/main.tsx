import App from 'App'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.less'
import 'vite/modulepreload-polyfill'

const container = document.querySelector('#root')
if (container) {
	const root = createRoot(container)
	root.render(
		<StrictMode>
			<App />
		</StrictMode>
	)
}
