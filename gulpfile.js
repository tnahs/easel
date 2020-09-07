const fs = require("fs")
const path = require("path")
const gulp = require("gulp")
const sass = require("gulp-sass")
const ts = require("gulp-typescript")
const minimist = require("minimist")

const THEMES_ROOT = path.join(__dirname, "src/easel/themes/")

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
        destSCSS: path.join(THEMES_ROOT, theme, "static/css"),
        srcTS: path.join(THEMES_ROOT, theme, "static/typescript/*.ts"),
        destTS: path.join(THEMES_ROOT, theme, "static/javascript"),
    }
}

const ARGS = minimist(process.argv.slice(2), { string: "theme" })
const PATHS = getThemePaths(ARGS.theme)

const tsProject = ts.createProject("tsconfig.json")

function runSCSS() {
    return gulp.src(PATHS.srcSCSS).pipe(sass()).pipe(gulp.dest(PATHS.destSCSS))
}

function runTS() {
    return gulp.src(PATHS.srcTS).pipe(tsProject()).pipe(gulp.dest(PATHS.destTS))
}

function dev() {
    console.log(`Watching files for theme: ${ARGS.theme}.`)
    gulp.watch(PATHS.srcSCSS, runSCSS)
    gulp.watch(PATHS.srcTS, runTS)
}

function build() {
    console.log(`Building files for theme: ${ARGS.theme}.`)
    gulp.parallel(runSCSS, runTS)
}

exports.dev = dev
exports.build = build
