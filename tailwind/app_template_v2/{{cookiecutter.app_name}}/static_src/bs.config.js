/*
 |--------------------------------------------------------------------------
 | Browser-sync config file
 |--------------------------------------------------------------------------
 |
 | For up-to-date information about the options:
 |   http://www.browsersync.io/docs/options/
 |
 | There are more options than you see here, these are just the ones that are
 | set internally. See the website for more info.
 |
 |
 */

const tailwindConfig = require('./tailwind.config.js');

module.exports = {
    ui: false,
    logSnippet: false,
    open: false,
    reloadOnRestart: true,
    files: [
        '../static/css/styles.css',
        ...tailwindConfig.purge
    ]
};