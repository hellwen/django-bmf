module.exports = (grunt) ->

  @initConfig

    pkg: grunt.file.readJSON "./package.json"

    clean: 
      all: [
        'static_files/build',
      ]

    copy:
      fonts:
        files: [
          {
              expand: true
              cwd: 'node_modules/bootstrap/fonts'
              src: ['glyphicons*']
              dest: 'djangobmf/static/djangobmf/fonts/'
          },
        ]
      js:
        files: [
          {
              expand: true
              cwd: 'node_modules'
              src: [
                'jquery/dist/jquery.min.js',
                'jquery/dist/jquery.min.map',
                'angular/angular.min.js',
                'angular/angular.min.js.map',
                'd3/d3.min.js',
                'angular-jwt/dist/angular-jwt.min.js',
                'bootstrap/dist/js/bootstrap.min.js',
              ]
              dest: 'djangobmf/static/djangobmf/js/'
              flatten: true
              filter: 'isFile'
          },
        ]

    uglify:
      options:
        compress:
          warnings: false
        mangle: true
        preserveComments: /^!|@preserve|@license|@cc_on/i
      jquerycookie:
        src: ['node_modules/jquery.cookie/jquery.cookie.js']
        dest: 'djangobmf/static/djangobmf/js/jquery.cookie.min.js'
      djangobmf:
        src: [
            'node_modules/jquery.cookie/jquery.cookie.js',
            'node_modules/bootstrap/dist/js/bootstrap.js',
            'djangobmf/static/djangobmf/js/djangobmf.js',
        ]
        dest: 'djangobmf/static/djangobmf/js/djangobmf.min.js'

    concat:
      djangobmf:
        src: [
          'static_files/js/variables.js',
          'static_files/js/bmf-autocomplete.js',
          'static_files/js/bmf-calendar.js',
          'static_files/js/bmf-editform.js',
          'static_files/js/bmf-buildform.js',
          'static_files/js/menu.js',
          'static_files/js/ui-init.js',
          'static_files/js/ui-config.js',
          'static_files/js/ui-filter.js',
          'static_files/js/ui-directive.js',
          'static_files/js/ui-factory.js',
          'static_files/js/ui-controller.js',
          'static_files/js/ui-run.js',
          'static_files/js/ui-close.js',
        ]
        dest: 'djangobmf/static/djangobmf/js/djangobmf.js'

    less:
      compile:
        files:
          'static_files/build/djangobmf.css': 'static_files/less/djangobmf.less'

    cssmin:
      compile:
        files:
          'djangobmf/static/djangobmf/css/djangobmf.min.css': 'static_files/build/djangobmf.css'

    watch:
      js:
        files: ["./static_files/js/*.js"]
        tasks: ["buildjs"]
      css:
        files: ["./static_files/less/*.less"]
        tasks: ["buildcss"]

  @loadNpmTasks "grunt-contrib-clean"
  @loadNpmTasks "grunt-contrib-concat"
  @loadNpmTasks "grunt-contrib-coffee"
  @loadNpmTasks "grunt-contrib-copy"
  @loadNpmTasks "grunt-contrib-cssmin"
  @loadNpmTasks "grunt-contrib-uglify"
  @loadNpmTasks "grunt-contrib-watch"
  @loadNpmTasks "grunt-contrib-less"

  @registerTask "buildjs", ["concat", "uglify"]

  @registerTask "buildcss", ["less", "cssmin"]

  @registerTask "default", ["clean", "buildjs", "buildcss", "copy"]
