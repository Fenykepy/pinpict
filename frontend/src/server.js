import Express from 'express'
import React from 'react'
import webpackDevMiddleware from 'webpack-dev-middleware'
import webpackHotMiddleware from 'webpack-hot-middleware'
import webpack from 'webpack'
import config from '../webpack.config'
import layout from './layout'

var app = new Express()

// we are in development mode
if (process.env.NODE_ENV != 'production') {

  // use hot reloading in development
  var compiler = webpack(config)
  app.use(webpackDevMiddleware(compiler, {noInfo: true, publicPath: config.output.publicPath }))
  app.use(webpackHotMiddleware(compiler))

  // we serve static files for development
  app.use('/assets', Express.static(__dirname + '/../assets'))
  
  // we serve index file for development
  app.get('*', function(req, res) {
    res.status(200).send(layout)
  })
}


app.listen(3000, function(err) {
  if (err) {
    return console.error(err)
  }
  console.log('Listening at http://localhost:3000/')
})
