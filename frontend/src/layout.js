import prodAssets from '../webpack-assets.json'
import devAssets from '../webpack-assets.dev.json'


// we change assets file on production
let assets
if (process.env.NODE_ENV != 'production') {
  assets = devAssets
} else {
  assets = prodAssets
}

export default  `
    <!DOCTYPE html>
    <html lang="fr">
      <head>
        <title>PinPict</title>
        <meta name="description" content="Save pictures you like" />
        <meta charset="utf-8" />
        <link rel="icon" type="image/png" href="/static/images/favicon.png" />
        <link rel="stylesheet" href="${assets.app.css}" />
      </head>
      <body>
        <div id="root"></div>
        <script src="${assets.app.js}"></script>
      </body>
    </html>
    `
