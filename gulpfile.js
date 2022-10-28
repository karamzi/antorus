const gulp = require('gulp');
const concatCss = require('gulp-concat-css');
const cssMinify = require('gulp-css-minify');


gulp.task('default', function () {
    return gulp.src('static/css/*.css')
        .pipe(concatCss(`bundle${Date.now()}.css`))
        .pipe(cssMinify())
        .pipe(gulp.dest('static/style/'));
})