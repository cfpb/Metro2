import autoprefixer from 'autoprefixer'
import pluginProcessIcons from './postcss/processIcons'

export default {
  plugins: [
    // Custom plugins.
    pluginProcessIcons(),

    // Autoprefixer goes last.
    autoprefixer()
  ]
}
