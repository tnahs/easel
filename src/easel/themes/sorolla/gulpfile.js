const gulp = require("gulp")
const sass = require("gulp-sass")
const ts = require("gulp-typescript")
const autoprefixer = require("gulp-autoprefixer")
const concat = require("gulp-concat")
const rev = require("gulp-rev")
const orderedReadStream = require("ordered-read-streams")

const paths = {
    srcSCSS: "./src/scss/**/*.scss",
    destCSS: "./sorolla/css",
    srcTS: "./src/typescript/**/*.ts",
    destJS: "./sorolla/javascript",
    srcLibs: {
        css: ["./node_modules/normalize.css/normalize.css"],
        js: ["./node_modules/hammerjs/hammer.js"],
    },
}

const tsProject = ts.createProject("./tsconfig.json")

function runSCSS() {
    const libs = gulp.src(paths.srcLibs.css)
    const scssStream = gulp
        .src(paths.srcSCSS)
        .pipe(sass({ outputStyle: "expanded" }))
        .pipe(autoprefixer("last 2 version"))

    return orderedReadStream([libs, scssStream])
        .pipe(concat("bundle.css"))
        .pipe(rev())
        .pipe(gulp.dest(paths.destCSS))
}

function runTS() {
    const libs = gulp.src(paths.srcLibs.js)
    const tsStream = gulp.src(paths.srcTS).pipe(tsProject())

    return orderedReadStream([libs, tsStream])
        .pipe(concat("bundle.js"))
        .pipe(rev())
        .pipe(gulp.dest(paths.destJS))
}

gulp.task("dev", () => {
    runSCSS()
    runTS()
    gulp.watch(paths.srcSCSS, runSCSS)
    gulp.watch(paths.srcTS, runTS)
})

gulp.task("build", gulp.parallel(runSCSS, runTS))
