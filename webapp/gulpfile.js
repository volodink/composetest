var gulp = require('gulp');
var browserSync = require('browser-sync').create();
var reload      = browserSync.reload;

gulp.task('serve', function () {

    // Serve files from the root of this project
    browserSync.init({
        //server: {
        //    baseDir: "./templates/"
        //}
        proxy:  "192.168.99.100",
        port: "5500"
    });

    gulp.watch("templates/*.html").on("change", reload);
});

gulp.task('default', ['serve']);