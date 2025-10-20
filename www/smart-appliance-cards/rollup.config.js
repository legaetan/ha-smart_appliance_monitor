import babel from '@rollup/plugin-babel';
import resolve from '@rollup/plugin-node-resolve';
import commonjs from '@rollup/plugin-commonjs';
import terser from '@rollup/plugin-terser';

const production = !process.env.ROLLUP_WATCH;

const createConfig = (inputFile, outputFile) => ({
  input: inputFile,
  output: {
    file: outputFile,
    format: 'es',
    sourcemap: !production
  },
  plugins: [
    resolve({
      browser: true,
      preferBuiltins: false
    }),
    commonjs(),
    babel({
      babelHelpers: 'bundled',
      exclude: 'node_modules/**',
      presets: [
        ['@babel/preset-env', {
          targets: {
            browsers: ['last 2 versions', 'not dead', 'not ie 11']
          }
        }]
      ]
    }),
    production && terser({
      format: {
        comments: false
      },
      compress: {
        drop_console: true
      }
    })
  ].filter(Boolean)
});

export default [
  createConfig('src/cards/smart-appliance-cycle-card.js', 'dist/smart-appliance-cycle-card.js'),
  createConfig('src/cards/smart-appliance-stats-card.js', 'dist/smart-appliance-stats-card.js')
];
