const path = require('path');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const webpack = require('webpack');
const TerserPlugin = require('terser-webpack-plugin');
const {CleanWebpackPlugin} = require('clean-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');
const autoprefixer = require('autoprefixer');


const postcssLoader = (env, options) => {
  return {
    loader: 'postcss-loader',
    options: {
      postcssOptions: {
        plugins: [
          autoprefixer
        ]
      }
    }
  };
};

const cssFileLoader = (env, options) => {
  return {
    loader: 'file-loader',
    options: {outputPath: 'css/', name: '[name].min.css'}
  };
};


const config = (env, options) => {
  let isProduction = options.mode === 'production';
  return {
    name: 'doku',
    entry: {
      main: './src/main.js',
      edit: './src/edit.js',
      edit_template: './src/edit_template.js',
      resources: './src/resources.js',
      templates: './src/templates.js',
      stylesheets: './src/stylesheets.js',
      snippet: './src/snippet.js',
    },
    output: {
      path: path.resolve(__dirname, './dist'),
      publicPath: '/static/',
      filename: '[name].bundle.js'
    },
    optimization: {
      splitChunks: {
        chunks: 'all',
        name: 'vendor',
        minChunks: 2
      },
      runtimeChunk: {
        name: 'runtime'
      },
      minimize: isProduction,
      minimizer: [
        new TerserPlugin()
      ]
    },
    module: {
      rules: [
        {
          test: /\.css$/,
          use: [
            cssFileLoader(env, options),
            'extract-loader',
            'css-loader',
            postcssLoader(env, options)
          ]
        },
        {
          test: /\.scss$/,
          exclude: /node_modules/,
          use: [
            cssFileLoader(env, options),
            'extract-loader',
            'css-loader',
            postcssLoader(env, options),
            {loader: 'sass-loader'}
          ]
        },
        {
          test: /\.vue$/,
          loader: 'vue-loader',
          options: {}
        },
        {
          test: /\.worker\.js$/,
          loader: 'worker-loader',
          options: {
            filename: '[name].bundle.js'
          }
        },
        {
          test: /\.js$/,
          loader: 'babel-loader',
          exclude: /node_modules/,
          options: {
            presets: ['@babel/preset-env'],
          }
        },
        {
          test: /\.(png|jpg|gif|svg)$/,
          loader: 'file-loader',
          options: {
            name: '[name].[ext]?[hash]',
            publicPath: '/static/assets',
            outputPath: 'assets',
            esModule: false,
          }
        },
        {
          test: /\.(woff|woff2|eot|ttf|otf)$/,
          loader: 'file-loader',
          options: {
            name: '[name].[ext]?[hash]',
            publicPath: '/static/assets',
            outputPath: 'assets',
            esModule: false,
          }
        }
      ]
    },
    target: 'browserslist',
    plugins: [
      new webpack.ProgressPlugin(),
      new CleanWebpackPlugin(),
      new VueLoaderPlugin(),
      new webpack.IgnorePlugin({resourceRegExp: /..\/..\/lib\/codemirror/}),
      new CopyWebpackPlugin({
        patterns: [
          {from: 'assets', to: 'assets'},
        ]
      }),
    ],
    watchOptions: {
      ignored: ['**/*.py', '**/node_modules'],
    },
    resolve: {
      alias: {
        'vue$': 'vue/dist/vue.esm.js'
      },
      extensions: ['*', '.js', '.vue', '.json']
    },
    performance: {
      hints: 'warning'
    },
    devServer: {
      historyApiFallback: true,
      noInfo: true,
      overlay: true
    },
    // use 'eval-source-map' for higher quality source maps
    devtool: (isProduction) ? false : 'eval-source-map',
    watch: !isProduction,
  };
};

module.exports = (env, options) => {
  return [
    config(env, options)
  ];
};
