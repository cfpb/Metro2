import autoprefixer from 'autoprefixer'
import pluginProcessIcons from './postcss/processIcons'

export default {
  plugins: [
    pluginProcessIcons(),

    // Autoprefixer goes last
    autoprefixer()
  ]
}
