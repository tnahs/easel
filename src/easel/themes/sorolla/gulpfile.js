const gulp = require("gulp")
const sass = require("gulp-sass")
const ts = require("gulp-typescript")
const concat = require("gulp-concat")
const orderedReadStream = require("ordered-read-streams")

const paths = {
    srcSCSS: "./assets/scss/*.scss",
    destCSS: "./src/css",
    srcTS: "./assets/typescript/*.ts",
    destJS: "./src/javascript",
    srcLibs: {
        css: ["./node_modules/normalize.css/normalize.css"],
        js: ["./node_modules/hammerjs/hammer.js"],
    },
}

const tsProject = ts.createProject("./tsconfig.json")

function runSCSS() {
    const libs = gulp.src(paths.srcLibs.css)
    const scssStream = gulp.src(paths.srcSCSS).pipe(sass())

    return orderedReadStream([libs, scssStream])
        .pipe(concat("main.css"))
        .pipe(gulp.dest(paths.destCSS))
}

function runTS() {
    const libs = gulp.src(paths.srcLibs.js)
    const tsStream = gulp.src(paths.srcTS).pipe(tsProject())

    return orderedReadStream([libs, tsStream])
        .pipe(concat("main.js"))
        .pipe(gulp.dest(paths.destJS))
}

gulp.task("dev", () => {
    gulp.parallel(runSCSS, runTS)
    gulp.watch(paths.srcSCSS, runSCSS)
    gulp.watch(paths.srcTS, runTS)
})

gulp.task("build", gulp.parallel(runSCSS, runTS))
