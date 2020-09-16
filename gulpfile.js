const fs = require("fs")
const path = require("path")
const gulp = require("gulp")
const sass = require("gulp-sass")
const ts = require("gulp-typescript")
const mergeStream = require("merge-stream")
const minimist = require("minimist")

const THEMES_ROOT = path.join(__dirname, "src/easel/themes/")
const NODE_MODULES = path.join(__dirname, "node_modules")

function getThemePaths(theme) {
    let defaultThemes = []

    fs.readdirSync(THEMES_ROOT).forEach((item) => {
        const absolutePath = path.join(THEMES_ROOT, item)

        // Ignore non-directories.
        if (!fs.lstatSync(absolutePath).isDirectory()) {
            return
        }

        // Ignore hidden files/directories.
        if (item.startsWith(".")) {
            return
        }

        defaultThemes.push(item)
    })

    if (!defaultThemes.includes(theme)) {
        throw `Theme '${theme}' does not exist.`
    }

    return {
        srcSCSS: path.join(THEMES_ROOT, theme, "/static/scss/*.scss"),
        destCSS: path.join(THEMES_ROOT, theme, "static/css"),
        libsCSS: path.join(THEMES_ROOT, theme, "static/css/libs"),
        srcTS: path.join(THEMES_ROOT, theme, "static/typescript/*.ts"),
        destJS: path.join(THEMES_ROOT, theme, "static/javascript"),
        libsJS: path.join(THEMES_ROOT, theme, "static/javascript/libs"),
    }
}

const ARGS = minimist(process.argv.slice(2), { string: "theme" })
const PATHS = getThemePaths(ARGS.theme)

const tsProject = ts.createProject("tsconfig.json")

function runSCSS() {
    return gulp.src(PATHS.srcSCSS).pipe(sass()).pipe(gulp.dest(PATHS.destCSS))
}

function runTS() {
    return gulp.src(PATHS.srcTS).pipe(tsProject()).pipe(gulp.dest(PATHS.destJS))
}

function copyExternalLibs() {
    console.log(`Copying eternal libs for theme: ${ARGS.theme}.`)
    const hammerJS = path.join(NODE_MODULES, "hammerjs/hammer.js")
    const normalizeCSS = path.join(NODE_MODULES, "normalize.css/normalize.css")
    return mergeStream(
        gulp.src(hammerJS).pipe(gulp.dest(PATHS.libsJS)),
        gulp.src(normalizeCSS).pipe(gulp.dest(PATHS.libsCSS))
    )
}

function dev() {
    copyExternalLibs()
    console.log(`Watching files for theme: ${ARGS.theme}.`)
    gulp.watch(PATHS.srcSCSS, runSCSS)
    gulp.watch(PATHS.srcTS, runTS)
}

function build() {
    console.log(`Building files for theme: ${ARGS.theme}.`)
    gulp.parallel(copyExternalLibs, runSCSS, runTS)
}

// gulp dev --theme=THEME-NAME
exports.dev = dev

// gulp build --theme=THEME-NAME
exports.build = build
