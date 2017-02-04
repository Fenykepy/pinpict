/* sources of learning webpack :
 *
 * http://christianalfoni.github.io/react-webpack-cookbook/Running-a-workflow.html
 * https://github.com/petehunt/webpack-howto
 *
 */

var path = require('path');
var webpack = require('webpack');
var ExtractTextPlugin = require("extract-text-webpack-plugin");
var AssetsPlugin = require('assets-webpack-plugin');
var BabelPolyfill = require("babel-polyfill");
var autoprefixer = require('autoprefixer');

var config = {
  // sourceMaps simplified to a single mapping per line
  //devtool: 'cheap-module-eval-source-map',
  devtool: 'eval',
  entry: {
    app: [
    'babel-polyfill',
    'webpack-hot-middleware/client',
    './src/client'
    ]
  },
  output: {
    path: path.join( __dirname, 'dist' ),
    filename: 'bundle.js',
    publicPath: '/static/',

  },
  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new webpack.NoErrorsPlugin(),
    new AssetsPlugin({filename: 'webpack-assets.dev.json'}),
    new ExtractTextPlugin("styles.css", {
      allChunks: true
    })
  ],
  module: {
    loaders: [
      {
        // json files
        test: /\.json$/, loader: 'json'
      },
      {
        // js files
        test: /\.js$/,
        loaders: ['babel'],
        exclude: path.join( __dirname, '/node_modules/'),
        include: __dirname
      },
      {
        // less files, get extracted
        test: /\.less$/,
        loader: ExtractTextPlugin.extract(
          'style-loader',
          [
            'css-loader?modules&importLoaders=2&localIdentName=[name]__[local]___[hash:base64:5]',
            'postcss-loader',
            'less-loader',
          ]
        ),
        exclude: path.join( __dirname, '/node_modules/'),
      },
      { 
        // images are stored separately
        test: /\.(png|jpg)$/, 
        loader: 'file-loader?name=images/[hash].[ext]',
        exclude: [
          path.join( __dirname, '/node_modules/'),
          path.join(__dirname, '/src/graphics/favicon.png'),
        ]
      },
      {
        // favicon png is stored with original name
        test: /favicon\.png$/,
        loader: 'file-loader?name=images/favicon.png',
        exclude: path.join( __dirname, '/node_modules/'),
      },

      { 
        // svg are optimised then stored separately
        test: /\.(svg)$/, 
        loaders: [ 'file-loader?name=images/[hash].[ext]', 'svgo-loader?useConfig=svgoConfig'],
        exclude: path.join( __dirname, '/node_modules/'),
      },    
    ],
  },
  postcss: function () {
      return [autoprefixer];
  },
  svgoConfig: {
    plugins: [
      {removeTitle: true},
      {convertColors: {shorthex: false}},
      {convertPathData: false}
    ]
  },
  resolve: {
    root: [
      path.resolve(path.join( __dirname, 'src')),
      path.resolve(path.join( __dirname, 'src/modules')),
    ]
  },
};

module.exports = config;


