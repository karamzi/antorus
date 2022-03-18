let gulp = require('gulp')
let concatCss = require('gulp-concat-css')
let csso = require('gulp-csso')
let cssName = 'bundle' + Date.now().toString() + '.css'


gulp.task('default', function () {
    return gulp.src('static/css/*.css')
        .pipe(concatCss(cssName))
        .pipe(csso())
        .pipe(gulp.dest('static/style/'))
})